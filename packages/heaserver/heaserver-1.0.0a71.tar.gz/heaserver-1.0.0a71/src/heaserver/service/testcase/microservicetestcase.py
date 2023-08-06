from .aiohttptestcase import HEAAioHTTPTestCase
from .expectedvalues import Action, Link, expected_values
from .. import wstl
from aiohttp.web import Application
from ..oidcclaimhdrs import SUB
from .testenv import app_context, RegistryContainerConfig, DockerContainerConfig
from ..db.database import DatabaseManager
from heaserver.service.testcase.mockmongo import MockMongoManager
from aiohttp import hdrs
from heaobject.user import NONE_USER
from heaobject.root import DesktopObjectDict
from abc import ABC
from typing import Union, Optional, Dict, Any, List, Iterable, Type
from copy import deepcopy
from yarl import URL
import logging


class MicroserviceTestCase(HEAAioHTTPTestCase, ABC):
    """
    Abstract base class for testing a service that connects to AWS.
    """

    def __init__(self, coll: str, desktop_objects: Dict[str, List[DesktopObjectDict]],
                 db_manager_cls: Optional[Type[DatabaseManager]] = MockMongoManager,
                 wstl_package: str = None, href: Union[URL, str] = None,
                 body_post: Optional[Dict[str, Dict[str, Any]]] = None,
                 body_put: Optional[Dict[str, Dict[str, Any]]] = None,
                 content_id: Optional[str] = None,
                 expected_all: Optional[List[Dict[str, Any]]] = None,
                 expected_one: Optional[List[Dict[str, Any]]] = None,
                 expected_one_wstl: Optional[Dict[str, Any]] = None, expected_all_wstl: Optional[Dict[str, Any]] = None,
                 expected_one_duplicate_form: Optional[Dict[str, Any]] = None,
                 expected_opener: Optional[Union[str, URL]] = None,
                 expected_opener_body: Optional[Dict[str, Any]] = None,
                 content: Optional[Dict[str, Dict[str, bytes]]] = None, content_type: Optional[str] = None,
                 put_content_status: Optional[int] = None, methodName = 'runTest', port: Optional[int] = None,
                 sub: Optional[str] = NONE_USER,
                 registry_docker_image: Optional[RegistryContainerConfig] = None,
                 other_docker_images: Iterable[DockerContainerConfig] = None):
        """
        Initializes a test case.

        :param coll: collection name (required).
        :param desktop_objects: HEA desktop objects to load into the database (required), as a map of collection ->
        list of desktop object dicts.
        :param db_manager_cls: the database factory class. Defaults to TestMockMongoManager.
        :param wstl_package: the name of the package containing the wstl data package. Required.
        :param href: the resource being tested. Defaults to /{coll}/, where {coll} is the collection name.
        :param body_post: a Collection+JSON template as a dict, to be used for submitting POST requests.
        :param body_put: a Collection+JSON template as a dict, to be used for submitting PUT requests.
        :param expected_all:
        :param methodName: the name of the method to test.
        """
        super().__init__(methodName=methodName, port=port)
        if href is None:
            href_ = str(URL(f'/{coll}/'))
        else:
            href_ = str(href)
            if not href_.endswith('/'):
                href_ = href_ + '/'
        self._href = URL(href_)
        self._coll = str(coll)
        self._body_post = body_post
        self._body_put = body_put
        self._content_id = content_id
        self._expected_all = expected_all
        self._expected_one = expected_one
        self._expected_one_wstl = expected_one_wstl
        self._expected_all_wstl = expected_all_wstl
        self._expected_one_duplicate_form = expected_one_duplicate_form
        self._expected_opener = expected_opener
        self._expected_opener_body = expected_opener_body
        self._wstl_package = wstl_package
        self.__desktop_objects = deepcopy(desktop_objects)
        self._content = deepcopy(content)
        self._content_type = content_type
        self._put_content_status = put_content_status
        self._headers = {SUB: sub if sub is not None else NONE_USER, hdrs.X_FORWARDED_HOST: 'localhost:8080'}
        self.__registry_docker_image = registry_docker_image
        self.__other_docker_images = other_docker_images
        self.__db_manager_cls = MockMongoManager if db_manager_cls is None else db_manager_cls
        self.maxDiff = None

    def run(self, result=None):
        """
        Runs a test using a freshly created MongoDB Docker container. The container is destroyed upon concluding
        the test.

        :param result: a TestResult object into which the test's result is collected.
        :return: the TestResult object.
        """
        _logger = logging.getLogger(__name__)
        with self._caplog.at_level(logging.DEBUG):
            with app_context(db_manager_cls=self.__db_manager_cls,
                             desktop_objects=self.__desktop_objects,
                             other_microservice_images=self.__other_docker_images,
                             registry_docker_image=self.__registry_docker_image,
                             content=self._content,
                             wstl_builder_factory=wstl.builder_factory(self._wstl_package,
                                                                       href=self._href)) as app:
                self.__app = app
                return super().run(result)

    async def get_application(self) -> Application:
        return self.__app


def get_test_case_cls_default(coll: str, fixtures: Dict[str, List[DesktopObjectDict]], duplicate_action_name: str,
                              db_manager_cls: Optional[Type[DatabaseManager]] = MockMongoManager,
                              wstl_package: str = None,
                              content: Optional[Dict[str, Dict[str, bytes]]] = None, content_type: Optional[str] = None,
                              put_content_status: Optional[int] = None, include_root=False,
                              href: Optional[Union[str, URL]] = None, get_actions: Optional[List[Action]] = None,
                              get_all_actions: Optional[List[Action]] = None,
                              expected_opener: Optional[Link] = None,
                              registry_docker_image: Optional[RegistryContainerConfig] = None,
                              other_docker_images: Iterable[DockerContainerConfig] = None,
                              port: Optional[int] = None, sub: Optional[str] = NONE_USER,
                              exclude: Optional[list[str]] = None) -> Type[MicroserviceTestCase]:
    exclude_ = exclude if exclude is not None else []
    expected_values_ = {k: v for k, v in expected_values(fixtures, coll, wstl.builder(package=wstl_package),
                                                         duplicate_action_name, href,
                                                         get_actions=get_actions,
                                                         get_all_actions=get_all_actions,
                                                         opener_link=expected_opener).items() if k not in exclude_}
    return _get_test_case_cls(coll=coll, fixtures=fixtures, db_manager_cls=db_manager_cls,
                              wstl_package=wstl_package, href=href, content=content, content_type=content_type,
                              put_content_status=put_content_status, registry_docker_image=registry_docker_image,
                              other_docker_images=other_docker_images, port=port, sub=sub, **expected_values_)


def _get_test_case_cls(coll: str, fixtures: Dict[str, List[DesktopObjectDict]],
                       db_manager_cls: Optional[Type[DatabaseManager]] = MockMongoManager,
                       wstl_package: str = None,
                       href: Union[URL, str] = None,
                       content: Optional[Dict[str, Dict[str, bytes]]] = None, content_type: Optional[str] = None,
                       put_content_status: Optional[int] = None, body_post: Optional[Dict[str, Dict[str, Any]]] = None,
                       body_put: Optional[Dict[str, Dict[str, Any]]] = None,
                       content_id: Optional[str] = None,
                       expected_one: Optional[List[Dict[str, Any]]] = None,
                       expected_one_wstl: Optional[Dict[str, Any]] = None,
                       expected_one_duplicate_form: Optional[Dict[str, Any]] = None,
                       expected_all: Optional[List[Dict[str, Any]]] = None,
                       expected_all_wstl: Optional[Dict[str, Any]] = None,
                       expected_opener: Optional[Union[str, URL]] = None,
                       expected_opener_body: Optional[Dict[str, Any]] = None,
                       registry_docker_image: Optional[RegistryContainerConfig] = None,
                       other_docker_images: Iterable[DockerContainerConfig] = None, port: Optional[int] = None,
                       sub: Optional[str] = NONE_USER) -> Type[MicroserviceTestCase]:
    """
    This function configures mocks. It returns a base test case class for testing a mongodb-based service with the
    provided fixtures. The test case class is a subclass of aiohttp.test_utils.AioHTTPTestCase, and the provided
    fixtures can be found in the following fields: _resource_path, _body_post, _body_put, _expected_all, and
    _expected_one.

    :param href: the resource being tested (required).
    :param wstl_package: the name of the package containing the wstl data package (required).
    :param coll: the MongoDB collection (required).
    :param fixtures: data to insert into the mongo database before running each test. Should be a dict of
    collection -> list of objects. Required.
    :param content: :param content: data to insert into GridFS (optional), as a collection string -> HEA Object id ->
    content as a bytes, bytearray, or array.array object.
    :param content_type: the MIME type of the content (optional).
    :param put_content_status: the expected status code for updating the content of the HEA object (optional). Normally
    should be 204 if the content is updatable and 405 if not. Default is None, which will cause associated tests to be
    skipped.
    :param body_post: JSON dict for data to be posted.
    :param body_put: JSON dict for data to be put. If None, the value of body_post will be used for PUTs.
    :param expected_one: The expected JSON dict list for GET calls. If None, the value of expected_all will be used.
    :param expected_one_wstl: The expected JSON dict for GET calls that return the
    application/vnd.wstl+json mime type.
    :param expected_one_duplicate_form: The expected JSON dict for GET calls that return the
    object's duplicate form.
    :param expected_all: The expected JSON dict list for GET-all calls.
    :param expected_all_wstl: The expected JSON dict for GET-all calls that return the
    application/vnd.wstl+json mime type.
    :param expected_opener: The expected URL of the resource that does the opening.
    :param expected_opener_body: The expected JSON dict for GET calls for an HEA desktop object's opener choices.
    :param registry_docker_image: an heaserver-registry docker image in REPOSITORY:TAG format, that will be launched
    after the MongoDB container is live.
    :param port: the port number to run aiohttp. If None, a random available port will be chosen.
    :return the base test case class.
    """
    class RealMicroserviceTestCase(MicroserviceTestCase):
        """
        Test case class for testing a mongodb-based service.
        """

        def __init__(self, methodName: str = 'runTest') -> None:
            """
            Initializes a test case.

            :param methodName: the name of the method to test.
            """
            super().__init__(coll=coll, desktop_objects=fixtures, db_manager_cls=db_manager_cls,
                             wstl_package=wstl_package, href=href, body_post=body_post, body_put=body_put,
                             content_id=content_id,
                             expected_all=expected_all, expected_one=expected_one or expected_all,
                             expected_one_wstl=expected_one_wstl or expected_all_wstl,
                             expected_all_wstl=expected_all_wstl,
                             expected_one_duplicate_form=expected_one_duplicate_form, expected_opener=expected_opener,
                             expected_opener_body=expected_opener_body, content=content, content_type=content_type,
                             put_content_status=put_content_status, methodName=methodName, port=port, sub=sub,
                             registry_docker_image=registry_docker_image, other_docker_images=other_docker_images)

    return RealMicroserviceTestCase

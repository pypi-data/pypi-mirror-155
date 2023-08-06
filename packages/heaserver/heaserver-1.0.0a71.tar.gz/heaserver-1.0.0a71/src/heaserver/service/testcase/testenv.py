"""
Portions of this module require that the testcontainers package is installed, as described below in the docstrings of
this module's functions and classes.
"""
from contextlib import ExitStack
from copy import deepcopy, copy
from typing import Optional, Dict, List, Type, Callable

from aiohttp import web
from heaobject.registry import Resource
from heaobject.root import DesktopObjectDict
from heaserver.service import runner
from heaserver.service import wstl
from heaserver.service.db.database import DatabaseManager
from heaserver.service.testcase.mockmongo import MockMongoManager
from contextlib import contextmanager, closing
from typing import Generator
from abc import ABC


class DockerVolumeMapping:
    """
    Docker volume mapping. This class is immutable.
    """

    def __init__(self, host: str, container: str, mode: str = 'ro'):
        """
        Creates a volume mapping.

        :param host: the path of the directory on the host to map (required).
        :param container: the path to mount the volume in the container (required).
        :param mode: access level in the container as Unix rwx-style permissions (defaults to 'ro').
        """
        if mode is None:
            self.__mode: str = 'ro'
        else:
            self.__mode = str(mode)
        self.__container = str(container)
        self.__host = str(host)

    @property
    def host(self) -> str:
        return self.__host

    @property
    def container(self) -> str:
        return self.__container

    @property
    def mode(self) -> str:
        return self.__mode


class DockerContainerConfig:
    """
    Docker image and configuration for starting a container. This class is immutable.
    """

    def __init__(self, image: str, port: int, check_path: Optional[str] = None,
                 resources: Optional[List[Resource]] = None,
                 volumes: Optional[List[DockerVolumeMapping]] = None,
                 env_vars: Optional[Dict[str, str]] = None,
                 db_manager_cls: Optional[type[DatabaseManager]] = None):
        """
        Constructor.

        :param image: the image tag (required).
        :param port: the exposed port (required).
        :param check_path: the URL path to check if the microservice is running.
        :param resources: a list of heaobject.registry.Resource dicts indicating what content types this image is designed for.
        :param volumes: a list of volume mappings.
        :param env_vars: a dict containing environment variable names mapped to string values.
        """
        if image is None:
            raise ValueError('image cannot be None')
        if port is None:
            raise ValueError('port cannot be None')
        if any(not isinstance(volume, DockerVolumeMapping) for volume in volumes or []):
            raise TypeError(f'volumes must contain only {DockerVolumeMapping} objects')
        if any(not isinstance(k, str) and isinstance(v, str) for k, v in (env_vars or {}).items()):
            raise TypeError('env_vars must be a str->str dict')
        if any(not isinstance(r, Resource) for r in resources or []):
            raise TypeError(f'resources must contain only {Resource} objects')
        self.__image = str(image)
        self.__port = int(port)
        self.__check_path = str(check_path)
        self.__resources = [deepcopy(e) for e in resources or []]
        self.__volumes = list(volumes) if volumes else []
        self.__env_vars = dict(env_vars) if env_vars is not None else {}
        self.__db_manager_cls = db_manager_cls  # immutable

    @property
    def image(self) -> str:
        """
        The image tag (read-only).
        """
        return self.__image

    @property
    def port(self) -> int:
        """
        The exposed port (read-only).
        """
        return self.__port

    @property
    def check_path(self) -> Optional[str]:
        """
        The URL path to check for whether the microservice is running (read-only).
        """
        return self.__check_path

    @property
    def resources(self) -> Optional[List[Resource]]:
        """
        A list of heaobject.registry.Resource dicts indicating what content types this image is designed for (read-only).
        """
        return deepcopy(self.__resources)

    @property
    def volumes(self) -> List[DockerVolumeMapping]:
        """
        A list of VolumeMapping instances indicating what volumes to map (read-only, never None).
        """
        return copy(self.__volumes)

    @property
    def env_vars(self) -> Dict[str, str]:
        """
        A dict of environment variable names to string values.
        """
        return copy(self.__env_vars)

    @property
    def db_manager_cls(self) -> Optional[type[DatabaseManager]]:
        return self.__db_manager_cls  # immutable

    def with_env_vars(self, env_vars: Optional[Dict[str, str]]) -> 'DockerContainerConfig':
        """
        Returns a new DockerContainerConfig with the same values as this one, plus any environment variables in the
        env_vars argument.

        :param env_vars: any environment variables.
        :return:
        """
        new_env_vars = self.env_vars
        if env_vars is not None:
            new_env_vars.update(env_vars)
        return DockerContainerConfig(self.image, self.port, self.check_path, self.resources, self.volumes,
                                     new_env_vars, self.db_manager_cls)


class RegistryContainerConfig(DockerContainerConfig, ABC):
    """
    Abstract base class for builders that configure and create HEA Registry Service docker containers.

    This class assumes that the testcontainers package is installed. Do not create instances of it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface. Using it as a type annotation for optional parameters and the like where no actual instances of it
    will be created is okay, however.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class MockRegistryContainerConfig(RegistryContainerConfig):
    """
    Creates an HEA Registry Service docker container configured to use a mock mongodb database for data management.

    This class assumes that the testcontainers package is installed. Do not create instances of it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface. Using it as a type annotation for optional parameters and the like where no actual instances of it
    will be created is okay, however.

    :param image: the label of the docker image to use (required).
    """
    def __init__(self, image: str):
        super().__init__(image=image, port=8080, check_path='/components', db_manager_cls=MockMongoManager)


@contextmanager
def app_context(db_manager_cls: Type[DatabaseManager],
                desktop_objects: Dict[str, List[DesktopObjectDict]],
                other_microservice_images: Optional[List[DockerContainerConfig]] = None,
                other_db_manager_cls: Optional[List[Type[DatabaseManager]]] = None,
                registry_docker_image: Optional[RegistryContainerConfig] = None,
                content: Dict[str, Dict[str, bytes]] = None,
                wstl_builder_factory: Optional[Callable[[], wstl.RuntimeWeSTLDocumentBuilder]] = None) -> Generator[web.Application, None, None]:
    """
    Starts the test environment. The test environment consists of: a "bridge" database that is accessible from the
    internal docker network; an "external" database that is accessible from outside the network; a "bridge" registry
    service that is accessible from the internal docker network; an "external" registry service that is accessible from
    outside the network; the service being tested, which is run from outside of docker; and any service dependencies,
    which are run as docker containers. The provided context manager will clean up any resources upon exit.

    Do not pass DockerContainerConfig nor RegistryContainerConfig objects into this function unless the testcontainer
    package is installed.

    :param db_manager_cls: the database manager class for the microservice being tested (required).
    :param desktop_objects: HEA desktop objects to load into the database (required), as a map of collection -> list of
    desktop object dicts.
    :param other_microservice_images: the docker images of any service dependencies.
    :param other_db_manager_cls: a list of database manager classes from the heaserver.server.db package, if any
    supporting microservices need database connectivity. If omitted or None, heaserver.service.db.mongo.MongoManager is
    used.
    :param registry_docker_image: an HEA registry service docker image.
    :param content: any content to load into the database.
    :param wstl_builder_factory: a zero-argument callable that will return a RuntimeWeSTLDocumentBuilder. Optional if
    this service has no actions. Typically, you will use the heaserver.service.wstl.get_builder_factory function to
    get a factory object.
    :param testing: whether this function was called by a test case in a HEAAioHTTPTestCase object. Default is False.
    :returns: a callable for creating the aiohttp Application.
    """

    def _bridge_dbs_to_start() -> set[type[DatabaseManager]]:
        bridge_db_manager_cls = set()
        if other_db_manager_cls:
            bridge_db_manager_cls.update(other_db_manager_cls)
        if registry_docker_image is not None and registry_docker_image.db_manager_cls is not None:
            bridge_db_manager_cls.add(registry_docker_image.db_manager_cls)
        return bridge_db_manager_cls

    with ExitStack() as context_manager, closing(db_manager_cls()) as external_db_, db_manager_cls.environment(), db_manager_cls.context():
        bridge_dbs = [context_manager.enter_context(closing(bridge_db_cls())) for bridge_db_cls in
                      _bridge_dbs_to_start()]
        bridge_desktop_objects, external_desktop_objects = deepcopy(desktop_objects), deepcopy(desktop_objects)
        external_db_.start_database(context_manager)
        if registry_docker_image is not None:
            assert registry_docker_image.db_manager_cls is not None
            if db_manager_cls != registry_docker_image.db_manager_cls:
                external_registry_db_ = context_manager.enter_context(closing(registry_docker_image.db_manager_cls()))
                external_registry_db_.start_database(context_manager)
            else:
                external_registry_db_ = external_db_
        for bridge_db in bridge_dbs:
            bridge_db.start_database(context_manager)
        if registry_docker_image is not None:
            from .docker import start_microservice_container
            bridge_config_ = _add_db_config(registry_docker_image, bridge_dbs)
            _, bridge_registry_url = start_microservice_container(bridge_config_, context_manager)
            external_config_ = _add_db_config(registry_docker_image, [external_registry_db_])
            external_registry_url, _ = start_microservice_container(external_config_, context_manager)
        else:
            external_registry_url = None
            bridge_registry_url = None
        if other_microservice_images:
            _start_other_docker_containers(bridge_desktop_objects, external_desktop_objects,
                                           other_microservice_images, bridge_registry_url, bridge_dbs, context_manager)
        config_file = _generate_config_file(external_db_, external_registry_url)
        if registry_docker_image is not None and type(external_db_) != registry_docker_image.db_manager_cls:
            external_db_.insert_all({k: v for k, v in external_desktop_objects.items() if k in (external_db_.get_relevant_collections() or [])}, content)
            external_registry_db_.insert_desktop_objects({k: v for k, v in external_desktop_objects.items() if k == 'components'})
        else:
            external_db_.insert_all({k: v for k, v in external_desktop_objects.items() if k in (external_db_.get_relevant_collections() or [])}, content)
        for bridge_db in bridge_dbs:
            bridge_db.insert_all({k: v for k, v in bridge_desktop_objects.items() if k in (bridge_db.get_relevant_collections() or [])}, content)
        yield runner.get_application(db=external_db_, wstl_builder_factory=wstl_builder_factory,
                                     config=runner.init(config_string=config_file))


def _add_db_config(docker_container_config: DockerContainerConfig, dbs: list[DatabaseManager]) -> DockerContainerConfig:
    """
    Returns a copy of the docker_container_config with additional environment variables needed for connecting to the
    database.

    This function assumes that the testcontainers package is installed. Do not use it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface.

    :param docker_container_config: a DockerContainerConfig (required).
    :param dbs: the available database containers.
    :return: a newly created DockerContainerConfig.
    """
    db_manager = _get_db_manager(dbs, docker_container_config.db_manager_cls)
    if db_manager is not None:
        env_vars = db_manager.get_microservice_env_vars()
    else:
        env_vars = None
    return docker_container_config.with_env_vars(env_vars)


def _get_db_manager(dbs: list[DatabaseManager], db_manager_cls_: Optional[type[DatabaseManager]]) -> Optional[DatabaseManager]:
    """
    Returns the database manager with the given type.

    :param dbs: the available database managers.
    :param db_manager_cls_: the type of interest.
    :return: a database manager, or None if no database manager with the given type is available.
    """
    if db_manager_cls_ is not None:
        return next((b for b in dbs if isinstance(b, db_manager_cls_)), None)
    else:
        return None


def _start_other_docker_containers(bridge_desktop_objects: Dict[str, List[DesktopObjectDict]],
                                   external_desktop_objects: Dict[str, List[DesktopObjectDict]],
                                   other_docker_images: Optional[List[DockerContainerConfig]],
                                   registry_url: Optional[str],
                                   bridge_dbs: list[DatabaseManager],
                                   stack: ExitStack):
    """
    Starts the provided microservice containers.

    This function assumes that the testcontainers package is installed. Do not use it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface.

    :param bridge_desktop_objects: data to go into the database that is internal to the docker network, as a map of
    collection -> list of desktop object dicts.
    :param external_desktop_objects: data to go into the database that is outside of the docker network, as a map of
    collection -> list of desktop object dicts.
    :param other_docker_images: a list of docker images to start.
    :param registry_url: the URL of the registry microservice.
    :param stack: the ExitStack.
    """
    from .docker import start_microservice_container
    for img in other_docker_images or []:
        db_manager = _get_db_manager(bridge_dbs, img.db_manager_cls)
        if db_manager is not None:
            env_vars = db_manager.get_microservice_env_vars()
            img_ = img.with_env_vars(env_vars)
        else:
            img_ = img
        external_url, bridge_url = start_microservice_container(img_, stack, registry_url)
        bridge_desktop_objects.setdefault('components', []).append(
            {'type': 'heaobject.registry.Component', 'base_url': bridge_url, 'name': bridge_url,
             "owner": "system|none", 'resources': [r.to_dict() for r in img_.resources or []]})
        external_desktop_objects.setdefault('components', []).append(
            {'type': 'heaobject.registry.Component', 'base_url': external_url, 'name': external_url,
             "owner": "system|none", 'resources': [r.to_dict() for r in img_.resources or []]})


def _generate_config_file(db_manager: DatabaseManager, registry_url: Optional[str]) -> str:
    """
    Generates a HEA microservice configuration file.

    :param db_manager: a DatabaseManager instance (required).
    :param registry_url: the URL of the registry service.
    :returns: the configuration file string.
    """
    if db_manager is not None:
        if registry_url is None:
            config_file = db_manager.get_config_file_section()
        else:
            config_file = f"""
    [DEFAULT]
    Registry={registry_url}

    {db_manager.get_config_file_section()}
                    """
    else:
        if registry_url is None:
            config_file = ''
        else:
            config_file = f"""
        [DEFAULT]
        Registry={registry_url}
                        """
    return config_file


def _with_hea_env_vars(container_config: DockerContainerConfig,
                       registry_url: Optional[str]) -> DockerContainerConfig:
    """
    Copies the provided container_spec, adding the environment variables corresponding to the provided arguments.

    This function assumes that the testcontainers package is installed. Do not use it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface.

    :param container_config: the image and configuration (required).
    :param db_manager: a TestDatabaseFactory instance (required).
    :param registry_url: the URL of the registry service, which populates the HEASERVER_REGISTRY_URL environment
    variable.
    :return: the copy of the provided container_spec.
    """
    env_vars: Dict[str, str] = {}
    if registry_url is not None:
        env_vars['HEASERVER_REGISTRY_URL'] = registry_url
    return container_config.with_env_vars(env_vars)

import abc
import configparser
from abc import ABC, abstractmethod
from contextlib import ExitStack, contextmanager, AbstractContextManager

from aiohttp import web, hdrs
from typing import Optional, Type, Tuple, Mapping, List, Callable, Awaitable, Union, Dict, Generator, AsyncGenerator

from aiohttp.web_request import Request
from aiohttp.web_response import Response
from heaobject.keychain import Credentials
from heaobject.volume import FileSystemTypeVar, FileSystem, Volume, AWSFileSystem
from heaobject.root import DesktopObjectDict, DesktopObject
from yarl import URL
from multidict import istr, CIMultiDict, CIMultiDictProxy

from heaserver.service import client, response
from heaserver.service.heaobjectsupport import type_to_resource_url
from heaserver.service.oidcclaimhdrs import SUB
from heaserver.service.util import modified_environ

from copy import copy, deepcopy
import logging


class NotStartedError(ValueError):

    def __init__(self, *args: object) -> None:
        super().__init__('The database is not running. Call start_database() first.', *args)

class Database(abc.ABC):
    """
    Connectivity to databases and other data storage systems for HEA microservices. The database object may be
    optionally configured by providing a ConfigParser object to the constructor. The ConfigParser class provides a
    similar structure to what is found in Windows INI files, including the use of section headers. Section headers
    should be prefixed by the Database subclass' full class name as produced by str(cls) to avoid name clashes.
    Properties in the ConfigParser object should be named using CamelCase. This class is not designed for multiple
    inheritance.
    """

    def __init__(self, config: Optional[configparser.ConfigParser], **kwargs) -> None:
        """
        Initializes the database object. Subclasses must call this constructor.

        :param config: Optional HEA configuration.
        """
        super().__init__(**kwargs)
        logger = logging.getLogger(__name__)
        logger.debug(f'Initialized {type(self)} database object')

    @classmethod
    def get_config_section(cls) -> str:
        """
        Gets this database type's section in the HEA configuration. By default, the section name is that produced by
        str(cls) in order to avoid name clashes. When overriding this method, take care not to construct a name that
        might clash with the current or future section header of another Database class.
        """
        return str(cls)

    async def get_file_system_and_credentials_from_volume(self, request: web.Request, volume_id: Optional[str]) -> Tuple[AWSFileSystem, Optional[Credentials]]:
        """
        Gets the file system and credentials for the given volume. It uses the registry microservice to access the
        file system and credentials microservices. Override this method to mock getting a file system and credentials.

        :param request: the aiohttp request (required).
        :param volume_id: a volume id string (required).
        :return: a tuple containing a FileSystem object and, if one exists, a Credentials object (or None if one does
        not).
        """
        return await get_file_system_and_credentials_from_volume(request, volume_id, AWSFileSystem)

    async def get_volumes(self, request: Request, file_system_type_or_type_name: Union[str, type[FileSystem]]) -> AsyncGenerator[Volume, None]:
        async for volume in get_volumes(request, file_system_type_or_type_name):
            yield volume


class InMemoryDatabase(Database, abc.ABC):
    """
    In-memory store of desktop objects and content.
    """

    def __init__(self, config: Optional[configparser.ConfigParser], **kwargs) -> None:
        """
        Initializes the in-memory database.

        :param config: a configparser.ConfigParser object.
        """
        super().__init__(config, **kwargs)
        self.__desktop_objects: Dict[str, List[DesktopObjectDict]] = {}
        self.__content: Dict[str, Dict[str, bytes]] = {}

    def add_desktop_objects(self, data: Optional[Dict[str, List[DesktopObjectDict]]]):
        self.__desktop_objects.update(deepcopy(data) if data is not None else {})

    def get_desktop_objects_by_collection(self, coll: str) -> List[DesktopObjectDict]:
        return deepcopy(self.__desktop_objects.get(coll, []))

    def get_desktop_object_by_collection_and_id(self, coll: str, id_: Optional[str]) -> Optional[DesktopObjectDict]:
        return deepcopy(next((d for d in self.__desktop_objects.get(coll, []) if d['id'] == id_), None))

    def add_content(self, content: Optional[Dict[str, Dict[str, bytes]]]):
        self.__content.update(deepcopy(content) if content is not None else {})

    def get_content_by_collection(self, coll: str) -> Optional[Dict[str, bytes]]:
        return copy(self.__content.get(coll, None))

    def get_content_by_collection_and_id(self, coll: str, id_: str) -> Optional[bytes]:
        if (result := self.__content.get(coll, None)) is not None:
            return result.get(id_, None)
        else:
            return None


async def get_file_system_and_credentials_from_volume(request: Request, volume_id: Optional[str], file_system_type: Type[FileSystemTypeVar]) -> Tuple[FileSystemTypeVar, Optional[Credentials]]:
    """
    Get the file system and credentials for the given volume.

    :param request: the aiohttp request (required).
    :param volume_id: a volume id string (required).
    :param file_system_type: the type of file system (required).
    :return: a tuple containing a FileSystem object and, if one exists, a Credentials object (or None if one does not).
    :raise ValueError: if no volume with that id exists, no file system exists for the given volume, or the volumes's
    credentials were not found.
    """
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    volume, volume_url = await _get_volume(request.app, volume_id, headers)
    if volume is None:
        raise ValueError(f'No volume with id {volume_id}')
    if volume_url is None:
        raise ValueError(f'Volume {volume_id} has no URL')
    fs_url = await type_to_resource_url(request, FileSystem)
    if fs_url is None:
        raise ValueError('No file system service registered')
    file_system = await client.get(request.app,
                                   URL(fs_url) / 'bytype' / file_system_type.get_type_name() / 'byname' / volume.file_system_name, file_system_type,
                                   headers=headers)
    if file_system is None:
        raise ValueError(f"Volume {volume.id}'s file system {volume.file_system_name} does not exist")
    return file_system, await _get_credentials(request.app, volume, headers)


async def has_volume(request: Request, volume_id: Optional[str] = None, headers: Optional[Mapping[str, str]] = None) -> Response:
    if volume_id is None:
        if 'volume_id' in request.match_info:
            volume_id_ = request.match_info['volume_id']
        elif 'id' in request.match_info:
            volume_id_ = request.match_info['id']
        else:
            volume_id_ = None
    else:
        volume_id_ = volume_id
    if volume_id_ is not None:
        volume_url = await type_to_resource_url(request, Volume)
        if volume_url is None:
            raise ValueError('No Volume service registered')
        volume = await client.get(request.app, URL(volume_url) / volume_id_, Volume, headers=headers)
        if volume is None:
            return response.status_not_found()
        return response.status_ok()
    else:
        return response.status_not_found()


async def get_volumes(request: Request, file_system_type_or_type_name: Union[str, type[FileSystem]]) -> AsyncGenerator[Volume, None]:
    headers = {SUB: request.headers[SUB]} if SUB in request.headers else None
    volume_url = await type_to_resource_url(request, Volume)
    if volume_url is None:
        raise ValueError('No Volume service registered')
    if issubclass(file_system_type_or_type_name, DesktopObject):
        file_system_type_or_type_name_ = file_system_type_or_type_name.get_type_name()
    else:
        file_system_type_or_type_name_ = str(file_system_type_or_type_name)
    get_volumes_url = URL(volume_url) / 'byfilesystemtype' / file_system_type_or_type_name_

    async for volume in client.get_all(request.app, get_volumes_url, Volume, headers=headers):
        yield volume


async def get_options(request: Request, methods: List[str], fn: Callable[[Request], Awaitable[Response]]):
    """
    Responds to an OPTIONS request. It calls the provided function, checks for the 200 status code, and if 200 is
    returned, returns a response with a 200 status code and an Allow header. The function should check if a REST API
    endpoint would return a 200 status code if called.

    :param request: the HTTP request (required).
    :param methods: a list of methods to include in the Allow header (required).
    :param fn: the function to call.
    :return: the HTTP response.
    """
    resp = await fn(request)
    if resp.status == 200:
        return await response.get_options(request, methods)
    else:
        headers: Union[Mapping[Union[str, istr], str], None] = {hdrs.CONTENT_TYPE: 'text/plain; charset=utf-8'}
        return response.status_generic(status=resp.status, body=resp.text, headers=headers)


async def _get_volume(app: web.Application, volume_id: Optional[str], headers: Union[Mapping[Union[str, istr], str], CIMultiDict[str], CIMultiDictProxy[str], None] = None) -> Tuple[Optional[Volume], Optional[Union[str, URL]]]:
    """
    Gets the volume with the provided id.

    :param app: the aiohttp app (required).
    :param volume_id: the id string of a volume.
    :param headers: any headers.
    :return: a two-tuple with either the Volume and its URL, or (None, None).
    :raise ValueError: if there is no volume with the provided volume id or no volume service is registered.
    """
    if volume_id is not None:
        volume_url = await client.get_resource_url(app, Volume)
        if volume_url is None:
            raise ValueError('No Volume service registered')
        volume = await client.get(app, URL(volume_url) / volume_id, Volume, headers=headers)
        if volume is None:
            raise ValueError(f'No volume with volume_id={volume_id}')
        return volume, volume_url
    else:
        return None, None


async def _get_credentials(app: web.Application, volume: Volume, headers: Optional[Mapping] = None) -> Optional[Credentials]:
    """
    Gets a credential specified in the provided volume, or if there is none, a credential with the where attribute set
    to the volume's URL.

    :param app: the aiohttp app (required).
    :param volume: the Volume (required).
    :param volume_url: the volume's URL (required).
    :param headers: any headers.
    :return: the Credentials, or None if the volume has no credentials.
    :raise ValueError: if no credentials service is registered or if the volume's credentials were not found.
    """
    if volume.credential_id is not None:
        cred_url = await client.get_resource_url(app, Credentials)
        if cred_url is None:
            raise ValueError('No credentials service registered')
        credential = await client.get(app, URL(cred_url) / volume.credential_id, Credentials, headers=headers)
        if credential is not None:
            return credential
        else:
            raise ValueError(f'Credentials {volume.credential_id} not found')
    else:
        return None


class DatabaseManager(ABC):
    """
    Abstract base class for database managers. These classes start a database, load data into it, return a Database
    object for manipulating the data, and delete the data. All subclasses of TestDatabaseManager must have a no-arg
    constructor, and they are expected to be immutable.
    """

    def __init__(self):
        self.__started = False

    def start_database(self, context_manager: ExitStack) -> None:
        """
        Starts the database. The provided context manager will destroy the database automatically. Override this
        method to start a database, such as in a docker container. Place the super() call after the database is
        already started.

        :param context_manager: a context manager for creating and destroying the database (required).
        """
        self.__started = True

    @property
    def started(self) -> bool:
        return self.__started

    def get_microservice_env_vars(self, ) -> Dict[str, str]:
        """
        Gets environment variables to pass into a microservice to connect to this database. This default implementation
        returns an empty dict. This method may only be called after the start_database() method. Override this method
        to return a dictionary of environment variable name-value pairs.

        :return: a str->str dict.
        """
        return {}

    def get_config_file_section(self) -> str:
        """
        Creates a HEA configuration file section for connecting to this database. This default implementation returns
        an empty string. This method may only be called after the start_database() method.

        :return: a string.
        """
        return ''

    @classmethod
    def get_relevant_collections(cls) -> Optional[list[str]]:
        return None

    def insert_desktop_objects(self, desktop_objects: Optional[Dict[str, list[DesktopObjectDict]]]):
        """
        Inserts data into the database. The start_database() method must be called before calling this method. The
        default implementation does nothing and is expected to be overridden with an implementation for a specific
        database technology. Implementations should anticipate multiple inheritance. Call super(), and do not pass
        desktop object collections that are handled by this collection into the superclass' implementation.

        :param desktop_objects: a dict of collection -> list of desktop object dicts. Required.
        :raises KeyError: if an unexpected key was found in the data.
        """
        if not self.started:
            raise NotStartedError

    def insert_content(self, content: Optional[dict[str, dict[str, bytes]]]):
        """
        Inserts content into the database. The start_database() method must be called before calling this method.
        The default implementation does nothing and is expected to be overridden with an implementation for a specific
        database technology. Implementations should anticipate multiple inheritance. Call super(), and do not pass
        content collections that are handled by this collection into the superclass' implementation.

        :param content: a dict of collection -> dict of desktop object id -> content. Required.
        :raises KeyError: if an unexpected key was found in the content.
        """
        if not self.started:
            raise NotStartedError

    def insert_all(self, desktop_objects: Optional[Dict[str, list[DesktopObjectDict]]], content: Optional[dict[str, dict[str, bytes]]]):
        """
        Inserts all data and content. Failure may put the object in an inconsistent state where one is properly
        inserted but the other is not. This method is not designed to be overridden.

        :raises KeyError: if an unexpected key was found in the data or the content.
        """
        self.insert_desktop_objects(desktop_objects)
        self.insert_content(content)

    def close(self):
        """
        Removes all data and content, and cleans up any other resources created by other methods of this object. This
        method is not designed to be overridden.
        """
        if self.started:
            self.delete_all()

    @classmethod
    def get_environment_to_remove(cls) -> list[str]:
        """
        Gets any environment variables that need to be removed temporarily for the database.

        :return: a list of environment variable names, or the empty list.
        """
        return []

    @classmethod
    def get_environment_updates(cls) -> dict[str, str]:
        """
        Gets a newly created dict with any environment variables that are needed by the database.

        :return: environment variable name -> value dict, or the empty dict if no environment variables are needed.
        """
        return {}

    @classmethod
    @contextmanager
    def environment(cls):
        with modified_environ(*cls.get_environment_to_remove(), **cls.get_environment_updates()):
            yield

    @classmethod
    def get_context(cls) -> list[AbstractContextManager]:
        """
        Gets a newly created list of context managers, or the empty list if there are none. This method is called by
        the context() context manager, which instantiates any context managers in the list.
        """
        return []

    @classmethod
    @contextmanager
    def context(cls):
        with ExitStack() as stack:
            for context_ in cls.get_context():
                stack.enter_context(context_)
            yield

    def delete_desktop_objects(self):
        """
        Deletes data from the database. The start_database() method must be called before calling this method. This
        should support being called multiple times, and after the first time have no effect. Override this method to
        delete the provided desktop objects from the database.

        :raises KeyError: if an unexpected key was found in the data.
        """
        if not self.started:
            raise NotStartedError

    def delete_content(self):
        """
        Deletes content from the database. The start_database() method must be called before calling this method. This
        should support being called multiple times, and after the first time have no effect. Override this method to
        delete the provided content from the database.

        :raises KeyError: if an unexpected key was found in the content.
        """
        if not self.started:
            raise NotStartedError

    def delete_all(self):
        try:
            self.delete_desktop_objects()
        finally:
            self.delete_content()

    @abstractmethod
    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[Database, None, None]:
        """
        Creates the corresponding Database object. The start_database() method must be called before calling this
        method. Override this method to return a Database instance.

        :param config: HEA configuration.
        :return: the database object.
        """
        pass

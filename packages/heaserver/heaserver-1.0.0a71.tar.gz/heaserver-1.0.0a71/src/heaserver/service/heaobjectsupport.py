"""
Convenience functions for handling HEAObjects.
"""

from . import client
from .representor import factory as representor_factory
from .representor.error import ParseException
from heaobject.root import DesktopObjectTypeVar, DesktopObjectDict, DesktopObject, desktop_object_type_for_name, Permission
from heaobject.volume import DEFAULT_FILE_SYSTEM, FileSystem, DefaultFileSystem
from heaobject.error import DeserializeException
from heaobject.user import NONE_USER
from heaserver.service.oidcclaimhdrs import SUB
from aiohttp import web
import logging
from typing import Union, Dict, Optional, Type, AsyncGenerator, List
from yarl import URL
from enum import Enum


class EnumWithAttrs(Enum):

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj


class PermissionGroup(EnumWithAttrs):
    """
    Enum that maps heaobject's root.Permission enum values to get, post, put, and delete REST API calls.

    In order to execute a GET request for an object, the user must have at least one of the permissions in the
    GETTER_PERMS permission group (VIEWER, COOWNER, or EDITOR) for the object.

    In order to execute a POST request to create an object, the user must have at least one of the permissions in the
    POSTER_PERMS permission group (CREATOR, COOWNER) for the container in which the object will be created.

    In order to execute a PUT request to update an object, the user must have at least one of the permissions in the
    PUTTER_PERMS permission group (EDITOR, COOWNER) for the object.

    In order to execute a DELETE request to delete an object, the user must have at least one of the permissions in the
    DELETER_PERMS permission group (DELETER, COOWNER) for the object.
    """

    def __init__(self, perms):
        self.perms = perms

    GETTER_PERMS = [Permission.VIEWER, Permission.COOWNER, Permission.EDITOR, Permission.CHECK_DYNAMIC]
    PUTTER_PERMS = [Permission.EDITOR, Permission.COOWNER, Permission.CHECK_DYNAMIC]
    POSTER_PERMS = [Permission.CREATOR, Permission.COOWNER]
    DELETER_PERMS = [Permission.DELETER, Permission.COOWNER, Permission.CHECK_DYNAMIC]


async def new_heaobject_from_type_name(request: web.Request, type_name: str) -> DesktopObject:
    """
    Creates a new HEA desktop object from the body of a HTTP request.
    :param request: the HTTP request.
    :param type_name: the type name of DesktopObject.
    :return: an instance of the given DesktopObject type.
    :raises DeserializeException: if creating a HEA object from the request body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    obj = desktop_object_type_for_name(type_name)()
    return await populate_heaobject(request, obj)


async def new_heaobject_from_type(request: web.Request, type_: Type[DesktopObjectTypeVar]) -> DesktopObjectTypeVar:
    """
    Creates a new HEA desktop object from the body of a HTTP request. If the object's owner is None or no owner
    property was provided, the owner is set to the current user.

    :param request: the HTTP request.
    :param type_: A DesktopObject type. This is compared to the type of the HEA desktop object in the request body, and
    a DeserializeException is raised if the type of the HEA object is not an instance of this type. If the desktop
    object in the body has no type attribute, the type is assumed to be the provided type_.
    :return: an instance of the given DesktopObject type.
    :raises DeserializeException: if creating a HEA object from the request body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    try:
        representor = representor_factory.from_content_type_header(request.headers['Content-Type'])
        _logger.debug('Using %s input parser', representor)
        result = await representor.parse(request)
        _logger.debug('Got dict %s', result)
        actual_type = desktop_object_type_for_name(result['type']) if 'type' in result else type_
        if not issubclass(actual_type, type_):
            raise TypeError(f'Type of object in request body must be type {type_} but was {actual_type}')
        if result.get('owner', None) is None:
            result['owner'] = request.headers.get(SUB, None)
        obj = actual_type()
        obj.from_dict(result)
        return obj
    except ParseException as e:
        _logger.exception('Failed to parse %s', await request.text())
        raise DeserializeException from e
    except (ValueError, TypeError) as e:
        _logger.exception('Failed to parse %s', result)
        raise DeserializeException from e
    except Exception as e:
        raise DeserializeException from e


async def populate_heaobject(request: web.Request, obj: DesktopObjectTypeVar) -> DesktopObjectTypeVar:
    """
    Populate an HEA desktop object from a POST or PUT HTTP request.

    :param request: the HTTP request. Required.
    :param obj: the HEAObject instance. Required.
    :return: the populated object.
    :raises DeserializeException: if creating a HEA object from the request body's contents failed.
    """
    _logger = logging.getLogger(__name__)
    try:
        representor = representor_factory.from_content_type_header(request.headers['Content-Type'])
        _logger.debug('Using %s input parser', representor)
        result = await representor.parse(request)
        _logger.debug('Got dict %s', result)
        obj.from_dict(result)
        return obj
    except (ParseException, ValueError) as e:
        _logger.exception('Failed to parse %s%s', obj, e)
        raise DeserializeException from e
    except Exception as e:
        _logger.exception('Got exception %s', e)
        raise DeserializeException from e


async def type_to_resource_url(request: web.Request, type_or_type_name: Union[str, Type[DesktopObject]],
                               file_system_type_or_type_name: Union[str, Type[FileSystem]] = DefaultFileSystem,
                               file_system_name: str = DEFAULT_FILE_SYSTEM) -> Optional[str]:
    """
    Use the HEA registry service to get the resource URL for accessing HEA objects of the given type.

    :param request: the HTTP request. Required.
    :param type_or_type_name: the type or type name of HEA desktop object. Required.
    :param file_system_type_or_type_name: the type of file system. The default is DefaultFileSystem.
    :param file_system_name: the name of a file system. The default is filesystems.DEFAULT.
    :return: the URL string, or None if no resource URL was found.
    """
    return await client.get_resource_url(request.app, type_or_type_name, file_system_type_or_type_name,
                                         file_system_name)


async def get_dict(request: web.Request, id_: str, type_or_type_name: Union[str, Type[DesktopObject]],
                   file_system_type_or_type_name: Union[str, Type[FileSystem]] = DefaultFileSystem,
                   file_system_name: str = DEFAULT_FILE_SYSTEM,
                   headers: Optional[Dict[str, str]] = None) -> Optional[DesktopObjectDict]:
    """
    Gets the HEA desktop object dict with the provided id from the service for the given type, file system type,
    and file system name.

    :param request: the aiohttp request (required).
    :param id_: the id of the HEA desktop object of interest.
    :param type_or_type_name: the desktop object type or type name.
    :param file_system_type_or_type_name: the file system type or type name.
    :param file_system_name: the file system name.
    :param headers: optional HTTP headers to use.
    :return: the requested HEA desktop object dict, or None if not found.
    :raises ValueError: if no appropriate service was found.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_or_type_name,
                                     file_system_type_or_type_name=file_system_type_or_type_name,
                                     file_system_name=file_system_name)
    if url is None:
        raise ValueError(
            f'No service for type {type_or_type_name}, file system type {file_system_type_or_type_name} and file system name {file_system_name} found')
    return await client.get_dict(request.app, URL(url) / id_, headers)


async def get(request: web.Request, id_: str, type_: Type[DesktopObjectTypeVar],
              file_system_type_or_type_name: Union[str, Type[FileSystem]] = DefaultFileSystem,
              file_system_name: str = DEFAULT_FILE_SYSTEM,
              headers: Optional[Dict[str, str]] = None) -> Optional[DesktopObjectTypeVar]:
    """
    Gets the HEA desktop object with the provided id from the service for the given type, file system type, and file
    system name.

    :param request: the aiohttp request (required).
    :param id_: the id of the HEA desktop object of interest.
    :param type_: the desktop object type.
    :param file_system_type_or_type_name: the file system type or type name.
    :param file_system_name: the file system name.
    :param headers: optional HTTP headers to use.
    :return: the requested HEA desktop object, or None if not found.
    :raises ValueError: if no appropriate service was found.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_,
                                     file_system_type_or_type_name=file_system_type_or_type_name,
                                     file_system_name=file_system_name)
    if url is None:
        raise ValueError(
            f'No service for type {type_}, file system type {file_system_type_or_type_name} and file system name {file_system_name} found')

    return await client.get(request.app, URL(url) / id_, type_, headers)


async def get_all(request: web.Request, type_: Type[DesktopObjectTypeVar],
                  file_system_type_or_type_name: Union[str, Type[FileSystem]] = DefaultFileSystem,
                  file_system_name: str = DEFAULT_FILE_SYSTEM,
                  headers: Optional[Dict[str, str]] = None) -> AsyncGenerator[DesktopObjectTypeVar, None]:
    """
    Async generator for all HEA desktop objects from the service for the given type, file system type, and file system
    name.

    :param request: the aiohttp request (required).
    :param type_: the desktop object type.
    :param file_system_type_or_type_name: the file system type or type name.
    :param file_system_name: the file system name.
    :param headers: optional HTTP headers to use.
    :return: an async generator with the requested desktop objects.
    :raises ValueError: if no appropriate service was found.
    """
    url = await type_to_resource_url(request, type_or_type_name=type_,
                                     file_system_type_or_type_name=file_system_type_or_type_name,
                                     file_system_name=file_system_name)
    if url is None:
        raise ValueError(
            f'No service for type {type_}, file system type {file_system_type_or_type_name} and file system name {file_system_name} found')

    return client.get_all(request.app, url, type_, headers)


def has_permissions(obj: DesktopObject, sub: Optional[str], permissions: List[Permission]) -> bool:
    """
    Return whether the provided user subject has any of the provided permissions to the object.

    :param obj: the HEA desktop object to check (required).
    :param sub: the user subject.
    :param permissions: a list of Permission enum values (required).
    :return: True or False.
    """
    return obj.has_permissions(sub if sub is not None else NONE_USER, permissions)

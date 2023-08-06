"""Connectivity to a MongoDB database for HEA resources.
"""
import io
from contextlib import contextmanager, ExitStack

from heaserver.service.db.mongoexpr import mongo_expr, sub_filter_expr
from heaserver.service.heaobjectsupport import PermissionGroup
from mongoquery import Query
from aiohttp import web
from pymongo.results import UpdateResult, DeleteResult
from motor.motor_asyncio import AsyncIOMotorGridOut
from heaobject.root import DesktopObject, DesktopObjectDict
from typing import Optional, List, IO, Generator, Dict
from unittest.mock import MagicMock
from heaserver.service.db.database import InMemoryDatabase, DatabaseManager
from heaserver.service.db.mongo import MONGO_RELEVANT_COLLECTIONS
from heaserver.service.aiohttp import AsyncReader
from heaserver.service.response import SupportsAsyncRead
import configparser


class MockMongo(InMemoryDatabase):

    def __init__(self, config: Optional[configparser.ConfigParser], **kwargs) -> None:
        """
        Sets the db property of the app context with a motor MongoDB client instance.

        :param config: a configparser.ConfigParser object. MockMongo does not have a config section of its own.
        """
        super().__init__(config, **kwargs)

    async def get(self, request: web.Request, collection: str, var_parts=None, mongoattributes=None,
                  sub: Optional[str] = None) -> Optional[dict]:
        """
        Gets an object from the database.

        :param request: the aiohttp Request object (required).
        :param collection: the Mongo DB collection (required).
        :param var_parts: the names of the dynamic resource's variable parts (required).
        :param mongoattributes: the attribute to query by. The default value is None. If None, the var_parts will be
        used as the attributes to query by.
        :param sub: the user to filter by.
        :return: a HEA name-value pair dict, or None if not found.
        """
        query = Query(mongo_expr(request,
                                 var_parts=var_parts,
                                 mongoattributes=mongoattributes,
                                 extra=sub_filter_expr(sub, permissions=[perm.name for perm in
                                                                         PermissionGroup.GETTER_PERMS.perms])))
        return next((d for d in self.get_desktop_objects_by_collection(collection) if query.match(d)), None)

    async def get_content(self, request: web.Request, collection: str, var_parts=None, mongoattributes=None,
                          sub: Optional[str] = None) -> Optional[SupportsAsyncRead]:
        """
        Handles getting a HEA object's associated content.

        :param request: the HTTP request. Required.
        :param collection: the Mongo collection name. Required.
        :return: a Response with the requested HEA object or Not Found.
        """
        obj = await self.get(request, collection, var_parts, mongoattributes, sub)
        if obj is None:
            return None
        b = self.get_content_by_collection_and_id(collection, obj['id'])
        if b is not None:
            return AsyncReader(b)
        else:
            return None

    async def get_all(self, request: web.Request, collection: str, var_parts=None, mongoattributes=None,
                      sub: Optional[str] = None) -> List[dict]:
        """
        Handle a get request.

        :param request: the HTTP request (required).
        :param collection: the MongoDB collection containing the requested object (required).
        :param var_parts: the names of the dynamic resource's variable parts (required).
        :param mongoattributes: the attributes to query by. The default value is None. If None, the var_parts will be
        used as the attributes to query by.
        :param sub: the user to filter by.
        :return: an iterator of HEA name-value pair dicts with the results of the mockmongo query.
        """
        query = Query(mongo_expr(request,
                                 var_parts=var_parts,
                                 mongoattributes=mongoattributes,
                                 extra=sub_filter_expr(sub, permissions=[perm.name for perm in
                                                                         PermissionGroup.GETTER_PERMS.perms])))
        return [d for d in self.get_desktop_objects_by_collection(collection) if query.match(d)]

    async def empty(self, request: web.Request, collection: str, var_parts=None, mongoattributes=None,
                    sub: Optional[str] = None) -> bool:
        """
        Returns whether there are no results returned from the query.

        :param request: the HTTP request (required).
        :param collection: the MongoDB collection containing the requested object (required).
        :param var_parts: the names of the dynamic resource's variable parts (required).
        :param mongoattributes: the attributes to query by. The default value is None. If None, the var_parts will be
        used as the attributes to query by.
        :param sub: the user to filter by.
        :return: True or False.
        """
        query = Query(mongo_expr(request,
                                 var_parts=var_parts,
                                 mongoattributes=mongoattributes,
                                 extra=sub_filter_expr(sub, permissions=[perm.name for perm in
                                                                         PermissionGroup.GETTER_PERMS.perms])))
        return not any(d for d in self.get_desktop_objects_by_collection(collection) if query.match(d))

    async def post(self, request: web.Request, obj: DesktopObject, collection: str,
                   default_content: Optional[IO] = None) -> Optional[str]:
        """
        Handle a post request.

        :param request: the HTTP request (required).
        :param obj: the HEAObject instance to post.
        :param collection: the MongoDB collection containing the requested object (required).
        :param default_content: the default content to store.
        :return: the generated id of the created object.
        """
        obj.id = '3'  # type: ignore[misc]
        f = self.get_desktop_object_by_collection_and_id(collection, obj.id)
        if obj is None or f is not None:
            return None
        else:
            return obj.id

    async def put(self, request: web.Request, obj: DesktopObject, collection: str,
                  sub: Optional[str] = None) -> UpdateResult:
        """
        Handle a put request.

        :param request: the HTTP request (required).
        :param obj: the HEAObject instance to put.
        :param collection: the MongoDB collection containing the requested object (required).
        :return: an object with a matched_count attribute that contains the number of records updated.
        """
        result = MagicMock(type=UpdateResult)
        result.raw_result = None
        result.acknowledged = True
        f = self.get_desktop_object_by_collection_and_id(collection, request.match_info['id'])
        result.matched_count = result.modified_count = 1 if f is not None else 0
        return result

    async def put_content(self, request: web.Request, collection: str, sub: Optional[str] = None) -> Optional[
        AsyncIOMotorGridOut]:
        """
        Handle a put request of an HEA object's content.

        :param request: the HTTP request (required).
        :param collection: the MongoDB collection containing the requested object (required).
        :return: Whether or not it was successful.
        """
        obj = await self.get(request, collection, var_parts=['id'])
        if obj is None:
            return None
        buffer = io.BytesIO()
        while chunk := await request.content.read(1024):
            buffer.write(chunk)
        if buffer.getvalue() != b'The quick brown fox jumps over the lazy dog':
            return None
        return buffer

    async def delete(self, request: web.Request, collection: str, var_parts=None, mongoattributes=None,
                     sub: Optional[str] = None) -> DeleteResult:
        """
        Handle a delete request.

        :param request: the HTTP request.
        :param collection: the MongoDB collection containing the requested object (required).
        :return: an object with a deleted_count attribute that contains the number of records deleted.
        """
        query = Query(mongo_expr(request,
                                 var_parts=var_parts,
                                 mongoattributes=mongoattributes,
                                 extra=sub_filter_expr(sub, permissions=[perm.name for perm in
                                                                         PermissionGroup.DELETER_PERMS.perms])))
        to_be_deleted = next((d for d in self.get_desktop_objects_by_collection(collection) if query.match(d)), None)
        result = MagicMock(type=DeleteResult)
        result.raw_result = None
        result.acknowledged = True
        result.deleted_count = 1 if to_be_deleted is not None else 0
        return result


class MockMongoManager(DatabaseManager):
    """
    Database manager for a mock of MongoDB that stores collections in memory.
    """

    def __init__(self) -> None:
        super().__init__()
        self.__mongo: Optional[MockMongo] = None

    @classmethod
    def get_relevant_collections(cls) -> Optional[list[str]]:
        super_colls = super().get_relevant_collections()
        return (super_colls or []) + MONGO_RELEVANT_COLLECTIONS

    def start_database(self, context_manager: ExitStack) -> None:
        self.__mongo = MockMongo(None)
        super().start_database(context_manager)

    def insert_desktop_objects(self, desktop_objects: Optional[Dict[str, List[DesktopObjectDict]]]):
        super().insert_desktop_objects(desktop_objects)
        assert self.__mongo is not None
        if desktop_objects:
            rel_coll = self.get_relevant_collections()
            self.__mongo.add_desktop_objects({k: v for k, v in desktop_objects.items() if k in (rel_coll if rel_coll is not None else [k])})

    def insert_content(self, content: Optional[Dict[str, Dict[str, bytes]]]):
        super().insert_content(content)
        assert self.__mongo is not None
        if content:
            rel_coll = self.get_relevant_collections()
            self.__mongo.add_content({k: v for k, v in content.items() if k in (rel_coll if rel_coll is not None else [k])})

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[MockMongo, None, None]:
        if self.__mongo is None:
            raise ValueError('The database is not running. Call start_database() first.')
        yield self.__mongo

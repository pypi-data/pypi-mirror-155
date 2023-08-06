"""
Code for running a docker container containing a mongodb database.

This module assumes the testcontainers package is installed. Do not import it into environments where testcontainers
will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI interface.
"""
from contextlib import ExitStack
from testcontainers.mongodb import MongoDbContainer

from .testenv import RegistryContainerConfig
from ..db.mongo import MongoManager, replace_id_with_object_id
from .docker import DockerImages, get_exposed_port, get_bridge_ip
from array import array
from io import BytesIO
from typing import Optional, List, Dict
from bson import ObjectId
from heaobject import root
import gridfs
import logging


class DockerMongoManager(MongoManager):
    def __init__(self):
        """
        No-arg constructor. Subclasses must call this constructor.
        """
        super().__init__()
        self.__mongo = None
        self.__mongodb_connection_string = None

    def start_database(self, context_manager: ExitStack):
        logger = logging.getLogger(__name__)
        mongo_container = MongoDbContainer(DockerImages.MONGODB.value)
        self.__mongo = context_manager.enter_context(mongo_container)
        self.__mongodb_connection_string = f'mongodb://test:test@{self.__mongo.get_container_host_ip()}:{get_exposed_port(self.__mongo, 27017)}/hea?authSource=admin'
        logger.info('Mongo has connection string %s', self.__mongodb_connection_string)
        super().start_database(context_manager)

    def insert_desktop_objects(self, desktop_objects: Optional[Dict[str, List[root.DesktopObjectDict]]]):
        assert self.started, 'Database not started'
        super().insert_desktop_objects(desktop_objects)
        db_ = self.__mongo.get_connection_client().hea
        for k, v in desktop_objects.items() if desktop_objects is not None else {}:
            rel_coll = self.get_relevant_collections()
            if v and k in (rel_coll if rel_coll is not None else [k]):
                db_[k].insert_many(replace_id_with_object_id(f) for f in v)

    def insert_content(self, content: Optional[Dict[str, Dict[str, bytes]]]):
        assert self.started, 'Database not started'
        super().insert_content(content)
        db_ = self.__mongo.get_connection_client().hea
        content_ = content if content is not None else {}
        for k in content_:
            rel_coll = self.get_relevant_collections()
            if k in (rel_coll if rel_coll is not None else [k]):
                fs = gridfs.GridFSBucket(db_, bucket_name=k)
                for id_, d in content_[k].items():
                    if isinstance(d, (bytes, bytearray, array)):
                        with BytesIO(d) as b:
                            fs.upload_from_stream_with_id(ObjectId(id_), id_, b)

    @classmethod
    def get_environment_updates(cls) -> dict[str, str]:
        result = super().get_environment_updates()
        result['MONGO_DB'] = 'hea'
        return result

    def get_microservice_env_vars(self) -> dict[str, str]:
        assert self.__mongo is not None, 'Database not started'
        result = super().get_microservice_env_vars()
        result.update({
            'MONGO_HEA_DATABASE': 'hea',
            'MONGO_HEA_USERNAME': 'test',
            'MONGO_HEA_PASSWORD': 'test',
            'MONGO_HOSTNAME': get_bridge_ip(self.__mongo)
        })
        return result

    def get_config_file_section(self) -> str:
        assert self.__mongodb_connection_string is not None, 'Database not started'
        result = super().get_config_file_section()
        result += f"""
    [MongoDB]
    ConnectionString = {self.__mongodb_connection_string}
    """
        return result


class RealRegistryContainerConfig(RegistryContainerConfig):
    """
    Creates a registry service configured to access another docker container containing a mongodb database. This
    class depends on the testcontainers package being installed.

    This class assumes that the testcontainers package is installed. Do not create instances of it when testcontainers
    will not be available, for example, in any code that needs to run outside automated testing or the SwaggerUI
    interface. Using it as a type annotation for optional parameters and the like where no actual instances of it
    will be created is okay, however.

    :param image: the label of the docker image to use (required).
    """
    def __init__(self, image: str):
        super().__init__(image=image, port=8080, check_path='/components', db_manager_cls=DockerMongoManager)

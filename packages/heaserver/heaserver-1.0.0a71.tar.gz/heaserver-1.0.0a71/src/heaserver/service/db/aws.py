import configparser
from abc import ABC
from contextlib import contextmanager
from functools import partial

import boto3
from aiohttp.web_request import Request

from heaobject.account import AWSAccount
from heaobject.bucket import AWSBucket
from heaobject.root import DesktopObjectDict
from heaobject.folder import AWSS3Folder
from heaobject.data import AWSS3FileObject

from .database import Database, DatabaseManager
from .awss3bucketobjectkey import decode_key
from typing import Optional, Any, Generator, Callable
from configparser import ConfigParser
import asyncio
from io import BytesIO
import logging


class AWS(Database, ABC):
    """
    Connectivity to Amazon Web Services (AWS) for HEA microservices. Subclasses must call this constructor.
    """

    def __init__(self, config: Optional[configparser.ConfigParser], **kwargs) -> None:
        super().__init__(config, **kwargs)


class S3(AWS):
    """
    Connectivity to AWS Simple Storage Service (S3) for HEA microservices.
    """

    def __init__(self, config: Optional[ConfigParser], **kwargs):
        super().__init__(config, **kwargs)

    async def get_client(self, request: Request, service_name: str, volume_id: str) -> Any:
        """
        Gets an AWS service client.  If the volume has no credentials, it uses the boto3 library to try and find them.
        This method is not designed to be overridden.

        :param request: the HTTP request (required).
        :param service_name: AWS service name (required).
        :param volume_id: the id string of a volume (required).
        :return: a Mongo client for the file system specified by the volume's file_system_name attribute. If no volume_id
        was provided, the return value will be the "default" Mongo client for the microservice found in the HEA_DB
        application-level property.
        :raise ValueError: if there is no volume with the provided volume id, the volume's file system does not exist,
        the volume's credentials were not found, or a necessary service is not registered.
        """

        if volume_id is not None:
            file_system, credentials = \
                await self.get_file_system_and_credentials_from_volume(request, volume_id)
            loop = asyncio.get_running_loop()
            if credentials is None:
                return await loop.run_in_executor(None, boto3.client, service_name)
            else:
                return await loop.run_in_executor(None, partial(boto3.client, service_name,
                                                                region_name=credentials.where,
                                                                aws_access_key_id=credentials.account,
                                                                aws_secret_access_key=credentials.password))
        else:
            raise ValueError('volume_id is required')

    async def get_resource(self, request: Request, service_name: str, volume_id: str) -> Any:
        """
        Gets an AWS resource. If the volume has no credentials, it uses the boto3 library to try and find them. This
        method is not designed to be overridden.

        :param request: the HTTP request (required).
        :param service_name: AWS service name (required).
        :param volume_id: the id string of a volume (required).
        :return: a Mongo client for the file system specified by the volume's file_system_name attribute. If no volume_id
        was provided, the return value will be the "default" Mongo client for the microservice found in the HEA_DB
        application-level property.
        :raise ValueError: if there is no volume with the provided volume id, the volume's file system does not exist,
        the volume's credentials were not found, or a necessary service is not registered.
        """

        if volume_id is not None:
            file_system, credentials = await self.get_file_system_and_credentials_from_volume(request, volume_id)
            loop = asyncio.get_running_loop()
            if credentials is None:
                return await loop.run_in_executor(None, boto3.resource, service_name)
            else:
                return await loop.run_in_executor(None, partial(boto3.resource, service_name,
                                                                region_name=credentials.where,
                                                                aws_access_key_id=credentials.account,
                                                                aws_secret_access_key=credentials.password))
        else:
            raise ValueError('volume_id is required')


class S3Manager(DatabaseManager):
    """
    Database manager for mock Amazon Web Services S3 buckets. It will not make any calls to actual S3 buckets. This
    class is not designed to be subclassed.
    """

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[S3, None, None]:
        yield S3(config)

    @classmethod
    def get_relevant_collections(cls) -> Optional[list[str]]:
        super_colls = super().get_relevant_collections()
        return (super_colls or []) + list(cls.get_desktop_object_inserters().keys())

    def insert_desktop_objects(self, desktop_objects: Optional[dict[str, list[DesktopObjectDict]]]):
        super().insert_desktop_objects(desktop_objects)
        logger = logging.getLogger(__name__)
        for k, v in desktop_objects.items() if desktop_objects is not None else {}:
            rel_coll = self.get_relevant_collections()
            if k not in (rel_coll if rel_coll is not None else [k]):
                continue
            logger.debug('Inserting %s collection object %s', k, v)
            inserters = self.get_desktop_object_inserters()
            if k in inserters:
                inserters[k](v)

    def insert_content(self, content: Optional[dict[str, dict[str, bytes]]]):
        super().insert_content(content)
        if content is not None:
            client = boto3.client('s3')
            for k, v in content.items():
                rel_coll = self.get_relevant_collections()
                if k not in (rel_coll if rel_coll is not None else [k]):
                    continue
                if k == 'awss3files':
                    for id_, content_ in content[k].items():
                        with BytesIO(content_) as f:
                            client.upload_fileobj(f, 'arp-scale-2-cloud-bucket-with-tags11', decode_key(id_))
                else:
                    raise KeyError(f'Unexpected key {k}')

    @classmethod
    def get_desktop_object_inserters(cls) -> dict[str, Callable[[list[DesktopObjectDict]], None]]:
        return {'awsaccounts': cls.__awsaccount_inserter,
                'buckets': cls.__bucket_inserter,
                'awss3folders': cls.__awss3folder_inserter,
                'awss3files': cls.__awss3file_inserter}

    @classmethod
    def __awss3file_inserter(cls, v):
        for awss3file_dict in v:
            awss3file = AWSS3FileObject()
            awss3file.from_dict(awss3file_dict)
            cls.__create_awss3file(awss3file)

    @classmethod
    def __awss3folder_inserter(cls, v):
        for awss3folder_dict in v:
            awss3folder = AWSS3Folder()
            awss3folder.from_dict(awss3folder_dict)
            cls.__create_awss3folder(awss3folder)

    @classmethod
    def __bucket_inserter(cls, v):
        for bucket_dict in v:
            awsbucket = AWSBucket()
            awsbucket.from_dict(bucket_dict)
            cls.__create_bucket(awsbucket)

    @classmethod
    def __awsaccount_inserter(cls, v):
        for awsaccount_dict in v:
            awsaccount = AWSAccount()
            awsaccount.from_dict(awsaccount_dict)
            cls.__create_awsaccount(awsaccount)

    @staticmethod
    def __create_awsaccount(account: AWSAccount):
        client = boto3.client('organizations')
        client.create_account(Email=account.email_address, AccountName=account.display_name)

    @staticmethod
    def __create_bucket(bucket: AWSBucket):
        client = boto3.client('s3')
        if bucket is not None :
            if bucket.name is None:
                raise ValueError('bucket.name cannot be None')
            if bucket.region != 'us-east-1':
                client.create_bucket(Bucket=bucket.name, CreateBucketConfiguration={'LocationConstraint': bucket.region})
            else:
                client.create_bucket(Bucket=bucket.name)

    @staticmethod
    def __create_awss3folder(awss3folder: AWSS3Folder):
        client = boto3.client('s3')
        client.put_object(Bucket='arp-scale-2-cloud-bucket-with-tags11', Key=awss3folder.display_name + '/')

    @staticmethod
    def __create_awss3file(awss3file):
        client = boto3.client('s3')
        client.put_object(Bucket='arp-scale-2-cloud-bucket-with-tags11', Key=awss3file.display_name)


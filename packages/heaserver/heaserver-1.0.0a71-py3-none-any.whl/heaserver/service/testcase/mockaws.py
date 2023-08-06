"""
Classes and functions for mocking Amazon S3 buckets.

This module assumes the moto package is installed. Do not import it into environments where moto will
not be available, for example, in any code that needs to run outside automated testing.
"""
import configparser
from configparser import ConfigParser
from contextlib import contextmanager, AbstractContextManager, ExitStack
from typing import Optional, Tuple, Generator, AsyncGenerator, Union

from heaserver.service.db.aws import S3, S3Manager

from heaobject.keychain import Credentials
from heaobject.volume import AWSFileSystem, Volume, FileSystem, DEFAULT_FILE_SYSTEM
from heaobject.root import DesktopObjectDict, DesktopObject
from aiohttp.web import Request

import boto3
from moto import mock_s3, mock_organizations
from heaserver.service.db.database import InMemoryDatabase
from freezegun import freeze_time


class MockS3WithMockMongo(S3, InMemoryDatabase):
    """
    Makes the S3 class' methods use moto instead of actual AWS. Moto is documented at
    https://github.com/spulec/moto.
    """

    def __init__(self, config: Optional[ConfigParser], **kwargs):
        super().__init__(config, **kwargs)
        section = super().get_config_section()
        if config and section in config:
            database_section = config[section]
            self.__region_name: Optional[str] = database_section.get('RegionName', None)
            self.__aws_access_key_id: Optional[str] = database_section.get('AWSAccessKeyId', None)
            self.__aws_secret_access_key: Optional[str] = database_section.get('AWSSecretAccessKey', None)
        else:
            self.__region_name = None
            self.__aws_access_key_id = None
            self.__aws_secret_access_key = None

    async def get_file_system_and_credentials_from_volume(self, request: Request, volume_id: Optional[str]) -> Tuple[
        AWSFileSystem, Optional[Credentials]]:

        if self.__aws_secret_access_key is not None or self.__aws_access_key_id is not None:
            creds = Credentials()
            creds.where = self.__region_name
            creds.account = self.__aws_access_key_id
            creds.password = self.__aws_secret_access_key
        else:
            volume_dict = self.get_desktop_object_by_collection_and_id('volumes', volume_id)
            if volume_dict is None:
                raise ValueError(f'No volume found with id {volume_id}')
            volume = Volume()
            volume.from_dict(volume_dict)
            if volume.credential_id is None:
                creds = None
            else:
                credentials_dict = self.get_desktop_object_by_collection_and_id('credentials', volume.credential_id)
                if credentials_dict is None:
                    raise ValueError(f'No credentials with id {volume.credential_id}')
                creds = Credentials()
                creds.from_dict(credentials_dict)
        return AWSFileSystem(), creds

    async def get_volumes(self, request: Request, file_system_type_or_type_name: Union[str, type[FileSystem]]) -> AsyncGenerator[Volume, None]:
        for volume_dict in self.get_desktop_objects_by_collection('volumes'):
            if isinstance(file_system_type_or_type_name, DesktopObject):
                file_system_type_or_type_name_ = file_system_type_or_type_name.get_type_name()
            else:
                file_system_type_or_type_name_ = str(file_system_type_or_type_name)
            if volume_dict.get('file_system_type', DEFAULT_FILE_SYSTEM) == file_system_type_or_type_name_:
                volume = Volume()
                volume.from_dict(volume_dict)
                yield volume



class MockS3Manager(S3Manager):
    def __init__(self):
        super().__init__()
        self.__mock_s3 = None

    @classmethod
    def get_environment_updates(cls) -> dict[str, str]:
        result = super().get_environment_updates()
        result.update({'AWS_ACCESS_KEY_ID': 'testing',
                'AWS_SECRET_ACCESS_KEY': 'testing',
                'AWS_SECURITY_TOKEN': 'testing',
                'AWS_SESSION_TOKEN': 'testing',
                'AWS_DEFAULT_REGION': 'us-east-1'
                })
        return result

    @classmethod
    def get_context(cls) -> list[AbstractContextManager]:
        result = super().get_context()
        result.extend([mock_s3(), mock_organizations(), freeze_time("2022-05-17")])
        return result

    def insert_desktop_objects(self, desktop_objects: Optional[dict[str, list[DesktopObjectDict]]]):
        client = boto3.client('organizations')
        client.create_organization(FeatureSet='ALL')
        super().insert_desktop_objects(desktop_objects)

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[S3, None, None]:
        yield S3(config)


class MockS3ManagerWithMockMongo(MockS3Manager):
    """
    Database manager for Amazon Web Services S3 buckets. It will make any calls to actual S3 buckets. This class is not
    designed to be subclassed.
    """

    def __init__(self):
        super().__init__()
        self.__mock_s3 = None

    @classmethod
    def get_relevant_collections(cls) -> Optional[list[str]]:
        return (super().get_relevant_collections() or []) + ['volumes', 'credentials']

    def start_database(self, context_manager: ExitStack) -> None:
        self.__mock_s3 = MockS3WithMockMongo(None)
        super().start_database(context_manager)

    @classmethod
    def get_context(cls) -> list[AbstractContextManager]:
        result = super().get_context()
        result.extend([mock_s3(), mock_organizations(), freeze_time("2022-05-17")])
        return result

    def insert_desktop_objects(self, desktop_objects: Optional[dict[str, list[DesktopObjectDict]]]):
        client = boto3.client('organizations')
        client.create_organization(FeatureSet='ALL')
        rel_coll = self.get_relevant_collections()
        self.__mock_s3.add_desktop_objects({k: v for k, v in desktop_objects.items() if k in (rel_coll if rel_coll is not None else [k])} if desktop_objects is not None else None)
        super().insert_desktop_objects(desktop_objects)

    def insert_content(self, content: Optional[dict[str, dict[str, bytes]]]):
        rel_coll = self.get_relevant_collections()
        self.__mock_s3.add_content({k: v for k, v in content.items() if k in (rel_coll if rel_coll is not None else [k])} if content is not None else None)
        return super().insert_content(content)

    @contextmanager
    def database(self, config: configparser.ConfigParser = None) -> Generator[MockS3WithMockMongo, None, None]:
        yield self.__mock_s3

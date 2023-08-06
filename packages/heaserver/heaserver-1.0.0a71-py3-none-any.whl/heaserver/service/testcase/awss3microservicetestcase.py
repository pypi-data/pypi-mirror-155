from heaobject.registry import Resource
from heaobject.volume import DEFAULT_FILE_SYSTEM

from ..testcase.dockermongo import DockerMongoManager
from .microservicetestcase import get_test_case_cls_default as _get_test_case_cls_default
from .testenv import DockerContainerConfig
from .dockermongo import RealRegistryContainerConfig
from functools import partial

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'
HEASERVER_VOLUMES_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-volumes:1.0.0a10'
HEASERVER_KEYCHAIN_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-keychain:1.0.0a4'
volume_microservice = DockerContainerConfig(image=HEASERVER_VOLUMES_IMAGE, port=8080, check_path='/volumes',
                                            resources=[Resource(resource_type_name='heaobject.volume.Volume',
                                                                base_path='/volumes',
                                                                file_system_name=DEFAULT_FILE_SYSTEM),
                                                       Resource(resource_type_name='heaobject.volume.FileSystem',
                                                                base_path='/filesystems',
                                                                file_system_name=DEFAULT_FILE_SYSTEM)],
                                            db_manager_cls=DockerMongoManager)
keychain_microservice = DockerContainerConfig(image=HEASERVER_KEYCHAIN_IMAGE, port=8080, check_path='/credentials',
                                              resources=[
                                                  Resource(resource_type_name='heaobject.keychain.Credentials',
                                                           base_path='/credentials',
                                                           file_system_name=DEFAULT_FILE_SYSTEM)],
                                              db_manager_cls=DockerMongoManager)

get_test_case_cls_default = partial(_get_test_case_cls_default,
                                                   registry_docker_image=RealRegistryContainerConfig(
                                                       HEASERVER_REGISTRY_IMAGE),
                                                   other_docker_images=[volume_microservice, keychain_microservice])

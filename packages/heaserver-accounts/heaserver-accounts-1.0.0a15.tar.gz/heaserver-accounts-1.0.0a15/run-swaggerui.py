#!/usr/bin/env python3

from heaserver.account import service
from heaserver.service.testcase import swaggerui
from integrationtests.heaserver.accountintegrationtest.testcase import db_store
from aiohttp.web import get, delete, post, put, view
from heaserver.service.testcase.testenv import DockerContainerConfig, DockerVolumeMapping
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaserver.service.db.aws import S3Manager
from heaserver.service.wstl import builder_factory
import logging
from heaobject.volume import DEFAULT_FILE_SYSTEM
from heaobject.registry import Resource
from pathlib import Path

logging.basicConfig(level=logging.DEBUG)

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'
HEASERVER_VOLUMES_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-volumes:1.0.0a10'
HEASERVER_KEYCHAIN_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-keychain:1.0.0a4'
HEASERVER_BUCKETS_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-buckets:1.0.0a5'

if __name__ == '__main__':
    volume_microservice = DockerContainerConfig(image=HEASERVER_VOLUMES_IMAGE, port=8080, check_path='/volumes',
                                                db_manager_cls=DockerMongoManager,
                                              resources=[Resource(resource_type_name='heaobject.volume.Volume',
                                                                  base_path='/volumes',
                                                                  file_system_name=DEFAULT_FILE_SYSTEM),
                                                         Resource(resource_type_name='heaobject.volume.FileSystem',
                                                                  base_path='/filesystems',
                                                                  file_system_name=DEFAULT_FILE_SYSTEM)])
    keychain_microservice = DockerContainerConfig(image=HEASERVER_KEYCHAIN_IMAGE, port=8080, check_path='/credentials',
                                                  db_manager_cls=DockerMongoManager,
                                                resources=[Resource(resource_type_name='heaobject.keychain.Credentials',
                                                                    base_path='/credentials',
                                                                    file_system_name=DEFAULT_FILE_SYSTEM)])
    bucket_microservice = DockerContainerConfig(image=HEASERVER_BUCKETS_IMAGE, port=8080, check_path='/ping',
                                                db_manager_cls=DockerMongoManager,  # Switch to S3Manager for version 1.0.0a6.
                                              resources=[Resource(resource_type_name='heaobject.bucket.AWSBucket',
                                                                  base_path='/volumes',
                                                                  file_system_type="heaobject.volume.AWSFileSystem",
                                                                  file_system_name=DEFAULT_FILE_SYSTEM)],
                                              volumes=[DockerVolumeMapping(host=str(Path.home() / '.aws'), container='/home/app/.aws')])
    swaggerui.run(project_slug='heaserver-accounts', desktop_objects={k: v for k, v in db_store.items() if k in DockerMongoManager.get_relevant_collections()},
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/volumes/{volume_id}/awsaccounts/me', service.get_awsaccount_by_volume_id),
                   (get, '/awsaccounts/{id}', service.get_awsaccount),
                   (get, '/awsaccounts', service.get_awsaccounts),
                   (view, '/volumes/{volume_id}/awsaccounts/me/opener', service.get_awsaccount_opener_by_volume_id),
                   (view, '/awsaccounts/{id}/opener', service.get_awsaccount_opener),
                   (get, '/volumes/{volume_id}/awsaccounts/me/buckets', service.get_buckets)],
                  registry_docker_image=HEASERVER_REGISTRY_IMAGE,
                  other_microservice_images=[keychain_microservice, volume_microservice, bucket_microservice],
                  db_manager_cls=S3Manager)

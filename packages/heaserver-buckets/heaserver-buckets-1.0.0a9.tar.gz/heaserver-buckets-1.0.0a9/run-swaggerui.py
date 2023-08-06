#!/usr/bin/env python3
from heaobject.registry import Resource
from heaobject import user

from heaserver.bucket import service
from heaserver.service.testcase import swaggerui
from heaserver.service.wstl import builder_factory
from heaserver.service.db.aws import S3Manager
from heaserver.service.testcase.dockermongo import DockerMongoManager
from aiohttp.web import get, delete, post, view, options
from heaserver.service.testcase.testenv import DockerContainerConfig
import logging
from heaobject.volume import DEFAULT_FILE_SYSTEM

logging.basicConfig(level=logging.DEBUG)

db_values = {
    'components': [
        {
            'id': '666f6f2d6261722d71757578',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Reximus',
            'invited': [],
            'modified': None,
            'name': 'reximus',
            'owner': user.NONE_USER,
            'shared_with': [],
            'source': None,
            'type': 'heaobject.registry.Component',
            'version': None,
            'base_url': 'http://localhost:8080',
            'resources': [{'type': 'heaobject.registry.Resource', 'resource_type_name': 'heaobject.folder.AWSS3Folder',
                           'base_path': '/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders'},
                          {'type': 'heaobject.registry.Resource', 'resource_type_name': 'heaobject.folder.AWSS3Item',
                           'base_path': '/items'}]
        }
    ],
    'filesystems': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': user.NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.AWSFileSystem',
        'version': None
    }],
    'volumes': [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'My Amazon Web Services',
        'invited': [],
        'modified': None,
        'name': 'amazon_web_services',
        'owner': user.NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.Volume',
        'version': None,
        'file_system_name': 'amazon_web_services',
        'file_system_type': 'heaobject.volume.AWSFileSystem',
        'credential_id': None  # Let boto3 try to find the user's credentials.
    }
    ]

}

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'
HEASERVER_VOLUMES_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-volumes:1.0.0a10'
HEASERVER_KEYCHAIN_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-keychain:1.0.0a4'

if __name__ == '__main__':
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
    swaggerui.run(project_slug='heaserver-buckets', desktop_objects=db_values,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/volumes/{volume_id}/buckets/{id}', service.get_bucket),
                          (get, '/volumes/{volume_id}/buckets', service.get_all_buckets),
                          (get, '/volumes/{volume_id}/buckets/byname/{bucket_name}', service.get_bucket_by_name),
                          (post, '/volumes/{volume_id}/buckets', service.post_bucket),
                          (view, '/volumes/{volume_id}/buckets/{id}/opener', service.get_bucket_opener),
                          (delete, '/volumes/{volume_id}/buckets/{id}', service.delete_bucket),
                          (options, '/volumes/{volume_id}/buckets', service.get_buckets_options),
                          (options, '/volumes/{volume_id}/buckets/{id}', service.get_bucket_options)
                          ],
                  registry_docker_image=HEASERVER_REGISTRY_IMAGE,
                  other_microservice_images=[keychain_microservice, volume_microservice],
                  db_manager_cls=S3Manager)

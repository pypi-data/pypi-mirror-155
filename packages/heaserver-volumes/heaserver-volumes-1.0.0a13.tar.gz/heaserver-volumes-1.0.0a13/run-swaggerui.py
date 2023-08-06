#!/usr/bin/env python3

from heaserver.volume import service
from heaserver.service.testcase import swaggerui
from heaserver.service.testcase.testenv import DockerContainerConfig
from heaserver.service.wstl import builder_factory
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaobject.registry import Resource
from aiohttp.web import get, delete, post, put, view
from integrationtests.heaserver.volumeintegrationtest.testcase import db_store
import logging

logging.basicConfig(level=logging.DEBUG)

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'
HEASERVER_FOLDER_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-folders:1.0.0a28'

if __name__ == '__main__':
    swaggerui.run(project_slug='heaserver-volumes', desktop_objects=db_store,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/volumes/{id}', service.get_volume),
                          (get, '/volumes/byname/{name}', service.get_volume_by_name),
                          (get, '/volumes/', service.get_all_volumes),
                          (get, '/volumes/{id}/content', service.get_volume_content),
                          (post, '/volumes', service.post_volume),
                          (put, '/volumes/{id}', service.put_volume),
                          (delete, '/volumes/{id}', service.delete_volume),
                          (view, '/volumes/{id}/opener', service.get_volume_opener),
                          (get, '/volumes/byfilesystemtype/{type}/',
                           service.get_volumes_by_file_system_type),
                          (get,
                           '/volumes/byfilesystemtype/{type}/byfilesystemname/{name}/',
                           service.get_volumes_by_file_system_type_and_name),
                          (get, '/filesystems/{id}', service.get_file_system),
                          (get, '/filesystems/bytype/{type}/byname/{name}',
                           service.get_file_system_by_type_and_name),
                          (get, '/filesystems/', service.get_all_file_systems),
                          (post, '/filesystems', service.post_file_system),
                          (put, '/filesystems/{id}', service.put_file_system),
                          (delete, '/filesystems/{id}', service.delete_file_system)
                          ],
                  registry_docker_image=HEASERVER_REGISTRY_IMAGE,
                  other_microservice_images=[DockerContainerConfig(image=HEASERVER_FOLDER_IMAGE,
                                                                   port=8086,
                                                                   check_path='/folders/root/items',
                                                                   db_manager_cls=DockerMongoManager,
                                                                   resources=[Resource(
                                                                       resource_type_name='heaobject.folder.Folder',
                                                                       base_path='/folders')])])

#!/usr/bin/env python3

from heaserver.folder import service
from heaserver.service.testcase import swaggerui
from heaserver.service.wstl import builder_factory
from aiohttp.web import get, post, put, delete, view
from integrationtests.heaserver.folderintegrationtest.foldertestcase import db_values
import logging

logging.basicConfig(level=logging.DEBUG)

HEASERVER_REGISTRY_IMAGE = 'registry.gitlab.com/huntsman-cancer-institute/risr/hea/heaserver-registry:1.0.0a24'

if __name__ == '__main__':
    swaggerui.run(project_slug='heaserver-folders', desktop_objects=db_values,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/folders/{folder_id}/items/{id}', service.get_item),
                   (get, '/folders/{folder_id}/items', service.get_items),
                   (post, '/folders/{folder_id}/items', service.post_item_in_folder),
                   (put, '/folders/{folder_id}/items/{id}', service.put_item_in_folder),
                   (delete, '/folders/{folder_id}/items/{id}', service.delete_item),
                   (get, '/folders/{id}', service.get_folder),
                   (get, '/folders/', service.get_folders),
                   (get, '/folders/byname/{name}', service.get_folder_by_name),
                   (view, '/folders/{id}/opener', service.get_folder_opener),
                   (post, '/folders', service.post_folder),
                   (put, '/folders/{id}', service.put_folder),
                   (delete, '/folders/{id}', service.delete_folder)
                   ], registry_docker_image=HEASERVER_REGISTRY_IMAGE)

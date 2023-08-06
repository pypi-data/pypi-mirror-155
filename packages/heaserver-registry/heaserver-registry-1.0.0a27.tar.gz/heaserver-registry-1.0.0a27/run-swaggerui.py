#!/usr/bin/env python3

from heaserver.registry import service
from heaserver.service.testcase import swaggerui
from heaserver.service.wstl import builder_factory
from integrationtests.heaserver.registryintegrationtest.componenttestcase import db_store
from aiohttp.web import get, delete, post, put, view
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    swaggerui.run(project_slug='heaserver-registry', desktop_objects=db_store,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/components/{id}', service.get_component),
                          (get, '/components/byname/{name}', service.get_component_by_name),
                          (get,
                           '/components/bytype/{type}/byfilesystemtype/{filesystemtype}/byfilesystemname/{filesystemname}',
                           service.get_component_by_type),
                          (get, '/components/', service.get_all_components),
                          (post, '/components', service.post_component),
                          (put, '/components/{id}', service.put_component),
                          (delete, '/components/{id}', service.delete_component),
                          (get, '/properties/{id}', service.get_property),
                          (get, '/properties/byname/{name}', service.get_property_by_name),
                          (get, '/properties/', service.get_all_properties),
                          (post, '/properties', service.post_property),
                          (put, '/properties/{id}', service.put_property),
                          (delete, '/properties/{id}', service.delete_property)
                          ])

#!/usr/bin/env python3

from heaserver.dataadapter import service
from heaserver.service.testcase import swaggerui
from heaserver.service.wstl import builder_factory
from integrationtests.heaserver.dataadapterintegrationtest.dataadaptertestcase import db_store
from aiohttp.web import get, delete, post, put, view
import logging

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    swaggerui.run(project_slug='heaserver-data-adapters', desktop_objects=db_store,
                  wstl_builder_factory=builder_factory(service.__package__),
                  routes=[(get, '/dataadapters/{id}', service.get_data_adapter),
                          (get, '/dataadapters/byname/{name}',
                           service.get_data_adapter_by_name),
                          (get, '/dataadapters/', service.get_all_data_adapters),
                          (post, '/dataadapters', service.post_data_adapter),
                          (put, '/dataadapters/{id}', service.put_data_adapter),
                          (delete, '/dataadapters/{id}',
                           service.delete_data_adapter)])

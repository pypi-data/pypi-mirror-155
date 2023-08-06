"""
Creates a test case class for use with the unittest library that is build into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.dataadapter import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGO_DATA_ADAPTER_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invited': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.dataadapter.FlatFileAdapter',
        'version': None,
        'base_url': 'http://localhost/foo',
        'resources': []
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus',
            'invited': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [],
            'source': None,
            'type': 'heaobject.dataadapter.FlatFileAdapter',
            'version': None,
            'base_url': 'http://localhost/foo',
            'resources': []
        }]}

DataAdapterTestCase = get_test_case_cls_default(coll=service.MONGO_DATA_ADAPTER_COLLECTION,
                                                href='http://localhost:8080/dataadapters/',
                                                wstl_package=service.__package__,
                                                fixtures=db_store,
                                                get_actions=[
                                                    Action(
                                                        name='heaserver-data-adapters-data-adapter-get-properties',
                                                        rel=['properties']),
                                                    Action(name='heaserver-data-adapters-data-adapter-duplicate',
                                                           url='http://localhost:8080/dataadapters/{id}/duplicator',
                                                           rel=['duplicator'])
                                                ],
                                                get_all_actions=[
                                                    Action(
                                                        name='heaserver-data-adapters-data-adapter-get-properties',
                                                        rel=['properties']),
                                                    Action(name='heaserver-data-adapters-data-adapter-duplicate',
                                                           url='http://localhost:8080/dataadapters/{id}/duplicator',
                                                           rel=['duplicator'])],
                                                duplicate_action_name='heaserver-data-adapters-data-adapter-duplicate-form')

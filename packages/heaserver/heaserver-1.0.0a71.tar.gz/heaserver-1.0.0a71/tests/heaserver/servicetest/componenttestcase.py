"""
Creates a test case class for use with the unittest library that is build into Python.
"""
import heaserver.service.db.database
import heaserver.service.testcase.mockmongo
from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase import expectedvalues, TEST_USER
from . import service
from heaobject.user import NONE_USER, ALL_USERS
from heaobject.root import Permission, HEAObjectDict
from heaobject.volume import DEFAULT_FILE_SYSTEM
from typing import Dict, List
from datetime import datetime
from pytz import utc

fixtures: Dict[str, List[HEAObjectDict]] = {
    service.MONGODB_COMPONENT_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': datetime(2021, 12, 2, 17, 31, 15, 630000, tzinfo=utc),
        'derived_by': None,
        'derived_from': ['foo', 'bar'],
        'description': None,
        'display_name': 'Reximus',
        'invites': [],
        'modified': datetime(2021, 12, 2, 17, 31, 15, 630000, tzinfo=utc),
        'name': 'reximus',
        'owner': NONE_USER,
        'shared_with': [],
        'shares': [{
            'type': 'heaobject.root.ShareImpl',
            'invite': None,
            'user': ALL_USERS,
            'permissions': [Permission.COOWNER.name]
        }],
        'source': None,
        'type': 'heaobject.registry.Component',
        'version': None,
        'base_url': 'http://localhost',
        'resources': [{
            'type': 'heaobject.registry.Resource',
            'resource_type_name': 'heaobject.folder.Folder',
            'base_path': '/folders',
            'file_system_name': DEFAULT_FILE_SYSTEM
        },
            {
                'type': 'heaobject.registry.Resource',
                'resource_type_name': 'heaobject.folder.Item',
                'base_path': '/items',
            }
        ]
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': datetime(2021, 12, 2, 17, 31, 15, 630000, tzinfo=utc),
            'derived_by': None,
            'derived_from': ['oof', 'rab'],
            'description': None,
            'display_name': 'Luximus',
            'invites': [],
            'modified': datetime(2021, 12, 2, 17, 31, 15, 630000, tzinfo=utc),
            'name': 'luximus',
            'owner': NONE_USER,
            'shared_with': [],
            'shares': [{
                'type': 'heaobject.root.ShareImpl',
                'invite': None,
                'user': ALL_USERS,
                'permissions': [Permission.EDITOR.name]
            }],
            'source': None,
            'type': 'heaobject.registry.Component',
            'version': None,
            'base_url': 'http://localhost/foo',
            'resources': [{
                'type': 'heaobject.registry.Resource',
                'resource_type_name': 'heaobject.folder.Folder',
                'base_path': '/folders',
            },
                {
                    'type': 'heaobject.registry.Resource',
                    'resource_type_name': 'heaobject.folder.Item',
                    'base_path': '/items',
                    'file_system_name': DEFAULT_FILE_SYSTEM
                }]
        }
    ]}

content = {
    service.MONGODB_COMPONENT_COLLECTION: {
        '666f6f2d6261722d71757578': b'The quick brown fox jumps over the lazy dog'
    }
}

ComponentTestCase = \
    get_test_case_cls_default(coll=service.MONGODB_COMPONENT_COLLECTION, fixtures=fixtures,
                              duplicate_action_name='component-duplicate-form',
                              db_manager_cls=heaserver.service.testcase.mockmongo.MockMongoManager,
                              wstl_package=service.__package__, content=content, content_type='text/plain',
                              put_content_status=204, include_root=True,
                              href='http://localhost:8080/components/',
                              get_actions=[expectedvalues.Action(name='component-get-properties',
                                                                 rel=['hea-properties']),
                                           expectedvalues.Action(name='component-get-open-choices',
                                                                 url='http://localhost:8080/components/{id}/opener',
                                                                 rel=['hea-opener-choices']),
                                           expectedvalues.Action(name='component-duplicate',
                                                                 url='http://localhost:8080/components/{id}/duplicator',
                                                                 rel=['hea-duplicator'])],
                              get_all_actions=[
                                  expectedvalues.Action(name='component-get-properties',
                                                        rel=['hea-properties']),
                                  expectedvalues.Action(name='component-get-open-choices',
                                                        url='http://localhost:8080/components/{id}/opener',
                                                        rel=['hea-opener-choices']),
                                  expectedvalues.Action(name='component-duplicate',
                                                        url='http://localhost:8080/components/{id}/duplicator',
                                                        rel=['hea-duplicator'])],
                              expected_opener=expectedvalues.Link(
                                  url=f'http://localhost:8080/components/{fixtures[service.MONGODB_COMPONENT_COLLECTION][0]["id"]}/content',
                                  rel=['hea-default', 'hea-opener', 'text/plain']), sub=TEST_USER)

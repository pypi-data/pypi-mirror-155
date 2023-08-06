from . import service
from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase.expectedvalues import Action, Link
from heaserver.service.testcase.dockermongo import DockerMongoManager

from typing import Dict, List, Any
from heaserver.service.testcase import TEST_USER
from heaobject.user import ALL_USERS, NONE_USER
from heaobject.root import Permission

fixtures: Dict[str, List[Dict[str, Any]]] = {
    service.MONGODB_COMPONENT_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': ['foo', 'bar'],
        'description': None,
        'display_name': 'Reximus',
        'invited': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [{
            'type': 'heaobject.root.ShareImpl',
            'invite': None,
            'user': ALL_USERS,
            'permissions': [Permission.COOWNER.name]
        }],
        'source': None,
        'type': 'heaobject.registry.Component',
        'version': None,
        'base_url': 'http://localhost/foo',
        'resources': [{
                'type': 'heaobject.registry.Resource',
                'resource_type_name': 'heaobject.folder.Folder',
                'base_path': '/folders'
            }]
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': ['oof', 'rab'],
            'description': None,
            'display_name': 'Luximus',
            'invited': [],
            'modified': None,
            'name': 'luximus',
            'owner': TEST_USER,
            'source': None,
            'type': 'heaobject.registry.Component',
            'version': None,
            'base_url': 'http://localhost/foo',
            'resources': [{
                'type': 'heaobject.registry.Resource',
                'resource_type_name': 'heaobject.folder.Folder',
                'base_path': '/folders'
            }]
        }
    ]}

content = {
    service.MONGODB_COMPONENT_COLLECTION: {
        '666f6f2d6261722d71757578': b'The quick brown fox jumps over the lazy dog'
    }
}

ComponentTestCase = get_test_case_cls_default(coll=service.MONGODB_COMPONENT_COLLECTION, fixtures=fixtures,
                                              duplicate_action_name='component-duplicate-form',
                                              db_manager_cls=DockerMongoManager, wstl_package=service.__package__,
                                              content=content, content_type='text/plain', put_content_status=204,
                                              include_root=True, href='http://localhost:8080/components/',
                                              get_actions=[Action(name='component-get-properties',
                                                                  rel=['hea-properties']),
                                                           Action(name='component-get-open-choices',
                                                                  url='http://localhost:8080/components/{id}/opener',
                                                                  rel=['hea-opener-choices']),
                                                           Action(name='component-duplicate',
                                                                  url='http://localhost:8080/components/{id}/duplicator',
                                                                  rel=['hea-duplicator'])],
                                              get_all_actions=[Action(name='component-get-properties',
                                                                      rel=['hea-properties']),
                                                               Action(name='component-get-open-choices',
                                                                      url='http://localhost:8080/components/{id}/opener',
                                                                      rel=['hea-opener-choices']),
                                                               Action(name='component-duplicate',
                                                                      url='http://localhost:8080/components/{id}/duplicator',
                                                                      rel=['hea-duplicator'])],
                                              expected_opener=Link(
                                                  url=f'http://localhost:8080/components/{fixtures[service.MONGODB_COMPONENT_COLLECTION][0]["id"]}/content',
                                                  rel=['hea-default', 'hea-opener', 'text/plain']), sub=TEST_USER)

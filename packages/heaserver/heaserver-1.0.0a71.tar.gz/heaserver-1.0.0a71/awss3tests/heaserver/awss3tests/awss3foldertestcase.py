"""
Runs integration tests for the HEA folder service.

Note that each test opens an aiohttp server listening on port 8080.
"""

from heaserver.service.testcase import expectedvalues, microservicetestcase
from . import service
from heaserver.service.testcase.mockaws import MockS3ManagerWithMockMongo
from heaobject import user


db_values = {'folders_items': [
    {
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'TestFolder',
        'id': 'VGVzdEZvbGRlci8=',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'VGVzdEZvbGRlci8=',
        'owner': user.NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.folder.AWSS3Item',
        'actual_object_type_name': 'heaobject.folder.AWSS3Folder',
        'actual_object_id': 'VGVzdEZvbGRlci8=',
        'actual_object_uri': '/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/VGVzdEZvbGRlci8=',
        'version': None,
        's3_uri':'s3://arp-scale-2-cloud-bucket-with-tags11/TestFolder/',
        'storage_class': 'STANDARD',
        'mime_type': 'application/x.item',
        'size': None,
        'human_readable_size': None,
        'volume_id': None,
        'folder_id': 'root'
    },
    {
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'TestFolder2',
        'id': 'VGVzdEZvbGRlcjIv',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'VGVzdEZvbGRlcjIv',
        'owner': user.NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.folder.AWSS3Item',
        'actual_object_type_name': 'heaobject.folder.AWSS3Folder',
        'actual_object_id': 'VGVzdEZvbGRlcjIv',
        'actual_object_uri': '/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/VGVzdEZvbGRlcjIv',
        'version': None,
        's3_uri':'s3://arp-scale-2-cloud-bucket-with-tags11/TestFolder2/',
        'storage_class': 'STANDARD',
        'mime_type': 'application/x.item',
        'size': None,
        'human_readable_size': None,
        'volume_id': None,
        'folder_id': 'root'
    }
],
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
    }],
'buckets': [ {
        "arn": None,
        "created": '2022-05-17T00:00:00+00:00',
        "derived_by": None,
        "derived_from": [],
        "description": None,
        "display_name": "arp-scale-2-cloud-bucket-with-tags11",
        "encrypted": True,
        "id": "arp-scale-2-cloud-bucket-with-tags11",
        "invites": [],
        "locked": False,
        "mime_type": "application/x.awsbucket",
        "modified": '2022-05-17T00:00:00+00:00',
        "name": "arp-scale-2-cloud-bucket-with-tags11",
        "object_count": None,
        "owner": "system|none",
        "permission_policy": None,
        "region": "us-west-2",
        "s3_uri": "s3://arp-scale-2-cloud-bucket-with-tags11/",
        "shares": [],
        "size": None,
        "source": None,
        "tags": [],
        "type": "heaobject.bucket.AWSBucket",
        "version": None,
        "versioned": False
  }],
    'awsaccounts': [
        {
            'email_address': 'no-reply@example.com',
            'alternate_contact_name': None,
            "alternate_email_address": None,
            "alternate_phone_number": None,
            "created": '2022-05-17T00:00:00+00:00',
            "derived_by": None,
            "derived_from": [],
            "description": None,
            "display_name": "311813441058",
            "full_name": None,
            "id": "311813441058",
            "invites": [],
            "mime_type": "application/x.awsaccount",
            "modified": '2022-05-17T00:00:00+00:00',
            "name": "311813441058",
            "owner": "system|none",
            "phone_number": None,
            "shares": [],
            "source": None,
            "type": "heaobject.account.AWSAccount",
            "version": None
        }
    ],
'awss3folders': [{
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'TestFolder',
        'id': 'VGVzdEZvbGRlci8=',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'VGVzdEZvbGRlci8=',
        'owner': user.NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.folder.AWSS3Folder',
        'version': None,
        'mime_type': 'application/x.folder',
        's3_uri': 's3://arp-scale-2-cloud-bucket-with-tags11/TestFolder/',
        'storage_class': 'STANDARD'
    },
    {
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'TestFolder2',
        'id': 'VGVzdEZvbGRlcjIv',
        'invites': [],
        'modified': '2022-05-17T00:00:00+00:00',
        'name': 'VGVzdEZvbGRlcjIv',
        'owner': user.NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.folder.AWSS3Folder',
        'version': None,
        'mime_type': 'application/x.folder',
        's3_uri': 's3://arp-scale-2-cloud-bucket-with-tags11/TestFolder2/',
        'storage_class': 'STANDARD'
    }
]

}

content_ = [{'collection': {'version': '1.0', 'href': 'http://localhost:8080/folders/root/items/', 'items': [{'data': [
    {'name': 'created', 'value': None, 'prompt': 'created', 'display': True},
    {'name': 'derived_by', 'value': None, 'prompt': 'derived_by', 'display': True},
    {'name': 'derived_from', 'value': [], 'prompt': 'derived_from', 'display': True},
    {'name': 'description', 'value': None, 'prompt': 'description', 'display': True},
    {'name': 'display_name', 'value': 'Reximus', 'prompt': 'display_name', 'display': True},
    {'name': 'id', 'value': '666f6f2d6261722d71757578', 'prompt': 'id', 'display': False},
    {'name': 'invites', 'value': [], 'prompt': 'invites', 'display': True},
    {'name': 'modified', 'value': None, 'prompt': 'modified', 'display': True},
    {'name': 'name', 'value': 'reximus', 'prompt': 'name', 'display': True},
    {'name': 'owner', 'value': 'system|none', 'prompt': 'owner', 'display': True},
    {'name': 'shares', 'value': [], 'prompt': 'shares', 'display': True},
    {'name': 'source', 'value': None, 'prompt': 'source', 'display': True},
    {'name': 'version', 'value': None, 'prompt': 'version', 'display': True},
    {'name': 'actual_object_type_name', 'value': 'heaobject.folder.Folder', 'prompt': 'actual_object_type_name',
     'display': True},
    {'name': 'actual_object_id', 'value': '666f6f2d6261722d71757579', 'prompt': 'actual_object_id', 'display': True},
    {'name': 'folder_id', 'value': 'root', 'prompt': 'folder_id', 'display': True},
    {'section': 'actual_object', 'name': 'created', 'value': None, 'prompt': 'created', 'display': True},
    {'section': 'actual_object', 'name': 'derived_by', 'value': None, 'prompt': 'derived_by', 'display': True},
    {'section': 'actual_object', 'name': 'derived_from', 'value': [], 'prompt': 'derived_from', 'display': True},
    {'section': 'actual_object', 'name': 'description', 'value': None, 'prompt': 'description', 'display': True},
    {'section': 'actual_object', 'name': 'display_name', 'value': 'Reximus', 'prompt': 'display_name', 'display': True},
    {'section': 'actual_object', 'name': 'id', 'value': '666f6f2d6261722d71757579', 'prompt': 'id', 'display': False},
    {'section': 'actual_object', 'name': 'invites', 'value': [], 'prompt': 'invites', 'display': True},
    {'section': 'actual_object', 'name': 'modified', 'value': None, 'prompt': 'modified', 'display': True},
    {'section': 'actual_object', 'name': 'name', 'value': 'reximus', 'prompt': 'name', 'display': True},
    {'section': 'actual_object', 'name': 'owner', 'value': 'system|none', 'prompt': 'owner', 'display': True},
    {'section': 'actual_object', 'name': 'shares', 'value': [], 'prompt': 'shares', 'display': True},
    {'section': 'actual_object', 'name': 'source', 'value': None, 'prompt': 'source', 'display': True},
    {'section': 'actual_object', 'name': 'version', 'value': None, 'prompt': 'version', 'display': True},
    {'section': 'actual_object', 'name': 'mime_type', 'value': 'application/x.folder', 'prompt': 'mime_type',
     'display': True}], 'links': [{'prompt': 'Move', 'rel': 'mover',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/mover'},
                                  {'prompt': 'Open', 'rel': 'hea-opener-choices',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/opener'},
                                  {'prompt': 'Duplicate', 'rel': 'duplicator',
                                   'href': 'http://localhost:8080/folders/root/items/666f6f2d6261722d71757578/duplicator'}]}],
                            'template': {'prompt': 'Properties', 'rel': 'properties', 'data': [
                                {'name': 'id', 'value': '666f6f2d6261722d71757578', 'prompt': 'Id', 'required': True,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'source', 'value': None, 'prompt': 'Source', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'version', 'value': None, 'prompt': 'Version', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'display_name', 'value': 'Reximus', 'prompt': 'Name', 'required': True,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'description', 'value': None, 'prompt': 'Description', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'owner', 'value': 'system|none', 'prompt': 'Owner', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'created', 'value': None, 'prompt': 'Created', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'modified', 'value': None, 'prompt': 'Modified', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'invites', 'value': [], 'prompt': 'Share invites', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'shares', 'value': [], 'prompt': 'Shared with', 'required': False,
                                 'readOnly': False, 'pattern': ''},
                                {'name': 'derived_by', 'value': None, 'prompt': 'Derived by', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'derived_from', 'value': [], 'prompt': 'Derived from', 'required': False,
                                 'readOnly': True, 'pattern': ''},
                                {'name': 'items', 'value': None, 'prompt': 'Items', 'required': False, 'readOnly': True,
                                 'pattern': ''}]}}}, {
                'collection': {'version': '1.0', 'href': 'http://localhost:8080/folders/root/items/', 'items': [{
                    'data': [
                        {
                            'name': 'created',
                            'value': None,
                            'prompt': 'created',
                            'display': True},
                        {
                            'name': 'derived_by',
                            'value': None,
                            'prompt': 'derived_by',
                            'display': True},
                        {
                            'name': 'derived_from',
                            'value': [],
                            'prompt': 'derived_from',
                            'display': True},
                        {
                            'name': 'description',
                            'value': None,
                            'prompt': 'description',
                            'display': True},
                        {
                            'name': 'display_name',
                            'value': 'Reximus',
                            'prompt': 'display_name',
                            'display': True},
                        {
                            'name': 'id',
                            'value': '0123456789ab0123456789ab',
                            'prompt': 'id',
                            'display': False},
                        {
                            'name': 'invites',
                            'value': [],
                            'prompt': 'invites',
                            'display': True},
                        {
                            'name': 'modified',
                            'value': None,
                            'prompt': 'modified',
                            'display': True},
                        {
                            'name': 'name',
                            'value': 'reximus',
                            'prompt': 'name',
                            'display': True},
                        {
                            'name': 'owner',
                            'value': 'system|none',
                            'prompt': 'owner',
                            'display': True},
                        {
                            'name': 'shares',
                            'value': [],
                            'prompt': 'shares',
                            'display': True},
                        {
                            'name': 'source',
                            'value': None,
                            'prompt': 'source',
                            'display': True},
                        {
                            'name': 'version',
                            'value': None,
                            'prompt': 'version',
                            'display': True},
                        {
                            'name': 'actual_object_type_name',
                            'value': 'heaobject.folder.Folder',
                            'prompt': 'actual_object_type_name',
                            'display': True},
                        {
                            'name': 'actual_object_id',
                            'value': '0123456789ab0123456789ac',
                            'prompt': 'actual_object_id',
                            'display': True},
                        {
                            'name': 'folder_id',
                            'value': 'root',
                            'prompt': 'folder_id',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'created',
                            'value': None,
                            'prompt': 'created',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'derived_by',
                            'value': None,
                            'prompt': 'derived_by',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'derived_from',
                            'value': [],
                            'prompt': 'derived_from',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'description',
                            'value': None,
                            'prompt': 'description',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'display_name',
                            'value': 'Reximus',
                            'prompt': 'display_name',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'id',
                            'value': '0123456789ab0123456789ac',
                            'prompt': 'id',
                            'display': False},
                        {
                            'section': 'actual_object',
                            'name': 'invites',
                            'value': [],
                            'prompt': 'invites',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'modified',
                            'value': None,
                            'prompt': 'modified',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'name',
                            'value': 'reximus',
                            'prompt': 'name',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'owner',
                            'value': 'system|none',
                            'prompt': 'owner',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'shares',
                            'value': [],
                            'prompt': 'shares',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'source',
                            'value': None,
                            'prompt': 'source',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'version',
                            'value': None,
                            'prompt': 'version',
                            'display': True},
                        {
                            'section': 'actual_object',
                            'name': 'mime_type',
                            'value': 'application/x.folder',
                            'prompt': 'mime_type',
                            'display': True}],
                    'links': [
                        {
                            'prompt': 'Move',
                            'rel': 'mover',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/mover'},
                        {
                            'prompt': 'Open',
                            'rel': 'hea-opener-choices',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/opener'},
                        {
                            'prompt': 'Duplicate',
                            'rel': 'duplicator',
                            'href': 'http://localhost:8080/folders/root/items/0123456789ab0123456789ab/duplicator'}]}],
                               'template': {'prompt': 'Properties', 'rel': 'properties', 'data': [
                                   {'name': 'id', 'value': '0123456789ab0123456789ab', 'prompt': 'Id', 'required': True,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'source', 'value': None, 'prompt': 'Source', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'version', 'value': None, 'prompt': 'Version', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'display_name', 'value': 'Reximus', 'prompt': 'Name', 'required': True,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'description', 'value': None, 'prompt': 'Description', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'owner', 'value': 'system|none', 'prompt': 'Owner', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'created', 'value': None, 'prompt': 'Created', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'modified', 'value': None, 'prompt': 'Modified', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'invites', 'value': [], 'prompt': 'Share invites', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'shares', 'value': [], 'prompt': 'Shared with', 'required': False,
                                    'readOnly': False, 'pattern': ''},
                                   {'name': 'derived_by', 'value': None, 'prompt': 'Derived by', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'derived_from', 'value': [], 'prompt': 'Derived from', 'required': False,
                                    'readOnly': True, 'pattern': ''},
                                   {'name': 'items', 'value': None, 'prompt': 'Items', 'required': False,
                                    'readOnly': True, 'pattern': ''}]}}}]

content = {
    'folders': {
        '666f6f2d6261722d71757579': content_
    }
}

AWSS3FolderTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/',
                                                   wstl_package=service.__package__,
                                                   coll='awss3folders',
                                                   fixtures=db_values,
                                                   db_manager_cls=MockS3ManagerWithMockMongo,
                                                   get_all_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-get-open-choices',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-duplicate',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-get-properties',
                                                           rel=['hea-properties']
                                                       )
                                                   ],
                                                   get_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-get-open-choices',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-duplicate',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-folder-get-properties',
                                                           rel=['hea-properties']
                                                       )
                                                   ],
                                                   duplicate_action_name='heaserver-awss3folders-folder-duplicate-form',
                                                   exclude=['body_put', 'body_post'])

AWSS3ItemTestCase = \
    microservicetestcase.get_test_case_cls_default(href='http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/arp-scale-2-cloud-bucket-with-tags11/awss3folders/root/items/',
                                                   wstl_package=service.__package__,
                                                   coll='folders_items',
                                                   fixtures=db_values,
                                                   db_manager_cls=MockS3ManagerWithMockMongo,
                                                   get_all_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-get-open-choices',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-duplicate',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-get-properties',
                                                           rel=['hea-properties']
                                                       ),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-move',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/mover',
                                                           rel=['hea-mover']
                                                       )
                                                   ],
                                                   get_actions=[
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-get-open-choices',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/opener',
                                                           rel=['hea-opener-choices']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-duplicate',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/duplicator',
                                                           rel=['hea-duplicator']),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-get-properties',
                                                           rel=['hea-properties']
                                                       ),
                                                       expectedvalues.Action(
                                                           name='heaserver-awss3folders-item-move',
                                                           url='http://localhost:8080/volumes/{volume_id}/buckets/{bucket_id}/awss3folders/{folder_id}/items/{id}/mover',
                                                           rel=['hea-mover']
                                                       )
                                                   ],
                                                   duplicate_action_name='heaserver-awss3folders-item-duplicate-form',
                                                   exclude=['body_put'])

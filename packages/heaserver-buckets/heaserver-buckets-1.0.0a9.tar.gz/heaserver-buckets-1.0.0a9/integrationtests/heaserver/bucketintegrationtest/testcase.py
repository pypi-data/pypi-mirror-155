"""
Creates a test case class for use with the unittest library that is built into Python.
"""
from heaserver.service.testcase.awss3microservicetestcase import get_test_case_cls_default
from heaserver.bucket import service
from heaserver.service.testcase.mockaws import MockS3Manager
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGODB_BUCKET_COLLECTION: [{
        'id': 'hci-foundation-1',
        'created': '2022-05-17T00:00:00+00:00',
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'object_count': None,
        'size': None,
        'display_name': 'hci-foundation-1',
        'invites': [],
        'modified': None,
        'name': 'hci-foundation-1',
        'owner': NONE_USER,
        'shares': [],
        'source': 'AWS Simple Cloud Storage (S3)',
        'type': 'heaobject.bucket.AWSBucket',
        'version': None,
        'arn': None,
        'versioned': None,
        'encrypted': False,
        'region': 'us-west-1',
        'permission_policy': None,
        'tags': [],
        's3_uri': 's3://hci-foundation-1/',
        'locked': False,
        'mime_type': 'application/x.awsbucket'
    },
        {
            'id': 'hci-foundation-2',
            'created': '2022-05-17T00:00:00+00:00',
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'object_count': None,
            'size': None,
            'display_name': 'hci-foundation-2',
            'invites': [],
            'modified': None,
            'name': 'hci-foundation-2',
            'owner': NONE_USER,
            'shares': [],
            'source': 'AWS Simple Cloud Storage (S3)',
            'type': 'heaobject.bucket.AWSBucket',
            'version': None,
            'arn': None,
            'versioned': None,
            'encrypted': False,
            'region': 'us-west-1',
            'permission_policy': None,
            'tags': [],
            's3_uri': 's3://hci-foundation-2/',
            'locked': False,
            'mime_type': 'application/x.awsbucket'
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
        'owner': NONE_USER,
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
        'owner': NONE_USER,
        'shared_with': [],
        'source': None,
        'type': 'heaobject.volume.Volume',
        'version': None,
        'file_system_name': 'amazon_web_services',
        'credential_id': None  # Let boto3 try to find the user's credentials.
    }]}


TestCase = get_test_case_cls_default(coll=service.MONGODB_BUCKET_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/volumes/666f6f2d6261722d71757578/buckets/',
                                     fixtures=db_store,
                                     db_manager_cls=MockS3Manager,
                                     get_actions=[Action(name='heaserver-buckets-bucket-get-properties',
                                                         rel=['hea-properties']),
                                                  Action(name='heaserver-buckets-bucket-get-open-choices',
                                                         url='http://localhost:8080/volumes/{volume_id}/buckets/{id}/opener',
                                                         rel=['hea-opener-choices']),
                                                  Action(name='heaserver-buckets-bucket-duplicate',
                                                         url='http://localhost:8080/volumes/{volume_id}/buckets/{id}/duplicator',
                                                         rel=['hea-duplicator'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-buckets-bucket-get-properties',
                                                             rel=['hea-properties']),
                                                      Action(name='heaserver-buckets-bucket-get-open-choices',
                                                             url='http://localhost:8080/volumes/{volume_id}/buckets/{id}/opener',
                                                             rel=['hea-opener-choices']),
                                                      Action(name='heaserver-buckets-bucket-duplicate',
                                                             url='http://localhost:8080/volumes/{volume_id}/buckets/{id}/duplicator',
                                                             rel=['hea-duplicator'])],
                                     duplicate_action_name='heaserver-buckets-bucket-duplicate-form',
                                     exclude=['body_put'])

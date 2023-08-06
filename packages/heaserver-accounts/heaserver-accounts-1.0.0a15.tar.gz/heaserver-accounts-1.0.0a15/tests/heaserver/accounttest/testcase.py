"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.account import service
from heaobject.user import NONE_USER
from heaserver.service.testcase import microservicetestcase, expectedvalues
from heaserver.service.testcase.mockaws import MockS3ManagerWithMockMongo

db_store = {
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
    }],
    'awsaccounts': [
        {
            "alternate_contact_name": None,
            "alternate_email_address": None,
            "alternate_phone_number": None,
            "created": "2021-06-08T17:38:31+00:00",
            "derived_by": None,
            "derived_from": [],
            "description": None,
            "display_name": "311813441058",
            "email_address": 'no-reply@example.com',
            "full_name": None,
            "id": "311813441058",
            "invites": [],
            "mime_type": "application/x.awsaccount",
            "modified": None,
            "name": "311813441058",
            "owner": "system|none",
            "phone_number": None,
            "shares": [],
            "source": None,
            "type": "heaobject.account.AWSAccount",
            "version": None
        },
        {
            "alternate_contact_name": None,
            "alternate_email_address": None,
            "alternate_phone_number": None,
            "created": "2021-06-08T17:38:31+00:00",
            "derived_by": None,
            "derived_from": [],
            "description": None,
            "display_name": "311813441058",
            "email_address": 'no-reply@example.com',
            "full_name": None,
            "id": "311813441058",
            "invites": [],
            "mime_type": "application/x.awsaccount",
            "modified": None,
            "name": "311813441058",
            "owner": "system|none",
            "phone_number": None,
            "shares": [],
            "source": None,
            "type": "heaobject.account.AWSAccount",
            "version": None
        }
    ]}

AWSAccountTestCase = \
    microservicetestcase.get_test_case_cls_default(
        href='http://localhost:8080/awsaccounts/',
        wstl_package=service.__package__,
        coll='awsaccounts',
        fixtures=db_store,
        db_manager_cls=MockS3ManagerWithMockMongo,
        get_all_actions=[
            expectedvalues.Action(
                name='heaserver-accounts-account-get-open-choices',
                url='http://localhost:8080/awsaccounts/{id}/opener',
                rel=['hea-opener-choices'])],
        get_actions=[
            expectedvalues.Action(
                name='heaserver-accounts-account-get-open-choices',
                url='http://localhost:8080/volumes/{volume_id}/buckets/{id}/opener',
                rel=['hea-opener-choices'])],
        put_content_status=404,
        duplicate_action_name='heaserver-awsaccounts-awsaccounts-duplicate-form',
        exclude=['body_put', 'body_post']
    )

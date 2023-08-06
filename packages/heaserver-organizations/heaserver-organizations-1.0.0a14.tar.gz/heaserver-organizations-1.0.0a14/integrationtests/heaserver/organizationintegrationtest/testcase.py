"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaserver.organization import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGODB_ORGANIZATION_COLLECTION: [
        {
            "id": "666f6f2d6261722d71757578",
            "source": None,
            "name": "Bob",
            "display_name": "Bob",
            "description": "Description of Bob lab",
            "owner": NONE_USER,
            "created": None,
            "modified": None,
            "invites": [],
            "shares": [],
            "derived_by": None,
            "derived_from": [],
            "aws_account_ids": [],
            "principal_investigator_id": "23423DAFSDF12adfasdf3",
            "manager_ids": ['666f6f2d6261722d71757578'],
            "member_ids": ['0123456789ab0123456789ab'],
            'type': 'heaobject.organization.Organization',
            'version': None
        },
        {
            "id": "0123456789ab0123456789ab",
            "source": None,
            "name": "Reximus",
            "display_name": "Reximus",
            "description": "Description of Reximus",
            "owner": NONE_USER,
            "created": None,
            "modified": None,
            "invites": [],
            "shares": [],
            "derived_by": None,
            "derived_from": [],
            "aws_account_ids": [],
            "principal_investigator_id": "11234867890b0123a56789ab",
            "manager_ids": ["11234867890b0123a56789ab"],
            "member_ids": [],
            'type': 'heaobject.organization.Organization',
            'version': None
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
        'name': 'DEFAULT_FILE_SYSTEM',
        'owner': NONE_USER,
        'shares': [],
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
        'shares': [],
        'source': None,
        'type': 'heaobject.volume.Volume',
        'version': None,
        'file_system_name': 'DEFAULT_FILE_SYSTEM',
        'file_system_type': 'heaobject.volume.AWSFileSystem',
        'credential_id': None  # Let boto3 try to find the user's credentials.
    }],
    'people': [{
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
        'type': 'heaobject.person.Person',
        'version': None
    }, {
        'id': '0123456789ab0123456789ab',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus Thomas',
        'invited': [],
        'modified': None,
        'title': 'Manager',
        'name': 'Reximus Thomas',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'type': 'heaobject.person.Person',
        'version': None
    }]
}
TestCase = get_test_case_cls_default(coll=service.MONGODB_ORGANIZATION_COLLECTION,
                                     href='http://localhost:8080/organizations/',
                                     db_manager_cls=DockerMongoManager,
                                     wstl_package=service.__package__,
                                     fixtures=db_store,
                                     get_actions=[Action(name='heaserver-organizations-organization-get-properties',
                                                         rel=['properties']),
                                                  Action(name='heaserver-organizations-organization-get-open-choices',
                                                         url='http://localhost:8080/organizations/{id}/opener',
                                                         rel=['hea-opener-choices']),
                                                  Action(name='heaserver-organizations-organization-duplicate',
                                                         url='http://localhost:8080/organizations/{id}/duplicator',
                                                         rel=['duplicator'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-organizations-organization-get-properties',
                                                             rel=['properties']),
                                                      Action(
                                                          name='heaserver-organizations-organization-get-open-choices',
                                                          url='http://localhost:8080/organizations/{id}/opener',
                                                          rel=['hea-opener-choices']),
                                                      Action(name='heaserver-organizations-organization-duplicate',
                                                             url='http://localhost:8080/organizations/{id}/duplicator',
                                                             rel=['duplicator'])],
                                     duplicate_action_name='heaserver-organizations-organization-duplicate-form')

"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.keychain import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGODB_CREDENTIALS_COLLECTION: [{
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
        'type': 'heaobject.keychain.Credentials',
        'version': None
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
            'type': 'heaobject.keychain.Credentials',
            'version': None
        }]}

TestCase = get_test_case_cls_default(coll=service.MONGODB_CREDENTIALS_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/credentials/',
                                     fixtures=db_store,
                                     get_actions=[Action(name='heaserver-keychain-credentials-get-properties',
                                                             rel=['properties']),
                                                  Action(name='heaserver-keychain-credentials-open',
                                                             url='http://localhost:8080/credentials/{id}/opener',
                                                             rel=['opener']),
                                                  Action(name='heaserver-keychain-credentials-duplicate',
                                                             url='http://localhost:8080/credentials/{id}/duplicator',
                                                             rel=['duplicator'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-keychain-credentials-get-properties',
                                                             rel=['properties']),
                                                      Action(name='heaserver-keychain-credentials-open',
                                                                 url='http://localhost:8080/credentials/{id}/opener',
                                                                 rel=['opener']),
                                                      Action(name='heaserver-keychain-credentials-duplicate',
                                                                 url='http://localhost:8080/credentials/{id}/duplicator',
                                                                 rel=['duplicator'])],
                                     duplicate_action_name='heaserver-keychain-credentials-duplicate-form')

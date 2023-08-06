"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.person import service
from heaserver.service.testcase.dockermongo import DockerMongoManager
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGODB_PERSON_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus Texamus',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'first_name': 'Reximus',
        'last_name': 'Texamus',
        'type': 'heaobject.person.Person',
        'version': None
    },
        {
            'id': '0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus Tuxamus',
            'invites': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [],
            'source': None,
            'first_name': 'Luximuss',
            'last_name': 'Tuxamus',
            'type': 'heaobject.person.Person',
            'version': None
        }]}

TestCase = get_test_case_cls_default(coll=service.MONGODB_PERSON_COLLECTION,
                                     href='http://localhost:8080/people/',
                                     wstl_package=service.__package__,
                                     db_manager_cls=DockerMongoManager,
                                     fixtures=db_store,
                                     get_actions=[Action(name='heaserver-people-person-get-properties',
                                                             rel=['properties']),
                                                  Action(name='heaserver-people-person-open',
                                                             url='http://localhost:8080/people/{id}/opener',
                                                             rel=['opener']),
                                                  Action(name='heaserver-people-person-duplicate',
                                                             url='http://localhost:8080/people/{id}/duplicator',
                                                             rel=['duplicator'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-people-person-get-properties',
                                                             rel=['properties']),
                                                      Action(name='heaserver-people-person-open',
                                                                 url='http://localhost:8080/people/{id}/opener',
                                                                 rel=['opener']),
                                                      Action(name='heaserver-people-person-duplicate',
                                                                 url='http://localhost:8080/people/{id}/duplicator',
                                                                 rel=['duplicator'])],
                                     duplicate_action_name='heaserver-people-person-duplicate-form')

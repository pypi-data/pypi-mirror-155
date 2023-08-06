"""
Creates a test case class for use with the unittest library that is built into Python.
"""
from typing import Optional

from heaobject.activity import Status
from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.service.testcase.mockmongo import MockMongoManager
from heaserver.activity import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

db_store = {
    service.MONGODB_ACTIVITY_COLLECTION: [{
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
        'action': 'GET',
        'status': Status.COMPLETE.name,
        'arn': 'a:1323444',
        'user_id': 'user-a',
        'source': None,
        'type': 'heaobject.activity.Activity',
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
            'action': 'GET',
            'status': Status.IN_PROGRESS.name,
            'arn': 'a:1323444',
            'user_id': 'user-a',
            'source': None,
            'type': 'heaobject.activity.Activity',
            'version': None
        }]}


class MyDockerMongoManager(MockMongoManager):

    @classmethod
    def get_relevant_collections(cls) -> Optional[list[str]]:
        return super().get_relevant_collections() + [service.MONGODB_ACTIVITY_COLLECTION]


TestCase = get_test_case_cls_default(coll=service.MONGODB_ACTIVITY_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/activity/',
                                     fixtures=db_store,
                                     db_manager_cls=MyDockerMongoManager,
                                     get_actions=[Action(name='heaserver-activity-activity-get-properties',
                                                         rel=['properties']),
                                                  Action(name='heaserver-activity-activity-open',
                                                         url='http://localhost:8080/activity/{id}/opener',
                                                         rel=['opener']),
                                                  Action(name='heaserver-activity-activity-duplicate',
                                                         url='http://localhost:8080/activity/{id}/duplicator',
                                                         rel=['duplicator'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-activity-activity-get-properties',
                                                             rel=['properties']),
                                                      Action(name='heaserver-activity-activity-open',
                                                             url='http://localhost:8080/activity/{id}/opener',
                                                             rel=['opener']),
                                                      Action(name='heaserver-activity-activity-duplicate',
                                                             url='http://localhost:8080/activity/{id}/duplicator',
                                                             rel=['duplicator'])],
                                     duplicate_action_name='heaserver-activity-activity-duplicate-form')

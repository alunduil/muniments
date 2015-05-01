# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

from muniments import common
from muniments.scheduler.api import information

from test_muniments import test_helpers
from test_muniments.test_fixtures import register_fixture
from test_muniments.test_unit.test_scheduler.test_api.test_schedule import SchedulesRequestFixture
from test_muniments.test_unit.test_scheduler.test_models.test_schedule.list_1fd27e1f92ba4ff5b0bffff979556e92 import f_1fd27e1f92ba4ff5b0bffff979556e92 as SCHEDULES

register_fixture(globals(), ( SchedulesRequestFixture, ), {
    'request': {
        'method': 'GET',
        'url': '/{i.API_VERSION}/schedules/'.format(i = information),
    },

    'response': lambda self: {
        'status': 200,
        'headers': {
            'Content-Type': 'application/json',
        },
        'body': json.dumps(
            [ test_helpers.update(_.python, url = '/{i.API_VERSION}/schedules/'.format(i = information)) for _ in self.list_fixture.model_fixtures ],
            default = common.json_encode,
            sort_keys = True
        ),
    },

    'list_fixture': SCHEDULES,
})

register_fixture(globals(), ( SchedulesRequestFixture, ), {
    'description': 'CORS',

    'request': {
        'method': 'GET',
        'url': '/{i.API_VERSION}/schedules/'.format(i = information),
        'headers': {
            'Origin': 'http://127.0.0.1:5000',
        },
    },

    'response': lambda self: {
        'status': 200,
        'headers': {
            'Access-Control-Allow-Origin': 'http://127.0.0.1:5000',
            'Content-Type': 'application/json',
        },
        'body': json.dumps(
            [ test_helpers.update(_.python, url = '/{i.API_VERSION}/schedules/'.format(i = information)) for _ in self.list_fixture.model_fixtures ],
            default = common.json_encode,
            sort_keys = True
        ),
    },

    'list_fixture': SCHEDULES,
})

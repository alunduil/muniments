# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json

from muniments.common import json_encode

from test_muniments.test_fixtures import register_fixture
from test_muniments.test_unit.test_scheduler.test_models.test_schedule import ScheduleModelReadFixture
from test_muniments.test_unit.test_scheduler.test_models.test_schedule import ScheduleModelWriteFixture

DATA = {
    'python': lambda self: {
        '_id': self.uuid,
        'created_at': datetime.datetime(2015, 4, 30, 10, 11, 37, 423780),
        'date': 'every sunday at 2300',
        'recurrences': [
            [ datetime.datetime(2015, 5, 3, 23, 0, 0, 0), None, datetime.timedelta(weeks = 1), ],
        ],
        'updated_at': datetime.datetime(2015, 4, 30, 10, 11, 37, 423780),
    },

    'url': lambda self: '/schedules/{0.uuid}'.format(self),

    'storage': lambda self: {
        'read': {
            'request': {
                'url': self.url,
                'method': 'GET',
            },

            'response': {
                'code': 200,
                'headers': {
                    'Cache-Control': 'must-revalidate',
                    'Content-Type': 'text/plain; charset=utf-8',
                },
                'body': json.dumps(self.python, default = json_encode, sort_keys = True, separators = ( ',', ':', )).encode('utf-8'),
            },
        },

        'write': {
            'request': {
                'url': self.url,
                'method': 'PUT',
                'body': json.dumps(self.python, default = json_encode, sort_keys = True).encode('utf-8'),
            },

            'response': {
                'code': 201,
                'headers': {
                    'Cache-Control': 'must-revalidate',
                    'Content-Type': 'text/plain; charset=utf-8',
                    'Location': 'http://localhost:5984/schedules/8c42557d-a273-4204-92cd-6a16c25a2d74',
                },
                'body': b'{"ok":true,"id":"8c42557d-a273-4204-92cd-6a16c25a2d74","rev":"1-575e3deff1aed7e98682b2e5f426ea90"}',
            },
        },
    },
}

register_fixture(globals(), ( ScheduleModelReadFixture, ), DATA)
register_fixture(globals(), ( ScheduleModelWriteFixture, ), DATA)

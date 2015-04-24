# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from muniments.scheduler.api import information

from test_muniments.test_fixtures import register_fixture
from test_muniments.test_unit.test_scheduler.test_api.test_schedule import SchedulesRequestFixture

register_fixture(globals(), ( SchedulesRequestFixture, ), **{
    'request': {
        'method': 'DELETE',
        'url': '/{i.API_VERSION}/schedules/'.format(i = information),
    },

    'response': {
        'status': 405,
        'headers': {
            'Allow': 'GET, HEAD, OPTIONS, POST',
        },
    },
})

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json

from test_muniments import test_helpers
from test_muniments.test_fixtures import register_fixture
from test_muniments.test_unit.test_scheduler.test_models.test_schedule import ScheduleModelListFixture
from test_muniments.test_unit.test_scheduler.test_models.test_schedule import ScheduleModelReadFixture

register_fixture(globals(), ( ScheduleModelListFixture, ), {
    'model_fixtures': test_helpers.fixtures_from_classes(( ScheduleModelReadFixture, )),

    'storage': lambda self: {
        'response': {
            'code': 200,
            'body': json.dumps({ 'rows': [ { 'id': str(_.uuid), } for _ in self.model_fixtures ] }, sort_keys = True).encode('utf-8'),
        },
    },
})

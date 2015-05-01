# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from test_muniments import test_helpers
from test_muniments.test_common import MetaTest
from test_muniments.test_fixtures.test_requests import RequestFixture
from test_muniments.test_unit.test_scheduler.test_api import SchedulerBaseApiUnitTest


class SchedulesRequestFixture(RequestFixture):
    pass

test_helpers.import_directory(__name__, os.path.dirname(__file__))


class SchedulesApiUnitTest(SchedulerBaseApiUnitTest, metaclass = MetaTest):
    mocks_mask = set().union(SchedulerBaseApiUnitTest.mocks_mask)
    mocks = set().union(SchedulerBaseApiUnitTest.mocks)

    fixture_classes = (
        SchedulesRequestFixture,
    )

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import functools
import os

from muniments.scheduler import models

from test_muniments import test_helpers
from test_muniments.test_common import MetaTest
from test_muniments.test_common.test_models import BaseModelsTest
from test_muniments.test_fixtures.test_models.test_couchdb import CouchDbModelListFixture
from test_muniments.test_fixtures.test_models.test_couchdb import CouchDbModelReadFixture
from test_muniments.test_fixtures.test_models.test_couchdb import CouchDbModelWriteFixture


class ScheduleModelListFixture(CouchDbModelListFixture):
    def run(self):
        self.result = self.context.io_loop.run_sync(models.schedule.list)


class ScheduleModelReadFixture(CouchDbModelReadFixture):
    def run(self):
        self.result = self.context.io_loop.run_sync(functools.partial(models.schedule.read, self.uuid))


class ScheduleModelWriteFixture(CouchDbModelWriteFixture):
    def run(self):
        self.result = self.context.io_loop.run_sync(functools.partial(models.schedule.write, self.python))

test_helpers.import_directory(__name__, os.path.dirname(__file__), sort_key = lambda _: 1 if _.rsplit('.', 1)[-1].startswith('list_') else 0)


class ScheduleModelsSchedulerUnitTest(BaseModelsTest, metaclass = MetaTest):
    mocks_mask = set().union(BaseModelsTest.mocks_mask)
    mocks = set().union(BaseModelsTest.mocks)

    fixture_classes = (
        ScheduleModelListFixture,
        ScheduleModelReadFixture,
        ScheduleModelWriteFixture,
    )

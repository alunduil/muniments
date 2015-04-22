# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from muniments.scheduler.api import SCHEDULER_API_APPLICATION

from test_muniments.test_common.test_api import BaseApiTest


class SchedulerBaseApiUnitTest(BaseApiTest):
    mocks_mask = set().union(BaseApiTest.mocks_mask)
    mocks = set().union(BaseApiTest.mocks)

    def get_app(self):
        SCHEDULER_API_APPLICATION.settings['serve_traceback'] = True
        return SCHEDULER_API_APPLICATION

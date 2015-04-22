# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import tornado.testing

from test_muniments import test_helpers
from test_muniments.test_common import BaseTest


class BaseApiTest(BaseTest, tornado.testing.AsyncHTTPTestCase):
    mocks_mask = set().union(BaseTest.mocks_mask)
    mocks = set().union(BaseTest.mocks)

    mocks.add('uuid')

    @test_helpers.mock('uuid')
    def mock_uuid(self):
        self._patch('uuid.uuid4')

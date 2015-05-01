# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import tornado.testing
import unittest.mock

from test_muniments import test_helpers
from test_muniments.test_common import BaseTest


class BaseModelsTest(BaseTest, tornado.testing.AsyncTestCase):
    mocks_mask = set().union(BaseTest.mocks_mask)
    mocks = set().union(BaseTest.mocks)

    mocks.add('tornado.httpclient')

    @test_helpers.mock('tornado.httpclient')
    def mock_tornado_httpclient(self):
        self._patch('tornado.httpclient')

        self.mocked_tornado_httpclient_asynchttpclient = unittest.mock.MagicMock()
        self.mocked_tornado_httpclient.AsyncHTTPClient.return_value = self.mocked_tornado_httpclient_asynchttpclient

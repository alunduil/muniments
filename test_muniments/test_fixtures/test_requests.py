# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import unittest.mock

from test_muniments.test_fixtures import Fixture

logger = logging.getLogger(__name__)


class RequestFixture(Fixture):
    @property
    def description(self):
        return '{0.uuid.hex}—{1}—{0.request[method]:6} {0.request[url]} → {0.response[status]}'.format(self, self.context.real_module)

    def run(self):
        kwargs = copy.deepcopy(self.request)
        url = kwargs.pop('url')
        self.result = self.context.fetch(url, **kwargs)

    def check(self):
        self.context.assertEqual(self.response['status'], self.result.code)

        if 'reason' in self.response:
            self.context.assertEqual(self.response['reason'], self.result.reason)

        expected_headers = self.response.get('headers', {})

        expected_headers.setdefault('Server', unittest.mock.ANY)
        expected_headers.setdefault('Content-Type', 'text/html; charset=UTF-8')
        expected_headers.setdefault('Content-Length', unittest.mock.ANY)
        expected_headers.setdefault('Date', unittest.mock.ANY)

        self.context.assertEqual(expected_headers, self.result.headers)

        self.context.maxDiff, _ = None, self.context.maxDiff
        self.context.assertEqual(self.result.body.decode('utf-8'), self.response.get('body', ''))
        self.context.maxDiff = _

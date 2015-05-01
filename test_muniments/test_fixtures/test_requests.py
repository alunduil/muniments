# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import unittest.mock

from test_muniments import test_helpers
from test_muniments.test_fixtures import Fixture

logger = logging.getLogger(__name__)


class RequestFixture(Fixture):
    @property
    def description(self):
        return '{0.uuid.hex}—{1}—{0.request[method]:6} {0.request[url]} → {0.response[status]}'.format(self, self.context.real_module)

    def setup(self):
        if self.context.mock_models():
            if self.response['status'] in range(200, 300):
                if hasattr(self, 'list_fixture'):
                    getattr(self.context, 'mocked_models_' + self.list_fixture.category).list.return_value = test_helpers.wrap_in_future(self.list_fixture.uuid_list)
                    getattr(self.context, 'mocked_models_' + self.list_fixture.category).read.side_effect = [ test_helpers.wrap_in_future(_.python) for _ in self.list_fixture.model_fixtures ]

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

        if 'Etag' in self.result.headers:
            expected_headers.setdefault('Etag', unittest.mock.ANY)

        self.context.assertEqual(expected_headers, self.result.headers)

        self.context.maxDiff, _ = None, self.context.maxDiff
        self.context.assertEqual(self.result.body.decode('utf-8'), self.response.get('body', ''))
        self.context.maxDiff = _

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import logging
import os
import re
import tornado.httpclient
import unittest.mock

from test_muniments import test_helpers
from test_muniments.test_common import MetaTest
from test_muniments.test_fixtures import Fixture
from test_muniments.test_integration import BaseIntegrationTest

logger = logging.getLogger(__name__)


class CouchDbFixture(Fixture):
    def setup(self):
        request = copy.deepcopy(self.storage['write']['request'])
        request['url'] = request['url'].rsplit('/', 1)[0] + '/'

        self.fetch_request({
            'url': request['url'],
            'method': 'DELETE',
        })

        self.fetch_request(request)

    def check_response(self, response):
        self.context.assertEqual(response['code'], self.result.code)

        if 'reason' in response:
            self.context.assertEqual(response['reason'], self.result.reason)

        expected_headers = response.get('headers', {})

        expected_headers.setdefault('Content-Length', unittest.mock.ANY)
        expected_headers.setdefault('Date', unittest.mock.ANY)
        expected_headers.setdefault('Etag', unittest.mock.ANY)
        expected_headers.setdefault('Server', unittest.mock.ANY)

        self.context.assertEqual(expected_headers, self.result.headers)

        self.context.maxDiff, _ = None, self.context.maxDiff
        self.context.assertEqual(re.sub(r',"_rev":"[^"]+"', '', self.result.body.decode('utf-8')).strip(), response.get('body', b'').decode('utf-8'))
        self.context.maxDiff = _

    def fetch_request(self, request):
        kwargs = copy.deepcopy(request)
        url = 'http://' + self.context.host + ':5984' + kwargs.pop('url')

        logger.debug('url: %s', url)
        logger.debug('kwargs: %s', kwargs)

        request = tornado.httpclient.HTTPRequest(url, **kwargs)

        return tornado.httpclient.HTTPClient().fetch(request, raise_error = False)


class CouchDbReadFixture(CouchDbFixture):
    @property
    def description(self):
        return '{0.uuid.hex}—external.couchdb—{0.storage[read][request][method]:6} {0.url}'.format(self, self.context.real_module)

    def setup(self):
        self.fetch_request(self.storage['write']['request'])

    def run(self):
        self.result = self.fetch_request(self.storage['read']['request'])

    def check(self):
        self.check_response(self.storage['read']['response'])


class CouchDbWriteFixture(CouchDbFixture):
    @property
    def description(self):
        return '{0.uuid.hex}—external.couchdb—{0.storage[write][request][method]:6} {0.url}'.format(self, self.context.real_module)

    def run(self):
        self.result = self.fetch_request(self.storage['write']['request'])

    def check(self):
        self.check_response(self.storage['write']['response'])

test_helpers.import_directory(__name__, os.path.dirname(__file__), sort_key = lambda _: 1 if _.rsplit('.', 1)[-1].startswith('list_') else 0)


class BaseCouchDbIntegrationTest(BaseIntegrationTest, tornado.testing.AsyncTestCase):
    mocks_mask = set(( 'tornado.httpclient', )).union(BaseIntegrationTest.mocks_mask)
    mocks = set().union(BaseIntegrationTest.mocks)

    docker_compose_services = set(( 'couchdb', )).union(BaseIntegrationTest.docker_compose_services)

    def setUp(self):
        super().setUp()

        couchdb_host = 'http://{0.host}:5984'.format(self)

        os.environ['COUCHDB_URL'] = couchdb_host

        def _():
            del os.environ['COUCHDB_URL']

        self.addCleanup(_)

        logger.info('waiting for couchdb resolution')

        while True:
            try:
                request = tornado.httpclient.HTTPRequest(couchdb_host)

                response = tornado.httpclient.HTTPClient().fetch(request, raise_error = False)
                logger.debug('response: %s', response)

                if response.code in range(200, 300):
                    break
            except tornado.httpclient.HTTPError:
                pass


class CouchDbIntegrationTest(BaseCouchDbIntegrationTest, metaclass = MetaTest):
    mocks_mask = set().union(BaseCouchDbIntegrationTest.mocks_mask)
    mocks = set().union(BaseCouchDbIntegrationTest.mocks)

    docker_compose_services = set().union(BaseCouchDbIntegrationTest.docker_compose_services)

    fixture_classes = (
        CouchDbFixture,
    )

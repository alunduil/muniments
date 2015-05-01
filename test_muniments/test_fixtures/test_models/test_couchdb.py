# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import unittest.mock

from test_muniments import test_helpers
from test_muniments.test_fixtures.test_models import ModelFixture
from test_muniments.test_fixtures.test_models import ModelListFixture
from test_muniments.test_fixtures.test_models import ModelReadFixture
from test_muniments.test_fixtures.test_models import ModelWriteFixture

logger = logging.getLogger(__name__)


class CouchDbModelFixture(ModelFixture):
    pass


class CouchDbModelListFixture(CouchDbModelFixture, ModelListFixture):
    def setup(self):
        if self.context.mock_tornado_httpclient():
            response = unittest.mock.MagicMock()

            logger.debug('self.storage[response]: %s', self.storage['response'])

            for key, value in self.storage['response'].items():
                setattr(type(response), key, unittest.mock.PropertyMock(return_value = value))

            self.context.mocked_tornado_httpclient_asynchttpclient.fetch.return_value = test_helpers.wrap_in_future(response)


class CouchDbModelReadFixture(CouchDbModelFixture, ModelReadFixture):
    def setup(self):
        if self.context.mock_tornado_httpclient():
            response = unittest.mock.MagicMock()

            logger.debug('self.storage[read][response]: %s', self.storage['read']['response'])

            for key, value in self.storage['read']['response'].items():
                setattr(type(response), key, unittest.mock.PropertyMock(return_value = value))

            self.context.mocked_tornado_httpclient_asynchttpclient.fetch.return_value = test_helpers.wrap_in_future(response)


class CouchDbModelWriteFixture(CouchDbModelFixture, ModelWriteFixture):
    def setup(self):
        if self.context.mock_tornado_httpclient():
            response = unittest.mock.MagicMock()

            logger.debug('self.storage[write][response]: %s', self.storage['write']['response'])

            for key, value in self.storage['write']['response'].items():
                setattr(type(response), key, unittest.mock.PropertyMock(return_value = value))

            self.context.mocked_tornado_httpclient_asynchttpclient.fetch.return_value = test_helpers.wrap_in_future(response)

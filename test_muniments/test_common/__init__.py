# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import re
import unittest
import unittest.mock

from test_muniments import test_helpers

logger = logging.getLogger(__name__)


@property
def real_module(self):
    return re.sub(r'\.[^.]+', '', self.__module__.replace('test_', ''), 1)


class MetaTest(type):
    real_module = real_module

    def __init__(cls, name, bases, dct):
        super(MetaTest, cls).__init__(name, bases, dct)

        def gen_case(fixture):
            def case(self):
                fixture.context = self
                fixture._execute()

            case.__name__ = fixture.name
            case.__doc__ = fixture.description

            if len(cls.mocks_mask):
                case.__doc__ += '—unmocked ' + ','.join(cls.mocks_mask)

            return case

        for fixture in test_helpers.fixtures_from_classes(cls.fixture_classes, context = cls):
            _ = gen_case(fixture)
            setattr(cls, _.__name__, _)


class BaseTest(unittest.TestCase):
    mocks_mask = set()
    mocks = set()

    real_module = real_module

    def setUp(self):
        super().setUp()

        logger.debug('self.mocks_mask: %s', self.mocks_mask)
        logger.debug('self.mocks: %s', self.mocks)

    def _patch(self, name):
        logger.info('mocking %s', self.__class__.real_module + '.' + name)

        m = unittest.mock.patch(self.__class__.real_module + '.' + name)

        setattr(self, 'mocked_' + name.replace('.', '_').strip('_'), m.start())

        self.addCleanup(m.stop)

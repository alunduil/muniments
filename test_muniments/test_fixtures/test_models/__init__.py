# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging

from test_muniments.test_fixtures import Fixture

logger = logging.getLogger(__name__)


class ModelFixture(Fixture):
    pass


class ModelListFixture(ModelFixture):
    @property
    def description(self):
        return '{0.uuid.hex}—{1}.list() == [ … ]'.format(self, self.context.real_module)

    def initialize(self):
        super().initialize()

        self.uuid_list = [ str(_.uuid) for _ in self.model_fixtures ]

    def check(self):
        self.context.assertEqual(sorted(self.uuid_list), sorted(self.result))


class ModelReadFixture(ModelFixture):
    @property
    def description(self):
        return '{0.uuid.hex}—{1}.read({0.uuid.hex}) == {{ \'_id\': {0.uuid.hex}, … }}'.format(self, self.context.real_module)

    def check(self):
        self.context.maxDiff, _ = None, self.context.maxDiff
        self.context.assertEqual(self.python, self.result)
        self.context.maxDiff = _


class ModelWriteFixture(ModelFixture):
    @property
    def description(self):
        return '{0.uuid.hex}—{1}.write({{ \'_id\': {0.uuid.hex}, … }})'.format(self, self.context.real_module)

    def check(self):
        self.context.assertIn(self.url, self.result)

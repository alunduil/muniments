# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from test_muniments.test_fixtures import register_fixture
from test_muniments.test_integration.test_external.test_couchdb import CouchDbReadFixture
from test_muniments.test_integration.test_external.test_couchdb import CouchDbWriteFixture
from test_muniments.test_unit.test_scheduler.test_models import test_schedule

for module in [ getattr(test_schedule, module_name) for module_name in dir(test_schedule) if module_name.startswith('model_') ]:
    register_fixture(globals(), ( CouchDbReadFixture, ), module.DATA)
    register_fixture(globals(), ( CouchDbWriteFixture, ), module.DATA)

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import os
import select
import subprocess
import urllib

from test_muniments.test_common import BaseTest

logger = logging.getLogger(__name__)


def call(command, *args, **kwargs):
    child = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.PIPE, *args, **kwargs)

    def log():
        for fh in select.select(( child.stdout, child.stderr, ), (), (), 0)[0]:
            line = fh.readline()[:-1]

            if len(line):
                getattr(logger, {
                    child.stdout: 'debug',
                    child.stderr: 'error',
                }[fh])('%s: %s', command, line)

    while child.poll() is None:
        log()

    log()

    return child.wait()

IS_DOCKER_COMPOSE_AVAILABLE = 0 == call('which docker-compose', shell = True)


def docker_compose_stop():
    return call(' '.join(( 'docker-compose', 'stop', )), shell = True)


def setupModule():
    global IS_DOCKER_COMPOSE_AVAILABLE

    IS_DOCKER_COMPOSE_AVAILABLE = 0 == docker_compose_stop()


def tearDownModule():
    if IS_DOCKER_COMPOSE_AVAILABLE:
        docker_compose_stop()


class BaseIntegrationTest(BaseTest):
    mocks_mask = set().union(BaseTest.mocks_mask)
    mocks = set().union(BaseTest.mocks)

    docker_compose_services = set()

    def setUp(self):
        if not IS_DOCKER_COMPOSE_AVAILABLE:
            self.skipTest('docker-compose not found')

        super().setUp()

        self.host = urllib.parse.urlparse(os.environ.get('DOCKER_HOST', 'tcp://localhost')).hostname

        command = ' '.join(( 'docker-compose', 'up', '-d', '--no-deps', )) + ' ' + ' '.join(tuple(self.docker_compose_services))
        logger.debug('command: %s', command)

        result = call(command, shell = True)

        self.assertEqual(0, result)

        self.addCleanup(docker_compose_stop)

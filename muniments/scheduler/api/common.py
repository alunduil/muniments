# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import tornado.web

from muniments import errors

logger = logging.getLogger(__name__)


class BaseSchedulerHandler(tornado.web.RequestHandler):
    def prepare(self):
        logger.info('STARTING: %s %s', self.request.method, self.request.uri)

    def on_finish(self):
        logger.info('STOPPING: %s %s', self.request.method, self.request.uri)

    def write_error(self, status_code, **kwargs):
        logger.debug('status_code: %s', status_code)

        if 'Origin' in self.request.headers:
            self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])

        if status_code == 405:
            self.set_header('Allow', ', '.join(self.SUPPORTED_METHODS))
            return

        if 'exc_info' in kwargs:
            error_type, error_value, error_traceback = kwargs['exc_info']

            if error_type is errors.InvalidError:
                self.set_status(status_code = error_value.status_code, reason = error_value.reason)
            else:
                logger.exception('unhandled exception in %s', self, exc_info = kwargs['exc_info'])

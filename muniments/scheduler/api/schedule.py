# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import tornado.gen

from muniments.scheduler.api import common

logger = logging.getLogger(__name__)


class ScheduleCollectionHandler(common.BaseSchedulerHandler):
    '''Schedule Collection Resource

    :``URL``: ``/schedules/``

    '''

    SUPPORTED_METHODS = (
        'GET',
        'HEAD',
        'OPTIONS',
        'POST',
    )

    def options(self):
        '''Resource Options

        Parameters
        ----------

        Headers
        ^^^^^^^

        :``Origin``: serving domain of requesting page; **optional**

        Return Value(s)
        ---------------

        :``204 No Content``: :**headers**: if ``Origin`` in request:
                                           * ``Access-Control-Allow-Methods``
                                           * ``Access-Control-Allow-Origin``
                                           * ``Access-Control-Expose-Headers``
                                           * ``Access-Control-Max-Age``

        Examples
        --------

        1. :request:::
               OPTIONS /schedules/ HTTP/1.1

           :response:::
               HTTP/1.1 204 No Content

           :curl:::
               curl -v -X OPTIONS http://127.0.0.1:5000/v1/schedules/

        2. :request:::
               OPTIONS /schedules/ HTTP/1.1
               Access-Control-Request-Method: POST
               Origin: http://127.0.0.1:5000

           :response:::
               HTTP/1.1 204 No Content
               Access-Control-Allow-Methods: GET, HEAD, POST
               Access-Control-Allow-Origin: http://127.0.0.1:5000
               Access-Control-Expose-Headers: Location
               Access-Control-Max-Age: 2419200

           :curl:::
               curl -v -X OPTIONS -H 'Access-Control-Request-Method: POST' -H 'Origin: http://127.0.0.1:5000' http://127.0.0.1:5000/v1/schedules/

        '''

        self.set_status(204)

        if 'Origin' in self.request.headers:
            return

        self.set_header('Access-Control-Allow-Methods', 'GET, HEAD, POST')
        self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])
        self.set_header('Access-Control-Max-Age', '2419200')

        self.set_header('Access-Control-Expose-Headers', ', '.join((
            'Location',
        )))

    @tornado.gen.coroutine
    def get(self):
        '''Get Schedule Resource

        Parameters
        ----------

        Headers
        ^^^^^^^

        :``Origin``: serving domain of requesting page; **optional**

        Return Value(s)
        ---------------

        :``200 OK``:        :**headers**: * ``Content-Type``
                                          if ``Origin`` in request:
                                          * ``Access-Control-Allow-Origin``
                            :**body**:    JSON representation of a list of
                                          schedules

        :``404 Not Found``: schedule does not exist

        Examples
        --------

        1. :request:::
               GET /schedules/ HTTP/1.1

           :response:::
               HTTP/1.1 200 OK
               Content-Type: application/json

               [ { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }, … ]

           :curl:::
               curl -v -X GET http://127.0.0.1:5000/v1/schedules/

        2. :request:::
               GET /schedules/ HTTP/1.1
               Origin: http://127.0.0.1:5000

           :response:::
               HTTP/1.1 200 OK
               Access-Control-Allow-Origin: http://127.0.0.1:5000
               Content-Type: application/json

               [ { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }, … ]

           :curl:::
               curl -v -X GET -H 'Origin: http://127.0.0.1:5000' http://127.0.0.1:5000/v1/schedules/

        '''

        if 'Origin' in self.request.headers:
            self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])

        # TODO list schedules
        # TODO add URL to schedules

        self.set_header('Content-Type', 'application/json')

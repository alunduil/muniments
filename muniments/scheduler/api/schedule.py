# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import json
import logging
import tornado.gen
import uuid

from muniments.common import json_encode
from muniments.scheduler import models
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

    @tornado.gen.coroutine
    def get(self):
        '''Get Schedule Collection Resource

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

        schedule_uuids = yield models.schedule.list()

        schedules = yield [ models.schedule.read(schedule_uuid) for schedule_uuid in schedule_uuids ]

        for schedule in schedules:
            schedule.setdefault('url', self.reverse_url('schedule', str(schedule['_id'])))

        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(schedules, default = json_encode, sort_keys = True))

    head = get

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
    def post(self):
        '''Create Schedule Resource

        Parameters
        ----------

        Headers
        ^^^^^^^

        :``Origin``: serving domain of requesting page; **optional**

        Return Value(s)
        ---------------

        :``201 Created``: :**headers**: * ``Location``
                                        * ``Content-Type``
                                        if ``Origin`` in request:
                                        * ``Access-Control-Allow-Origin``
                                        * ``Access-Control-Expose-Headers``
                          :**body**:    JSON representation of the created
                                        schedule
        Examples
        --------

        1. :request:::
               POST /schedules/ HTTP/1.1

           :response:::
               HTTP/1.1 200 OK
               Content-Type: application/json
               Location: /v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

               { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }

           :curl:::
               curl -v -X POST http://127.0.0.1:5000/v1/schedules/

        2. :request:::
               POST /schedules/ HTTP/1.1
               Origin: http://127.0.0.1:5000

           :response:::
               HTTP/1.1 200 OK
               Access-Control-Allow-Origin: http://127.0.0.1:5000
               Access-Control-Expose-Headers: Location
               Content-Type: application/json
               Location: /v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

               { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }

           :curl:::
               curl -v -X POST -H 'Origin: http://127.0.0.1:5000' http://127.0.0.1:5000/v1/schedules/

        '''

        if 'Origin' in self.request.headers:
            self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])
            self.set_header('Access-Control-Expose-Headers', 'Location')

        schedule = {
            'uuid': uuid.uuid4(),
        }

        self.set_header('Location', self.reverse_url('schedule', str(schedule['uuid'])))

        # TODO write schedule to store

        self.set_header('Content-Type', 'application/json')

        # TODO write json

        self.set_status(201)


class ScheduleHandler(common.BaseSchedulerHandler):
    '''Schedule Resource

    :``URL``: ``/schedules/{SCHEDULE_UUID}``

    '''

    SUPPORTED_METHODS = (
        'DELETE',
        'GET',
        'HEAD',
        'OPTIONS',
        'PATCH',
        'PUT',
    )

    def delete(self, schedule_uuid):
        '''Delete Schedule Resource

        Return Value(s)
        ---------------

        :``200 OK``: schedule does not exist

        Examples
        --------

        1. :request:::
               DELETE /schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847 HTTP/1.1

           :response:::
               HTTP/1.1 200 OK

           :curl:::
               curl -v -X DELETE http://127.0.0.1:5000/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

        '''

        self.set_status(500)

    @tornado.gen.coroutine
    def get(self, schedule_uuid):
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
                            :**body**:    JSON representation of the schedule
        :``404 Not Found``: schedule does not exist

        Examples
        --------

        1. :request:::
               GET /schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847 HTTP/1.1

           :response:::
               HTTP/1.1 200 OK
               Content-Type: application/json

               { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }

           :curl:::
               curl -v -X GET http://127.0.0.1:5000/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

        2. :request:::
               GET /schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847 HTTP/1.1
               Origin: http://127.0.0.1:5000

           :response:::
               HTTP/1.1 200 OK
               Access-Control-Allow-Origin: http://127.0.0.1:5000
               Content-Type: application/json

               { "url": "/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847", "uuid": "7d2bbfae-5a0a-4328-8079-2660f0d19847", … }

           :curl:::
               curl -v -X POST -H 'Origin: http://127.0.0.1:5000' http://127.0.0.1:5000/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

        '''

        if 'Origin' in self.request.headers:
            self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])

        # TODO read schedule

        self.set_header('Content-Type', 'application/json')

        if self.request.method.lower() == 'head':
            return

        # TODO write json

    head = get

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
               OPTIONS /schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847 HTTP/1.1

           :response:::
               HTTP/1.1 204 No Content

           :curl:::
               curl -v -X OPTIONS http://127.0.0.1:5000/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

        2. :request:::
               OPTIONS /schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847 HTTP/1.1
               Access-Control-Request-Method: GET
               Origin: http://127.0.0.1:5000

           :response:::
               HTTP/1.1 204 No Content
               Access-Control-Allow-Methods: DELETE, GET, HEAD, PATCH, PUT
               Access-Control-Allow-Origin: http://127.0.0.1:5000
               Access-Control-Max-Age: 2419200

           :curl:::
               curl -v -X OPTIONS -H 'Access-Control-Request-Method: GET' -H 'Origin: http://127.0.0.1:5000' http://127.0.0.1:5000/v1/schedules/7d2bbfae-5a0a-4328-8079-2660f0d19847

        '''

        self.set_status(204)

        if 'Origin' in self.request.headers:
            return

        self.set_header('Access-Control-Allow-Methods', 'DELETE, GET, HEAD, PUT, PATCH')
        self.set_header('Access-Control-Allow-Origin', self.request.headers['Origin'])
        self.set_header('Access-Control-Max-Age', '2419200')

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import json
import logging
import tornado.gen
import uuid

from muniments.common import json_encode
from muniments.parameters import couchdb  # flake8: noqa—populate parameters
from muniments.parameters import PARAMETERS

logger = logging.getLogger(__name__)


@tornado.gen.coroutine
def list():
    '''List Schedule UUIDs

    Return Value(s)
    ---------------

    List of Schedule UUIDs.

    '''

    request = tornado.httpclient.HTTPRequest(
        PARAMETERS['couchdb.url'] + '/schedules/_all_docs',
    )

    response = yield tornado.httpclient.AsyncHTTPClient().fetch(request, raise_error = False)
    logger.debug('response: %s', response)

    return [ _['id'] for _ in json.loads(response.body.decode('utf-8'))['rows'] ]


@tornado.gen.coroutine
def read(schedule_uuid):
    '''Read Schedule

    Arguments
    ---------

    :``schedule_uuid``: Schedule UUID

    Return Value(s)
    ---------------

    Schedule python structure—dict with the following keys:
    :``created_at``:  the datetime the Schedule was first written
    :``date``:        todoist style date string describing this Schedule
    :``recurrences``: list of 3-tuples that specify start, end, and stride for
                      the recurrences that compose this schedule
    :``updated_at``:  the datetime the Schedule was last written
    :``id``:          the UUID of the Schedule

    '''

    request = tornado.httpclient.HTTPRequest(
        PARAMETERS['couchdb.url'] + '/schedules/' + str(schedule_uuid)
    )

    response = yield tornado.httpclient.AsyncHTTPClient().fetch(request, raise_error = False)
    logger.debug('response: %s', response)

    raw = json.loads(response.body.decode('utf-8'))
    raw.update({
        'created_at': datetime.datetime.strptime(raw['created_at'], '%Y-%m-%dT%H:%M:%S.%f'),
        'updated_at': datetime.datetime.strptime(raw['updated_at'], '%Y-%m-%dT%H:%M:%S.%f'),
        '_id': uuid.UUID(raw['_id']),
    })

    for recurrence in raw['recurrences']:
        if recurrence[0] is not None:
            recurrence[0] = datetime.datetime.strptime(recurrence[0], '%Y-%m-%dT%H:%M:%S.%f')

        if recurrence[1] is not None:
            recurrence[1] = datetime.datetime.strptime(recurrence[1], '%Y-%m-%dT%H:%M:%S.%f')

        if recurrence[2] is not None:
            recurrence[2] = datetime.timedelta(seconds = recurrence[2])

    logger.debug('raw: %s', raw)

    return raw


@tornado.gen.coroutine
def write(schedule):
    '''Write Schedule

    Arguments
    ---------

    :``schedule``: Schedule python structure—dict with the following keys:
                   :``created_at``:  the datetime the Schedule was first written
                   :``date``:        todoist style date string describing this
                                     Schedule
                   :``recurrences``: list of 3-tuples that specify start, end,
                                     and stride for the recurrences that compose
                                     this schedule; **populated from date**
                   :``updated_at``:  the datetime the Schedule was last written
                   :``id``:          the UUID of the Schedule
                 
    Exceptions
    ----------

    :``InvalidError``: Raised if any attributes have invalid values.  The fix
                       is included as the error's reason.

    '''

    validate(schedule)

    schedule['recurrences'] = parse(schedule['date'])

    url = PARAMETERS['couchdb.url'] + '/schedules/' + str(schedule['_id'])

    request = tornado.httpclient.HTTPRequest(
        url,
        method = 'PUT',
        body = json.dumps(schedule, default = json_encode, sort_keys = True)
    )

    response = yield tornado.httpclient.AsyncHTTPClient().fetch(request, raise_error = False)
    logger.debug('response: %s', response)

    return url


def validate(schedule):
    '''Validate Schedule

    .. seealso::
        models.schedule.write
        
    '''

    pass


def parse(date):
    '''Parse date into list of 3-tuples that specify start, end, and stride.

    Parameters
    ----------

    :``date``: todoist style date string (i.e. every day at 14:30 starting 1
               Jan)

    Return Value(s)
    ---------------

    List of 3-tuples where the three elements are start datetime, end datetime,
    and time between occurences.

    '''

    pass

# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import tornado.web

from muniments.scheduler.api import information
from muniments.scheduler.api import schedule

logger = logging.getLogger(__name__)


PREFIX = '/{i.API_VERSION}'.format(i = information)

UUID_REGEX = r'([\da-f]{8}-[\da-f]{4}-[\da-f]{4}-[\da-f]{4}-[\da-f]{12})'

SCHEDULER_API_APPLICATION = tornado.web.Application(
    [
        ( '/'.join(( PREFIX, 'schedules', UUID_REGEX, )), schedule.ScheduleHandler, None, 'schedule', ),
        ( '/'.join(( PREFIX, 'schedules', '', )), schedule.ScheduleCollectionHandler, None, 'schedule_collection', ),
    ]
)

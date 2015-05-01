# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import datetime
import logging
import uuid

logger = logging.getLogger(__name__)


def json_encode(obj):
    '''Transform commonly used objects to JSON-able formats.

    Parameters
    ----------

    :``obj``: object to make JSON encodable

    Return Value(s)
    ---------------

    JSON encodable version of object.

    '''

    if isinstance(obj, datetime.datetime):
        return obj.strftime('%Y-%m-%dT%H:%M:%S.%f')

    if isinstance(obj, datetime.timedelta):
        return obj.total_seconds()

    if isinstance(obj, uuid.UUID):
        return str(obj)

    raise TypeError

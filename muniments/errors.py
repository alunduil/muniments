# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import tornado.web


class InvalidError(tornado.web.HTTPError):
    '''Raised when invalid model properties are encountered.'''

    def __init__(self, code, message):
        '''Construct InvalidError

        Arguments
        ---------

        :``code``:    HTTP error code
        :``message``: HTTP error message

        '''

        super().__init__(code, message)
        self.reason = message

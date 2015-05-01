# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

from muniments.parameters import PARAMETERS

PARAMETERS.add_parameter(
    group = 'couchdb',
    options = [ '--url', ],
    default = 'http://localhost:5984',
    help = 'CouchDB URL; default %(default)s'
)

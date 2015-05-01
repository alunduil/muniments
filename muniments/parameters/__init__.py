# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import crumbs
import logging
import logging.config
import os
import warnings

logger = logging.getLogger(__name__)

CONFIGURATION_DIRECTORY = os.path.join(os.path.sep, 'etc', 'muniments')

PARAMETERS = crumbs.Parameters(conflict_handler = 'resolve')

PARAMETERS.add_parameter(
    options = [ '--configuration-file-path', '-c', ],
    metavar = 'FILE',
    environment_prefix = None,
    default = os.path.join(CONFIGURATION_DIRECTORY, 'muniments.ini'),
    help = 'file path to search for muniments parameters; default: %(default)s'
)

PARAMETERS.add_parameter(
    group = 'logging',
    options = [ '--configuration-file-path', ],
    metavar = 'FILE',
    environment_prefix = None,
    default = os.path.join(CONFIGURATION_DIRECTORY, 'logging.ini'),
    help = 'file path to search for logging configuration; default %(default)s'
)

with warnings.catch_warnings():
    warnings.simplefilter('ignore')

    PARAMETERS.parse(only_known = True)

    if os.access(PARAMETERS['configuration-file-path'], os.R_OK):
        PARAMETERS.add_configuration_file(PARAMETERS['configuration-file-path'])

    if os.access(PARAMETERS['logging.configuration-file-path'], os.R_OK):
        logging.config.fileConfig(PARAMETERS['logging.configuration-file-path'])

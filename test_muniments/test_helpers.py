# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import concurrent
import functools
import importlib
import itertools
import logging
import os
import sys

logger = logging.getLogger(__name__)


def fixtures_from_classes(fixture_classes, context = None):
    '''Retrieve fixtures for the given classes.

    Parameters
    ----------

    :``fixture_classes``: classes whose children are instantiated as fixtures
    :``context``:         testing context

    Return Value(s)
    ---------------

    Instantiated fixture objects.

    '''

    classes = list(copy.copy(fixture_classes))

    fixtures = []

    while len(classes):
        current = classes.pop()

        if len(current.__subclasses__()):
            classes.extend(current.__subclasses__())
        else:
            fixtures.append(current(context))

    return fixtures


def import_directory(module_basename, directory, update_path = False, sort_key = None):
    '''Recursively import all modules in a directory.

    Parameters
    ----------

    :``module_basename``: module name prefix for loaded modules
    :``directory``:       directory to recursively import modules from
    :``update_path``:     if true, system path for modules is updated to include
                          directory; otherwise, system path is unmodified
    :``sort_key``:        function to order imports of modules in this directory

    '''

    if update_path:
        update_path = bool(sys.path.count(directory))
        sys.path.append(directory)

    logger.info('loading submodules of %s', module_basename)
    logger.info('loading modules from %s', directory)

    file_names = itertools.chain(*[ [ os.path.join(directory_path, file_name) for file_name in file_names ] for directory_path, directory_names, file_names in os.walk(directory) if len(file_names) ])

    module_names = []

    for file_name in file_names:
        if file_name.endswith('.py'):
            name = file_name

            name = name.replace(directory, '')
            name = name.replace('__init__', '')
            name = name.replace('.py', '')
            name = name.replace('/', '.')

            name = name.strip('.')

            if not len(name):
                continue

            name = module_basename + '.' + name

            known_parts = set()
            name = '.'.join([ part for part in name.split(',') if part not in known_parts and not known_parts.add(part) ])

            if len(name):
                module_names.append(name)

    for module_name in sorted(module_names, key = sort_key):
        try:
            importlib.import_module(module_name)
        except ImportError:
            logger.exception('NOT loaded %s', module_name)
        else:
            logger.info('loaded %s', module_name)

    if update_path:
        sys.path.remove(directory)


def mock(name):
    def _(function):
        @functools.wraps(function)
        def wrapper(self, *args, **kwargs):
            logger.info('STARTING: mock ' + name)

            result = False

            if name in self.mocks_mask:
                logger.info('STOPPING: mock ' + name + '—MASKED')
            elif getattr(self, 'is_mocked_' + name.replace('.', '_').strip('_'), False):
                result = True

                logger.info('STOPPING: mock ' + name + '—EXISTS')
            else:
                function(self, *args, **kwargs)

                result = True

                logger.info('STOPPING: mock ' + name)

            setattr(self, 'is_mocked_' + name.replace('.', '_').strip('_'), result)

            return result

        return wrapper

    return _


def wrap_in_future(thing):
    '''Wrap thing in a future.

    Arguments
    ---------

    :``thing``: thing to be wrapped in future

    Return Value(s)
    ---------------

    future whose result is thing.

    '''

    future = concurrent.futures.Future()
    future.set_result(thing)

    return future

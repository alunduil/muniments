# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# crumbs is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import copy
import inspect
import logging
import os
import uuid

logger = logging.getLogger(__name__)


class Fixture(object):
    def __init__(self, context):
        self.context = context

    @property
    def name(self):
        return 'test_' + self.__class__.__name__

    @property
    def category(self):
        return self.__module__.__name__.rsplit('.', 2)[-2].replce('test_', '')

    def initialize(self):
        pass

    def setup(self):
        pass

    def check(self):
        pass

    def _execute(self):
        executed = {
            'setup': { id(Fixture.setup), },
            'check': { id(Fixture.check), },
        }

        classes = list(reversed(self.__class__.mro()))[2:]

        for cls in classes:
            setup = getattr(cls, 'setup')

            if id(setup) not in executed['setup']:
                setup(self)
                executed['setup'].add(id(setup))

        self.run()

        for cls in classes:
            check = getattr(cls, 'check')

            if id(check) not in executed['check']:
                check(self)
                executed['check'].add(id(check))


def register_fixture(namespace, base_classes, **kwargs):
    args = copy.deepcopy(kwargs)

    desc = args.pop('description', None)

    @property
    def description(self):
        _ = super(self.__class__, self).description

        if desc is not None:
            _ += '—' + desc

        return _

    def __init__(self, context):
        super(self.__class__, self).__init__(context)

        functions = {}

        for name, value in args.items():
            if name == 'error':
                self.error = value['class'](*value.get('args', ()), **value.get('kwargs', {}))
                continue

            if inspect.isfunction(value):
                functions[name] = value
                continue

            if inspect.isclass(value):
                if issubclass(value, Fixture):
                    value = value(self.context)
                else:
                    value = value()

            setattr(self, name, value)

        function_count = float('inf')
        while function_count > len(functions):
            function_count = len(functions)

            for name, function in copy.copy(functions).items():
                try:
                    value = copy.deepcopy(function(self))

                    setattr(self, name, value)
                except AttributeError:
                    logger.exception('function: %s', name)
                    continue
                else:
                    del functions[name]

        if len(functions):
            logger.warning('unprocessed fixture properties: %s', ','.join(functions.keys()))

        self.initialize()

    caller_frame = inspect.stack()[1]

    caller_file = caller_frame[1]
    caller_module = inspect.getmodule(caller_frame[0])

    my_uuid = uuid.UUID(os.path.basename(caller_file).replace('.py', '').rsplit('_', 1)[-1])

    class_name = 'f_' + my_uuid.hex

    original_length = len(class_name)
    count = 0

    while class_name in namespace:
        count += 1
        class_name = class_name[:original_length] + '_' + str(count)

    logger.debug('class_name: %s', class_name)

    namespace[class_name] = type(class_name, base_classes, {
        '__init__': __init__,
        '__module__': caller_module,
        'description': description,
        'uuid': my_uuid,
    })

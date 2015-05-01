# Copyright (C) 2015 by Alex Brandt <alunduil@alunduil.com>
#
# muniments is freely distributable under the terms of an MIT-style license.
# See COPYING or http://www.opensource.org/licenses/mit-license.php.

import os

from setuptools import find_packages
from setuptools import setup
from codecs import open

with open(os.path.join(os.path.dirname(__file__), 'muniments', 'information.py'), 'r', encoding = 'utf-8') as fh:
    exec(fh.read(), globals(), locals())

PARAMS = {}

PARAMS['name'] = NAME  # flake8: noqa—provided by exec
PARAMS['version'] = VERSION  # flake8: noqa—provided by exec
PARAMS['description'] = DESCRIPTION  # flake8: noqa—provided by exec

with open(os.path.join(os.path.dirname(__file__), 'README.rst'), 'r', encoding = 'utf-8') as fh:
    PARAMS['long_description'] = fh.read()

PARAMS['url'] = URL  # flake8: noqa—provided by exec
PARAMS['author'] = AUTHOR  # flake8: noqa—provided by exec
PARAMS['author_email'] = AUTHOR_EMAIL  # flake8: noqa—provided by exec
PARAMS['license'] = LICENSE  # flake8: noqa—provided by exec

PARAMS['classifiers'] = (
    'Development Status :: 1 - Planning',
    # 'Development Status :: 2 - Pre-Alpha',
    # 'Development Status :: 3 - Alpha',
    # 'Development Status :: 4 - Beta',
    # 'Development Status :: 5 - Production/Stable',
    # 'Development Status :: 6 - Mature',
    'Environment :: Console',
    'Environment :: No Input/Output (Daemon)',
    'Environment :: Web Environment',
    'Intended Audience :: End Users/Desktop',
    'Intended Audience :: Information Technology',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Internet',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    'Topic :: System',
    'Topic :: System :: Archiving',
    'Topic :: System :: Archiving :: Backup',
    'Topic :: System :: Distributed Computing',
)

PARAMS['keywords'] = (
    'backup',
    'cloud',
    'distributed',
    'scheduled',
)

PARAMS['packages'] = find_packages(exclude = ( 'test_*', ))

PARAMS['install_requires'] = (
    'crumbs',
    'tornado',
)

# ..note::
#     Documentation Requires:
#     * sphinx_rtd_theme

PARAMS['extras_require'] = {}

PARAMS['test_suite'] = 'nose.collector'
PARAMS['tests_require'] = (
    'coverage',
    'nose',
)

PARAMS['entry_points'] = {
    'console_scripts': (
        'muniments = muniments:main',
        'muniments-scheduler = muniments.scheduler.api:main',
    ),
}

PARAMS['data_files'] = (
    ( 'share/doc/{P[name]}-{P[version]}'.format(P = PARAMS), (
        'README.rst',
    )),
    ( 'share/doc/{P[name]}-{P[version]}/conf'.format(P = PARAMS), (
        'conf/logging.ini',
        'conf/muniments.ini',
    )),
)

setup(**PARAMS)

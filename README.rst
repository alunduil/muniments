Description
===========

Composable backup micro-services.

A collection of services and utilities that allows one to create a backup system
that is cloud aware and ad-hoc.

Installation
============

This package is stored in PyPI and can be installed the standard way::

    pip install muniments

The latest release available is:

.. image:: https://badge.fury.io/py/muniments.png
    :target: http://badge.fury.io/py/muniments

Using Muniments
===============

Usage of this package is as simple as starting the services::

    systemctl start muniments.service

Developing Muniments
====================

If you would prefer to clone this package directly from git or assist with
development, the URL is https://github.com/alunduil/muniments.

Muniments is tested continuously by Travis-CI and running the tests is quite
simple::
  
    flake8
    nosetests

The current status of the build is:

.. image:: https://secure.travis-ci.org/alunduil/muniments.png?branch=master
    :target: http://travis-ci.org/alunduil/muniments

Authors
=======

* Alex Brandt <alunduil@alunduil.com>

Known Issues
============

Known issues can be found in the github issue list at
https://github.com/alunduil/muniments/issues.

Troubleshooting
===============

If you need to troubleshoot an issue or submit information in a bug report, we
recommend obtaining the logs while running the service in question with
debugging enabled.

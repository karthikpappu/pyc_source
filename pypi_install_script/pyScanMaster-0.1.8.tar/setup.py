#!/usr/bin/env python
# -*- coding: utf-8 -*-
################################################################################
#
#  pyScanMaster -- Python Interface to ScanMaster POS
#  Copyright © 2013-2014 Sacramento Natural Foods Co-op, Inc
#
#  This file is part of pyScanMaster.
#
#  pyScanMaster is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  pyScanMaster is distributed in the hope that it will be useful, but WITHOUT
#  ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
#  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  pyScanMaster.  If not, see <http://www.gnu.org/licenses/>.
#
################################################################################


import os.path
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))
execfile(os.path.join(here, u'scanmaster', u'_version.py'))
README = open(os.path.join(here, u'README.rst')).read()


requires = [
    #
    # Version numbers within comments below have specific meanings.
    # Basically the 'low' value is a "soft low," and 'high' a "soft high."
    # In other words:
    #
    # If either a 'low' or 'high' value exists, the primary point to be
    # made about the value is that it represents the most current (stable)
    # version available for the package (assuming typical public access
    # methods) whenever this project was started and/or documented.
    # Therefore:
    #
    # If a 'low' version is present, you should know that attempts to use
    # versions of the package significantly older than the 'low' version
    # may not yield happy results.  (A "hard" high limit may or may not be
    # indicated by a true version requirement.)
    #
    # Similarly, if a 'high' version is present, and especially if this
    # project has laid dormant for a while, you may need to refactor a bit
    # when attempting to support a more recent version of the package.  (A
    # "hard" low limit should be indicated by a true version requirement
    # when a 'high' version is present.)
    #
    # In any case, developers and other users are encouraged to play
    # outside the lines with regard to these soft limits.  If bugs are
    # encountered then they should be filed as such.
    #
    # package                           # low                   high

    u'sqlalchemy-pervasive',            # 0.1.0

    # Something about the 3.0.X versions of pyodbc is causing a segmentation
    # fault on Linux when CURRENCY fields are accessed.  For now this seems to
    # be a reasonable workaround:
    u'pyodbc<3.0',                      # 2.1.11
    ]


setup(
    name = u"pyScanMaster",
    version = __version__,
    author = u"Sacramento Natural Foods Co-op, Inc",
    author_email = u"developer@sacfoodcoop.com",
    url = u"https://github.com/SacNaturalFoods/pyscanmaster",
    license = u"GNU GPL v3",
    description = u"Python Interface to ScanMaster POS",
    long_description = README,

    classifiers = [
        u'Development Status :: 3 - Alpha',
        u'Intended Audience :: Developers',
        u'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        u'Natural Language :: English',
        u'Operating System :: OS Independent',
        u'Programming Language :: Python',
        u'Programming Language :: Python :: 2.6',
        u'Programming Language :: Python :: 2.7',
        u'Topic :: Office/Business',
        u'Topic :: Software Development :: Libraries :: Python Modules',
        ],

    install_requires = requires,
    packages = find_packages(exclude=[u'tests.*', u'tests']),
    tests_require = [u'nose', u'fixture'],

    entry_points = {
        u'console_scripts': [
            u'decipher-tlog = scanmaster.tlogs:decipher_tlog',
            ],
        },
    )

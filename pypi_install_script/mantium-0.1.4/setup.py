#!/usr/bin/python
# -*- coding: utf-8 -*-

# Hive Mantium System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of Hive Mantium System.
#
# Hive Mantium System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Hive Mantium System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Hive Mantium System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import setuptools

setuptools.setup(
    name = "mantium",
    version = "0.1.4",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "Mantium Web Interface",
    license = "GNU General Public License (GPL), Version 3",
    keywords = "mantium build automation",
    url = "http://mantium.hive.pt",
    zip_safe = False,
    packages = [
        "mantium",
        "mantium.models",
        "mantium.views",
        "mantium.views.web"
    ],
    package_dir = {
        "" : os.path.normpath("src")
    },
    install_requires = [
        "automium",
        "flask",
        "quorum"
    ],
    package_data = {
        "mantium" : [
            "projects/readme.md",
            "static/css/*",
            "static/images/*",
            "static/js/*",
            "templates/*.tpl",
            "templates/partials/*.tpl"
        ]
    },
    entry_points = {
        "console_scripts" : [
            "mantium = mantium.run:main"
        ]
    },
    classifiers = [
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ]
)

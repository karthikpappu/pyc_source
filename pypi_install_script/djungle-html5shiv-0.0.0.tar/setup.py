#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# djungle-html5shiv – html5shiv as Django app.
# Copyright © 2012  Hendrik M Halkow
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <http://www.gnu.org/licenses/>.
"""
Installation script for djungle-html5shiv.
"""

import os
from setuptools import setup, find_packages


def main():
    """
    The main entry point of the setup script.
    """
    readme_file = open(os.path.join(os.path.dirname(__file__), 'README.md'))
    readme = readme_file.read()
    readme_file.close()

    setup(
        name='djungle-html5shiv',
        version='0.0.0',
        description='html5shiv as Django app.',
        long_description=readme,
        author='Hendrik M Halkow',
        author_email='hendrik@halkow.com',
        url='https://github.com/djungle/djungle-html5shiv',
        classifiers=[
            'Development Status :: 1 - Planning',
            'Environment :: Web Environment',
            'Framework :: Django',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: GNU General Public License (GPL)',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Internet :: WWW/HTTP',
            'Topic :: Software Development :: User Interfaces',
            'Topic :: Text Processing :: Markup :: HTML'
        ],
        install_requires=[
            'Django>=1.4',
        ],
        packages=find_packages(),
        package_data={
            'djungle.html5shiv': [
                'static/djungle/*',
            ],
        },
        namespace_packages=['djungle'],
        zip_safe=False,
    )


if __name__ == '__main__':
    main()

#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <laurent.el-shafey@idiap.ch>
#
# Copyright (C) 2011-2013 Idiap Research Institute, Martigny, Switzerland
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

# The only thing we do in this file is to call the setup() function with all
# parameters that define our package.
setup(

    name='xbob.db.mobio',
    version='1.2.1',
    description='MOBIO Database Access API for Bob',
    url='https://pypi.python.org/pypi/xbob.db.mobio',
    license='GPLv3',
    author='Laurent El Shafey',
    author_email='laurent.el-shafey@idiap.ch',
    keywords='face recognition, speaker recognition, bob, xbob, xbob.db, mobio',
    long_description=open('README.rst').read(),

    # This line is required for any distutils based packaging.
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
      'setuptools',
      'six',  # py2/3 compatibility library
      'bob',  # base signal proc./machine learning library
      'xbob.db.verification.utils>=1.0.0' # defines a set of utilities for face verification databases like this one.
    ],

    namespace_packages = [
      'xbob',
      'xbob.db',
      ],

    entry_points = {
      # bob database declaration
      'bob.db': [
        'mobio = xbob.db.mobio.driver:Interface',
        ],

      # bob unittest declaration
      'bob.test': [
        'mobio = xbob.db.mobio.test:MobioDatabaseTest',
        ],
      # scripts
      'console_scripts': [
        'generate_filelist = xbob.db.mobio.generate_filelist:main',
        ],
      },

    classifiers = [
      'Development Status :: 5 - Production/Stable',
      'Environment :: Console',
      'Intended Audience :: Developers',
      'Intended Audience :: Education',
      'Intended Audience :: Science/Research',
      'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
      'Natural Language :: English',
      'Programming Language :: Python',
      'Programming Language :: Python :: 3',
      'Topic :: Scientific/Engineering :: Artificial Intelligence',
      'Topic :: Database :: Front-Ends',
      ],
)

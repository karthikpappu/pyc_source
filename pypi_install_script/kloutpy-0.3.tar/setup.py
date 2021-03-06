#!/usr/bin/env python
#-*-coding:utf-8-*-

# Copyright (C) - 2012 @rogeliorv
# Based on previous work by Juan Cabral

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


#==============================================================================
# DOCS
#==============================================================================

"""Setup for kloutpy"""

#==============================================================================
# IMPORTS
#==============================================================================

from setuptools import setup
import kloutpy
import test

#==============================================================================
# SETUP
#==============================================================================

name = "kloutpy"

version = str(kloutpy.__version__)


setup(name=name,
      version=version,
      description="Python client for the klout api (http://klout.com/)",
      author="@rogeliorv",  # Based on earlier work by JBC
      url="https://github.com/rogeliorv/kloutpy/",
      download_url='https://github.com/rogeliorv/kloutpy/tarball/master',
      license="LGPL3",
      keywords="klout",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   "Topic :: Utilities",
                   "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python :: 2",
                   "Topic :: Internet",
                   "Topic :: Internet :: WWW/HTTP", 
                   ],
      py_modules = ['kloutpy', 'kloutpy_util'],
)


#==============================================================================
# MAIN
#==============================================================================

if __name__ == '__main__':
    print(__doc__)

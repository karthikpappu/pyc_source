#!/usr/bin/env python
# encoding: utf-8

#    Copyright © 2008 Arne Babenhauserheide
# 
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>

"""pymarkdown_minisite - Parse a list of markdown files to a website with index. 
"""

# We use the advanced setuptools. 
from setuptools import setup
# If we have one or more packages, we also need to import find packages  
# It is currently not necessary. 
# The corresponding line in setup() is commented out, too. 
# from setuptools import find_packages

# Get the docstring of the main module. This will serve as long description.
from pymarkdown_minisite import __doc__ as babtools__doc__

# Also get version and changelog. Changelog is read from the file Changelog.txt
from pymarkdown_minisite import __version__, __changelog__

# Create the desription from the docstrings 

# The name for PyPI
NAME = __doc__.split("\n")[0].split(" - ")[0]

# The one line description for PyPI is the part after the dash (" - ") in the first line of this fiels docstring.. 
DESCRIPTION = __doc__.split("\n")[0].split(" - ")[1:]

# The longer description is built from various sources. 

#  The second and following lines of this files doocstring
LONG_DESCRIPTION = "\n".join(__doc__.split("\n")[1:])

# The docstring in the main file (module). 
LONG_DESCRIPTION += "\n\n" + "\n".join(babtools__doc__.split("\n")[1:])

# And the Changelog from Changelog.txt
LONG_DESCRIPTION += "\n\n" + __changelog__


# Fire up setup with these values.i- must be modified. 
setup(name=NAME,
      version=__version__,
      description=DESCRIPTION,
      long_description=LONG_DESCRIPTION, 
      author='Arne Babenhauserheide',
      author_email='arne_bab@web.de',
      keywords=["babtools", "markdown"], 
      license="GNU GPL-3 or later", 
      platforms=["any"], 
      requires = ["markdown (>=2.0)"], 
      # All classifiers can be found via python setup.py register --list-classifiers
      classifiers = [
            "License :: OSI Approved :: GNU General Public License (GPL)",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Intended Audience :: Developers", 
            "Intended Audience :: End Users/Desktop", 
            "Environment :: Console", 
            "Development Status :: 4 - Beta"
            ],
      url='http://freehg.org/u/ArneBab/pymarkdown_minisite',
      #packages = find_packages('.'), 
      py_modules=['pymarkdown_minisite'],
      scripts=["parse_and_list_markdown_files.py", "parse_and_list_markdown_files.sh"]
     )

#!/usr/bin/env python

import os
import sys
try:
      from setuptools import setup
except ImportError:
      from distutils.core import setup

__author__ = "Colin Bell <colin.bell@uwaterloo.ca>"
__copyright__ = "Copyright 2011, University of Waterloo"
__license__ = "BSD-new"

# A utility function to read the README file into the long_description field.
def read(fname):
    """ Takes a filename and returns the contents of said file relative to
    the current directory.
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

# A utility function that to get version number from package source tree.
def get_package_version():
    """ Adds current directory and src/ to sys.path.  imports qualysutils
    to get __version__ and returns it.
    """
    save_path = list(sys.path)
    sys.path.insert(0, os.path.join(os.path.dirname(__file__),"src"))
    # Get the version string from the module itself.
    from qualysutils import __version__ as VERSION
    # Reset the path to pre-import.
    sys.path = save_path
    return VERSION

setup(name='QualysUtils',
      version=get_package_version(),
      author='Colin Bell',
      author_email='colin.bell@uwaterloo.ca',
      description='uWaterloo QualysGuard(R) QualysUtils Package',
      license = "BSD-new",
      keywords = "Qualys QualysGuard API helper network security",
      url='http://ist.uwaterloo.ca/iss/projects/qualysutils.html',
      package_dir={'': 'src'},
      packages=['qualysutils'],
      package_data={'qualysutils':['LICENSE']},
      #scripts=[],
      long_description=read('README'),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Utilities",
          "License :: OSI Approved :: BSD License"
      ],
      install_requires=[
          'QualysConnect',
          'lxml'
      ],
     )

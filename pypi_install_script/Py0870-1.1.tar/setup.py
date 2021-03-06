'''
Created on 30 Aug 2014

@author: Robert Putt
'''

# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages
import os

base_name='Py0870'

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name=base_name,
    version='1.1',
    author=u'Robert Putt',
    author_email='rob@puttfamily.co.uk',
    include_package_data = True,
    packages=find_packages(), # include all packages under this directory
    description='to update',
    zip_safe=False,

    # Adds dependencies
    install_requires = ['requests',
                        ],
)

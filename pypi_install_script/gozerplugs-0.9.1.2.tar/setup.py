#!/usr/bin/env python
#
#

__copyright__ = 'this file is in the public domain'
__revision__ = '$Id: setup.py 71 2005-11-10 13:37:50Z bart $'

from setuptools import setup

setup(
    name='gozerplugs',
    version='0.9.1.2',
    url='http://gozerbot.org',
    author='Bart Thate',
    author_email='bthate@gmail.com',
    description='plugin package for gozerbot ',
    license='BSD',
    packages = ['gozerplugs', 'gozerplugs.webserver', 'gozerplugs.tracserver'],
)

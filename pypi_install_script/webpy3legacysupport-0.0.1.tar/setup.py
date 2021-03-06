#!/usr/bin/env python

from setuptools import setup
from web import __version__

setup(name='webpy3legacysupport',
      version='0.0.1',
      description='web.py: makes web apps',
      author='Aaron Swartz',
      author_email='me@aaronsw.com',
      maintainer='Anand Chitipothu',
      maintainer_email='anandology@gmail.com',
      url='https://github.com/webpy/webpy',
      packages=['web', 'web.wsgiserver', 'web.contrib'],
      long_description="Think about the ideal way to write a web app. Write the code to make it happen.",
      license="Public domain",
      platforms=["any"],
     )

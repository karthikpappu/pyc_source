#!/usr/bin/env python

from distutils.core import setup
setup(name='dumb',
      version='0.4.1',
      description='Distributed Unified Mangler of Bookmarks',
      author='Elena "of Valhalla" Grandi',
      author_email='elena.valhalla@gmail.com',
      url='http://dumb.trueelena.org',
      download_url='http://dumb.trueelena.org/dumb/downloads/dumb-0.4.1.tar.gz',
      requires = ['yaml'],
      classifiers=[
          'Environment :: Console',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Utilities'
          ],
      packages = ['dumb'],
      scripts=['scripts/dumb-add','scripts/dumb-add-mirror','scripts/dumb-add-position','scripts/dumb-add-related','scripts/dumb-edit','scripts/dumb-list','scripts/dumb-list-keywords','scripts/dumb-show','scripts/dumb-to-jinja2','scripts/dumb-touch']
      )


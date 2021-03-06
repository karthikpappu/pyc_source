#!/usr/bin/env python
from distutils.core import setup
from ini_handler.__init__ import __release__

setup(name='Ini-Handler',
      version=__release__,
      description='An easy to use ini file handler library',
      author='Trevalyan Stevens',
      author_email='etstevens60@gmail.com',
      url='http://www.kerneweksoftware.com/software.html',
      packages=['ini_handler'],
      classifiers=[
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 3',
                   'License :: OSI Approved :: MIT License',
                   'Operating System :: OS Independent',
                   'Development Status :: 3 - Alpha',
                   'Intended Audience :: Developers',
                   'Topic :: Software Development :: Libraries',
                   'Topic :: Software Development :: Libraries :: Python Modules',
      ])

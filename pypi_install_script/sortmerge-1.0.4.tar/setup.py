#!/usr/bin/env python
from setuptools import setup, find_packages

setup(name = 'sortmerge',
      version = '1.0.4',
      author = 'Sergio Tocalini Joerg',
      author_email = 'sergiotocalini@gmail.com',
      url = 'https://github.com/sergiotocalini/sortmerge',
      license = 'GNU GPLv3',
      packages = find_packages(),
      classifiers=[
          'Programming Language :: Python',
          ],
      zip_safe=True,
      include_package_data=True,
      entry_points = {
          'console_scripts': [
              'sortmerge = sortmerge.sortmerge:main'
          ]
      }
)

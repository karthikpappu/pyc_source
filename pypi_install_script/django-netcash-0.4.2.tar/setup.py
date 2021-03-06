#!/usr/bin/env python
from distutils.core import setup

setup(
    name='django-netcash',
    version='0.4.2',
    author='Mikhail Korobov',
    author_email='kmike84@gmail.com',

    packages=['netcash', 'netcash.migrations'],

    url='http://bitbucket.org/kmike/django-netcash/',
    download_url = 'http://bitbucket.org/kmike/django-netcash/get/tip.gz',
    license = 'MIT license',
    description = 'A pluggable Django application for integrating netcash.co.za payment system.',
    long_description = open('README.rst').read().decode('utf8'),

    classifiers=(
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
)

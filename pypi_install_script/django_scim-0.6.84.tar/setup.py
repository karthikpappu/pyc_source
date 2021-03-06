#!/usr/bin/env python
# Installs django_scim.

import os
import sys
from distutils.core import setup


def long_description():
    """Get the long description from the README"""
    return open(os.path.join(sys.path[0], 'README.rst')).read()


def get_version():
    return open('version.txt', 'r').read().strip()


setup(
    author='Erik van Zijst',
    author_email='erik.van.zijst@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    description='A partial implementation of the SCIM 2.0 provider specification for use with Django.',
    download_url='https://bitbucket.org/atlassian/django_scim/downloads/django_scim-0.6.tar.gz',
    keywords='django scim',
    license='MIT',
    long_description=long_description(),
    name='django_scim',
    packages=['django_scim'],
    scripts=['scim'],
    url='https://bitbucket.org/atlassian/django_scim',
    version=get_version(),
)

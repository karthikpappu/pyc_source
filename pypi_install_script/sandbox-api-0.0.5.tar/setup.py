"""Setuptools entry point."""

import codecs
import os


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: POSIX :: Linux',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

dirname = os.path.dirname(__file__)
description = ('Provide a Python 3 interface to communicate with a sandbox '
               '(https://github.com/PremierLangage/sandbox)')
long_description = (
    codecs.open(os.path.join(dirname, 'README.md'), encoding='utf-8').read()
    + '\n\n______\n\n'
    + codecs.open(os.path.join(dirname, 'CHANGES.md'), encoding='utf-8').read()
)

setup(
    name='sandbox-api',
    version="0.0.5",
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Coumes Quentin',
    author_email='coumes.quentin@gmail.com',
    url='https://github.com/qcoumes/sandbox-api',
    packages=['sandbox_api'],
    install_requires=['requests'],
    classifiers=CLASSIFIERS
)

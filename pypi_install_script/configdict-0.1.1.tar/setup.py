#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup, find_packages

readme = open('README.rst').read()
version = (0, 1, 1)

setup(
    name='configdict',
    python_requires=">=3.7",
    version=".".join(map(str, version)),
    description='A persistent dict used as configuration',
    long_description=readme,
    author='Eduardo Moguillansky',
    author_email='eduardo.moguillansky@gmail.com',
    url='https://github.com/gesellkammer/configdict',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "setuptools",
        "appdirs",
        "tabulate",
    ],
    license="BSD",
    zip_safe=False,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English', 'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8'
    ],
)

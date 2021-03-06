#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

version = '0.1.0'

setup(
    name='gdtools',
    version=version,
    description='GeneDock command-line client for interacting with GeneDock platform',
    author='Wu Yarong',
	author_email='wuyarong@genedock.com',
    # long_description=readme,
    packages=find_packages(),
    install_requires=['gdpy>=0.0.1', 'prettytable==0.7.2'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'gdtools = gdtools.gdtools_scripts:main',
        ]
    },
    url="https://www.genedock.com",
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)

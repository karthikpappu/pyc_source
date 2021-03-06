# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='newlibcode',
    version='0.1.1',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

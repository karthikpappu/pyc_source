#!/usr/bin/env python

# Copyright 2013 Free Electrons

#
"""Build tar.gz for pdf-link-checker

Required packages:
    python-pdfminer
    pdfminer-data # recommended for encoding data needed to read some PDF documents
                  # in CJK (Chinese, Japanese, Korean) languages.
"""

from setuptools import setup

setup(
    name='pdf-link-checker',
    version='1.1.1',
    description='Reports broken hyperlinks in PDF documents',
    long_description=open('README.rst').read(),

    author='Ezequiel Garcia',
    author_email='ezequiel.garcia@free-electrons.com',
    license='GPL-2',

    url='http://git.free-electrons.com/pdf-link-checker',
    scripts=['bin/pdf-link-checker'],
    install_requires=['pdfminer'],
)

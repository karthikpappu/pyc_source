#!/usr/bin/env python

from setuptools import setup,find_packages
import os

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
	return open(os.path.join(os.path.dirname(__file__), fname)).read()

PACKAGE = "botohelper"
NAME = "botohelper"
DESCRIPTION = "a library to make boto3 easier"
AUTHOR = "Banio Carpenter"
AUTHOR_EMAIL = "banio@mncarpenters.net"
URL = "http://example.com"
VERSION = "0.59"

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=read("README.md"),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    license="BSD",
    url=URL,
    packages=find_packages(),
    install_requires=['setuptools', 'twine', 'termcolor', 'vmtools', 'argparse', 'boto3', 'awsretry'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
    ],
    zip_safe=False,
)

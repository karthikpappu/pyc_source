#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import os

from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-unordered",
    version="0.1.0",
    author="Ivan Zaikin",
    author_email="ut@pyngo.tom.ru",
    maintainer="Ivan Zaikin",
    maintainer_email="ut@pyngo.tom.ru",
    license="MIT",
    url="https://github.com/utapyngo/pytest-unordered",
    description="Test equality of unordered sequences of unhashable items",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    py_modules=["pytest_unordered"],
    install_requires=["pytest>=4.0.0"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["unordered = pytest_unordered"]},
)

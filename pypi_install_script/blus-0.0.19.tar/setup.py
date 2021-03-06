#!/usr/bin/python

import os

from setuptools import setup, find_packages

setup(
    name="blus",
    version="0.0.19",
    description="Simple Bluez D-Bus client interface",
    url="https://github.com/molobrakos/blus",
    license="",
    author="Erik",
    author_email="error.errorsson@gmail.com",
    include_package_data=True,
    packages=find_packages(),
    py_modules=["blus"],
    keywords="bluez",
    long_description=(
        open("README.md").read() if os.path.exists("README.md") else ""
    ),
    install_requires=list(open("requirements.txt").read().strip().split("\n")),
    entry_points={"conusole_scripts": ["blus=blus.__main__:main"]},
)

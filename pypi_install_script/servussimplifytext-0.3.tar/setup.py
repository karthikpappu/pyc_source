#!/usr/bin/env python3

from setuptools import setup


with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="servussimplifytext",
    packages=["servussimplifytext"],
    version="0.3",
    license="GPL3",
    description="Python3 module to simplify text removing unnecesary symbols.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Carlos A. Planchón",
    author_email="bubbledoloresuruguay2@gmail.com",
    url="https://github.com/carlosplanchon/servussimplifytext",
    download_url="https://github.com/carlosplanchon/"
        "servussimplifytext/archive/v0.3.tar.gz",
    keywords=["simplify", "text", "regex"],
    classifiers=[
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)

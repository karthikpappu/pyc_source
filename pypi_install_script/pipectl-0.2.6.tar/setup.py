# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(
    name="pipectl",
    version="0.2.6",
    description="A CI/CD Build pipeline DSL",
    license="MIT",
    author="adamar",
    author_email="none@none.com",
    url="http://github.com/adamar/pipectl",
    packages=find_packages(),
    install_requires=[
        "bamboo_api_v2>=0.0.1",
        "GitPython>=2.0.0",
        "safygiphy>=1.1.0",
        "slacker>=0.9.29"
        ],
    scripts=['pipectl/pipectl'],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ]
)

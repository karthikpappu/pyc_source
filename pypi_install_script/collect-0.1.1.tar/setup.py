import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="collect",
    version="0.1.1",
    author="Philipp Bosch",
    author_email="hello@pb.io",
    packages=find_packages(),
    url="http://collect.io/libraries/python/",
    license="http://philippbosch.mit-license.org/",
    description="Python library for collecting data at collect.io",
    long_description=read('README.md'),
    test_suite="collect.tests.get_suite",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Topic :: Database",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Utilities",
    ],
    install_requires=[
        "couchdbkit>=0.5.7",
    ],
)
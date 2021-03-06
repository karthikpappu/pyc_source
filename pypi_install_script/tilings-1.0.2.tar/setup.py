#!/usr/bin/env python
import os

from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname), encoding="utf-8").read()


setup(
    name="tilings",
    version="1.0.2",
    author="Permuta Triangle",
    author_email="permutatriangle@gmail.com",
    description="A Python library for gridded permutations and tilings.",
    license="BSD-3",
    keywords=("permutation perm gridded pattern tiling avoid contain"
              "occurrences grid class"),
    url="https://github.com/PermutaTriangle/Tilings",
    project_urls={
        'Source': 'https://github.com/PermutaTriangle/Tilings',
        'Tracker': 'https://github.com/PermutaTriangle/Tilings/issues'
    },
    packages=find_packages(),
    long_description=read("README.rst"),
    install_requires=['comb-spec-searcher==0.5.0',
                      'permuta==1.3.0',
                      'pymongo==3.10.1',
                      'sympy==1.5.1'],
    setup_requires=['pytest-runner==5.1'],
    tests_require=['pytest==5.1.1',
                   'pytest-cov==2.7.1',
                   'pytest-pep8==1.0.6',
                   'pytest-isort==0.3.1'],
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',

        'Topic :: Education',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)

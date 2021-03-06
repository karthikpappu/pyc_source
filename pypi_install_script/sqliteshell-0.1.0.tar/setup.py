#!/usr/bin/env python

import ast
import os

from setuptools import setup, find_packages


def this_dir():
    return os.path.dirname(os.path.abspath(__file__))


def read_version(path):
    with open(path) as fh:
        for line in fh:
            stripped = line.strip()
            if stripped == '' or stripped.startswith('#'):
                continue
            elif line.startswith('from __future__ import'):
                continue
            else:
                if not line.startswith('__version__ = '):
                    raise Exception("Can't find __version__ line in " + path)
                break
        else:
            raise Exception("Can't find __version__ line in " + path)
        _, _, quoted = line.rstrip().partition('= ')
        return ast.literal_eval(quoted)


classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: POSIX',
    'Programming Language :: Python :: 3',
]

install_requires = []

version = read_version(
    os.path.join(this_dir(), 'src/sqliteshell/_version.py'))

setup(
    name='sqliteshell',
    url='https://github.com/jlee_made/sqliteshell',
    author='John Lee',
    classifiers=classifiers,
    description=(
        'Just-about-tolerable sqlite shell for use with in-memory sqlite.'),
    install_requires=install_requires,
    license='MIT',
    package_dir={'': 'src'},
    packages=find_packages('src'),
    platforms=['any'],
    version=version,
    zip_safe=True,
)

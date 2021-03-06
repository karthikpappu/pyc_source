#!/usr/bin/env python3
# -*- coding: utf-8; -*-
#
# Copyright (c) 2016 Álan Crístoffer
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import codecs
import glob
import shutil
from os import path

import moirai
from setuptools import Command, find_packages, setup

PWD = path.abspath(path.dirname(__file__))
with codecs.open(path.join(PWD, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = [
        './build', './dist', './*.pyc', './*.tgz', './*.egg-info',
        './**/__pycache__'
    ]

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        cwd = path.realpath(path.curdir)
        ps = [glob.glob(p) for p in self.CLEAN_FILES]
        ps = [path.normpath(path.join(cwd, p)) for p in sum(ps, [])]
        ps = [p for p in ps if p.startswith(cwd)]
        for p in ps:
            print('removing %s' % p)
            shutil.rmtree(p)


setup(
    name='moirai',
    version=moirai.__version__,
    description='Digital Control Manager Backend',
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English', 'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces'
    ],
    keywords='digital control manager',
    author='Álan Crístoffer',
    author_email='acristoffers@gmail.com',
    url='https://www.github.com/acristoffers/moirai',
    packages=find_packages(),
    license="MIT",
    install_requires=[
        'appdirs', 'ahio', 'Flask', 'pymongo', 'python-dateutil', 'numpy',
        'scipy', 'cheroot'
    ],
    entry_points={'console_scripts': ['moirai = moirai.moirai:start']},
    cmdclass={'clean': CleanCommand})

#!/usr/bin/env python

# Copyright 2009-2015 Canonical Ltd.  All rights reserved.
#
# This file is part of lazr.sshserver
#
# lazr.sshserver is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# lazr.sshserver is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with lazr.sshserver.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages

# generic helpers primarily for the long_description
def generate(*docname_or_string):
    res = []
    for value in docname_or_string:
        if value.endswith('.txt'):
            f = open(value)
            value = f.read()
            f.close()
        res.append(value)
        if not value.endswith('\n'):
            res.append('')
    return '\n'.join(res)
# end generic helpers


__version__ = open("src/txpkgupload/version.txt").read().strip()

setup(
    name='txpkgupload',
    version=__version__,
    packages=find_packages('src') + ['twisted.plugins'],
    package_dir={'':'src'},
    include_package_data=True,
    zip_safe=False,
    maintainer='LAZR Developers',
    maintainer_email='lazr-developers@lists.launchpad.net',
    description=open('README.txt').readline().strip(),
    long_description=generate('src/txpkgupload/NEWS.txt'),
    license='AGPL v3',
    install_requires=[
        'FormEncode',
        'lazr.sshserver',
        'oops',
        'oops-datedir-repo',
        'oops-twisted',
        'PyYAML',
        'setuptools',
        'Twisted',
        'zope.component',
        'zope.interface',
        'zope.security',
        'zope.server',
        ],
    url='https://launchpad.net/txpkgupload',
    download_url= 'https://launchpad.net/txpkgupload/+download',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python"],
    extras_require=dict(
        test=['fixtures',
              'testtools'],
    ),
    # This does not play nicely with buildout because it downloads but does
    # not cache the package.
    #setup_requires=['eggtestinfo', 'setuptools_bzr'],
    test_suite='txpkgupload.tests',
    )

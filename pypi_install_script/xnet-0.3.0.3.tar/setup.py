#!/usr/bin/env python

# Bootstrap installation of Distribute
#import distribute_setup
#distribute_setup.use_setuptools()

import os

from setuptools import setup


PROJECT = 'xnet'
VERSION = '0.3.0.3'  # release 0.2.1.0 when all tools support expandable addrs
URL = 'http://xnet.tripleaes.com/'
AUTHOR = u'Krister Hedfors'
AUTHOR_EMAIL = u'krister.hedfors@gmail.com'
DESC = "XNet - Your Swiss Army Pitchfork of Networking"


def read_file(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
    )
    return open(file_path).read()

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=read_file('README.rst'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license='LICENSE',
    #py_module=['xnet'],
    #namespace_packages=[],
    packages=[
        'xnet',
        'xnet.tests',
        'xnet.testing',
        'xnet.debug',
        'xnet.tools',
        'xnet.net',
        'xnet.net.ipv4',
        'xnet.net.http',
        'xnet.net.ssh',
        'xnet.packages',
        'xnet.packages.urllib3',
        'xnet.packages.urllib3.packages',
        'xnet.packages.urllib3.packages.ssl_match_hostname',
    ],
    #package_dir = {{'': os.path.dirname(__file__)}},
    #package_dir = {'xnet': 'xnet'},
    #include_package_data=True,
    #zip_safe=False,
    #install_requires=[
    #    # -*- Requirements -*-
    #],
    entry_points={
        #
        # populate automatically
        #
        'console_scripts': [
            'xnet = xnet.tools.run:main',
            'iissn = xnet.tools.iissn:main',
            'iprange = xnet.tools.iprange:main',
            'resolv = xnet.tools.resolv:main',
            'sslinfo = xnet.tools.sslinfo:main',
            'tcpstate = xnet.tools.tcpstate:main',
            'webget = xnet.tools.webget:main',
            'xselenium = xnet.tools.seleniumtool:main',
            'netcats = xnet.tools.netcats:main',
            'netfuzz = xnet.tools.netfuzz:main',
        ],
    },
    classifiers=[
        # see http://pypi.python.org/pypi?:action=list_classifiers
        # -*- Classifiers -*-
        'License :: OSI Approved',
        'License :: OSI Approved :: BSD License',
        "Programming Language :: Python",
    ],
)

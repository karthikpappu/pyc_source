"""A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, environ
from distutils.extension import Extension
from distutils.util import get_platform, check_environ, log

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
description = 'A free opensource globalplatform library for java card and smartcard. https://www.javacardos.com'


include_dirs = []
define_macros = []
library_dirs = []

if 'win32' == get_platform():
    gp_include_dir = ''
    gp_library_dir = ''

    import sys
    gp_include_dir = ''
    gp_library_dir = ''
    if ('install' in sys.argv) or ('bdist' in sys.argv) or ('sdist' in sys.argv) or ('bdist_wininst' in sys.argv):
        gp_root = environ.get('GLOBALPLATFORM_ROOT', '')
        if len(gp_root) == 0:
            print('Please set environment variable GLOBALPLATFORM_ROOT to specify the root of library GlobalPlatform.')
            exit(-1)
            
        gp_include_dir = gp_root
        gp_library_dir = gp_root

    include_dirs = [gp_include_dir, ]
    define_macros = [('_WIN32', 1), ('WIN32', 1), ]
    library_dirs = [gp_library_dir, ]
else:
    include_dirs = ['/usr/include/PCSC']
    define_macros = []
    library_dirs = []

setup(
    name='pyGlobalPlatform',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.4.16',

    description=description,
    long_description=long_description,

    # The project's main homepage.
    url='http://www.javacardos.com/',

    # Author details
    author='www.JavaCardOS.com',
    author_email='javacardos@gmail.com',

    # Choose your license
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.3',
        'Programming Language :: Python :: 2.4',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    # What does your project relate to?
    keywords='smartcard javacard globalplatform',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['peppercorn'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
        # 'dev': ['check-manifest'],
        # 'test': ['coverage'],
    # },

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={
        # 'sample': ['package_data.dat'],
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        # 'console_scripts': [
            # 'sample=sample:main',
        # ],
    },

    ext_modules = [
        Extension(
            'pyGlobalPlatform.pyGlobalPlatform'
            , ['src/main.cpp', 'src/gp_functions.cpp']
            , include_dirs = include_dirs
            , define_macros = define_macros
            , libraries = ['globalplatform', ]
            , library_dirs = library_dirs
        )
    ],
)

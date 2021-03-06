import os.path
from setuptools import setup, find_packages
import sys


tests_require = []
if sys.version_info[0] == 2:
    tests_require.append('mock')

setup(
    name='gocept.cache',
    version='4.0',
    author="gocept",
    author_email="mail@gocept.com",
    description="Cache descriptors for Python and Zope",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: Zope Public License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    keywords='cache transaction bound zope',
    long_description=(
        ".. contents::\n\n" +
        open(os.path.join('src', 'gocept', 'cache', 'README.rst')).read() +
        '\n\n' +
        open('CHANGES.rst').read()),
    license="ZPL 2.1",
    url='https://github.com/gocept/gocept.cache',
    packages=find_packages('src'),
    package_dir={'': 'src'},

    include_package_data=True,
    zip_safe=False,

    namespace_packages=['gocept'],
    install_requires=[
        'decorator',
        'setuptools',
        'transaction',
        'zope.testing',
    ],
    extras_require=dict(
        test=tests_require),
)

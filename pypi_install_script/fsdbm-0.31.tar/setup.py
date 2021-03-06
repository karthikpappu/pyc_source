#!/usr/bin/env python
import os
from setuptools import setup

PACKAGE = 'fsdbm'
VERSION = '0.31'

readme = open(os.path.join(os.path.dirname(__file__), 'README')).read()

if __name__ == '__main__':
    # Compile the list of packages available, because distutils doesn't have
    # an easy way to do this.
    packages, data_files = [], []
    root_dir = os.path.dirname(__file__)
    if root_dir:
        os.chdir(root_dir)

    for dirpath, dirnames, filenames in os.walk(PACKAGE):
        for i, dirname in enumerate(dirnames):
            if dirname in ['.', '..']:
                del dirnames[i]
        if '__init__.py' in filenames:
            pkg = dirpath.replace(os.path.sep, '.')
            if os.path.altsep:
                pkg = pkg.replace(os.path.altsep, '.')
            packages.append(pkg)
        elif filenames:
            prefix = dirpath[len(PACKAGE) + 1:] # Strip package directory + path separator
            for f in filenames:
                data_files.append(os.path.join(prefix, f))


    setup(
        version = VERSION,
        description = 'Dict-style file system based DBM, suitable for large data (such as images).',
        long_description = readme,
        author = 'Imbolc',
        author_email = 'imbolc@imbolc.name',
        url = 'http://bitbucket.org/imbolc/fsdbm/',
        name = PACKAGE,

        packages = packages,
        package_data = {'fsdbm': data_files},

        license = "BSD",
        keywords = "dbm",
        classifiers=[
            'Development Status :: 4 - Beta',
            'License :: OSI Approved :: BSD License',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
    )

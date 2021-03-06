# -*- coding: utf-8 -*-
"""Setup file for the SnakeCycles project.
"""

import codecs
import os.path
import re

from setuptools import setup, find_packages

# avoid a from snakecycles import __version__ as version (that compiles snakecycles.__init__ and
# is not compatible with bdist_deb)
version = None
for line in codecs.open(os.path.join('snakecycles', '__init__.py'), 'r', encoding='utf-8'):
    matcher = re.match(r"""^__version__\s*=\s*['"](.*)['"]\s*$""", line)
    version = version or matcher and matcher.group(1)

# get README content from README.md file
with codecs.open(os.path.join(os.path.dirname(__file__), 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()

entry_points = {u'console_scripts': [u'snakecycles = snakecycles.cli:main']}

setup(
    name='snakecycles',
    version=version,
    description='Parse snakefood output and detect import cycles.',
    long_description=long_description,
    author='mgallet',
    author_email='github@19pouces.net',
    license='CeCILL-B',
    url='',
    entry_points=entry_points,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    test_suite='snakecycles.tests',
    install_requires=['networkx', 'snakefood'],
    setup_requires=[],
    classifiers=['Development Status :: 3 - Alpha', 'Operating System :: MacOS :: MacOS X',
                 'Operating System :: Microsoft :: Windows', 'Operating System :: POSIX :: BSD',
                 'Operating System :: POSIX :: Linux', 'Operating System :: Unix',
                 'License :: OSI Approved :: CEA CNRS Inria Logiciel Libre License, version 2.1 (CeCILL-2.1)',
                 'Programming Language :: Python :: 2.7', 'Programming Language :: Python :: 3.3',
                 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5'],
)

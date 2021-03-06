# This program is free software: you can redistribute it and/or modify it under the
# terms of the Apache License (v2.0) as published by the Apache Software Foundation.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE. See the Apache License for more details.
#
# You should have received a copy of the Apache License along with this program.
# If not, see <https://www.apache.org/licenses/LICENSE-2.0>.

"""Setup and installation script for dist_exe."""

# standard libs
import os
from setuptools import setup, find_packages

# internal libs
from dist_exe.__meta__ import (__appname__, __version__, __authors__,
                               __contact__, __license__, __description__,
                               __keywords__, __website__)


def readme_file():
    """Use README.md as long_description."""
    with open(os.path.join(os.path.dirname(__file__), "README.md"), 'r') as readme:
        return readme.read()


setup(
    name             = __appname__,
    version          = __version__,
    author           = __authors__,
    author_email     = __contact__,
    description      = __description__,
    license          = __license__,
    keywords         = __keywords__,
    url              = __website__,
    packages         = find_packages(),
    long_description = readme_file(),
    long_description_content_type='text/markdown',
    classifiers      = ['Development Status :: 4 - Beta',
                        'Programming Language :: Python :: 3.7',
                        'License :: OSI Approved :: Apache Software License', ],
    install_requires = [],
    entry_points     = {'console_scripts': ['dist_exe=dist_exe:main',]},
)

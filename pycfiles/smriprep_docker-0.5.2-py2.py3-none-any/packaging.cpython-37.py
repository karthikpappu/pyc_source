# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pn36swhz/pip/pip/_internal/utils/packaging.py
# Compiled at: 2020-02-14 17:24:54
# Size of source mod 2**32: 3035 bytes
from __future__ import absolute_import
import logging
from email.parser import FeedParser
from pip._vendor import pkg_resources
from pip._vendor.packaging import specifiers, version
from pip._internal.exceptions import NoneMetadataError
from pip._internal.utils.misc import display_path
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Optional, Tuple
    from email.message import Message
    from pip._vendor.pkg_resources import Distribution
logger = logging.getLogger(__name__)

def check_requires_python(requires_python, version_info):
    """
    Check if the given Python version matches a "Requires-Python" specifier.

    :param version_info: A 3-tuple of ints representing a Python
        major-minor-micro version to check (e.g. `sys.version_info[:3]`).

    :return: `True` if the given Python version satisfies the requirement.
        Otherwise, return `False`.

    :raises InvalidSpecifier: If `requires_python` has an invalid format.
    """
    if requires_python is None:
        return True
    requires_python_specifier = specifiers.SpecifierSet(requires_python)
    python_version = version.parse('.'.join(map(str, version_info)))
    return python_version in requires_python_specifier


def get_metadata(dist):
    """
    :raises NoneMetadataError: if the distribution reports `has_metadata()`
        True but `get_metadata()` returns None.
    """
    metadata_name = 'METADATA'
    if isinstance(dist, pkg_resources.DistInfoDistribution) and dist.has_metadata(metadata_name):
        metadata = dist.get_metadata(metadata_name)
    else:
        if dist.has_metadata('PKG-INFO'):
            metadata_name = 'PKG-INFO'
            metadata = dist.get_metadata(metadata_name)
        else:
            logger.warning('No metadata found in %s', display_path(dist.location))
            metadata = ''
    if metadata is None:
        raise NoneMetadataError(dist, metadata_name)
    feed_parser = FeedParser()
    feed_parser.feed(metadata)
    return feed_parser.close()


def get_requires_python(dist):
    """
    Return the "Requires-Python" metadata for a distribution, or None
    if not present.
    """
    pkg_info_dict = get_metadata(dist)
    requires_python = pkg_info_dict.get('Requires-Python')
    if requires_python is not None:
        requires_python = str(requires_python)
    return requires_python


def get_installer(dist):
    if dist.has_metadata('INSTALLER'):
        for line in dist.get_metadata_lines('INSTALLER'):
            if line.strip():
                return line.strip()

    return ''
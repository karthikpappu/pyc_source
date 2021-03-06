# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-pti7pv2_/pip/pip/_internal/utils/virtualenv.py
# Compiled at: 2020-02-14 17:24:43
# Size of source mod 2**32: 3396 bytes
from __future__ import absolute_import
import logging, os, re, site, sys
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List, Optional
logger = logging.getLogger(__name__)
_INCLUDE_SYSTEM_SITE_PACKAGES_REGEX = re.compile('include-system-site-packages\\s*=\\s*(?P<value>true|false)')

def _running_under_venv():
    """Checks if sys.base_prefix and sys.prefix match.

    This handles PEP 405 compliant virtual environments.
    """
    return sys.prefix != getattr(sys, 'base_prefix', sys.prefix)


def _running_under_regular_virtualenv():
    """Checks if sys.real_prefix is set.

    This handles virtual environments created with pypa's virtualenv.
    """
    return hasattr(sys, 'real_prefix')


def running_under_virtualenv():
    """Return True if we're running inside a virtualenv, False otherwise.
    """
    return _running_under_venv() or _running_under_regular_virtualenv()


def _get_pyvenv_cfg_lines():
    """Reads {sys.prefix}/pyvenv.cfg and returns its contents as list of lines

    Returns None, if it could not read/access the file.
    """
    pyvenv_cfg_file = os.path.join(sys.prefix, 'pyvenv.cfg')
    try:
        with open(pyvenv_cfg_file) as (f):
            return f.read().splitlines()
    except IOError:
        return


def _no_global_under_venv():
    """Check `{sys.prefix}/pyvenv.cfg` for system site-packages inclusion

    PEP 405 specifies that when system site-packages are not supposed to be
    visible from a virtual environment, `pyvenv.cfg` must contain the following
    line:

        include-system-site-packages = false

    Additionally, log a warning if accessing the file fails.
    """
    cfg_lines = _get_pyvenv_cfg_lines()
    if cfg_lines is None:
        logger.warning("Could not access 'pyvenv.cfg' despite a virtual environment being active. Assuming global site-packages is not accessible in this environment.")
        return True
    for line in cfg_lines:
        match = _INCLUDE_SYSTEM_SITE_PACKAGES_REGEX.match(line)
        if match is not None and match.group('value') == 'false':
            return True

    return False


def _no_global_under_regular_virtualenv():
    """Check if "no-global-site-packages.txt" exists beside site.py

    This mirrors logic in pypa/virtualenv for determining whether system
    site-packages are visible in the virtual environment.
    """
    site_mod_dir = os.path.dirname(os.path.abspath(site.__file__))
    no_global_site_packages_file = os.path.join(site_mod_dir, 'no-global-site-packages.txt')
    return os.path.exists(no_global_site_packages_file)


def virtualenv_no_global():
    """Returns a boolean, whether running in venv with no system site-packages.
    """
    if _running_under_regular_virtualenv():
        return _no_global_under_regular_virtualenv()
    if _running_under_venv():
        return _no_global_under_venv()
    return False
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_internal/operations/build/metadata_legacy.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 3957 bytes
"""Metadata generation logic for legacy source distributions.
"""
import logging, os
from pip._internal.exceptions import InstallationError
from pip._internal.utils.misc import ensure_dir
from pip._internal.utils.setuptools_build import make_setuptools_egg_info_args
from pip._internal.utils.subprocess import call_subprocess
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
import pip._internal.vcs as vcs
if MYPY_CHECK_RUNNING:
    from typing import List, Optional
    from pip._internal.build_env import BuildEnvironment
logger = logging.getLogger(__name__)

def _find_egg_info(source_directory, is_editable):
    """Find an .egg-info in `source_directory`, based on `is_editable`.
    """

    def looks_like_virtual_env(path):
        return os.path.lexists(os.path.join(path, 'bin', 'python')) or os.path.exists(os.path.join(path, 'Scripts', 'Python.exe'))

    def locate_editable_egg_info(base):
        candidates = []
        for root, dirs, files in os.walk(base):
            for dir_ in vcs.dirnames:
                if dir_ in dirs:
                    dirs.remove(dir_)

            for dir_ in list(dirs):
                if looks_like_virtual_env(os.path.join(root, dir_)):
                    dirs.remove(dir_)

            candidates.extend((os.path.join(root, dir_) for dir_ in dirs))

        return [f for f in candidates if f.endswith('.egg-info')]

    def depth_of_directory(dir_):
        return dir_.count(os.path.sep) + (os.path.altsep and dir_.count(os.path.altsep) or 0)

    base = source_directory
    if is_editable:
        filenames = locate_editable_egg_info(base)
    else:
        base = os.path.join(base, 'pip-egg-info')
        filenames = os.listdir(base)
    if not filenames:
        raise InstallationError('Files/directories not found in {}'.format(base))
    if len(filenames) > 1:
        filenames.sort(key=depth_of_directory)
    return os.path.join(base, filenames[0])


def generate_metadata(build_env, setup_py_path, source_dir, editable, isolated, details):
    """Generate metadata using setup.py-based defacto mechanisms.

    Returns the generated metadata directory.
    """
    logger.debug('Running setup.py (path:%s) egg_info for package %s', setup_py_path, details)
    egg_info_dir = None
    if not editable:
        egg_info_dir = os.path.join(source_dir, 'pip-egg-info')
        ensure_dir(egg_info_dir)
    args = make_setuptools_egg_info_args(setup_py_path,
      egg_info_dir=egg_info_dir,
      no_user_config=isolated)
    with build_env:
        call_subprocess(args,
          cwd=source_dir,
          command_desc='python setup.py egg_info')
    return _find_egg_info(source_dir, editable)
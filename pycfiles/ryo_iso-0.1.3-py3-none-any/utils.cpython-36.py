# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/src_import/ryo-iso/ryo_iso/utils.py
# Compiled at: 2019-11-12 05:13:56
# Size of source mod 2**32: 2860 bytes
import appdirs as _appdirs
from pathlib import Path as _Path
import importlib_resources as _resources, shutil as _shutil, time as _time, yaml as _yaml, sys as _sys, os as _os, re as _re
from loguru import logger as _logger
import requests as _requests, delegator as _delegator, subprocess as _subprocess

def cleanup_data():
    """
    Clean up build artifacts

    Removes ['./squashfs-root','./image','./build']

    .. warning:: Do not manually ``rm -rf squashfs-root`` if the chrooted devices are mounted
    """
    paths = [
     './squashfs-root', './image', './build']
    paths = map(_Path, paths)
    paths = filter(lambda path: path.exists(), paths)
    for path in paths:
        p = _subprocess.run(['sudo', 'rm', '--one-file-system', '--recursive', str(path)])
        if p.returncode != 0:
            _logger.debug('rm failed' + repr(p))
        else:
            _logger.debug('rm: %s' % str(path))
            _logger.debug(repr(p))


def umount_dev():
    """
    Unmount chrooted pseudo-filesystems

    umount ['proc/sys/fs/binfmt_misc', 'proc', 'sys', 'dev/pts', 'dev'] inside the chroot
    """
    _logger.info('Umounting chroot pseudo-filesystems')
    devices = [
     'proc/sys/fs/binfmt_misc', 'proc', 'sys', 'dev/pts', 'dev']
    devices = map(lambda device: 'squashfs-root/' + device, devices)
    mounted = list(filter(_os.path.ismount, devices))
    if len(mounted) == 0:
        _logger.debug('No pseudo-filesystems mounted in chroot')
    else:
        for device in mounted:
            p = _subprocess.run(['sudo', 'umount', device])
            if p.returncode != 0:
                _logger.debug('umount failed' + repr(p))
            else:
                _logger.debug('umount: %s' % device)


def profile_start():
    """
    Start pydoit profiler

    This `python-action <https://pydoit.org/tasks.html#python-action>`_
    returns a dictionary with the profiler start time, which is made
    available to other actions in the same Task instance

    Returns
    -------
    dict
        'start': start time of the profiler
    """
    return {'start': _time.time()}


def profile_stop(task, **kwargs):
    """
    Stop pydoit profiler

    This `python-action <https://pydoit.org/tasks.html#python-action>`_
    accesses the start time from the :func:`profile_start` action

    Parameters
    ----------
    task: dict
        Access to start time via pydoit Task instance
    **kwargs: dict
        Keyword argument access to start time

    Returns
    -------
    dict
        'duration': profiler duration
    """
    if 'start' in kwargs:
        duration = _time.time() - kwargs['start']
    else:
        duration = _time.time() - task.values['start']
    _logger.debug(task.name + ': ' + str(duration) + ' seconds')
    return {'duration': duration}
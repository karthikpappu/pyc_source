# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/dockerfabric/utils/output.py
# Compiled at: 2014-10-01 05:30:56
from __future__ import unicode_literals
from fabric import operations
from fabric.context_managers import hide
from fabric.utils import error

def stdout_result(cmd, expected_errors=(), shell=True, sudo=False, quiet=False):
    """
    Runs a command and returns the result, that would be written to `stdout`, as a string. The output itself can
    be suppressed.

    :param cmd: Command to run.
    :type cmd: unicode
    :param expected_errors: If the return code is non-zero, but found in this tuple, it will be ignored. ``None`` is
      returned in this case.
    :type expected_errors: tuple
    :param shell: Use a shell.
    :type shell: bool
    :param sudo: Use `sudo`.
    :type sudo: bool
    :param quiet: If set to ``True``, does not show any output.
    :type quiet: bool
    :return: The result of the command as would be written to `stdout`.
    :rtype: unicode
    """
    which = operations.sudo if sudo else operations.run
    with hide(b'warnings'):
        result = which(cmd, shell=shell, quiet=quiet, warn_only=True)
    if result.return_code == 0:
        return result
    else:
        if result.return_code not in expected_errors:
            error((b'Received unexpected error code {0} while executing!').format(result.return_code))
        return


def check_int(value):
    """
    Tests a given string for a possible conversion to integer. Uses Fabric's :func:`fabric.utils.error` instead of
    raising a :class:`TypeError`. ``None`` is not converted but returns ``None`` instead.

    :param value: Value to test for conversion.
    :type value: unicode
    :return: Integer value.
    :rtype: int
    """
    if value is not None:
        try:
            return int(value)
        except TypeError:
            error((b"Unexpected non-integer value '{0}'.").format(value))

    return


single_line = lambda val: val.split(b'\n')[0] if val is not None else None

def single_line_stdout(cmd, expected_errors=(), shell=True, sudo=False, quiet=False):
    """
    Runs a command and returns the first line of the result, that would be written to `stdout`, as a string.
    The output itself can be suppressed.

    :param cmd: Command to run.
    :type cmd: unicode
    :param expected_errors: If the return code is non-zero, but found in this tuple, it will be ignored. ``None`` is
      returned in this case.
    :type expected_errors: tuple
    :param shell: Use a shell.
    :type shell: bool
    :param sudo: Use `sudo`.
    :type sudo: bool
    :param quiet: If set to ``True``, does not show any output.
    :type quiet: bool
    :return: The result of the command as would be written to `stdout`.
    :rtype: unicode
    """
    return single_line(stdout_result(cmd, expected_errors, shell, sudo, quiet))
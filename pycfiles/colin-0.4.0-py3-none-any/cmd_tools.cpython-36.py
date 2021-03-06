# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/utils/cmd_tools.py
# Compiled at: 2018-09-21 02:53:51
# Size of source mod 2**32: 3260 bytes
import subprocess

def get_version_of_the_python_package(module):
    """
    Return the str containing the name version and package location.

    :param module: module to show info about
    :return: str 'name version path'
    """
    return '{} {} {}'.format(module.__name__, module.__version__, module.__path__[0])


def get_version_msg_from_the_cmd(package_name, cmd=None, use_rpm=None, max_lines_of_the_output=None):
    """
    Get str with the version (or string representation of the error).

    :param package_name: str
    :param cmd: str or [str] (defaults to [package_name, "--version"])
    :param use_rpm: True/False/None (whether to use rpm -q for getting a version)
    :param max_lines_of_the_output: use first n lines of the output
    :return: str
    """
    if use_rpm is None:
        use_rpm = is_rpm_installed()
    else:
        if use_rpm:
            rpm_version = get_rpm_version(package_name=package_name)
            if rpm_version:
                return '{} (rpm)'.format(rpm_version)
        try:
            cmd = cmd or [package_name, '--version']
            version_result = subprocess.run(cmd, stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
            if version_result.returncode == 0:
                version_output = version_result.stdout.decode().rstrip()
                if max_lines_of_the_output:
                    version_output = ' '.join(version_output.split('\n')[:max_lines_of_the_output])
                return version_output
            else:
                return '{}: cannot get version with {}'.format(package_name, cmd)
        except FileNotFoundError:
            return '{} not accessible!'.format(package_name)


def get_rpm_version(package_name):
    """Get a version of the package with 'rpm -q' command."""
    version_result = subprocess.run(['rpm', '-q', package_name], stdout=(subprocess.PIPE),
      stderr=(subprocess.PIPE))
    if version_result.returncode == 0:
        return version_result.stdout.decode().rstrip()
    else:
        return


def is_rpm_installed():
    """Tests if the rpm command is present."""
    try:
        version_result = subprocess.run(['rpm', '--usage'], stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        rpm_installed = not version_result.returncode
    except FileNotFoundError:
        rpm_installed = False

    return rpm_installed
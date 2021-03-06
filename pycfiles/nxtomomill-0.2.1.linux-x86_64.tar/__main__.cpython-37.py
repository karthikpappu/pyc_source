# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/payno/.local/share/virtualenvs/tomwer_venv/lib/python3.7/site-packages/nxtomomill/__main__.py
# Compiled at: 2020-04-08 08:00:12
# Size of source mod 2**32: 2793 bytes
"""This module describe nxtomomill applications which are available  through
the silx launcher.

Your environment should provide a command `nxtomomill`. You can reach help with
`tomwer --help`, and check the version with `nxtomomill --version`.
"""
__authors__ = [
 'V. Valls', 'P. Knobel', 'H. Payno']
__license__ = 'MIT'
__date__ = '04/01/2018'
import logging
logging.basicConfig()
import sys
from silx.utils.launcher import Launcher
import nxtomomill.version

def main():
    """Main function of the launcher

    This function is referenced in the setup.py file, to create a
    launcher script generated by setuptools.

    :rtype: int
    :returns: The execution status
    """
    _version = nxtomomill.version.version
    launcher = Launcher(prog='nxtomomill', version=_version)
    launcher.add_command('tomoedf2nx', module_name='nxtomomill.app.tomoedf2nx',
      description='convert some scan acquire with edf file format to nx compliant file format')
    launcher.add_command('tomoh52nx', module_name='nxtomomill.app.tomoh52nx',
      description='Compute center of rotation of a scan or between two projections')
    status = launcher.execute(sys.argv)
    return status


if __name__ == '__main__':
    status = main()
    sys.exit(status)
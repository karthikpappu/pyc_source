# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.5/site-packages/caritang/bootstrap.py
# Compiled at: 2010-04-24 16:44:56
"""
Created on 5 avr. 2010

@author: thierry
"""
from caritang.core import caritang
from optparse import OptionParser
from caritang.common import version
version.getInstance().submitRevision('$Revision: 109 $')

def showGui(login, password, folder, remove=False, flatten=False, verbose=False, *dirs):
    from caritang.gui.caritangGui import CaritangGui
    gui = CaritangGui()
    gui.run()


def backupDir(login, password, folder, remove, flatten, verbose, *dirs):
    """
    Backup one or more given directories
    """
    ccore = caritang.Caritang(login, password, folder, remove, flatten, verbose, *dirs)
    ccore.save()


def run():
    versionManager = version.getInstance()
    usage = '%prog -l <login> -p <pasword>  [-d <destination>] [-r] [-f] directory ...'
    str_version = '%prog ' + versionManager.getVersion() + '(' + versionManager.getRevision() + ')'
    parser = OptionParser(usage=usage, version=str_version)
    parser.add_option('-l', '--login', action='store', dest='login', help='the login of the user without the @gmail')
    parser.add_option('-p', '--password', action='store', dest='password', help='the password for the given login')
    parser.add_option('-d', '--destination', action='store', dest='folder', help='the remote folder or album name')
    parser.add_option('-r', '--remove', action='store_true', dest='remove', default=False, help='remove local file when uploaded')
    parser.add_option('-f', '--flatten', action='store_true', dest='flatten', default=False, help='subfolder are flattened to folder with name prefixed by given -d option value if any')
    parser.add_option('-v', '--verbose', action='store_true', dest='verbose', default=False, help='print verbose output of saving progress')
    parser.add_option('-g', '--gui', action='store_true', dest='gui', default=False, help='show the gui')
    (options, args) = parser.parse_args()
    if options.gui:
        showGui(options.login, options.password, options.folder, options.remove, options.flatten, options.verbose, *args)
    else:
        backupDir(options.login, options.password, options.folder, options.remove, options.flatten, options.verbose, *args)


if __name__ == '__main__':
    run()
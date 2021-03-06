# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\pycake\src\pycake\cli_utils.py
# Compiled at: 2018-11-08 01:02:06
import crayons

def format_help(help):
    """Formats the help string."""
    help = help.replace('Options:', str(crayons.white('Options:', bold=True)))
    help = help.replace('Usage: pycake', str(('Usage: {0}').format(crayons.white('pycake', bold=True))))
    help = help.replace('  prepare', str(crayons.green('  prepare', bold=True)))
    additional_help = ('\nUsage Examples:\n   Prepare the stuff for start new Python project\n   $ {0}\n\nCommands:').format(crayons.red('pycake prepare'))
    help = help.replace('Commands:', additional_help)
    return help
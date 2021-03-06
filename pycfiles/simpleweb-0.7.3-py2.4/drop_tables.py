# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simpleweb/admin/plugins/drop_tables.py
# Compiled at: 2007-01-10 11:34:47
import sys, simpleweb.utils

def drop_tables(name, args):
    """Usage: simpleweb-admin droptables

Drop all the tables defined in the models for a simpleweb project.
config.db_plugin has to be configured first.
"""
    if len(args) > 0:
        simpleweb.utils.msg_err("command '%s' takes no arguments" % name)
        sys.exit(0)
    try:
        sys.path.insert(0, '.')
        config = __import__('config')
        config.db_plugin.droptables()
    except ImportError, e:
        simpleweb.utils.msg_err('Could not successfully import config.py: %s' % e)
    except AttributeError:
        simpleweb.utils.msg_err('No db_plugin has been setup in config.py. Please do so first')
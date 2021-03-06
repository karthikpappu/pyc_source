# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/eventdaemon.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 462 bytes
"""Treadmill event daemon, subscribes to scheduler events."""
import click
from .. import eventmgr

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    def eventdaemon(approot):
        """Listens to Zookeeper events."""
        evmgr = eventmgr.EventMgr(root=approot)
        evmgr.run()

    return eventdaemon
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ngergo/Workspaces/Nordcloud/ratatoskr/ratatoskr/internal_logger.py
# Compiled at: 2019-03-20 06:58:46
# Size of source mod 2**32: 313 bytes
import logging
try:
    from logging import NullHandler
except ImportError:

    class NullHandler(logging.Handler):

        def emit(self, record):
            pass


LOG = logging.getLogger(__name__)
LOG.addHandler(NullHandler())
# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib64/python3.4/site-packages/PyIRC/extensions/isupport.py
# Compiled at: 2015-10-08 05:15:23
# Size of source mod 2**32: 3517 bytes
__doc__ = 'Enumeration of IRC server features and extensions.\n\nISUPPORT is a non-standard but widely supported IRC extension that is used to\nadvertise what a server supports to a client. Whilst non-standard, most\nservers follow a standard format for many parameters.\n\n'
from copy import deepcopy
from functools import lru_cache
from logging import getLogger
from PyIRC.signal import event
from PyIRC.auxparse import isupport_parse
from PyIRC.extensions import BaseExtension
from PyIRC.numerics import Numerics
_logger = getLogger(__name__)

class ISupport(BaseExtension):
    """ISupport"""
    defaults = {'PREFIX': [
                'o', 'v', '@', '+'], 
     'CHANTYPES': '#&!+', 
     'NICKLEN': '8', 
     'CASEMAPPING': 'RFC1459', 
     'CHANMODES': [
                   'b', 'k', 'l', 'imnstp']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base.isupport = self
        self.supported = deepcopy(self.defaults)

    @lru_cache(maxsize=16)
    def get(self, string):
        """Get an ISUPPORT string.

        Returns False if not found, True for keyless values, and the value
        for keyed values.

        The following values are guaranteed to be present:

        - CHANTYPES (value is a string)
        - PREFIX (value is of format "(modes)symbols for modes")
        - CASEMAPPING (ascii or rfc1459)
        - NICKLEN (value is a number, but stored as a string)
        - CHANMODES (list of values enumerating modes into four distinct
          classes, respectively: list modes, modes that send a parameter, modes
          that send a parameter only when set, and parameterless modes)

        :param string:
            ISUPPORT string to look up.

        """
        if string not in self.supported:
            return False
        value = self.supported[string]
        if value is None:
            return True
        return value

    @event('link', 'disconnected')
    def close(self, _):
        """Reset ISUPPORT state since we are disconnected."""
        self.supported.clear()

    @event('commands', Numerics.RPL_ISUPPORT)
    def isupport(self, _, line):
        """Handle ISUPPORT event."""
        if not line.params[(-1)].endswith('server'):
            _logger.warning('Really old IRC server detected!')
            _logger.warning("It's probably fine but things might break.")
            return
        values = isupport_parse(line.params[1:-1])
        if 'CASEMAPPING' in values:
            self.case_change()
        self.supported.update(values)
        self.get.cache_clear()
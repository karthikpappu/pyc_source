# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/x86_debug.py
# Compiled at: 2019-11-14 13:57:46
"""
Parsers for file ``/sys/kernel/debug/x86/*_enabled`` outputs
============================================================

This module provides the following parsers:

X86PTIEnabled - file ``/sys/kernel/debug/x86/pti_enabled``
----------------------------------------------------------

X86IBPBEnabled - file ``/sys/kernel/debug/x86/ibpb_enabled``
------------------------------------------------------------

X86IBRSEnabled - file ``/sys/kernel/debug/x86/ibrs_enabled``
------------------------------------------------------------

X86RETPEnabled - file ``/sys/kernel/debug/x86/retp_enabled``
------------------------------------------------------------

"""
from insights import parser
from insights import Parser
from insights.specs import Specs
from insights.parsers import SkipException

class X86DebugEnabled(Parser):
    """
    Class for parsing file ``/sys/kernel/debug/x86/*_enabled``

    Attributes:
        value (int): the result parsed of `/sys/kernel/debug/x86/*_enabled`

    Raises:
        SkipException: When input content is empty
    """

    def parse_content(self, content):
        if not content:
            raise SkipException('Input content is empty')
        self.value = int(content[0])


@parser(Specs.x86_ibpb_enabled)
class X86IBPBEnabled(X86DebugEnabled):
    """
    Class for parsing file ``/sys/kernel/debug/x86/ibpb_enabled``
    Typical output of file ``/sys/kernel/debug/x86/retp_enabled`` looks like::

        1

    Examples:
        >>> type(dva)
        <class 'insights.parsers.x86_debug.X86IBPBEnabled'>
        >>> dva.value
        1

    Attributes:
        value (int): the result parsed of '/sys/kernel/debug/x86/ibpb_enabled'

    Raises:
        SkipException: When input content is empty
    """
    pass


@parser(Specs.x86_ibrs_enabled)
class X86IBRSEnabled(X86DebugEnabled):
    """
    Class for parsing file ``/sys/kernel/debug/x86/ibrs_enabled``
    Typical output of file ``/sys/kernel/debug/x86/ibrs_enabled`` looks like::

        0

    Examples:
        >>> type(dl)
        <class 'insights.parsers.x86_debug.X86IBRSEnabled'>
        >>> dl.value
        1

    Attributes:
        value (int): the result parsed of '/sys/kernel/debug/x86/ibrs_enabled'

    Raises:
        SkipException: When input content is empty
    """
    pass


@parser(Specs.x86_pti_enabled)
class X86PTIEnabled(X86DebugEnabled):
    """
    Class for parsing file ``/sys/kernel/debug/x86/pti_enabled``
    Typical output of file ``/sys/kernel/debug/x86/pti_enabled`` looks like::

        0

    Examples:
        >>> type(dv)
        <class 'insights.parsers.x86_debug.X86PTIEnabled'>
        >>> dv.value
        1

    Attributes:
        value (int): the result parsed of '/sys/kernel/debug/x86/pti_enabled'

    Raises:
        SkipException: When input content is empty
    """
    pass


@parser(Specs.x86_retp_enabled)
class X86RETPEnabled(X86DebugEnabled):
    """
    Class for parsing file ``/sys/kernel/debug/x86/retp_enabled``
    Typical output of file ``/sys/kernel/debug/x86/retp_enabled`` looks like::

        1

    Examples:
        >>> type(dval)
        <class 'insights.parsers.x86_debug.X86RETPEnabled'>
        >>> dval.value
        1

    Attributes:
        value (int): the result parsed of '/sys/kernel/debug/x86/retp_enabled'

    Raises:
        SkipException: When input content is empty
    """
    pass
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/cpuset_cpus.py
# Compiled at: 2019-05-16 13:41:33
"""
CpuSetCpus - File ``/sys/fs/cgroup/cpuset/cpuset.cpus``
=======================================================

This parser reads the content of ``/sys/fs/cgroup/cpuset/cpuset.cpus``.
This file shows the default cgroup cpuset.cpu of system. The format
of the content is string including comma.
"""
from .. import parser, CommandParser
from insights.specs import Specs

@parser(Specs.cpuset_cpus)
class CpusetCpus(CommandParser):
    """
    Class ``CpusetCpus`` parses the content of the ``/sys/fs/cgroup/cpuset/cpuset.cpus``.

    Attributes:
        cpu_set (list): It is used to show the list of allowed cpu.

        cpu_number (int): It is used to display the number of allowed cpu.

    A small sample of the content of this file looks like::

        0,2-4,7

    Examples:
        >>> type(cpusetinfo)
        <class 'insights.parsers.cpuset_cpus.CpusetCpus'>
        >>> cpusetinfo.cpuset
        ["0", "2", "3", "4", "7"]
        >>> cpusetinfo.cpu_number
        5
    """

    def parse_content(self, content):
        self.cpu_set = []
        self.cpu_number = 0
        values = content[0].strip().split(',')
        for value in values:
            if '-' in value:
                start, end = value.split('-')
                self.cpu_set.extend([ str(i) for i in range(int(start), int(end) + 1) ])
            else:
                self.cpu_set.append(value)

        self.cpu_number = len(self.cpu_set)
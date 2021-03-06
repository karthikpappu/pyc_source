# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/ipaupgrade_log.py
# Compiled at: 2019-05-16 13:41:33
"""
IpaupgradeLog - file ``/var/log/ipaupgrade.log``
================================================

This file records the information of IPA server upgrade process while
executing command ``ipa-server-upgrade``
"""
from .. import LogFileOutput, parser
from insights.specs import Specs

@parser(Specs.ipaupgrade_log)
class IpaupgradeLog(LogFileOutput):
    """
    This parser is used to parse the content of file `/var/log/ipaupgrade.log`.

    .. note::
        Please refer to its super-class :class:`insights.core.LogFileOutput`

    Typical content of ``ipaupgrade.log`` file is::

        2017-08-07T07:36:50Z DEBUG Starting external process
        2017-08-07T07:36:50Z DEBUG args=/bin/systemctl is-active pki-tomcatd@pki-tomcat.service
        2017-08-07T07:36:50Z DEBUG Process finished, return code=0
        2017-08-07T07:36:50Z DEBUG stdout=active
        2017-08-07T07:41:50Z ERROR IPA server upgrade failed: Inspect /var/log/ipaupgrade.log and run command ipa-server-upgrade manually.

    Example:
        >>> ipaupgradelog = shared[IpaupgradeLog]
        >>> len(list(log.get('DEBUG')))
        4
        >>> from datetime import datetime
        >>> len(log.get_after(datetime(2017, 8, 7, 7, 37, 30)))
        1
    """
    time_format = '%Y-%m-%dT%H:%M:%SZ'
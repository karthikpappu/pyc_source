# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/xsser/XSSer/reporter.py
# Compiled at: 2013-12-09 06:41:17
"""
$Id$

This file is part of the xsser project, http://xsser.sourceforge.net.

Copyright (c) 2011/2012 psy <root@lordepsylon.net> - <epsylon@riseup.net>

xsser is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

xsser is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along
with xsser; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""

class XSSerReporter(object):

    def start_attack(self):
        pass

    def end_attack(self):
        pass

    def mosquito_crashed(self, dest_url, reason='unknown'):
        pass

    def report_state(self, state):
        pass

    def add_link(self, orig_url, dest_url):
        pass

    def report_error(self, error_msg):
        pass

    def start_token_check(self, dest_url):
        pass

    def start_crawl(self, dest_url):
        pass

    def post(self, msg):
        pass

    def token_arrived(self, token):
        pass

    def add_checked(self, dest_url):
        pass

    def add_success(self, dest_url):
        pass

    def add_failure(self, dest_url):
        pass
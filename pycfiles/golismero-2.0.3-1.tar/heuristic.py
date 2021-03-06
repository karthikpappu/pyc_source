# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/xsser/XSSer/fuzzing/heuristic.py
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
heuristic_test = [
 {'payload': 'XSS\\XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS/XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS>XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS<XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS;XSS', 'browser': '[Heuristic test]'},
 {'payload': "XSS'XSS", 'browser': '[Heuristic test]'},
 {'payload': 'XSS"XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS=XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%5CXSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%3EXSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%3CXSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%3BXSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%27XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%22XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS%3DXSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#92XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#47XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#62XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#60XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#59XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#39XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#34XSS', 'browser': '[Heuristic test]'},
 {'payload': 'XSS&#61XSS', 'browser': '[Heuristic test]'}]
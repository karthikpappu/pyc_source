# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: sqlalchemy_mate/pkg/prettytable/_compact.py
# Compiled at: 2019-04-26 17:27:18
import sys
py3k = sys.version_info[0] >= 3
if py3k:
    str_types = (
     str,)
    unicode_ = str
    basestring_ = str
    itermap = map
    iterzip = zip
    uni_chr = chr
    from html.parser import HTMLParser
    import io as StringIO
else:
    unicode_ = unicode
    basestring_ = basestring
    str_types = (unicode, str)
    import itertools
    itermap = itertools.imap
    iterzip = itertools.izip
    uni_chr = unichr
    from HTMLParser import HTMLParser
    import StringIO
(HTMLParser, StringIO)
if py3k and sys.version_info[1] >= 2:
    from html import escape
else:
    from cgi import escape
escape
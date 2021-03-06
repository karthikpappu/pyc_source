# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web/core/release.py
# Compiled at: 2016-09-25 02:31:52
# Size of source mod 2**32: 1190 bytes
"""Release information about WebCore."""
from __future__ import unicode_literals
import sys
from collections import namedtuple
version_info = namedtuple('version_info', ('major', 'minor', 'micro', 'releaselevel',
                                           'serial'))(2, 0, 3, 'final', 0)
version = '.'.join([str(i) for i in version_info[:3]]) + (version_info.releaselevel[0] + str(version_info.serial) if version_info.releaselevel != 'final' else '')
author = namedtuple('Author', ['name', 'email'])('Alice Bevan-McGregor', 'alice@gothcandy.com')
description = "A powerful web development nanoframework so small it's not even a microframework."
copyright = '2009-2016, Alice Bevan-McGregor and contributors'
url = 'https://github.com/marrow/WebCore/'
colophon = 'Powered by:\n\t<a class="noicon" href="http://www.python.org/" title="A programming language that lets you work more quickly and integrate your systems more effectively.">Python</a> <em class="version">{0.major}.{0.minor}</em>\n\tand <a class="noicon" href="{1}" title="A lightweight and extremely fast Python web framework.">WebCore</a> <em class="version">{2}</em>.'.format(sys.version_info, url, version)
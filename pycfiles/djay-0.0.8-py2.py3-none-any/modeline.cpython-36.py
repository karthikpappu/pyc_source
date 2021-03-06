# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/modeline.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1010 bytes
"""
    pygments.modeline
    ~~~~~~~~~~~~~~~~~

    A simple modeline parser (based on pymodeline).

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
__all__ = [
 'get_filetype_from_buffer']
modeline_re = re.compile('\n    (?: vi | vim | ex ) (?: [<=>]? \\d* )? :\n    .* (?: ft | filetype | syn | syntax ) = ( [^:\\s]+ )\n', re.VERBOSE)

def get_filetype_from_line(l):
    m = modeline_re.search(l)
    if m:
        return m.group(1)


def get_filetype_from_buffer(buf, max_lines=5):
    """
    Scan the buffer for modelines and return filetype if one is found.
    """
    lines = buf.splitlines()
    for l in lines[-1:-max_lines - 1:-1]:
        ret = get_filetype_from_line(l)
        if ret:
            return ret

    for i in range(max_lines, -1, -1):
        if i < len(lines):
            ret = get_filetype_from_line(lines[i])
            if ret:
                return ret
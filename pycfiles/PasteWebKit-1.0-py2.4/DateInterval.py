# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/DateInterval.py
# Compiled at: 2006-10-22 17:01:01
"""
DateInterval.py

Convert interval strings (in the form of 1w2d, etc) to
seconds, and back again.  Is not exactly about months or
years (leap years in particular).

Accepts (y)ear, (b)month, (w)eek, (d)ay, (h)our, (m)inute, (s)econd.

Exports only timeEncode and timeDecode functions.  
"""
import re
second = 1
minute = second * 60
hour = minute * 60
day = hour * 24
week = day * 7
month = day * 30
year = day * 365
timeValues = {'y': year, 'b': month, 'w': week, 'd': day, 'h': hour, 'm': minute, 's': second}
timeOrdered = timeValues.items()
timeOrdered.sort(lambda a, b: -cmp(a[1], b[1]))

def timeEncode(seconds):
    """Encodes a number of seconds (representing a time interval)
    into a form like 1h2d3s."""
    s = ''
    for (char, amount) in timeOrdered:
        if seconds >= amount:
            (i, seconds) = divmod(seconds, amount)
            s += '%i%s' % (i, char)

    return s


_timeRE = re.compile('[0-9]+[a-zA-Z]')

def timeDecode(s):
    """Decodes a number in the format 1h4d3m (1 hour, 3 days, 3 minutes)
    into a number of seconds"""
    time = 0
    for match in allMatches(s, _timeRE):
        char = match.group(0)[(-1)].lower()
        if not timeValues.has_key(char):
            continue
        time += int(match.group(0)[:-1]) * timeValues[char]

    return time


def allMatches(source, regex):
    """Return a list of matches for regex in source
    """
    pos = 0
    end = len(source)
    rv = []
    match = regex.search(source, pos)
    while match:
        rv.append(match)
        match = regex.search(source, match.end())

    return rv


__all__ = [
 timeEncode, timeDecode]
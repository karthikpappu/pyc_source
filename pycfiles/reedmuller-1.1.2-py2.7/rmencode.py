# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/reedmuller/rmencode.py
# Compiled at: 2018-05-19 10:35:14
"""rmencode.py

By Sebastian Raaphorst, 2012.

Simple command-line application for Reed-Muller encoding of one or more 0-1 strings."""
import sys, reedmuller
if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.stderr.write('Usage: %s r m word [word [...]]\n' % (sys.argv[0],))
        sys.exit(1)
    r, m = map(int, sys.argv[1:3])
    if m <= r:
        sys.stderr.write('We require r < m.\n')
        sys.exit(2)
    rm = reedmuller.ReedMuller(r, m)
    k = rm.message_length()
    for word in sys.argv[3:]:
        try:
            listword = list(map(int, word))
            if not set(listword).issubset([0, 1]) or len(listword) != k:
                sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (word, k))
            else:
                print ('').join(map(str, rm.encode(listword)))
        except:
            sys.stderr.write('FAIL: word %s is not a 0-1 string of length %d\n' % (word, k))
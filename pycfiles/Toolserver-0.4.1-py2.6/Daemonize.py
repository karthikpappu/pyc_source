# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Toolserver/Daemonize.py
# Compiled at: 2010-03-01 05:50:23
"""

Tool Server Framework - become a daemon

Copyright (c) 2002, Georg Bauer <gb@rfc1437.de>

Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the "Software"), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so, 
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
 
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import os, sys
if os.name == 'posix':

    def become_daemon(ourHomeDir='.', outLog='/dev/null', errLog='/dev/null'):
        """
                Robustly turn us into a UNIX daemon, running in ourHomeDir.
                Modelled after the original code of this module and some
                sample code from the net.
                """
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #1 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        os.setsid()
        os.chdir(ourHomeDir)
        os.umask(0)
        try:
            if os.fork() > 0:
                sys.exit(0)
        except OSError, e:
            sys.stderr.write('fork #2 failed: (%d) %s\n' % (e.errno, e.strerror))
            sys.exit(1)

        si = open('/dev/null', 'r')
        so = open(outLog, 'a+', 0)
        se = open(errLog, 'a+', 0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())


else:

    def become_daemon(ourHomeDir='.', outLog=None, errLog=None):
        """
                If we are not running under a POSIX system, just simulate
                the daemon mode by doing redirections and directory changeing
                """
        os.chdir(ourHomeDir)
        os.umask(0)
        sys.stdin.close()
        sys.stdout.close()
        sys.stderr.close()
        if errLog and outLog:
            sys.stderr = open(errLog, 'a', 0)
            sys.stdout = open(outLog, 'a', 0)
        elif errLog:
            sys.stderr = open(errLog, 'a', 0)
            sys.stdout = NullDevice()
        elif outLog:
            sys.stdout = open(outLog, 'a', 0)
            sys.stderr = NullDevice()
        else:
            sys.stdout = NullDevice()
            sys.stderr = NullDevice()


    class NullDevice:
        """
                A substitute for stdout and stderr that writes to nowhere.
                This is a substitute for /dev/null
                """

        def write(self, s):
            pass
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/at/tests.py
# Compiled at: 2009-08-27 19:43:20
import datetime, unittest
from at import *

class AtTest(unittest.TestCase):

    def test_parse_at_stderr(self):
        stderr = 'job 9 at Fri Aug 21 17:10:00 2009\n'
        job = parse_at_stderr(stderr)
        self.assertEquals(2, len(job))
        self.assertEquals(9, job['number'])
        self.assertEquals(datetime.datetime(2009, 8, 21, 17, 10), job['datetime'])

    def test_parse_atq_stdout_line(self):
        stdout_line = '9\tFri Aug 21 17:10:00 2009 a eddymul'
        job = parse_atq_stdout_line(stdout_line)
        self.assertEquals(4, len(job))
        self.assertEquals(9, job['number'])
        self.assertEquals(datetime.datetime(2009, 8, 21, 17, 10), job['datetime'])
        self.assertEquals('a', job['queue'])
        self.assertEquals('eddymul', job['username'])

    def test_parse_atq_stdout(self):
        stdout = ''
        self.assertEquals(0, len(parse_atq_stdout(stdout)))
        for stdout in [
         '9\tFri Aug 21 17:10:00 2009 a eddymul\n',
         '11\tMon Aug 24 15:05:00 2009 a eddymul\n10\tMon Aug 24 15:03:00 2009 a eddymul\n']:
            self.assertEquals(len(stdout.splitlines()), len(parse_atq_stdout(stdout)))

    def test_submit_at_job(self):
        control = len(atq())
        _datetime = datetime.datetime.now() + datetime.timedelta(1)
        job = at(_datetime=_datetime, popen_args=['whoami'])
        _atq = atq()
        self.assertEquals(control + 1, len(_atq))
        self.assert_(job in _atq)
        self.assertEquals(_datetime.replace(**REPLACE_KWARGS), job['datetime'])
        atrm([job])
        _atq = atq()
        self.assertEquals(control, len(_atq))
        self.assertFalse(job in _atq)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/Zpydoc/tests/runalltests.py
# Compiled at: 2011-09-28 02:31:46
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
import unittest
TestRunner = unittest.TextTestRunner
suite = unittest.TestSuite()
tests = os.listdir(os.curdir)
tests = [ n[:-3] for n in tests if n.startswith('test') if n.endswith('.py') ]
for test in tests:
    m = __import__(test)
    if hasattr(m, 'test_suite'):
        suite.addTest(m.test_suite())

if __name__ == '__main__':
    TestRunner().run(suite)
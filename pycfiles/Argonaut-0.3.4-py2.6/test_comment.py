# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/tests/functional/test_comment.py
# Compiled at: 2011-02-18 19:15:08
from argonaut.tests import *

class TestCommentController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='comment', action='index'))
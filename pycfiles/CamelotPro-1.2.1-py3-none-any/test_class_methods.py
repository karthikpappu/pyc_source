# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_orm/test_class_methods.py
# Compiled at: 2013-04-11 17:47:52
__doc__ = '\n    simple test case\n'
import threading
from . import TestMetaData
from camelot.core.orm import Field, Session
from sqlalchemy.types import String, Unicode, Integer

class TestClassMethods(TestMetaData):

    def test_get(self):

        class A(self.Entity):
            name = Field(String(32))

        self.create_all()
        with self.session.begin():
            a1 = A(name='a1')
        self.session.expire_all()
        self.assertEqual(A.get(1).name, 'a1')

    def test_query(self):
        from PyQt4 import QtCore

        class A(self.Entity):
            name = Field(String(32))

        self.create_all()
        with self.session.begin():
            a1 = A(name='a1')
        self.assertEqual(A.query.count(), 1)
        session_1 = A.query.session
        self.assertEqual(session_1, Session())

        class QueryThread(QtCore.QThread):

            def run(self):
                self.query_session_2 = A.query.session
                self.orm_session_2 = Session()

        thread = QueryThread()
        thread.start()
        thread.wait()
        self.assertNotEqual(session_1, thread.orm_session_2)
        self.assertNotEqual(session_1, thread.query_session_2)
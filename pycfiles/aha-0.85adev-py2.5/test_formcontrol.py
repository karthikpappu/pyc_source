# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/widget/tests/test_formcontrol.py
# Compiled at: 2010-10-20 22:45:01
from unittest import TestCase
import logging
log = logging.getLogger(__name__)
from nose.tools import *
from coregae.controller.formcontrol import *

def dummy():
    pass


def dummy2(*params, **kwd):
    return params


def dummy3(*params):
    return params + [1000]


class TestFormcontrol(TestCase):

    def test_01_instantiation(self):
        """
        Test for instantiation of FormControl class
        """
        f0 = FormControl()
        f1 = FormControl({FormControl.INITIAL: dummy, FormControl.FAILURE: (
                               dummy, dummy)})
        assert_equal(sorted(f1.get_states()), sorted([FormControl.INITIAL, FormControl.FAILURE]))
        f2 = FormControl({FormControl.INITIAL: dummy, FormControl.SUCCESS: dummy})
        assert_raises(KeyError, FormControl, {'foo': (1, 2), 'bar': 1})
        assert_raises(ValueError, FormControl, {'foo': (1, 2), FormControl.INITIAL: 1})
        assert_raises(ValueError, FormControl, {'foo': (dummy, 2), FormControl.INITIAL: 1})
        assert_raises(ValueError, FormControl, {'foo': (dummy, dummy), FormControl.INITIAL: 1})

    def test_02_utilities(self):
        """
        Test for utility methods, such as getting / checking state, etc.
        """
        f1 = FormControl({FormControl.INITIAL: dummy, FormControl.FAILURE: (
                               dummy2, dummy)})
        assert_equal(sorted(f1.get_states()), sorted([FormControl.INITIAL, FormControl.FAILURE]))
        assert_raises(KeyError, f1.check_state, 'foo')
        assert_equal(f1.get_validator(FormControl.FAILURE), dummy)
        assert_equal(f1.get_validator(FormControl.INITIAL), None)
        assert_equal(f1.get_processor(FormControl.INITIAL), dummy)
        assert_equal(f1.get_processor(FormControl.FAILURE), dummy2)
        f2 = FormControl({FormControl.INITIAL: dummy, FormControl.FAILURE: (
                               dummy, dummy2)})
        assert_equal(f2.validate(FormControl.FAILURE, range(10)), (
         range(10),))
        assert_equal(f2.validate(FormControl.INITIAL, range(10)), FormControl.INITIAL)
        f1.add_state(FormControl.SUCCESS, dummy)
        assert_equal(f1.get_processor(FormControl.SUCCESS), dummy)
        assert_equal(f1.get_validator(FormControl.SUCCESS), None)
        f1.add_method('foo', dummy)
        assert_equal(f1.get_processor('foo'), dummy)
        assert_equal(f1.get_validator('foo'), None)
        return

    def test_03_methoddecorator(self):
        """
        Test for method decorator
        """

        class TestClass(object):
            FC = FormControl()

            @handle_state(FC, FC.INITIAL)
            def method_1(self):
                return 'method_1'

            @validate(FC, FC.INITIAL)
            def method_2(self):
                return 'method_2'

        tc = TestClass()
        assert_equal(tc.FC.get_processor(tc.FC.INITIAL).__name__, tc.method_1.__name__)
        assert_equal(tc.FC.get_validator(tc.FC.INITIAL).__name__, tc.method_2.__name__)

    def test_03_methoddecorator2(self):
        """
        Test for method decorator
        """

        class TestClass(object):
            FC = FormControl()

            @handle_state(FC, (FC.INITIAL, FC.FAILURE))
            def method_1(self):
                return 'method_1'

            @validate(FC, (FC.INITIAL, FC.FAILURE))
            def method_2(self):
                return 'method_2'

        tc = TestClass()
        assert_equal(tc.FC.get_processor(tc.FC.INITIAL).__name__, tc.method_1.__name__)
        assert_equal(tc.FC.get_processor(tc.FC.FAILURE).__name__, tc.method_1.__name__)
        assert_equal(tc.FC.get_validator(tc.FC.INITIAL).__name__, tc.method_2.__name__)
        assert_equal(tc.FC.get_validator(tc.FC.FAILURE).__name__, tc.method_2.__name__)

    def test_04_methoddecorator2(self):
        """
        Test for method decorator
        """

        class TestClass(object):
            FC = FormControl()

            @FC.handle_state(FC.INITIAL, FC.FAILURE)
            def method_1(self):
                return 'method_1'

            @FC.handle_validate(FC.INITIAL, FC.FAILURE)
            def method_2(self):
                return 'method_2'

        tc = TestClass()
        assert_equal(tc.FC.get_processor(tc.FC.INITIAL).__name__, tc.method_1.__name__)
        assert_equal(tc.FC.get_processor(tc.FC.FAILURE).__name__, tc.method_1.__name__)
        assert_equal(tc.FC.get_validator(tc.FC.INITIAL).__name__, tc.method_2.__name__)
        assert_equal(tc.FC.get_validator(tc.FC.FAILURE).__name__, tc.method_2.__name__)
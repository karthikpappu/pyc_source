# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_basic.py
# Compiled at: 2013-09-21 05:43:10
from pyquchk import *
from pyquchk.arbitraries import *
from pytest import *

@qc
def test_out_of_class_definition(a=int_):
    assert type(a) == int


def test_unbounded_var():
    with raises(TypeError):

        @qc
        def unbounded_var(self, a=int_):
            pass


def test_unbounded_var_in_class():
    with raises(TypeError):

        class test_class:

            @qc
            def unbounded_var(self, a=int_):
                pass


class Test_spec_options:

    @qc
    def test_arb_noparam(a=int_, b=int_):
        assert type(a) == int
        assert type(b) == int
        assert a + b == b + a

    @qc
    def test_type_spec(a=int, b=int):
        assert type(a) == int
        assert type(b) == int
        assert a + b == b + a

    @qc
    def test_arb_withparam(a=int_(low=1000), b=int_(low=1073741824)):
        assert type(a) == int
        assert type(b) == int
        assert a >= 1000
        assert b >= 1073741824
        assert a + b == b + a


class Test_numbers:

    @qc
    def test_int_add_associativity(a=int, b=int, c=int):
        assert a + (b + c) == a + b + c


class Test_list:

    @qc
    def test_int_ops(lst=list_):
        if lst:
            avg_i = sum(lst) / len(lst)
            avg_f = 1.0 * sum(lst) / len(lst)
        assert len(lst) == 0 or len(set(lst)) == 1 and min(lst) == avg_i == max(lst) or min(lst) < avg_f < max(lst)

    @qc
    def test_shrink_props(lst=list_, n=int_(0, 5), m=int_(0, 5)):
        shrinked_n = list(list_(length=int_(n, n)).shrink(lst))
        assert all(len(l) == n for l in shrinked_n)
        shrinked_nm = list(list_(length=int_(n, m)).shrink(lst))
        assert all(n <= len(l) <= m for l in shrinked_nm)


@qc
def test_with_assume(x=list, y=list):
    assume(len(x) == len(y))
    assert len(x) == len(y)
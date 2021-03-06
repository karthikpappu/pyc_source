# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\assert_tests.py
# Compiled at: 2013-11-14 20:24:41
from pyinq.tags import *
from pyinq.asserts import *

@test
def test0():
    assert_true()


@test
def test1():
    assert_true(True)
    assert_true(False)
    assert_false(True)
    assert_false(False)
    assert_none(None)
    assert_none(8)
    assert_not_none(None)
    assert_not_none(8)
    assert_equal(4, 4)
    assert_equal(4, 5)
    return


@test
def test2():
    assert_true(True)
    assert_equal(4, 4)
    assert_false(False)
    assert_not_equal(4, 4)


@test
def test3():
    assert_true(True)
    assert_equal(4, 4)
    assert_equal(4, 5)
    assert_false(False)


@test
def test4():
    assert_true(True)
    assert_equal(8 + '')


@test
def test5():
    assert_equal(8 + '')


@test
def test6():
    assert 5 == 6


@test(expected=IOError)
def test7():
    raise IOError()


@test(expected=IOError)
def test8():
    pass


@test
def test9():
    assert_true('hello')


@test
def test10():
    assert_in(3, [1, 1, 2, 3, 5])
    assert_in(4, [1, 1, 2, 3, 5])


@test
def test11():
    assert_not_in(3, [1, 1, 2, 3, 5])
    assert_not_in(4, [1, 1, 2, 3, 5])


@test
def test12():
    eval_in(3, [1, 1, 2, 3, 5])
    eval_in(4, [1, 1, 2, 3, 5])
    eval_not_in(3, [1, 1, 2, 3, 5])
    eval_not_in(4, [1, 1, 2, 3, 5])


@test
def test13():
    eval_is_instance(IOError(), Exception)
    eval_is_instance(IOError(), WindowsError)
    eval_is_not_instance(IOError(), Exception)
    eval_is_not_instance(IOError(), WindowsError)


@test
def test14():
    assert_is_instance(IOError(), Exception)
    assert_is_not_instance(IOError(), WindowsError)


@test
def test15():
    assert_is_instance(IOError(), WindowsError)


@test
def test16():
    assert_is_not_instance(IOError(), Exception)


@test
def test17():
    assert_true(True)
    fail('Test failure')
    assert_true(False)


@test
def test18():
    assert_true(True)
    fail('Another test failure')


@test
def test19():
    assert_attrib(list, 'append')
    assert_not_attrib(list(), 'appends')


@test
def test20():
    assert_attrib(list(), 'appends')


@test
def test21():
    assert_not_attrib(list(), 'append')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsr/tests/test_number.py
# Compiled at: 2019-11-14 13:57:46
from insights.parsr import Number

def test_zero():
    assert Number('0') == 0.0


def test_positive_integer():
    assert Number('123') == 123.0


def test_negative_integer():
    assert Number('-123') == -123.0


def test_positive_float():
    assert Number('123.97') == 123.97


def test_negative_float():
    assert Number('-123.97') == -123.97
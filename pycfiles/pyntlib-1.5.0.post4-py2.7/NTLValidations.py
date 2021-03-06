# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/ntlib/NTLArchive/NTLValidations.py
# Compiled at: 2018-04-23 08:51:10
import inspect, sys
from .NTLExceptions import BoolError, ComplexError, DictError, DigitError, IntError, ListError, OEError, PCError, PNError, ZeroError, RealError, TupleError
from .NTLUtilities import jsbytes, jsstr
__all__ = [
 'int_check', 'real_check', 'complex_check', 'number_check',
 'str_check', 'basestring_check', 'bool_check', 'list_check', 'tuple_check', 'dict_check',
 'neg_check', 'pos_check', 'notneg_check', 'notpos_check', 'notzero_check',
 'odd_check', 'even_check', 'prime_check', 'composit_check']

def int_check(*args):
    from numbers import Integral
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, Integral):
            if sys.version_info[0] > 2:
                raise IntError('Function %s expected int, %s got instead.' % (
                 func, type(var).__name__))
            else:
                raise IntError('Function %s expected int or long, %s got instead.' % (
                 func, type(var).__name__))


def real_check(*args):
    from numbers import Real
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, Real):
            raise RealError('Function %s expected real number, %s got instead.' % (
             func, type(var).__name__))


def complex_check(*args):
    from numbers import Complex
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, Complex):
            raise ComplexError('Function %s expected complex number, %s got instead.' % (
             func, type(var).__name__))


def number_check(*args):
    from numbers import Number
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, Number):
            raise DigitError('Function %s expected number, %s got instead.' % (
             func, type(var).__name__))


def str_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, (jsbytes, jsstr)):
            raise StringError('Function %s expected str, %s got instead.' % (
             func, type(var).__name__))


def basestring_check(*args):
    func = inspect.stack()[2][3]
    if sys.version_info[0] > 2:
        for var in args:
            if not isinstance(var, str):
                raise StringError('Function %s expected str, %s got instead.' % (
                 func, type(var).__name__))

    else:
        for var in args:
            if not isinstance(var, basestring):
                raise StringError('Function %s expected basestring, %s got instead.' % (
                 func, type(var).__name__))


def bool_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, bool):
            raise BoolError('Function %s expected bool, %s got instead.' % (
             func, type(var).__name__))


def list_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, list):
            raise ListError('Function %s expected list, %s got instead.' % (
             func, type(var).__name__))


def dict_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, dict):
            raise DictError('Function %s expected dict, %s got instead.' % (
             func, type(var).__name__))


def tuple_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if not isinstance(var, tuple):
            raise TupleError('Function %s expected tuple, %s got instead.' % (
             func, type(var).__name__))


def neg_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var >= 0:
            raise PNError('Function %s expected negative, possitive got instead.' % func)


def pos_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var <= 0:
            raise PNError('Function %s expected positive, negative got instead.' % func)


def notneg_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var < 0:
            raise PNError('Function %s expected positive or zero, negative got instead.' % func)


def notpos_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var > 0:
            raise PNError('Function %s expected negative or zero, possitive got instead.' % func)


def notzero_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var == 0:
            raise ZeroError('Function %s expected non-zero, zero got instead.' % func)


def odd_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var % 2 == 0:
            raise OEError('Function %s expected odd, even got instead.' % func)


def even_check(*args):
    func = inspect.stack()[2][3]
    for var in args:
        if var % 2 == 1:
            raise OEError('Function %s expected even, odd got instead.' % func)


def prime_check(trust, *args):
    if trust:
        return
    from .NTLTrivialDivision import trivialDivision
    func = inspect.stack()[2][3]
    for var in args:
        if not trivialDivision(var):
            raise PCError('Function %s expected prime, composit got instead.' % func)


def composit_check(trust, *args):
    if trust:
        return
    from .NTLTrivialDivision import trivialDivision
    func = inspect.stack()[2][3]
    for var in args:
        if trivialDivision(var):
            raise PCError('Function %s expected composit, prime got instead.' % func)
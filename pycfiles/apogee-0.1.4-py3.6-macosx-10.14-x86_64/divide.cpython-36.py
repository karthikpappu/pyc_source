# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/apogee/factors/discrete/operations/divide.py
# Compiled at: 2019-06-15 16:42:10
# Size of source mod 2**32: 979 bytes
import numpy as np
from .arithmetic import factor_arithmetic

def factor_division(a, b):
    """
    Calculate the division of two factors. Currently aimed at discrete factors.

    Parameters
    ----------
    a: Factor-like
        A factor object.
    b: Factor-like
        A factor object.

    Returns
    -------
    scope: ndarray
        An array containing the scope of the resulting factor.
    card: ndarray
        An array containing the cardinality of the resulting factor.
    vals: ndarray
        An array containing the probability distribution of the resulting factor.

    Examples
    --------
    >>> a = Factor([0], [2], [0.1, 0.9])
    >>> b = Factor([1, 0], [2, 2], [[0.2, 0.8], [0.7, 0.3]])
    >>> c = Factor(*factor_division(a, b))  # generate new factor from factors a and b

    """
    return factor_arithmetic((
     a.scope, a.card, a.params, a.assignments), (
     a.scope, a.card, a.params, a.assignments), np.subtract)
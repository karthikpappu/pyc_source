# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pyhexad\renderer.py
# Compiled at: 2014-12-08 16:27:29
import logging
logger = logging.getLogger(__name__)
try:
    import win32com.client
except ImportError:
    logger.warning('*** win32com.client could not be imported          ***')
    logger.warning('*** some of the automation examples will not work  ***')
    logger.warning('*** to fix this, install the pywin32 extensions.   ***')

import numpy as np, pyxll

def xl_app():
    """returns a Dispatch object for the current Excel instance"""
    xl_window = pyxll.get_active_object()
    xl_app = win32com.client.Dispatch(xl_window).Application
    win32com.client.gencache.EnsureDispatch(xl_app)
    return xl_app


def draw(arr):
    """Renders a one- or twodimensional scalar array."""
    if not isinstance(arr, np.ndarray):
        raise TypeError('Numpy ndarray expected.')
    caller = pyxll.xlfCaller()
    address = caller.address

    def update_func(x):
        xl = xl_app()
        if xl is not None:
            range = xl.Range(address)
            y = None
            try:
                if x.ndim == 1:
                    range = xl.Range(range.Resize(2, 1), range.Resize(x.shape[0] + 1, 1))
                    y = np.reshape(x, (x.shape[0], 1))
                elif x.ndim == 2:
                    range = xl.Range(range.Resize(2, 1), range.Resize(x.shape[0] + 1, x.shape[1]))
                    y = x
                else:
                    raise ValueError('Array rank must be 1 or 2.')
                range.Value = y
            except Exception as ex:
                logger.info(ex)

        return

    pyxll.async_call(update_func, arr)


def draw_table(tbl):
    """
    Renders a table = list of rows = list of lists.

    We assume the CALLER did the proper type conversions!!!
    (We can handle strings, int32, and float64 colums.)
    """
    if not isinstance(tbl, list):
        raise TypeError('List expected.')
    caller = pyxll.xlfCaller()
    address = caller.address

    def update_func(x):
        xl = xl_app()
        if xl is not None:
            range = xl.Range(address)
            try:
                header = x[0]
                num_cols = len(header)
                num_rows = len(x)
                range = xl.Range(range.Resize(2, 1), range.Resize(num_rows + 1, num_cols))
                range.Value = x
            except Exception as ex:
                logger.info(ex)

        return

    pyxll.async_call(update_func, tbl)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/cumret.py
# Compiled at: 2016-11-29 01:45:48
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
from pyalgotrade import technical

class CumRetEventWindow(technical.EventWindow):

    def __init__(self):
        super(CumRetEventWindow, self).__init__(2)
        self.__prevCumRet = 0

    def getValue(self):
        ret = None
        if self.windowFull():
            values = self.getValues()
            prev = values[0]
            actual = values[1]
            netReturn = (actual - prev) / float(prev)
            ret = (1 + self.__prevCumRet) * (1 + netReturn) - 1
            self.__prevCumRet = ret
        return ret


class CumulativeReturn(technical.EventBasedFilter):
    """This filter calculates cumulative returns over another dataseries.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, maxLen=None):
        super(CumulativeReturn, self).__init__(dataSeries, CumRetEventWindow(), maxLen)
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/winkidney/.virtualenvs/huobi/lib/python2.7/site-packages/pyalgotrade/technical/linreg.py
# Compiled at: 2016-11-29 01:45:48
__doc__ = '\n.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>\n'
from pyalgotrade import technical
from pyalgotrade.utils import collections
from pyalgotrade.utils import dt
import numpy as np
from scipy import stats

def lsreg(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    res = stats.linregress(x, y)
    return (
     res[0], res[1])


class LeastSquaresRegressionWindow(technical.EventWindow):

    def __init__(self, windowSize):
        assert windowSize > 1
        super(LeastSquaresRegressionWindow, self).__init__(windowSize)
        self.__timestamps = collections.NumPyDeque(windowSize)

    def onNewValue(self, dateTime, value):
        technical.EventWindow.onNewValue(self, dateTime, value)
        if value is not None:
            timestamp = dt.datetime_to_timestamp(dateTime)
            assert len(self.__timestamps) and timestamp > self.__timestamps[(-1)]
            self.__timestamps.append(timestamp)
        return

    def __getValueAtImpl(self, timestamp):
        ret = None
        if self.windowFull():
            a, b = lsreg(self.__timestamps.data(), self.getValues())
            ret = a * timestamp + b
        return ret

    def getTimeStamps(self):
        return self.__timestamps

    def getValueAt(self, dateTime):
        return self.__getValueAtImpl(dt.datetime_to_timestamp(dateTime))

    def getValue(self):
        ret = None
        if self.windowFull():
            ret = self.__getValueAtImpl(self.__timestamps.data()[(-1)])
        return ret


class LeastSquaresRegression(technical.EventBasedFilter):
    """Calculates values based on a least-squares regression.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param windowSize: The number of values to use to calculate the regression.
    :type windowSize: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.
    """

    def __init__(self, dataSeries, windowSize, maxLen=None):
        super(LeastSquaresRegression, self).__init__(dataSeries, LeastSquaresRegressionWindow(windowSize), maxLen)

    def getValueAt(self, dateTime):
        """Calculates the value at a given time based on the regression line.

        :param dateTime: The datetime to calculate the value at.
            Will return None if there are not enough values in the underlying DataSeries.
        :type dateTime: :class:`datetime.datetime`.
        """
        return self.getEventWindow().getValueAt(dateTime)


class SlopeEventWindow(technical.EventWindow):

    def __init__(self, windowSize):
        super(SlopeEventWindow, self).__init__(windowSize)
        self.__x = np.asarray(range(windowSize))

    def getValue(self):
        ret = None
        if self.windowFull():
            y = self.getValues()
            ret = lsreg(self.__x, y)[0]
        return ret


class Slope(technical.EventBasedFilter):
    """The Slope filter calculates the slope of a least-squares regression line.

    :param dataSeries: The DataSeries instance being filtered.
    :type dataSeries: :class:`pyalgotrade.dataseries.DataSeries`.
    :param period: The number of values to use to calculate the slope.
    :type period: int.
    :param maxLen: The maximum number of values to hold.
        Once a bounded length is full, when new items are added, a corresponding number of items are discarded from the
        opposite end. If None then dataseries.DEFAULT_MAX_LEN is used.
    :type maxLen: int.

    .. note::
        This filter ignores the time elapsed between the different values.
    """

    def __init__(self, dataSeries, period, maxLen=None):
        super(Slope, self).__init__(dataSeries, SlopeEventWindow(period), maxLen)


class TrendEventWindow(SlopeEventWindow):

    def __init__(self, windowSize, positiveThreshold, negativeThreshold):
        if negativeThreshold > positiveThreshold:
            raise Exception('Invalid thresholds')
        super(TrendEventWindow, self).__init__(windowSize)
        self.__positiveThreshold = positiveThreshold
        self.__negativeThreshold = negativeThreshold

    def getValue(self):
        ret = super(TrendEventWindow, self).getValue()
        if ret is not None:
            if ret > self.__positiveThreshold:
                ret = True
            elif ret < self.__negativeThreshold:
                ret = False
            else:
                ret = None
        return ret


class Trend(technical.EventBasedFilter):

    def __init__(self, dataSeries, trendDays, positiveThreshold=0, negativeThreshold=0, maxLen=None):
        super(Trend, self).__init__(dataSeries, TrendEventWindow(trendDays, positiveThreshold, negativeThreshold), maxLen)
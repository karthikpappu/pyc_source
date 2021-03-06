# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Library/Python/2.7/site-packages/pycast/errors/symmetricmeanabsolutepercentageerror.py
# Compiled at: 2015-05-28 03:51:42
from pycast.errors import BaseErrorMeasure

class SymmetricMeanAbsolutePercentageError(BaseErrorMeasure):
    """Implements the symmetric mean absolute percentage error whose values are
    between 0 and 200%.

    Explanation:
    http://www.stat.iastate.edu/preprint/articles/2004-10.pdf (page 14)

    If the calculated value and the original value are equal, the error is 0.
    """

    def _calculate(self, startingPercentage, endPercentage, startDate, endDate):
        """This is the error calculation function that gets called by :py:meth:`BaseErrorMeasure.get_error`.

        Both parameters will be correct at this time.

        :param float startingPercentage: Defines the start of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, where the error calculation should be started. 
            25.0 for example means that the first 25% of all calculated errors will be ignored.
        :param float endPercentage:    Defines the end of the interval. This has to be a value in [0.0, 100.0].
            It represents the value, after which all error values will be ignored. 90.0 for example means that
            the last 10% of all local errors will be ignored.
        :param float startDate: Epoch representing the start date used for error calculation.
        :param float endDate: Epoch representing the end date used in the error calculation.

        :return:    Returns a float representing the error.
        :rtype: float
        """
        errorValues = self._get_error_values(startingPercentage, endPercentage, startDate, endDate)
        return float(sum(errorValues)) / float(len(errorValues))

    def local_error(self, originalValue, calculatedValue):
        """Calculates the error between the two given values.

        :param list originalValue:    List containing the values of the original data.
        :param list calculatedValue:    List containing the values of the calculated TimeSeries that
            corresponds to originalValue.

        :return:    Returns the error measure of the two given values.
        :rtype:     numeric
        """
        originalValue = originalValue[0]
        calculatedValue = calculatedValue[0]
        if not originalValue and not calculatedValue:
            return 0.0
        return abs(calculatedValue - originalValue) / ((abs(originalValue) + abs(calculatedValue)) / 2) * 100


SMAPE = SymmetricMeanAbsolutePercentageError
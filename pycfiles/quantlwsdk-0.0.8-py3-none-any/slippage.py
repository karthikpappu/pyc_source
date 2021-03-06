# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\indicatorModule\pyalgotrade\broker\slippage.py
# Compiled at: 2018-10-21 21:07:45
"""
.. moduleauthor:: Gabriel Martin Becedillas Ruiz <gabriel.becedillas@gmail.com>
"""
import abc, six

@six.add_metaclass(abc.ABCMeta)
class SlippageModel(object):
    """Base class for slippage models.

    .. note::
        This is a base class and should not be used directly.
    """

    @abc.abstractmethod
    def calculatePrice(self, order, price, quantity, bar, volumeUsed):
        """
        Returns the slipped price per share for an order.

        :param order: The order being filled.
        :type order: :class:`pyalgotrade.broker.Order`.
        :param price: The price for each share before slippage.
        :type price: float.
        :param quantity: The amount of shares that will get filled at this time for this order.
        :type quantity: float.
        :param bar: The current bar.
        :type bar: :class:`pyalgotrade.bar.Bar`.
        :param volumeUsed: The volume size that was taken so far from the current bar.
        :type volumeUsed: float.
        :rtype: float.
        """
        raise NotImplementedError()


class NoSlippage(SlippageModel):
    """A no slippage model."""

    def calculatePrice(self, order, price, quantity, bar, volumeUsed):
        return price


class VolumeShareSlippage(SlippageModel):
    """
    A volume share slippage model as defined in Zipline's VolumeShareSlippage model.
    The slippage is calculated by multiplying the price impact constant by the square of the ratio of the order
    to the total volume.

    Check https://www.quantopian.com/help#ide-slippage for more details.

    :param priceImpact: Defines how large of an impact your order will have on the backtester's price calculation.
    :type priceImpact: float.
    """

    def __init__(self, priceImpact=0.1):
        super(VolumeShareSlippage, self).__init__()
        self.__priceImpact = priceImpact

    def calculatePrice(self, order, price, quantity, bar, volumeUsed):
        assert bar.getVolume(), "Can't use 0 volume bars with VolumeShareSlippage"
        totalVolume = volumeUsed + quantity
        volumeShare = totalVolume / float(bar.getVolume())
        impactPct = volumeShare ** 2 * self.__priceImpact
        if order.isBuy():
            ret = price * (1 + impactPct)
        else:
            ret = price * (1 - impactPct)
        return ret
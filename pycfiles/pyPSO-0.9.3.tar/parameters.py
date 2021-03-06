# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dswistowski/pso/pypso/src/pypso/parameters.py
# Compiled at: 2007-07-01 05:34:22
"""Moduł zawiera klase paramety, umiżliwiająco posiadanie przez iine obiekrty typu funkcja, strategia parametrów. Te parametry mogą być stałe, lub zmieniane w czasie działania algorytmu"""

class _parametr(object):
    """
    Pojedyńczy parametr.
    """

    def __init__(self, parameters, name, default=0, min=-1, max=1, digits=0, documentation=''):
        self._parameters = parameters
        self._name = name
        (self._value, self._min, self._max, self._digits) = (default, min, max, digits)
        self.__doc__ = documentation

    def _setValue(self, value):
        self._value = min(max(value, self._min), self._max)
        self._parameters.parameter_set(self._name, self._value)

    def _setFloatValue(self, value):
        self._setValue(value * 10 ** self._digits)

    def _getValue(self):
        return self._value

    def _getMin(self):
        return self._min

    def _getMax(self):
        return self._max

    def _getDigits(self):
        return self._digits

    def _getFloatValue(self):
        return float(self._value) / 10 ** self._digits

    value = property(_getValue, _setValue, doc='Wartość argumentu')
    floatValue = property(_getFloatValue, _setFloatValue, doc='Wartość argumentu z uwzględnieniej przecinka')
    min = property(_getMin, doc='Wartość minimalna')
    floatMin = property(lambda self: float(self._min) / 10 ** self._digits, doc='Wartość minimalna z uwzględnieniem przecinka')
    floatMax = property(lambda self: float(self._max) / 10 ** self._digits, doc='Wartość maksymalna z uwzględnieniem przecinka')
    max = property(_getMax, doc='Wartość maksymalna')
    digits = property(_getDigits, doc='Liczba miejsc po przecinku')

    def __repr__(self):
        return str(self.value)


class Parameters(object):
    """
    Klasa reprezentująca parametry funkcji, lub strategi.
    Klasa, która ma posiadać parametry powinna mieć stałe pole o nazwie __parameters__ będące kolekcją krotek: (wartość_domyslna, min, max).
    """

    def __init__(self, parameters=None):
        if parameters != None:
            self.__parameters__ = parameters
        self._parameters = {}
        self.onUpdate = None
        for prop in self.__parameters__:
            self._parameters[prop] = _parametr(self, prop, *self.__parameters__[prop])

        return

    def add_parameter(self, name, default, min, max, digits=0, doc=''):
        self._parameters[name] = _parametr(self, name, default, min, max, digits, doc)

    def __getitem__(self, key):
        return self._parameters[key].value

    def __setitem__(self, parm, val):
        self._parameters[parm].value = val
        self.parameter_set(parm, val)

    def parm(self, name):
        u"""zwraca prawdziwą wartość parametru"""
        return self._parameters[name].floatValue

    def parameter_set(self, name, value):
        u"""Ustawienie parametrowi o nazwie name wartości value"""
        pass

    def parameters(self):
        u"""Zwraca słownik z parametrami"""
        return self._parameters


if __name__ == '__main__':
    p = Parameters({'a': (3, -4, 5)})
    print p['a']
    p['a'] = 2000
    print p['a']
    print p.parameters()['a'].min
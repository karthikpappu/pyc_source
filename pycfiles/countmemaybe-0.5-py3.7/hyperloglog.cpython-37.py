# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/countmemaybe/hyperloglog.py
# Compiled at: 2019-12-09 06:49:34
# Size of source mod 2**32: 3100 bytes
"""
This is a small implemintation of the hyper loglog algorithm for distinct
value estimation using the alorithm descibed in [1].  Benchmarks on 1.8 GHz
core i7 Macbook air yields 3.74 us per insertion and a relative error of
~1.34% for 160000 16bit integers using b=8 and 32bit murmur hash.

micha gorelick, mynameisfiber@gmail.com
http://micha.gd/

[1]: http://algo.inria.fr/flajolet/Publications/FlFuGaMe07.pdf
"""
import math, mmh3
from .base_dve import BaseDVE

class InvalidParameters(Exception):
    pass


class HyperLogLog(BaseDVE):

    def __init__(self, items=[], b=4, hasher=mmh3.hash):
        if not 4 <= b <= 16:
            raise InvalidParameters()
        else:
            self.b = b
            self.m = 2 ** b
            self.M = [0] * self.m
            self.hasher = hasher
            self._width = 31 - self.b
            if self.m >= 128:
                self.alpha = 0.7213 / (1.0 + 1.079 / self.m)
            else:
                if self.m == 64:
                    self.alpha = 0.709
                else:
                    if self.m == 32:
                        self.alpha = 0.697
                    else:
                        if self.m == 16:
                            self.alpha = 0.673
        self.update(items)

    def _hash(self, item):
        return self.hasher(str(item))

    def rho(self, x, width=0):
        mask = 1 << width - 1
        i = 1
        while x & mask == 0 and mask > 0:
            mask >>= 1
            i += 1

        return i

    def add(self, item):
        x = self._hash(item)
        j = x >> self._width
        w = x ^ j << self._width
        self.M[j] = max(self.M[j], self.rho(w, width=(self._width)))

    def _indicator(self, M):
        return 1.0 / sum((2 ** (-m) for m in M))

    def union(self, other):
        assert self.m == other.m
        assert self.hasher == other.hasher
        assert self._width == other._width
        for i in range(self.m):
            self.M[i] = max(self.M[i], other.M[i])

    def cardinality(self):
        return self._card_helper(self.M, self.m, self.alpha)

    def cardinality_union(self, other):
        assert self.m == other.m
        assert self.hasher == other.hasher
        assert self._width == other._width
        M = [max(self.M[i], other.M[i]) for i in range(self.m)]
        return self._card_helper(M, self.m, self.alpha)

    def cardinality_intersection(self, other):
        A = self.cardinality()
        B = other.cardinality()
        AuB = self.cardinality_union(other)
        return A + B - AuB

    def jaccard(self, other):
        A = self.cardinality()
        B = other.cardinality()
        AuB = self.cardinality_union(other)
        return (A + B) / AuB - 1

    def _card_helper(self, M, m, alpha):
        E = alpha * m * m * self._indicator(M)
        if E <= 2.5 * m:
            V = M.count(0)
            if V != 0:
                Estar = m * math.log(m / (1.0 * V), 2)
            else:
                Estar = E
        elif E <= 143165576.53333333:
            Estar = E
        else:
            Estar = -4294967296 * math.log(1 - E / 4294967296, 2)
        return Estar

    def relative_error(self):
        return 1.04 / math.sqrt(self.m)
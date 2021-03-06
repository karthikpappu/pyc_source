# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/datando/jd.py
# Compiled at: 2013-03-13 10:29:38
import re
from datando.kernel import *

class JDDateTime(CalendarBase):
    __SECS_PER_DAY = 86400
    __MICROSECS_PER_DAY = 86400000000.0
    __JD_DIFFERENCE = 148731163200

    def __init__(self, day=0, fraction=0):
        self.day = day
        self.fraction = fraction

    def __str__(self):
        return ('JD \\ {0}.{1:020}').format(self.day, self.fraction)

    def to_LPDateTime(self):
        secs = self.day * self.__SECS_PER_DAY
        microsecs = int(self.fraction * (self.__MICROSECS_PER_DAY / 1000000000000000000000))
        secs += microsecs / 1000000
        microsecs = microsecs % 1000000
        positive = self.day >= 0
        lpd1 = LPDateTime(positive, secs, microsecs)
        return lpd1 - LPDateTime(True, self.__JD_DIFFERENCE, 0)

    @classmethod
    def from_LPDateTime(cls, lp_datetime):
        lp2 = lp_datetime + LPDateTime(True, cls.__JD_DIFFERENCE, 0)
        day = lp2.second / cls.__SECS_PER_DAY
        if not lp2.positive:
            day = -day
        float_fraction = lp2.second % cls.__SECS_PER_DAY / float(86400.0) + lp2.microsecond / cls.__MICROSECS_PER_DAY
        fraction = int(float_fraction * 1000000000000000000000)
        return JDDateTime(day, fraction)

    @classmethod
    def parse(cls, date_string):
        reg_expr = '^JD \\\\ (?P<sign>\\+|\\-){0,1}(?P<day>\\d+).(?P<fraction>\\d{1,20})$'
        m = re.match(reg_expr, date_string)
        if m:
            gd = m.groupdict()
            day = int(gd['day'])
            fraction = int(gd['fraction'])
            len_fr = len(gd['fraction'])
            if len_fr < 20:
                fraction = fraction * 10 ** (20 - len_fr)
            if gd['sign'] == '-':
                day = -day
            return JDDateTime(day, fraction)
        else:
            return
            return

    @staticmethod
    def get_prefix():
        return 'JD \\'
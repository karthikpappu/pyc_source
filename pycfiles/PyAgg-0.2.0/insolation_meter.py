# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/solutions/insolation_meter.py
# Compiled at: 2014-10-18 19:15:55


class StaticInsolation(object):

    def __init__(self, surface_insolation=1, insolation_factor=0.1):
        super(StaticInsolation, self).__init__()
        self.surface_insolation = surface_insolation
        self.insolation_factor = insolation_factor

    def get_insolation(self, cell, step=0):
        depth = getattr(cell, 'depth', 0)
        return max(0, self.surface_insolation - depth * self.insolation_factor)


class DynamicInsolation(object):

    def __init__(self, seasons):
        super(DynamicInsolation, self).__init__()
        self.seasons = seasons

    def get_insolation(self, cell, step=0):
        depth = getattr(cell, 'depth', 0)
        step = step % sum(season[0] for season in self.seasons)
        if step == 0:
            season = self.seasons[(-1)]
        else:
            s = 0
            while step > self.seasons[s][0]:
                step -= self.seasons[s][0]
                s += 1

            season = self.seasons[s]
        return max(0, season[1] - depth * season[2])
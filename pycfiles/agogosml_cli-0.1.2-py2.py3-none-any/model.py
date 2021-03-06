# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/agn_periodics/model.py
# Compiled at: 2014-11-11 16:17:44
__author__ = 'yarnaid'
from agn_periodics import utils
import numpy
from scipy import interpolate
conf = utils.load_config()
default_params = dict()
load_params = default_params
dump_params = default_params

class AbstractData(object):
    time_var = None
    values = None
    errors = None
    n = None
    __interpolated__ = False

    def __init__(self, file_name=None, **kwargs):
        self.load(file_name, **kwargs)

    def load(self, file_name, **args):
        print self.__name__ + ' load method stub'

    def dump(self, file_name):
        print self.__name__ + ' dump method stub'

    def __interpolate__(self):
        if self.__interpolated__:
            return
        else:
            x = self.time_var
            y = self.values
            self.n = self.n * 10
            tck = interpolate.splrep(x, y)
            x_new = numpy.linspace(min(x), max(x), self.n)
            y_new = interpolate.splev(x_new, tck)
            self.time_var = x_new
            self.values = y_new
            if self.errors is not None:
                err = self.errors
                tck = interpolate.splrep(x, err)
                err_new = interpolate.splev(x_new, tck)
                self.errors = err_new
            self.__interpolated__ = True
            return


class TimeRow(AbstractData):
    X_q = None

    def load(self, file_name=None, row=None, time=None, errors=None):
        if file_name is not None:
            self.load_file(file_name)
        elif row is not None and time is not None:
            self.load_arrays(row, time, errors)
        else:
            raise 'Cannot load data'
        self.__interpolate__()
        return

    def load_file(self, file_name):
        self.raw_data = numpy.loadtxt(file_name, **load_params)
        self.time_var = self.raw_data[:, 0] + self.raw_data[:, 1] / 12.0
        self.values = self.raw_data[:, 4]
        self.n = len(self.time_var)

    def load_arrays(self, row, time, errors=None):
        if len(row) != len(time):
            raise ValueError('row and time must have the same length')
        self.raw_data = numpy.asarray(row)
        self.time_var = numpy.asarray(time)
        self.values = numpy.asarray(row)
        if errors is not None:
            self.errors = numpy.asarray(errors)
        self.n = len(self.time_var)
        return

    def __str__(self):
        res = str()
        if self.errors is not None:
            get_line = lambda i: str(self.time_var[i]) + ' ' + str(self.values[i]) + ' ' + str(self.errors[i]) + '\n'
        else:
            get_line = lambda i: str(self.time_var[i]) + ' ' + str(self.values[i]) + '\n'
        for i in xrange(self.n):
            res += get_line(i)

        return res
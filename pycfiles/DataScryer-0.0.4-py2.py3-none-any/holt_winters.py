# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\default_methods\holt_winters.py
# Compiled at: 2016-09-02 08:17:33
from __future__ import division
import logging, math, numpy, scipy.optimize
from datascryer.methods.abc_forecast import ForecastMethod

class ZeroException(Exception):
    pass


class HoltWinters(ForecastMethod):
    """
    Based on: https://gist.github.com/andrequeiroz/5888967
    """

    def _rmse_linear(self, params, *args):
        Y, alpha, beta, rmse = self.linear(args[0], 0, *params)
        return rmse

    def _rmse_additive(self, params, *args):
        Y, alpha, beta, gamma, rmse = self.additive(args[0], args[1], 0, *params)
        return rmse

    def _rmse_multiplicative(self, params, *args):
        Y, alpha, beta, gamma, rmse = self.multiplicative(args[0], args[1], 0, *params)
        return rmse

    def _rmse_damped(self, params, *args):
        Y, alpha, beta, gamma, rmse, phi = self.damped(args[0], args[1], 0, *params)
        return rmse

    @staticmethod
    def _calc_rmse(Y, y, fc):
        if fc > 0:
            return math.sqrt(sum([ (m - n) ** 2 for m, n in zip(Y[:-fc], y[:-fc - 1]) ]) / len(Y[:-fc]))
        else:
            return math.sqrt(sum([ (m - n) ** 2 for m, n in zip(Y, y[:-1]) ]) / len(Y))

    @staticmethod
    def _bfgs(y, m, f):
        return scipy.optimize.fmin_l_bfgs_b(func=f, args=(
         y, m), x0=numpy.array([0.5, 0.5, 0.5]), bounds=[
         (0, 1), (0, 1), (0, 1)], approx_grad=True, maxiter=100, maxfun=100)[0]

    def linear(self, x, fc, alpha=None, beta=None):
        Y = x[:]
        if alpha is None or beta is None:
            alpha, beta = scipy.optimize.fmin_l_bfgs_b(func=self._rmse_linear, args=(
             Y,), x0=numpy.array([0.5, 0.5]), bounds=[
             (0, 1), (0, 1)], approx_grad=True)[0]
        a = [
         Y[0]]
        b = [Y[1] - Y[0]]
        y = [a[0] + b[0]]
        for i in range(len(Y) + fc):
            if i == len(Y):
                Y.append(a[(-1)] + b[(-1)])
            a.append(alpha * Y[i] + (1 - alpha) * (a[i] + b[i]))
            b.append(beta * (a[(i + 1)] - a[i]) + (1 - beta) * b[i])
            y.append(a[(i + 1)] + b[(i + 1)])

        return (Y[-fc:], alpha, beta, self._calc_rmse(Y, y, fc))

    def additive(self, x, m, fc, alpha=None, beta=None, gamma=None):
        Y = x[:]
        m = int(m)
        if alpha is None or beta is None or gamma is None:
            alpha, beta, gamma = self._bfgs(Y, m, self._rmse_additive)
        a = [sum(Y[0:m]) / float(m)]
        b = [(sum(Y[m:2 * m]) - sum(Y[0:m])) / m ** 2]
        s = [ Y[i] - a[0] for i in range(m) ]
        y = [a[0] + b[0] + s[0]]
        for i in range(len(Y) + fc):
            if i == len(Y):
                Y.append(a[(-1)] + b[(-1)] + s[(-m)])
            a.append(alpha * (Y[i] - s[i]) + (1 - alpha) * (a[i] + b[i]))
            b.append(beta * (a[(i + 1)] - a[i]) + (1 - beta) * b[i])
            s.append(gamma * (Y[i] - a[i] - b[i]) + (1 - gamma) * s[i])
            y.append(a[(i + 1)] + b[(i + 1)] + s[(i + 1)])

        return (Y[-fc:], alpha, beta, gamma, self._calc_rmse(Y, y, fc))

    def multiplicative(self, x, m, fc, alpha=None, beta=None, gamma=None):
        if 0 in x:
            raise ZeroException('Series contains zeros which is not allowed for multiplicative')
        Y = x[:]
        if alpha is None or beta is None or gamma is None:
            alpha, beta, gamma = self._bfgs(Y, m, self._rmse_multiplicative)
        a = [sum(Y[0:m]) / float(m)]
        b = [(sum(Y[m:2 * m]) - sum(Y[0:m])) / m ** 2]
        s = [ Y[i] / a[0] for i in range(m) ]
        y = [(a[0] + b[0]) * s[0]]
        for i in range(len(Y) + fc):
            if i == len(Y):
                Y.append((a[(-1)] + b[(-1)]) * s[(-m)])
            a.append(alpha * (Y[i] / s[i]) + (1 - alpha) * (a[i] + b[i]))
            b.append(beta * (a[(i + 1)] - a[i]) + (1 - beta) * b[i])
            s.append(gamma * (Y[i] / (a[i] + b[i])) + (1 - gamma) * s[i])
            y.append((a[(i + 1)] + b[(i + 1)]) * s[(i + 1)])

        return (Y[-fc:], alpha, beta, gamma, self._calc_rmse(Y, y, fc))

    def damped(self, x, m, fc, alpha=None, beta=None, gamma=None, phi=None):
        if 0 in x:
            raise ZeroException('Series contains zeros which is not allowed for multiplicative')
        Y = x[:]
        if alpha is None or beta is None or gamma is None:
            alpha, beta, gamma, phi = scipy.optimize.fmin_l_bfgs_b(func=self._rmse_damped, args=(
             Y, m), x0=numpy.array([0.5, 0.5, 0.5, 0.5]), bounds=[
             (0, 1), (0, 1), (0, 1), (0, 1)], approx_grad=True, maxiter=100, maxfun=100)[0]
        a = [sum(Y[0:m]) / float(m)]
        b = [(sum(Y[m:2 * m]) - sum(Y[0:m])) / m ** 2]
        s = [ Y[i] / a[0] for i in range(m) ]
        y = [(a[0] + phi * b[0]) * s[0]]
        for i in range(len(Y) + fc):
            if i == len(Y):
                Y.append((a[(-1)] + math.pow(phi, i) * b[(-1)]) * s[(-m)])
            a.append(alpha * (Y[i] / s[i]) + (1 - alpha) * (a[i] + phi * b[i]))
            b.append(beta * (a[(i + 1)] - a[i]) + (1 - beta) * phi * b[i])
            s.append(gamma * (Y[i] / (a[i] + phi * b[i])) + (1 - gamma) * s[i])
            y.append((a[(i + 1)] + math.pow(phi, i) * b[(i + 1)]) * s[(i + 1)])

        return (Y[-fc:], alpha, beta, gamma, self._calc_rmse(Y, y, fc), phi)

    def find_min_rmse(self, series, function, fc):
        if function not in [self.additive, self.multiplicative, self.damped]:
            raise Exception(str(function) + ' is not supported')
        min_rmse = 1000
        best_m = 1
        best_forecast = None
        for m in range(2, int(len(series) * 0.6)):
            try:
                r = function(series, m, fc)
                if r[4] < min_rmse:
                    best_m = m
                    best_forecast = r[0]
                    min_rmse = r[4]
            except ZeroException:
                pass
            except Exception as e:
                print 'skipping: ' + function.__name__ + ' ' + str(m) + ' due to: ' + str(e)

        return (
         best_forecast, best_m, min_rmse)

    def find_best_function(self, series, fc):
        fc = round(fc)
        linear_forecast, _, _, linear_rmse = self.linear(series, fc)
        add_forecast, add_m, add_rmse = self.find_min_rmse(series, self.additive, fc)
        mul_forecast, mul_m, mul_rmse = self.find_min_rmse(series, self.multiplicative, fc)
        min_rmse = min(linear_rmse, add_rmse, mul_rmse)
        if min_rmse == linear_rmse:
            return (linear_forecast, 1, linear_rmse, 'linear')
        if min_rmse == add_rmse:
            return (add_forecast, add_m, add_rmse, 'additive')
        if min_rmse == mul_rmse:
            return (mul_forecast, mul_m, mul_rmse, 'multiplicative')
        raise Exception('This should not happen')

    def calc_forecast(self, options, forecast_start, forecast_range, forecast_interval, lookback_range, lookback_data):
        resolution = 100
        if 'resolution' in options:
            resolution = options['resolution']
        start = lookback_data[0][0]
        end = lookback_data[(len(lookback_data) - 1)][0]
        forecast_length_simple = resolution * (forecast_range / lookback_range)
        raw_data = []
        for d in lookback_data:
            raw_data.append(d[1])

        forecast = None
        if 'mode' in options:
            if options['mode'] == 'linear':
                forecast, _, _, rmse = self.linear(raw_data, forecast_length_simple)
                logging.getLogger(__name__).debug('Name: linear, RMSE: ' + str(rmse))
            elif options['mode'] == 'additive':
                forecast, m, rmse = self.find_min_rmse(raw_data, self.additive, forecast_length_simple)
                logging.getLogger(__name__).debug('Name: additive,' + 'Season: ' + str(m) + ', RMSE: ' + str(rmse))
            elif options['mode'] == 'multiplicative':
                forecast, m, rmse = self.find_min_rmse(raw_data, self.multiplicative, forecast_length_simple)
                logging.getLogger(__name__).debug('Name: multiplicative,' + 'Season: ' + str(m) + ', RMSE: ' + str(rmse))
            else:
                logging.getLogger(__name__).warning('Unkown mode: ' + str(options['mode']))
        else:
            forecast, m, rmse, name = self.find_best_function(raw_data, forecast_length_simple)
            logging.getLogger(__name__).debug('Name: ' + name + 'Season: ' + str(m) + ', RMSE: ' + str(rmse))
        if not forecast:
            logging.getLogger(__name__).warning('no forecast was made')
            return
        else:
            step = int(lookback_range / len(lookback_data))
            x_forecast = [ end + y * step for y in range(len(forecast)) ]
            r = list(zip(x_forecast, forecast))
            return r

    def calc_intersection(self, options, forecast_start, forecast_range, forecast_interval, lookback_range, lookback_data, y):
        return self.gen_intersection(forecast_data=self.calc_forecast(options=options, forecast_start=forecast_start, forecast_range=forecast_range, forecast_interval=forecast_interval, lookback_range=lookback_range, lookback_data=lookback_data), forecast_start=forecast_start, y=y)


def print_forecast(series, forecast=None, m=None, typ=None):
    if forecast is None or m is None:
        forecast, m, rmse, typ = HoltWinters().find_best_function(series, len(series) / 2)
    try:
        import matplotlib.pyplot as plt
        if typ:
            plt.title(typ + ' ' + str(m))
        plt.plot(series, label='v')
        if m:
            plt.plot(series[:m + 1], label='s')
        plt.plot([None] * len(series) + forecast, label='f')
        plt.show()
    except:
        print (
         'Data: ', series)
        print ('Seasonlength: ', m)
        print ('Forecast: ', forecast)

    return


def sinus_example():
    series = []
    for i in range(round(math.pi * 4.5 * 10)):
        series.append(math.sin(i / 10) + 1)

    print_forecast(series)


def trunc_example():
    series = []
    for i in range(round(math.pi * 4.5 * 10)):
        series.append(math.trunc(i / 10))

    print_forecast(series)


def log_example():
    series = []
    for i in range(1, 15):
        series.append(math.log10(i) * 10)

    print_forecast(series)


if __name__ == '__main__':
    sinus_example()
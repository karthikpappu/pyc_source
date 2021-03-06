# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zeus/autocorr.py
# Compiled at: 2020-01-05 09:20:49
# Size of source mod 2**32: 2108 bytes
import numpy as np

def _autocorr_func_1d(x, norm=True):
    """
    Autocorrelation Function of 1-dimensional chain.

    Args:
        x (array) : 1-dimensional chain.
        norm (bool) : By default norm=True and the autocorrelation function will be normalized.

    Returns:
        The (normalised if norm=True) autocorrelation function of the chain x.
    """
    x = np.atleast_1d(x)
    if len(x.shape) != 1:
        raise ValueError('invalid dimensions for 1D autocorrelation function')
    n = 1
    while n < len(x):
        n = n << 1

    f = np.fft.fft((x - np.mean(x)), n=(2 * n))
    acf = np.fft.ifft(f * np.conjugate(f))[:len(x)].real
    acf /= 4 * n
    if norm:
        acf /= acf[0]
    return acf


def _autocorr_time_1d(y, c=5.0):
    """
    Integrated Autocorrelation Time (IAT) for 1-dimensional chain.

    Args:
        y (array) : (nwalkers,nsteps) array for one parameter.
        c (float) : Truncation parameter of automated windowing procedure of Sokal (1989), default is 5.0

    Returns:
        The IAT of the chain y.
    """
    f = np.zeros(y.shape[1])
    for yy in y:
        f += _autocorr_func_1d(yy)

    f /= len(y)
    taus = 2.0 * np.cumsum(f) - 1.0

    def auto_window(taus, c):
        m = np.arange(len(taus)) < c * taus
        if np.any(m):
            return np.argmin(m)
        return len(taus) - 1

    window = auto_window(taus, c)
    return taus[window]


def _autocorr_time(samples, c=5.0):
    """
    Integrated Autocorrelation Time (IAT) for all the chains.

    Args:
        samples (array) : 3-dimensional array of shape (nwalkers, nsteps, ndim)
        c (float) : Truncation parameter of automated windowing procedure of Sokal (1989), default is 5.0

    Returns:
        Array with the IAT of all the chains.
    """
    _, _, ndim = np.shape(samples)
    taus = np.empty(ndim)
    for i in range(ndim):
        taus[i] = _autocorr_time_1d(samples[:, :, i], c)

    return taus
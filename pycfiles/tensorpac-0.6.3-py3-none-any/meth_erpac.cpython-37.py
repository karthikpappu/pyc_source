# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /run/media/etienne/DATA/Toolbox/tensorpac/tensorpac/methods/meth_erpac.py
# Compiled at: 2019-10-07 10:13:11
# Size of source mod 2**32: 5469 bytes
"""Individual methods for assessing ERPAC."""
import numpy as np
from scipy.stats import chi2
from joblib import Parallel, delayed
from tensorpac.gcmi import nd_mi_gg
from tensorpac.config import CONFIG

def pearson(x, y, st='i...j, k...j->ik...'):
    """Pearson correlation for multi-dimensional arrays.

    Parameters
    ----------
    x, y : array_like
        Compute pearson correlation between the multi-dimensional arrays
        x and y.
    st : string | 'i..j, k..j->ik...'
        The string to pass to the np.einsum function.

    Returns
    -------
    cov: array_like
        The pearson correlation array.
    """
    n = x.shape[(-1)]
    mu_x = x.mean((-1), keepdims=True)
    mu_y = y.mean((-1), keepdims=True)
    s_x = x.std((-1), ddof=(n - 1), keepdims=True)
    s_y = y.std((-1), ddof=(n - 1), keepdims=True)
    cov = np.einsum(st, x, y)
    mu_xy = np.einsum(st, mu_x, mu_y)
    cov -= n * mu_xy
    cov /= np.einsum(st, s_x, s_y)
    return cov


def erpac(pha, amp):
    """Correlation coefficient between a circular and a linear random variable.

    Adapted from the function circ_corrcc Circular Statistics Toolbox for
    Matlab By Philipp Berens, 2009.

    Parameters
    ----------
    pha, amp : array_like
        Respectively the arrays of phases of shape (n_pha, ..., n_epochs) and
        the array of amplitudes of shape (n_amp, ..., n_epochs).

    Returns
    -------
    rho : array_like
        Array of correlation coefficients of shape (n_amp, n_pha, ...)
    pval : array_like
        Array of p-values of shape (n_amp, n_pha, ...).

    References
    ----------
    Voytek B, D’Esposito M, Crone N, Knight RT (2013) A method for
    event-related phase/amplitude coupling. NeuroImage 64:416–424.
    """
    n = pha.shape[(-1)]
    sa, ca = np.sin(pha), np.cos(pha)
    rxs = pearson(amp, sa)
    rxc = pearson(amp, ca)
    rcs = pearson(sa, ca, st='i...j, k...j->i...')
    rcs = rcs[(np.newaxis, ...)]
    rho = np.sqrt((rxc ** 2 + rxs ** 2 - 2 * rxc * rxs * rcs) / (1 - rcs ** 2))
    pval = 1.0 - chi2.cdf(n * rho ** 2, 2)
    return (
     rho, pval)


def ergcpac(pha, amp, smooth=None, n_jobs=-1):
    """Event Related PAC computed using the Gaussian Copula Mutual Information.

    This function assumes that phases and amplitudes have already been
    prepared i.e. phases should be represented in a unit circle
    (np.c_[np.sin(pha), np.cos(pha)]) and both inputs should also have been
    copnormed.

    Parameters
    ----------
    pha, amp : array_like
        Respectively arrays of phases of shape (n_pha, n_times, 2, n_epochs)
        and the array of amplitudes of shape (n_amp, n_times, 1, n_epochs).

    Returns
    -------
    erpac : array_like
        Array of correlation coefficients of shape (n_amp, n_pha, n_times)

    References
    ----------
    Ince RAA, Giordano BL, Kayser C, Rousselet GA, Gross J, Schyns PG (2017) A
    statistical framework for neuroimaging data analysis based on mutual
    information estimated via a gaussian copula: Gaussian Copula Mutual
    Information. Human Brain Mapping 38:1541–1573.
    """
    (n_pha, n_times, _, n_epochs), n_amp = pha.shape, amp.shape[0]
    ergcpac = np.zeros((n_amp, n_pha, n_times))
    if isinstance(smooth, int):
        vec = np.arange(smooth, n_times - smooth, 1)
        times = [slice(k - smooth, k + smooth + 1) for k in vec]
        pha, amp = np.moveaxis(pha, 1, -2), np.moveaxis(amp, 1, -2)

        def _fcn(t):
            _erpac = np.zeros((n_amp, n_pha), dtype=float)
            xp, xa = pha[..., t, :], amp[..., t, :]
            for a in range(n_amp):
                _xa = xa.reshape(n_amp, 1, -1)
                for p in range(n_pha):
                    _xp = xp.reshape(n_pha, 2, -1)
                    _erpac[(a, p)] = nd_mi_gg(_xp[(p, ...)], _xa[(a, ...)])

            return _erpac

        _ergcpac = Parallel(n_jobs=n_jobs, **CONFIG['JOBLIB_CFG'])((delayed(_fcn)(t) for t in times))
        for a in range(n_amp):
            for p in range(n_pha):
                mean_vec = np.zeros((n_times,), dtype=float)
                for t, _gc in zip(times, _ergcpac):
                    ergcpac[(a, p, t)] += _gc[(a, p)]
                    mean_vec[t] += 1

                ergcpac[a, p, :] /= mean_vec

    else:
        for a in range(n_amp):
            for p in range(n_pha):
                ergcpac[(a, p, ...)] = nd_mi_gg(pha[(p, ...)], amp[(a, ...)])

    return ergcpac


def swap_erpac_trials(pha):
    """Swap trials across the last dimension."""
    tr_ = np.random.permutation(pha.shape[(-1)])
    return pha[(..., tr_)]


def _ergcpac_perm(pha, amp, smooth=None, n_jobs=-1, n_perm=200):

    def _ergcpac_single_perm():
        p = swap_erpac_trials(pha)
        return ergcpac(p, amp, smooth=smooth, n_jobs=1)

    out = Parallel(n_jobs=n_jobs, **CONFIG['JOBLIB_CFG'])((delayed(_ergcpac_single_perm)() for _ in range(n_perm)))
    return np.stack(out)
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/exoworlds/lightcurves/utils.py
# Compiled at: 2018-11-09 10:57:44
# Size of source mod 2**32: 4359 bytes
"""
Created on Tue Apr  5 15:07:00 2016

@author:
Maximilian N. Günther
MIT Kavli Institute for Astrophysics and Space Research,
Massachusetts Institute of Technology,
77 Massachusetts Avenue,
Cambridge, MA 02109,
USA
Email: maxgue@mit.edu
Web: www.mnguenther.com
"""
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np, os, glob, time
from astropy.coordinates import SkyCoord
import astropy.units as u
import pandas as pd
from pprint import pprint

def medsig(a):
    """Compute median and MAD-estimated scatter of array a"""
    med = np.nanmedian(a)
    sig = 1.48 * np.nanmedian(abs(a - med))
    return (med, sig)


def running_mean(x, N):
    x[np.isnan(x)] = 0.0
    cumsum = np.cumsum(np.insert(x, 0.0, 0.0))
    return 1.0 * (cumsum[N:] - cumsum[:-N]) / N


def running_mean_pandas(x, N):
    ts = pd.Series(x).rolling(window=N, center=False).mean()
    return ts[(~np.isnan(ts))].as_matrix()


def running_median_pandas(x, N):
    ts = pd.Series(x).rolling(window=N, center=False).median()
    return ts[(~np.isnan(ts))].as_matrix()


def mask_ranges(x, x_min, x_max):
    """"
    Crop out values and indices out of an array x for multiple given ranges x_min to x_max.
    
    Input:
    x: array, 
    x_min: lower limits of the ranges
    x_max: upper limits of the ranges
    
    Output:
    
    
    Example:
    x = np.arange(200)    
    x_min = [5, 25, 90]
    x_max = [10, 35, 110]
    """
    mask = np.zeros((len(x)), dtype=bool)
    for i in range(len(x_min)):
        mask = mask | (x >= x_min[i]) & (x <= x_max[i])

    ind_mask = np.arange(len(mask))[mask]
    return (
     x[mask], ind_mask, mask)


def mystr(x, digits=0):
    if np.isnan(x):
        return '.'
    if digits == 0:
        return str(int(round(x, digits)))
    return str(round(x, digits))


def format_2sigdigits(x1, x2, x3, nmax=3):
    n = int(np.max([-np.floor(np.log10(np.abs(x))) for x in [x1, x2, x3]]) + 1)
    scaling = 0
    extra = None
    if n > nmax:
        scaling = n - 1
        n = 1
        extra = '\\cdot 10^{' + str(-scaling) + '}'
    return (
     str(round(x1 * 10 ** scaling, n)).ljust(n + 2, '0'), str(round(x2 * 10 ** scaling, n)).ljust(n + 2, '0'), str(round(x3 * 10 ** scaling, n)).ljust(n + 2, '0'), extra)


def deg2hmsdms(ra, dec):
    c = SkyCoord(ra=(ra * u.degree), dec=(dec * u.degree), frame='icrs')
    return c.to_string('hmsdms', precision=2, sep=':')


def format_latex(x1, x2, x3, nmax=3):
    r, l, u, extra = format_2sigdigits(x1, x2, x3, nmax)
    if l == u:
        core = r + '\\pm' + l
    else:
        core = r + '^{+' + l + '}_{-' + u + '}'
    if extra is None:
        return '$' + core + '$'
    return '$(' + core + ')' + extra + '$'


def merge_two_dicts(x, y):
    """Given two dicts, merge them into a new dict as a shallow copy."""
    z = x.copy()
    z.update(y)
    return z


def table_view(dic):
    from astropy.table import Table
    dic_table = {}
    subkeys = [
     'OBJ_ID', 'SYSREM_FLUX3_median', 'PERIOD', 'DEPTH', 'WIDTH', 'NUM_TRANSITS']
    for key in subkeys:
        dic_table[key] = dic[key]

    dic_table = Table(dic_table)
    dic_table = dic_table[subkeys]
    pprint(dic_table)
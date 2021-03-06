# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ely/codebase/refstis/refstis/basedark.py
# Compiled at: 2016-06-01 14:00:53
"""Functions to create a BaseDark for the STIS instrument

#. If not already done, perform bias subtraction
#. If after switch to side-2 electronics, perform temperature scaling
#. Join all imsets from input list into single file
#. combine and cr-reject
#. normalize to e/s by dividing by (exptime/gain)
#. update DQ array with hot pixel information

.. note::

  * Side 1 operations ended on May 16, 2001.
  * Side 2 operations started on July 10, 2001.
  * The dark correction will only be applied to datasets after July 1, 2001 (MJD 52091.0).
"""
from astropy.io import fits
from astropy.stats import sigma_clipped_stats
import numpy as np
from scipy.ndimage.filters import median_filter
import shutil
from . import functions

def update_sci(filename):
    """Create the science extension of the baseline dark

    THIS APPEARS

    .. note:: The input file will be updated in-place.

    Parameters
    ----------
    filename, str
        name of the file to be updated

    """
    with fits.open(filename, mode='update') as (hdu):
        im_mean, im_median, im_std = sigma_clipped_stats(hdu[('sci', 1)].data, sigma=5, iters=50)
        fivesig = im_mean + 5.0 * im_std
        only_hotpix = np.where(hdu[('sci', 1)].data >= fivesig, hdu[('sci', 1)].data - im_mean, 0)
        med_im = median_filter(hdu[('sci', 1)].data, (3, 3))
        only_baseline = np.where(hdu[('sci', 1)].data >= fivesig, med_im, hdu[('sci',
                                                                               1)].data)
        hdu[('dq', 1)].data = np.where(only_hotpix >= 0.1, 16, hdu[('dq', 1)].data)


def find_hotpix(filename):
    """Find hotpixels and update DQ array

    Pixels hotter that median + 5*sigma will be updated to have a
    DQ value of 16.

    .. note:: The input file will be updated in-place.

    Parameters:
    -----------
    filename, str
        filename of the input biasfile

    """
    with fits.open(filename, mode='update') as (hdu):
        im_mean, im_median, im_std = sigma_clipped_stats(hdu[('sci', 1)].data, sigma=3, iters=40)
        five_sigma = im_median + 5 * im_std
        index = np.where((hdu[('SCI', 1)].data > five_sigma) & (hdu[('SCI', 1)].data > im_mean + 0.1))
        hdu[('DQ', 1)].data[index] = 16


def make_basedark(input_list, refdark_name='basedark.fits', bias_file=None):
    """Make a monthly baseline dark from the input list.

    Parameters:
    -----------
    input_list : list
        list of input dark files

    refdark_name : str
        name of the output reference file

    bias_file : str
        bias file to be used in calibration

    """
    print '#-------------------------------#'
    print '#        Running basedark       #'
    print '#-------------------------------#'
    print 'output to: %s' % refdark_name
    print 'with biasfile %s' % bias_file
    flt_list = [ functions.bias_subtract_data(item, bias_file) for item in input_list ]
    for filename in flt_list:
        texpstrt = fits.getval(filename, 'texpstrt', 0)
        if texpstrt > 52091.0:
            functions.apply_dark_correction(filename, texpstrt)

    joined_filename = refdark_name.replace('.fits', '_joined.fits')
    crj_filename = joined_filename.replace('.fits', '_crj.fits')
    print 'Joining images'
    functions.msjoin(flt_list, joined_filename)
    print 'Performing CRREJECT'
    crdone = functions.bd_crreject(joined_filename)
    if not crdone:
        functions.bd_calstis(joined_filename, bias_file)
    functions.normalize_crj(crj_filename)
    shutil.copy(crj_filename, refdark_name)
    update_sci(refdark_name)
    find_hotpix(refdark_name)
    functions.update_header_from_input(refdark_name, input_list)
    fits.setval(refdark_name, 'TASKNAME', ext=0, value='BASEDARK')
    print 'Cleaning...'
    functions.RemoveIfThere(crj_filename)
    functions.RemoveIfThere(joined_filename)
    print ('basedark done for {}').format(refdark_name)
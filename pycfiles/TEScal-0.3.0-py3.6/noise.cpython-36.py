# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tescal/detcal/noise.py
# Compiled at: 2018-09-12 19:18:31
# Size of source mod 2**32: 17649 bytes
""" 
Created by Caleb Fink 5/7/2018
"""
import numpy as np
from scipy.signal import savgol_filter
from math import ceil
from scipy.signal import csd
from scipy.optimize import least_squares
from scipy.interpolate import interp1d
from itertools import product, combinations
import scipy.constants as constants, pickle, matplotlib.pyplot as plt, seaborn as sns, tescal.plotting as utils

def slope(x, y, removemeans=True):
    """
    Computes the maximum likelihood slope of a set of x and y points.
    
    Parameters
    ----------
        x : array_like
            Array of real-valued independent variables.
        y : array_like
            Array of real-valued dependent variables.
        removemeans : boolean
            Boolean flag for if the mean of x should be subtracted. This
            should be set to True if x has not already had its mean subtracted.
            Set to False if the mean has been subtracted. Default is True.
            
    Returns
    -------
        slope : float
            Maximum likelihood slope estimate, calculated as
            sum((x-<x>)(y-<y>))/sum((x-<x>)**2)
    """
    if removemeans:
        slope = np.sum((x - np.mean(x)) * (y - np.mean(x))) / np.sum((x - np.mean(x)) ** 2)
    else:
        slope = np.sum(x * y) / np.sum(x ** 2)
    return slope


def fill_negatives(arr):
    """
    Simple helper function to remove negative and zero values from PSD's and replace
    them with interpolated values.
    
    Parameters
    ----------
        arr: ndarray
            Array of values to replace neagive values on
            
    Returns
    -------
        arr: ndarray
            Modified input array with the negative and zero values replace by interpelate values
            
    """
    zeros = np.array(arr <= 0)
    inds_zero = np.where(zeros)[0]
    inds_not_zero = np.where(~zeros)[0]
    good_vals = arr[(~zeros)]
    if len(good_vals) != 0:
        arr[zeros] = np.interp(inds_zero, inds_not_zero, good_vals)
    return arr


class Noise(object):
    __doc__ = '\n    This class allows the user to calculate the power spectral densities of signals \n    from detectors, study correlations, and decouple the intrinsic noise from cross \n    channel correlated noise. \n    \n    Attributes\n    ----------\n    traces : ndarray\n        Array of the traces to use in the noise analysis. Should be shape \n        (# of traces, # of channels, # of bins)\n    fs : float\n        The digitization rate of the data in Hz.\n    channames : list\n        A list of strings that name each of the channels.\n    time : ndarray\n        The time values for each bin in each trace.\n    fname : str\n        The file name of the data, this will be used when saving the file.\n    tracegain : float\n        The factor that traces should be divided by to convert the units to Amps. If rawtraces\n        already has units of Amps, then this should be set to 1.0\n    freqs : ndarray\n        The frequencies that correspond to each value in the spectral densities\n    psd : ndarray\n        The power spectral density of the data in A^2/Hz\n    realpsd : ndarray\n        The real power spectral density of the data in A^2/Hz\n    imagpsd : ndarray\n        The imaginary power spectral density of the data in A^2/Hz\n    corrcoeff : ndarray\n        The array of the correlation coefficients between each of the channels\n    uncorrnoise : ndarray\n        The uncorrelated noise psd in A^2/Hz\n    corrnoise : ndarray\n        The correlated noise psd in A^2/Hz\n    realcsd : ndarray\n        The real part of the cross spectral density in A^2/Hz\n    imagcsd : ndarray\n        The imaginary part of the cross spectral density in A^2/Hz\n    realcsdstd : ndarray\n        The standard deviation of the real part of the cross spectral density at each frequency\n    imagcsdstd : ndarray \n        The standard deviation of the imaginary part of the cross spectral density at each frequency\n    csd : ndarray\n        The cross spectral density of the traces\n    chandict : dict\n        A dictionary that stores the channel number for each channel name.\n            \n    '

    def __init__(self, traces, fs, channames, tracegain=1.0, fname=None, time=None):
        """
        Initialization of the Noise object.
        
        Parameters
        ----------
            traces : ndarray
                Array of the traces to use in the noise analysis. Should be shape 
                (# of traces, # of channels, # of bins)
            fs : float
                The digitization rate of the data in Hz.
            channames : list
                A list of strings that name each of the channels.
            tracegain : float, optional
                The factor that traces should be divided by to convert the units to Amps. If rawtraces
                already has units of Amps, then this should be set to 1.0
            fname : str, optional
                The file name of the data, this will be used when saving the file.
            time : ndarray, optional
                The time values for each bin in each trace.
        """
        if len(traces.shape) == 1:
            raise ValueError('Need more than one trace')
        else:
            if len(traces.shape) == 2:
                traces = np.expand_dims(traces, 1)
            if len(channames) != traces.shape[1]:
                raise ValueError('The number of channel names must match the number of channels in traces!')
            self.traces = traces / tracegain
            self.fs = fs
            self.channames = channames
            if time is None:
                self.time = np.arange(0, traces.shape[(-1)]) / self.fs
            else:
                self.time = time
        self.fname = fname
        self.tracegain = tracegain
        self.freqs = np.fft.rfftfreq((self.traces.shape[2]), d=(1 / fs))
        self.psd = None
        self.real_psd = None
        self.imag_psd = None
        self.corrcoeff = None
        self.uncorrnoise = None
        self.corrnoise = None
        self.real_csd = None
        self.imag_csd = None
        self.real_csd_std = None
        self.imag_csd_std = None
        self.csd = None
        temp_dict = {}
        for ind, chann in enumerate(channames):
            temp_dict[chann] = ind

        self.chandict = temp_dict

    def remove_trace_slope(self):
        """
        Function to remove the slope from each trace. self.traces is changed to be the slope subtracted traces.
        """
        tracenoslope = np.empty_like(self.traces)
        for ichan in range(self.traces.shape[1]):
            for itrace in range(self.traces.shape[0]):
                s = slope(self.time, self.traces[itrace][ichan])
                tracenoslope[itrace][ichan] = self.traces[itrace][ichan] - s * self.time

        self.traces = tracenoslope

    def calculate_psd(self):
        """
        Calculates the psd for each channel in traces. Stores psd in self.psd
        """
        traceshape = self.traces.shape
        if traceshape[2] % 2 != 0:
            lenpsd = int((traceshape[2] + 1) / 2)
        else:
            lenpsd = int(traceshape[2] / 2 + 1)
        psd = np.empty(shape=(traceshape[1], lenpsd))
        real_psd = np.empty(shape=(traceshape[1], lenpsd))
        imag_psd = np.empty(shape=(traceshape[1], lenpsd))
        fft = np.fft.rfft(self.traces)
        psd_chan = np.abs(fft) ** 2
        real_psd_chan = np.real(fft) ** 2
        imag_psd_chan = np.imag(fft) ** 2
        psd = np.mean(psd_chan, axis=0) * 2.0 / (traceshape[2] * self.fs)
        real_psd = np.mean(real_psd_chan, axis=0) * 2.0 / (traceshape[2] * self.fs)
        imag_psd = np.mean(imag_psd_chan, axis=0) * 2.0 / (traceshape[2] * self.fs)
        self.psd = psd
        self.real_psd = real_psd
        self.imag_psd = imag_psd

    def calculate_corrcoeff(self):
        """
        Calculates the correlations between channels as a function of frequency. Stores
        results in self.corrcoeff
        Inputs: None
        Returns: None
        """
        nsizematrix = self.traces.shape[1]
        if nsizematrix == 1:
            raise ValueError('Need more than one channel to calculate cross channel correlations')
        else:
            if self.traces.shape[2] % 2 != 0:
                lenpsd = int((self.traces.shape[2] + 1) / 2)
            else:
                lenpsd = int(self.traces.shape[2] / 2 + 1)
        nDataPoints = self.traces.shape[0]
        corr_coeff = np.empty(shape=(lenpsd, nsizematrix, nsizematrix))
        traces_fft_chan = np.abs(np.fft.rfft(self.traces))
        traces_fft_chan = np.swapaxes(traces_fft_chan, 0, 1)
        for n in range(lenpsd):
            corr_coeff[n] = np.corrcoef(traces_fft_chan[:, :, n])

        self.corrcoeff = np.swapaxes(corr_coeff, 0, 2)

    def calculate_uncorr_noise(self):
        """
        Calculates the uncorrelated and correlated total noise.
        """
        if self.csd is None:
            self.calculate_csd()
        else:
            inv_csd = np.zeros_like(self.csd)
            uncorrnoise = np.zeros(shape=(self.csd.shape[0], self.csd.shape[2]))
            corrnoise = np.zeros(shape=(self.csd.shape[0], self.csd.shape[2]))
            for ii in range(self.csd.shape[2]):
                inv_csd[:, :, ii] = np.linalg.inv(self.csd[:, :, ii])

            for jj in range(self.csd.shape[0]):
                uncorrnoise[jj] = 1 / np.abs(inv_csd[jj][jj][:])
                corrnoise[jj] = self.real_csd[jj][jj] - 1 / np.abs(inv_csd[jj][jj][:])

            self.corrnoise = corrnoise
            self.uncorrnoise = uncorrnoise

    def calculate_csd(self):
        """
        Calculates the csd for each channel in traces. Stores csd in self.csd
        """
        traceshape = self.traces.shape
        if traceshape[1] == 1:
            raise ValueError('Need more than one channel to calculate csd')
        else:
            lencsd = traceshape[2]
            if lencsd % 2 != 0:
                nfreqs = int((lencsd + 1) / 2)
            else:
                nfreqs = int(lencsd / 2 + 1)
        nrows = traceshape[1]
        ntraces = traceshape[0]
        trace_csd = np.zeros(shape=(nrows, nrows, ntraces, nfreqs), dtype=(np.complex128))
        csd_mean = np.zeros(shape=(nrows, nrows, nfreqs), dtype=(np.complex128))
        real_csd_mean = np.zeros(shape=(nrows, nrows, nfreqs), dtype=(np.float64))
        imag_csd_mean = np.zeros(shape=(nrows, nrows, nfreqs), dtype=(np.float64))
        real_csd_std = np.zeros(shape=(nrows, nrows, nfreqs), dtype=(np.float64))
        imag_csd_std = np.zeros(shape=(nrows, nrows, nfreqs), dtype=(np.float64))
        for irow, jcolumn in product((list(range(nrows))), repeat=2):
            for n in range(ntraces):
                _, temp_csd = csd((self.traces[n, irow, :]), (self.traces[n, jcolumn, :]), nperseg=lencsd,
                  fs=(self.fs),
                  nfft=lencsd)
                trace_csd[irow][jcolumn][n] = temp_csd

            csd_mean[irow][jcolumn] = np.mean((trace_csd[irow][jcolumn]), axis=0)
            real_csd_mean[irow][jcolumn] = fill_negatives(np.mean((np.real(trace_csd[irow][jcolumn])), axis=0))
            imag_csd_mean[irow][jcolumn] = fill_negatives(np.mean((np.imag(trace_csd[irow][jcolumn])), axis=0))
            real_csd_std[irow][jcolumn] = fill_negatives(np.std((np.real(trace_csd[irow][jcolumn])), axis=0))
            imag_csd_std[irow][jcolumn] = fill_negatives(np.std((np.imag(trace_csd[irow][jcolumn])), axis=0))

        self.csd = csd_mean
        self.real_csd = real_csd_mean
        self.imag_csd = imag_csd_mean
        self.real_csd_std = real_csd_std
        self.imag_csd_std = imag_csd_std

    def plot_psd(self, lgcoverlay=True, lgcsave=False, savepath=None):
        """
        Function to plot the noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz).

        Parameters
        ----------
            lgcoverlay : boolean, optional
                If True, psd's for all channels are overlayed in a single plot, 
                If False, each psd for each channel is plotted in a seperate subplot
            lgcsave : boolean, optional
                If True, the figure is saved in the user provided directory
            savepath : str, optional
                Absolute path for the figure to be saved
        """
        utils.plot_psd(self, lgcoverlay, lgcsave, savepath)

    def plot_reim_psd(self, lgcsave=False, savepath=None):
        """
        Function to plot the real vs imaginary noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz).
        This is done to check for thermal muon tails making it passed the quality cuts

        Parameters
        ----------
            lgcsave : boolean, optional
                If True, the figure is saved in the user provided directory
            savepath : str, optional
                Absolute path for the figure to be saved

        """
        utils.plot_reim_psd(self, lgcsave=False, savepath=None)

    def plot_corrcoeff(self, lgcsmooth=True, nwindow=7, lgcsave=False, savepath=None):
        """
        Function to plot the cross channel correlation coefficients. Since there are typically few traces,
        the correlations are often noisy. a savgol_filter is used to smooth out some of the noise

        Parameters
        ----------
            lgcsmooth : boolean, optional
                If True, a savgol_filter will be used when plotting. 
            nwindow : int, optional
                the number of bins used for the window in the savgol_filter
            lgcsave : boolean, optional
                If True, the figure is saved in the user provided directory
            savepath : str, optional
                Absolute path for the figure to be saved
        """
        utils.plot_corrcoeff(self, lgcsmooth, nwindow, lgcsave, savepath)

    def plot_csd(self, whichcsd=[
 '01'], lgcreal=True, lgcsave=False, savepath=None):
        """
        Function to plot the cross channel noise spectrum referenced to the TES line in
        units of Amperes^2/Hz

        Parameters
        ----------
            whichcsd : list, optional
                a list of strings, where each element of the list refers to the pair of 
                indices of the desired csd plot
            lgcreal : boolean, optional
                If True, the Re(csd) is plotted. If False, the Im(csd) is plotted
            lgcsave : boolean, optional
                If True, the figure is saved in the user provided directory
            savepath : str, optional
                Absolute path for the figure to be saved
        """
        utils.plot_csd(self, whichcsd, lgcreal, lgcsave, savepath)

    def plot_decorrelatednoise(self, lgcoverlay=False, lgcdata=True, lgcuncorrnoise=True, lgccorrelated=False, lgcsum=False, lgcsave=False, savepath=None):
        """
        Function to plot the de-correlated noise spectrum referenced to the TES line in units of Amperes/sqrt(Hz) 
        from fitted parameters calculated calculate_deCorrelated_noise

        Parameters
        ----------
            lgcoverlay : boolean, optional
                If True, de-correlated for all channels are overlayed in a single plot, 
                If False, the noise for each channel is plotted in a seperate subplot
            lgcdata : boolean, optional
                Only applies when lgcoverlay = False. If True, the csd data is plotted
            lgcuncorrnoise : boolean, optional
                Only applies when lgcoverlay = False. If True, the de-correlated noise is plotted
            lgccorrelated : boolean, optional
                Only applies when lgcoverlay = False. If True, the correlated component of the fitted noise 
                is plotted
            lgcsum : boolean, optional
                Only applies when lgcoverlay = False. If True, the sum of the fitted de-correlated noise and
                and correlated noise is plotted
            lgcsave : boolean, optional
                If True, the figure is saved in the user provided directory
            savepath : str, optional
                Absolute path for the figure to be saved
        """
        utils.plot_decorrelatednoise(self, lgcoverlay, lgcdata, lgcuncorrnoise, lgccorrelated, lgcsum, lgcsave, savepath)

    def save(self, path):
        """
        Saves the noise object as a pickle file
        
        Parameters
        ----------
            path : str
                Path where the noise object should be saved.
        """
        if path[(-1)] != '/':
            path += '/'
        with open(path + self.fname.replace(' ', '_') + '.pkl', 'wb') as (savefile):
            pickle.dump(self, savefile, pickle.HIGHEST_PROTOCOL)
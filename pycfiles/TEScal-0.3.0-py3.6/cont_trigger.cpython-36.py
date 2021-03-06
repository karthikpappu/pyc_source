# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/tescal/trigger/cont_trigger.py
# Compiled at: 2018-09-12 19:18:31
# Size of source mod 2**32: 27304 bytes
import numpy as np
from scipy.signal import correlate
from numpy.fft import ifft, fft, fftfreq, rfft, rfftfreq
from numpy.random import choice
from collections import Counter
from math import log10, floor
from tescal.io import loadstanfordfile
from tescal.utils import inrange

def getchangeslessthanthresh(x, threshold):
    """
    Helper function that returns a list of the start and ending indices of the ranges of inputted 
    values that change by less than the specified threshold value
       
    Parameters
    ----------
        x : ndarray
            1-dimensional of values.
        threshold : int
            Value to detect the different ranges of vals that change by less than this threshold value.
        
    Returns
    -------
        ranges : ndarray
            List of tuples that each store the start and ending index of each range.
            For example, vals[ranges[0][0]:ranges[0][1]] gives the first section of values that change by less than 
            the specified threshold.
        vals : ndarray
            The corresponding starting and ending values for each range in x.
    
    """
    diff = x[1:] - x[:-1]
    a = diff > threshold
    inds = np.where(a)[0] + 1
    start_inds = np.zeros((len(inds) + 1), dtype=int)
    start_inds[1:] = inds
    end_inds = np.zeros((len(inds) + 1), dtype=int)
    end_inds[-1] = len(x)
    end_inds[:-1] = inds
    ranges = np.array(list(zip(start_inds, end_inds)))
    if len(x) != 0:
        vals = np.array([(x[st], x[(end - 1)]) for st, end in ranges])
    else:
        vals = np.array([])
    return (ranges, vals)


def rand_sections(x, n, l, t=None, fs=1.0):
    """
    Return random, non-overlapping sections of a 1 or 2 dimensional array.
    For 2-dimensional arrays, the function treats each row as independent from the other rows.
    
    Parameters
    ----------
        x : ndarray
            n dimensional array to choose sections from
        n : int
            Number of sections to choose
        l : int
            Length in bins of sections
        t : array_like or float, optional
            Start times (in s) associated with x
        fs : float, optional
            Sample rate of data (in Hz)
            
    Returns
    -------
        evttimes : ndarray
            Array of the corresponding event times for each section
        res : ndarray
            Array of the n sections of x, each with length l
        
    """
    if len(x.shape) == 1:
        if len(x) - l * n < 0:
            raise ValueError('Either n or l is too large, trying to find more random sections than are possible.')
        if t is None:
            t = 0.0
        else:
            if not np.isscalar(t):
                raise ValueError('x is 1-dimensional, t should be a scalar value')
        res = np.zeros((n, l))
        evttimes = np.zeros(n)
        j = 0
        offset = 0
        inds = np.arange(len(x) - (l - 1) * n)
        for ind in sorted(choice(inds, size=n, replace=False)):
            ind += offset
            res[j] = x[ind:ind + l]
            evttimes[j] = t + (ind + l // 2) / fs
            j += 1
            offset += l - 1

    else:
        if t is None:
            t = np.arange(x.shape[0]) * x.shape[(-1)]
        else:
            if np.isscalar(t):
                raise ValueError(f"x is {len(x.shape)}-dimensional, t should be an array")
            else:
                if len(x) != len(t):
                    raise ValueError('x and t have different lengths')
            tup = (
             (
              n,), x.shape[1:-1], (l,))
            sz = sum(tup, ())
            res = np.zeros(sz)
            evttimes = np.zeros(n)
            j = 0
            nmax = int(x.shape[(-1)] / l)
            if x.shape[0] * nmax < n:
                raise ValueError('Either n or l is too large, trying to find more random sections than are possible.')
            choicelist = list(range(len(x))) * nmax
            np.random.shuffle(choicelist)
            rows = np.array(choicelist[:n])
            counts = Counter(rows)
            for key in counts.keys():
                offset = 0
                ncounts = counts[key]
                inds = np.arange(x.shape[(-1)] - (l - 1) * ncounts)
                for ind in sorted(choice(inds, size=ncounts, replace=False)):
                    ind += offset
                    res[j] = x[key, ..., ind:ind + l]
                    evttimes[j] = t[key] + (ind + l // 2) / fs
                    j += 1
                    offset += l - 1

    return (
     evttimes, res)


def rand_sections_wrapper(filelist, n, l, datashape=None, iotype='stanford'):
    """
    Wrapper for the rand_sections function for getting random sections from many different files. This allows 
    the user to input a list of files that the random sections should be pulled from.
    
    Parameters
    ----------
        filelist : list of strings
            List of files to be opened to take random sections from (should be full paths)
        n : int
            Number of sections to choose
        l : int
            Length in bins of sections
        datashape : tuple, NoneType, optional
            The shape of the data in each file. If inputted, this should be a tuple that is 
            (# of traces in a dataset, # of bins in each trace). If left as None, then the first file in filelist
            is opened, and the shape of the data in it is used.
        iotype : string, optional
            Type of file to open, uses a different IO function. Default is "stanford".
                "stanford" : Use pycdms.io.loadstanfordfile to open the files
                
    Returns
    -------
        evttimes : ndarray
            Array of the corresponding event times for each section
        res : ndarray
            Array of the n sections of x, each with length l
        
    """
    if datashape is None:
        if iotype == 'stanford':
            traces = loadstanfordfile(filelist[0])[0]
            datashape = (traces.shape[0], traces.shape[(-1)])
        else:
            raise ValueError('Unrecognized iotype inputted.')
    nmax = int(datashape[(-1)] / l)
    choicelist = list(range(len(filelist))) * nmax * datashape[0]
    np.random.shuffle(choicelist)
    rows = np.array(choicelist[:n])
    counts = Counter(rows)
    evttimes_list = []
    res_list = []
    for key in counts.keys():
        if iotype == 'stanford':
            traces, t, fs, _ = loadstanfordfile(filelist[key])
        else:
            raise ValueError('Unrecognized iotype inputted.')
        et, r = rand_sections(traces, (counts[key]), l, t=t, fs=fs)
        evttimes_list.append(et)
        res_list.append(r)

    evttimes = np.concatenate(evttimes_list)
    res = np.vstack(res_list)
    return (
     evttimes, res)


class OptimumFilt(object):
    __doc__ = '\n    Class for applying a time-domain optimum filter to a long trace, which can be thought of as an FIR filter.\n    \n    Attributes\n    ----------\n        phi : ndarray \n            The optimum filter in time-domain, equal to the inverse FT of (FT of the template/power \n            spectral density of noise)\n        norm : float\n            The normalization of the optimal amplitude.\n        tracelength : int\n            The desired trace length (in bins) to be saved when triggering on events.\n        fs : float\n            The sample rate of the data (Hz).\n        pulse_range : int\n            If detected events are this far away from one another (in bins), \n            then they are to be treated as the same event.\n        traces : ndarray\n            All of the traces to be filtered, assumed to be an ndarray of \n            shape = (# of traces, # of channels, # of trace bins). Should be in units of Amps.\n        template : ndarray\n            The template that will be used for the Optimum Filter.\n        noisepsd : ndarray\n            The two-sided noise PSD that will be used to create the Optimum Filter.\n        filts : ndarray \n            The result of the FIR filter on each of the traces.\n        resolution : float\n            The expected energy resolution in Amps given by the template and the noisepsd, calculated\n            from the Optimum Filter.\n        times : ndarray\n            The absolute start time of each trace (in s), should be a 1-dimensional ndarray.\n        pulsetimes : ndarray\n            If we triggered on a pulse, the time of the pulse trigger in seconds. Otherwise this is zero.\n        pulseamps : \n            If we triggered on a pulse, the optimum amplitude at the pulse trigger time. Otherwise this is zero.\n        trigtimes : ndarray\n            If we triggered due to ttl, the time of the ttl trigger in seconds. Otherwise this is zero.\n        pulseamps : \n            If we triggered due to ttl, the optimum amplitude at the ttl trigger time. Otherwise this is zero.\n        traces : ndarray\n            The corresponding trace for each detected event.\n        trigtypes: ndarray\n            Array of boolean vectors each of length 3. The first value indicates if the trace is a random or not.\n            The second value indicates if we had a pulse trigger. The third value indicates if we had a ttl trigger.\n            \n    '

    def __init__(self, fs, template, noisepsd, tracelength, trigtemplate=None):
        """
        Initialization of the FIR filter.
        
        Parameters
        ----------
            fs : float
                The sample rate of the data (Hz)
            template : ndarray
                The pulse template to be used when creating the optimum filter (assumed to be normalized)
            noisepsd : ndarray
                The two-sided power spectral density in units of A^2/Hz
            tracelength : int
                The desired trace length (in bins) to be saved when triggering on events.
            trigtemplate : NoneType, ndarray, optional
                The template for the trigger channel pulse. If left as None, then the trigger channel will not
                be analyzed.
        
        """
        self.tracelength = tracelength
        self.fs = fs
        self.template = template
        self.noisepsd = noisepsd
        self.phi = ifft(fft(self.template) / self.noisepsd).real
        self.norm = np.dot(self.phi, self.template)
        self.resolution = 1 / (np.dot(self.phi, self.template) / self.fs) ** 0.5
        tmax_ind = np.argmax(self.template)
        half_pulse_ind = np.argmin(abs(self.template[tmax_ind:] - self.template[tmax_ind] / 2)) + tmax_ind
        self.pulse_range = half_pulse_ind - tmax_ind
        self.trigtemplate = trigtemplate
        if trigtemplate is not None:
            self.trignorm = np.dot(trigtemplate, trigtemplate)
        else:
            self.trignorm = None
        self.traces = None
        self.filts = None
        self.times = None
        self.trig = None
        self.trigfilts = None
        self.pulsetimes = None
        self.pulseamps = None
        self.trigtimes = None
        self.trigamps = None
        self.evttraces = None
        self.trigtypes = None

    def filtertraces(self, traces, times, trig=None):
        """
        Method to apply the FIR filter the inputted traces with specified times.
        
        Parameters
        ----------
            traces : ndarray
                All of the traces to be filtered, assumed to be an ndarray of 
                shape = (# of traces, # of channels, # of trace bins). Should be in units of Amps.
            times : ndarray
                The absolute start time of each trace (in s), should be a 1-dimensional ndarray.
            trig : NoneType, ndarray, optional
                The trigger channel traces to be filtered using the trigtemplate (if it exists). If
                left as None, then only the traces are analyzed. If the trigtemplate attribute
                has not been set, but this was set, then an error is raised.
        
        """
        self.traces = traces
        self.times = times
        self.trig = trig
        pulsestot = np.sum(traces, axis=1)
        self.filts = np.array([correlate(trace, (self.phi), mode='same') / self.norm for trace in pulsestot])
        cut_len = np.max([len(self.phi), self.tracelength])
        self.filts[:, :cut_len // 2] = 0.0
        self.filts[:, -(cut_len // 2) + (cut_len + 1) % 2:] = 0.0
        if self.trigtemplate is None:
            if trig is not None:
                raise ValueError('trig values have been inputted, but trigtemplate attribute has not been set, cannot filter the trig values')
        if trig is not None:
            self.trigfilts = np.array([np.correlate(trace, (self.trigtemplate), mode='same') / self.trignorm for trace in trig])
            self.trigfilts[:, :cut_len // 2] = 0.0
            self.trigfilts[:, -(cut_len // 2) + (cut_len + 1) % 2:] = 0.0

    def eventtrigger(self, thresh, trigthresh=None, positivepulses=True):
        """
        Method to detect events in the traces with an optimum amplitude greater than the specified threshold.
        Note that this may return duplicate events, so care should be taken in post-processing to get rid of 
        such events.
           
        Parameters
        ----------
            thresh : float
                The number of standard deviations of the energy resolution to use as the threshold for which events
                will be detected as a pulse.
            trigthresh : NoneType, float, optional
                The threshold value (in units of the trigger channel) such that any amplitudes higher than this will be 
                detected as ttl trigger event. If left as None, then only the pulses are analyzed.
            positivepulses : boolean, optional
                Boolean flag for which direction the pulses go in the traces. If they go in the positive direction, 
                then this should be set to True. If they go in the negative direction, then this should be set to False.
                Default is True.
        
        """
        pulseamps_list = []
        pulsetimes_list = []
        trigamps_list = []
        trigtimes_list = []
        traces_list = []
        trigtypes_list = []
        for ii, filt in enumerate(self.filts):
            if self.trigfilts is None or trigthresh is None:
                if positivepulses:
                    evts_mask = filt > thresh * self.resolution
                else:
                    evts_mask = filt < -thresh * self.resolution
                evts = np.where(evts_mask)[0]
                ranges = getchangeslessthanthresh(evts, self.pulse_range)[0]
                trigtypes = np.zeros((len(ranges), 3), dtype=bool)
                trigtypes[:, 1] = True
            else:
                if trigthresh is not None:
                    if positivepulses:
                        pulseevts_mask = filt > thresh * self.resolution
                    else:
                        pulseevts_mask = filt < -thresh * self.resolution
                    pulseevts = np.where(pulseevts_mask)[0]
                    pulseranges, pulsevals = getchangeslessthanthresh(pulseevts, self.pulse_range)
                    pulse_mask = np.zeros((self.filts[ii].shape), dtype=bool)
                    for evt_range in pulseranges:
                        if evt_range[1] > evt_range[0]:
                            evt_inds = pulseevts[evt_range[0]:evt_range[1]]
                            pulse_mask[evt_inds] = True

                    trigevts_mask = self.trigfilts[ii] > trigthresh
                    trigevts = np.where(trigevts_mask)[0]
                    trigranges, trigvals = getchangeslessthanthresh(trigevts, 1)
                    tot_mask = np.logical_or(trigevts_mask, pulse_mask)
                    evts = np.where(tot_mask)[0]
                    ranges, totvals = getchangeslessthanthresh(evts, self.pulse_range)
                    trigtypes = np.zeros((len(ranges), 3), dtype=bool)
                    for ival, vals in enumerate(totvals):
                        for v in pulsevals:
                            if np.any(inrange(v, vals)):
                                trigtypes[(ival, 1)] = True

                        for v in trigvals:
                            if np.any(inrange(v, vals)):
                                trigtypes[(ival, 2)] = True

                pulseamps = []
                pulsetimes = []
                trigamps = []
                trigtimes = []
                traces = []
                for irange, evt_range in enumerate(ranges):
                    if evt_range[1] > evt_range[0]:
                        evt_inds = evts[evt_range[0]:evt_range[1]]
                        if trigtypes[irange][2]:
                            evt_ind = evt_inds[np.argmax(self.trigfilts[ii][evt_inds])]
                        else:
                            if positivepulses:
                                evt_ind = evt_inds[np.argmax(filt[evt_inds])]
                            else:
                                evt_ind = evt_inds[np.argmin(filt[evt_inds])]
                            if trigtypes[irange][1]:
                                if trigtypes[irange][2]:
                                    if positivepulses:
                                        pulse_ind = evt_inds[np.argmax(filt[evt_inds])]
                                    else:
                                        pulse_ind = evt_inds[np.argmin(filt[evt_inds])]
                                    pulsetimes.append(pulse_ind / self.fs + self.times[ii])
                                    pulseamps.append(filt[pulse_ind])
                                    trigtimes.append(evt_ind / self.fs + self.times[ii])
                                    trigamps.append(filt[evt_ind])
                            if trigtypes[irange][2]:
                                pulsetimes.append(0.0)
                                pulseamps.append(0.0)
                                trigtimes.append(evt_ind / self.fs + self.times[ii])
                                trigamps.append(filt[evt_ind])
                            else:
                                pulsetimes.append(evt_ind / self.fs + self.times[ii])
                                pulseamps.append(filt[evt_ind])
                                trigtimes.append(0.0)
                                trigamps.append(0.0)
                        traces.append(self.traces[ii, ...,
                         evt_ind - self.tracelength // 2:evt_ind + self.tracelength // 2 + self.tracelength % 2])

                pulsetimes = np.array(pulsetimes)
                pulseamps = np.array(pulseamps)
                trigtimes = np.array(trigtimes)
                trigamps = np.array(trigamps)
                traces = np.array(traces)
                if np.any(trigtypes):
                    trigtypes = np.vstack([r for r in trigtypes if np.any(r)])
                else:
                    trigtypes = np.array([])
            pulsetimes_list.append(pulsetimes)
            pulseamps_list.append(pulseamps)
            trigtimes_list.append(trigtimes)
            trigamps_list.append(trigamps)
            traces_list.append(traces)
            trigtypes_list.append(trigtypes)

        self.pulsetimes = np.concatenate(pulsetimes_list)
        self.pulseamps = np.concatenate(pulseamps_list)
        self.trigtimes = np.concatenate(trigtimes_list)
        self.trigamps = np.concatenate(trigamps_list)
        if len(self.pulseamps) == 0:
            self.evttraces = np.array([])
            self.trigtypes = np.array([])
        else:
            self.evttraces = np.vstack([t for t in traces_list if len(t) > 0])
            self.trigtypes = np.vstack([t for t in trigtypes_list if len(t) > 0])


def optimumfilt_wrapper(filelist, template, noisepsd, tracelength, thresh, trigtemplate=None, trigthresh=None, positivepulses=True, iotype='stanford'):
    """
    Wrapper function for the OptimumFilt class for running the continuous trigger on many different files. This allows 
    the user to input a list of files that should be analyzed.
    
    Parameters
    ----------
        filelist : list of strings
            List of files to be opened to take random sections from (should be full paths)
        template : ndarray
            The pulse template to be used when creating the optimum filter (assumed to be normalized)
        noisepsd : ndarray
            The two-sided power spectral density in units of A^2/Hz
        tracelength : int
            The desired trace length (in bins) to be saved when triggering on events.
        thresh : float
            The number of standard deviations of the energy resolution to use as the threshold for which events
            will be detected as a pulse.
        trigtemplate : NoneType, ndarray, optional
            The template for the trigger channel pulse. If left as None, then the trigger channel will not
            be analyzed.
        trigthresh : NoneType, float, optional
            The threshold value (in units of the trigger channel) such that any amplitudes higher than this will be 
            detected as ttl trigger event. If left as None, then only the pulses are analyzed.
        positivepulses : boolean, optional
            Boolean flag for which direction the pulses go in the traces. If they go in the positive direction, 
            then this should be set to True. If they go in the negative direction, then this should be set to False.
            Default is True.
        iotype : string, optional
            Type of file to open, uses a different IO function. Default is "stanford".
                "stanford" : Use pycdms.io.loadstanfordfile to open the files
                
    Returns
    -------
        pulsetimes : ndarray
            If we triggered on a pulse, the time of the pulse trigger in seconds. Otherwise this is zero.
        pulseamps : 
            If we triggered on a pulse, the optimum amplitude at the pulse trigger time. Otherwise this is zero.
        trigtimes : ndarray
            If we triggered due to ttl, the time of the ttl trigger in seconds. Otherwise this is zero.
        trigamps : 
            If we triggered due to ttl, the optimum amplitude at the ttl trigger time. Otherwise this is zero.
        traces : ndarray
            The corresponding trace for each detected event.
        trigtypes: ndarray
            Array of boolean vectors each of length 3. The first value indicates if the trace is a random or not.
            The second value indicates if we had a pulse trigger. The third value indicates if we had a ttl trigger.
            
    """
    if type(filelist) == str:
        filelist = [
         filelist]
    else:
        pulsetimes_list = []
        pulseamps_list = []
        trigtimes_list = []
        trigamps_list = []
        traces_list = []
        trigtypes_list = []
        for f in filelist:
            if iotype == 'stanford':
                traces, times, fs, trig = loadstanfordfile(f)
                if trigtemplate is None:
                    trig = None
            else:
                raise ValueError('Unrecognized iotype inputted.')
            filt = OptimumFilt(fs, template, noisepsd, tracelength, trigtemplate=trigtemplate)
            filt.filtertraces(traces, times, trig=trig)
            filt.eventtrigger(thresh, trigthresh=trigthresh)
            pulsetimes_list.append(filt.pulsetimes)
            pulseamps_list.append(filt.pulseamps)
            trigtimes_list.append(filt.trigtimes)
            trigamps_list.append(filt.trigamps)
            traces_list.append(filt.evttraces)
            trigtypes_list.append(filt.trigtypes)

        pulsetimes = np.concatenate(pulsetimes_list)
        pulseamps = np.concatenate(pulseamps_list)
        trigtimes = np.concatenate(trigtimes_list)
        trigamps = np.concatenate(trigamps_list)
        if len(pulseamps) == 0:
            traces = np.array([])
            trigtypes = np.array([])
        else:
            traces = np.vstack([t for t in traces_list if len(t) > 0])
        trigtypes = np.vstack([t for t in trigtypes_list if len(t) > 0])
    return (pulsetimes, pulseamps, trigtimes, trigamps, traces, trigtypes)
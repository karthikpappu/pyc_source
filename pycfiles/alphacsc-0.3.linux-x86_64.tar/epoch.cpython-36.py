# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/viz/epoch.py
# Compiled at: 2019-06-04 04:10:26
# Size of source mod 2**32: 4173 bytes
from copy import deepcopy
import mne, numpy as np
from joblib import Parallel, delayed

def make_epochs(z_hat, info, t_lim, n_times_atom=1):
    """Make Epochs on the activations of atoms.
    n_splits, n_atoms, n_times_valid = z_hat.shape
    n_trials, n_atoms, n_times_epoch = z_hat_epoch.shape
    """
    n_splits, n_atoms, n_times_valid = z_hat.shape
    n_times = n_times_valid + n_times_atom - 1
    padding = np.zeros((n_splits, n_atoms, n_times_atom - 1))
    z_hat = np.concatenate([z_hat, padding], axis=2)
    z_hat = np.reshape(z_hat.swapaxes(0, 1), (n_atoms, n_splits * n_times))
    new_info = mne.create_info(ch_names=n_atoms, sfreq=(info['sfreq']))
    rawarray = mne.io.RawArray(data=z_hat, info=new_info, verbose=False)
    t_min, t_max = t_lim
    epochs = mne.Epochs(rawarray, (info['events']), (info['event_id']), t_min, t_max,
      verbose=False)
    z_hat_epoched = epochs.get_data()
    return z_hat_epoched


def make_evoke(array, info, t_lim):
    """Compute evoked activations"""
    if array.ndim == 1:
        array = array[(None, None)]
    else:
        if array.ndim == 2:
            array = array[None]
    epoched_array = make_epochs(array, info, t_lim=t_lim)
    evoked_array = epoched_array.mean(axis=0)
    return evoked_array


def make_evoke_one_surrogate(array, info, t_lim):
    info = deepcopy(info)
    n_events = info['events'].shape[0]
    events = np.random.randint((array.shape[(-1)]), size=n_events)
    events = np.sort(np.unique(events))
    n_events = events.shape[0]
    event_id = np.atleast_1d(info['event_id']).astype('int')
    n_tile = int(np.ceil(n_events / float(event_id.shape[0])))
    event_id_tiled = np.tile(event_id, n_tile)[:n_events]
    events = np.c_[(events, np.zeros_like(events), event_id_tiled)]
    info['events'] = events
    evoked_array = make_evoke(array, info, t_lim)
    return evoked_array


def make_evoke_all_surrogates(array, info, t_lim, n_jobs, n_surrogates=100):
    delayed_func = delayed(make_evoke_one_surrogate)
    evoked_arrays = Parallel(n_jobs=n_jobs)(delayed_func(array, info, t_lim) for i in range(n_surrogates))
    return np.array(evoked_arrays)


def plot_evoked_surrogates(array, info, t_lim, ax, n_jobs, label='', threshold=0.005):
    """Compute and plot evoked array distribution over random events"""
    if not array.ndim == 1:
        raise AssertionError
    elif not ax is not None:
        raise AssertionError
    evoked = make_evoke(array, info, t_lim)[0]
    evoked_surrogate = make_evoke_all_surrogates(array, info, t_lim, n_jobs)[:, 0]
    low, high = 100 * threshold / 2.0, 100 * (1 - threshold / 2.0)
    threshold_low = np.percentile(evoked_surrogate.min(axis=1), low)
    threshold_high = np.percentile(evoked_surrogate.max(axis=1), high)
    t = np.arange(len(evoked)) / info['sfreq'] + t_lim[0]
    outside_thresholds = (evoked > threshold_high) + (evoked < threshold_low)
    color = 'C1' if np.any(outside_thresholds) else 'C2'
    ax.plot(t, evoked, label=label, color=color)
    label_th = str(100 * (1 - threshold)) + ' %'
    ax.fill_between(t, threshold_low, threshold_high, color='k', alpha=0.2, label=label_th)
    ax.fill_between(t, threshold_low, threshold_high, where=outside_thresholds, color='y',
      alpha=0.2)
    ax.axvline(0, color='k', linestyle='--')
    ax.set_ylim([0, None])
    ax.legend()
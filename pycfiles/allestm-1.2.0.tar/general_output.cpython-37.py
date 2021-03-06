# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mx/Dropbox (MIT)/Science/Code/allesfitter/allesfitter/general_output.py
# Compiled at: 2020-03-31 06:08:08
# Size of source mod 2**32: 43282 bytes
__doc__ = '\nCreated on Fri Oct  5 01:10:51 2018\n\n@author:\nMaximilian N. Günther\nMIT Kavli Institute for Astrophysics and Space Research, \nMassachusetts Institute of Technology,\n77 Massachusetts Avenue,\nCambridge, MA 02109, \nUSA\nEmail: maxgue@mit.edu\nWeb: www.mnguenther.com\n'
from __future__ import print_function, division, absolute_import
import seaborn as sns
sns.set(context='paper', style='ticks', palette='deep', font='sans-serif', font_scale=1.5, color_codes=True)
sns.set_style({'xtick.direction':'in',  'ytick.direction':'in'})
sns.set_context(rc={'lines.markeredgewidth': 1})
import numpy as np
import matplotlib.pyplot as plt
import os, sys, warnings
from astropy.time import Time
from tqdm import tqdm
warnings.filterwarnings('ignore', category=(np.VisibleDeprecationWarning))
warnings.filterwarnings('ignore', category=(np.RankWarning))
from . import config
from .utils import latex_printer
from .computer import update_params, calculate_model, rv_fct, flux_fct, calculate_baseline, calculate_stellar_var, calculate_yerr_w
import exoworlds_rdx.lightcurves as lct
from exoworlds_rdx.lightcurves.index_transits import get_tmid_observed_transits

class bcolors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def logprint(*text, typ='default'):
    if config.BASEMENT.settings['print_progress']:
        if typ == 'default':
            print(*text)
        elif typ == 'success':
            fulltext = ' '.join([str(t) for t in text])
            print(bcolors.OKGREEN + fulltext + bcolors.ENDC)
        elif typ == 'warning':
            fulltext = ' '.join([str(t) for t in text])
            print(bcolors.WARNING + fulltext + bcolors.ENDC)
        elif typ == 'failure':
            fulltext = ' '.join([str(t) for t in text])
            print(bcolors.FAIL + fulltext + bcolors.ENDC)
    original = sys.stdout
    try:
        with open(os.path.join(config.BASEMENT.outdir, 'logfile_' + config.BASEMENT.now + '.log'), 'a') as (f):
            sys.stdout = f
            print(*text)
    except OSError:
        pass

    sys.stdout = original


def draw_initial_guess_samples(Nsamples=1):
    if Nsamples == 1:
        samples = np.array([config.BASEMENT.theta_0])
    else:
        samples = config.BASEMENT.theta_0 + config.BASEMENT.init_err * np.random.randn(Nsamples, len(config.BASEMENT.theta_0))
    return samples


def plot_panel(datadir):
    config.init(datadir)
    if len(config.BASEMENT.settings['inst_phot']) > 0 and len(config.BASEMENT.settings['inst_rv']) > 0:
        fig, axes = plt.subplots(2, 1, figsize=(20, 10))
    elif len(config.BASEMENT.settings['inst_phot']) > 0:
        fig, axes = plt.subplots(1, 1, figsize=(20, 5))
        axes = [axes]
    elif len(config.BASEMENT.settings['inst_rv']) > 0:
        fig, axes = plt.subplots(1, 1, figsize=(20, 5))
        axes = [None, axes]
    for inst in config.BASEMENT.settings['inst_phot']:
        ax = axes[0]
        ax.plot((config.BASEMENT.fulldata[inst]['time']), (config.BASEMENT.fulldata[inst]['flux']), marker='.', ls='none', color='lightgrey', rasterized=True)
        ax.plot((config.BASEMENT.data[inst]['time']), (config.BASEMENT.data[inst]['flux']), marker='.', ls='none', label=inst, rasterized=True)
        ax.legend()
        ax.set(ylabel='Relative Flux', xlabel='Time (BJD)')

    for inst in config.BASEMENT.settings['inst_rv']:
        ax = axes[1]
        ax.plot((config.BASEMENT.data[inst]['time']), (config.BASEMENT.data[inst]['rv']), marker='.', ls='none', label=inst)
        ax.legend()
        ax.set(ylabel='RV (km/s)', xlabel='Time (BJD)')

    fig.savefig((os.path.join(config.BASEMENT.outdir, 'data_panel.pdf')), bbox_inches='tight')
    return (
     fig, axes)


def plot_panel_transits(datadir, ax=None, insts=None, companions=None, colors=None, title=None, ppm=False, ylim=None, yticks=None, fontscale=2):
    config.init(datadir)
    SMALL_SIZE = 8 * fontscale
    MEDIUM_SIZE = 10 * fontscale
    BIGGER_SIZE = 12 * fontscale
    plt.rc('font', size=MEDIUM_SIZE)
    plt.rc('axes', titlesize=BIGGER_SIZE)
    plt.rc('axes', labelsize=BIGGER_SIZE)
    plt.rc('xtick', labelsize=MEDIUM_SIZE)
    plt.rc('ytick', labelsize=MEDIUM_SIZE)
    plt.rc('legend', fontsize=MEDIUM_SIZE)
    plt.rc('figure', titlesize=BIGGER_SIZE)
    samples = draw_initial_guess_samples()
    params_median, params_ll, params_ul = get_params_from_samples(samples)
    if companions is None:
        companions = config.BASEMENT.settings['companions_phot']
    else:
        if colors is None:
            colors = [sns.color_palette('deep')[i] for i in (0, 1, 3)]
        else:
            if insts is None:
                insts = config.BASEMENT.settings['inst_phot']
            ally = []
            if ax is None:
                ax_init = None
                fig, axes = plt.subplots((len(insts)), (len(companions)), figsize=(6 * len(companions), 4 * len(insts)), sharey=True, sharex=True)
                axes = np.atleast_2d(axes).T
            else:
                ax_init = ax
            axes = np.atleast_2d(ax).T
        for i, (companion, color) in enumerate(zip(companions, colors)):
            for j, inst in enumerate(insts):
                ax = axes[(i, j)]
                key = 'flux'
                if title is None:
                    if i == 0:
                        title = inst
                    else:
                        title = ''
                else:
                    if j == len(insts) - 1:
                        xlabel = '$\\mathrm{ T - T_0 \\ (h) }$'
                    else:
                        xlabel = ''
                    if i == 0:
                        if ppm:
                            ylabel = '$\\Delta$ Flux (ppm)'
                        else:
                            ylabel = 'Relative Flux'
                    else:
                        ylabel = ''
                alpha = 1.0
                x = config.BASEMENT.data[inst]['time']
                baseline_median = calculate_baseline(params_median, inst, key)
                y = config.BASEMENT.data[inst][key] - baseline_median
                zoomfactor = params_median[(companion + '_period')] * 24.0
                for other_companion in config.BASEMENT.settings['companions_phot']:
                    if companion != other_companion:
                        model = flux_fct(params_median, inst, other_companion)
                        y -= model
                        y += 1.0

                if ppm:
                    y = (y - 1) * 1000000.0
                dt = 0.013888888888888888 / params_median[(companion + '_period')]
                phase_time, phase_y, phase_y_err, _, phi = lct.phase_fold(x, y, (params_median[(companion + '_period')]), (params_median[(companion + '_epoch')]), dt=dt, ferr_type='meansig', ferr_style='sem', sigmaclip=True)
                ax.plot((phi * zoomfactor), y, 'b.', color='silver', rasterized=True)
                ax.errorbar((phase_time * zoomfactor), phase_y, yerr=phase_y_err, linestyle='none', marker='o', ms=8, color=color, capsize=0, zorder=11)
                ax.set_xlabel(xlabel, fontsize=BIGGER_SIZE)
                ax.set_ylabel(ylabel, fontsize=BIGGER_SIZE)
                ax.text(0.97, 0.87, companion, ha='right', va='bottom', transform=(ax.transAxes), fontsize=BIGGER_SIZE)
                ax.text(0.03, 0.87, title, ha='left', va='bottom', transform=(ax.transAxes), fontsize=MEDIUM_SIZE)
                ally += list(phase_y)
                xx = np.linspace(-4.0 / zoomfactor, 4.0 / zoomfactor, 1000)
                xx2 = params_median[(companion + '_epoch')] + np.linspace(-4.0 / zoomfactor, 4.0 / zoomfactor, 1000) * params_median[(companion + '_period')]
                for ii in range(samples.shape[0]):
                    s = samples[ii, :]
                    p = update_params(s)
                    model = flux_fct(p, inst, companion, xx=xx2)
                    if ppm:
                        model = (model - 1) * 1000000.0
                    ax.plot((xx * zoomfactor), model, 'r-', alpha=alpha, zorder=12, lw=2)

        if ppm:
            ylim0 = np.nanmin(ally) - 500
            ylim1 = np.nanmax(ally) + 500
        else:
            ylim0 = np.nanmin(ally) - 0.0005
        ylim1 = np.nanmax(ally) + 0.0005
    if ylim is None:
        ylim = [
         ylim0, ylim1]
    for i in range(len(companions)):
        for j in range(len(insts)):
            ax = axes[(i, j)]
            ax.set(xlim=[-4, 4], ylim=ylim)
            if yticks is not None:
                ax.set(yticks=yticks)
            ax.set_xticklabels(ax.get_xticks(), {'fontsize': MEDIUM_SIZE})
            ax.set_yticklabels(ax.get_yticks(), {'fontsize': MEDIUM_SIZE})

    plt.tight_layout()
    if ax_init is None:
        fig.savefig((os.path.join(config.BASEMENT.outdir, 'data_panel_transits.pdf')), bbox_inches='tight')
        return (
         fig, axes)
    return ax


def afplot(samples, companion):
    """
    Inputs:
    -------
    samples : array
        samples from the initial guess, or from the MCMC / Nested Sampling posteriors
    """
    N_inst = len(config.BASEMENT.settings['inst_all'])
    if 'do_not_phase_fold' in config.BASEMENT.settings and config.BASEMENT.settings['do_not_phase_fold']:
        fig, axes = plt.subplots(N_inst, 1, figsize=(6, 4 * N_inst))
        styles = ['full']
    elif config.BASEMENT.settings['phase_curve']:
        fig, axes = plt.subplots(N_inst, 5, figsize=(30, 4 * N_inst))
        styles = ['full', 'phase', 'phase_curve', 'phasezoom', 'phasezoom_occ']
    elif config.BASEMENT.settings['secondary_eclipse']:
        fig, axes = plt.subplots(N_inst, 4, figsize=(24, 4 * N_inst))
        styles = ['full', 'phase', 'phasezoom', 'phasezoom_occ']
    else:
        fig, axes = plt.subplots(N_inst, 3, figsize=(18, 4 * N_inst))
        styles = ['full', 'phase', 'phasezoom']
    axes = np.atleast_2d(axes)
    for i, inst in enumerate(config.BASEMENT.settings['inst_all']):
        for j, style in enumerate(styles):
            if ('zoom' in style) & (inst in config.BASEMENT.settings['inst_rv']):
                axes[(i, j)].axis('off')
            elif (inst in config.BASEMENT.settings['inst_phot']) & (companion not in config.BASEMENT.settings['companions_phot']):
                axes[(i, j)].axis('off')
            elif (inst in config.BASEMENT.settings['inst_rv']) & (companion not in config.BASEMENT.settings['companions_rv']):
                axes[(i, j)].axis('off')
            else:
                plot_1(axes[(i, j)], samples, inst, companion, style)

    plt.tight_layout()
    return (
     fig, axes)


def plot_1(ax, samples, inst, companion, style, base=None, dt=None, zoomwindow=8.0, kwargs_data=None, kwargs_model=None, kwargs_ax=None):
    """
    Inputs:
    -------
    ax : matplotlib axis
    
    samples : array
        Prior or posterior samples to plot the fit from
    
    inst: str
        Name of the instrument (e.g. 'TESS')
        
    companion : None or str
        None or 'b'/'c'/etc.
        
    style: str
        'full' / 'per_transit' / 'phase' / 'phasezoom' / 'phasezoom_occ' /'phase_curve'
        'full_residuals' / 'phase_residuals' / 'phasezoom_residuals' / 'phasezoom_occ_residuals' / 'phase_curve_residuals'
    
    zoomwindow: int or float
        the full width of the window to zoom into (in hours)
        default: 8 hours
    
    base: a BASEMENT class object
        (for internal use only)
        
    dt : float
        time steps on which the model should be evaluated for plots
        in days
        default for style='full': 2 min for <1 day of data; 30 min for >1 day of data.
        
    Notes:
    ------
    yerr / epoch / period: 
        come either from
        a) the initial_guess value or 
        b) the MCMC median,
        depending on what is plotted (i.e. not from individual samples)

    """
    if base == None:
        base = config.BASEMENT
    elif samples is not None:
        params_median, params_ll, params_ul = get_params_from_samples(samples)
    elif kwargs_data is None:
        kwargs_data = {}
    else:
        if 'marker' not in kwargs_data:
            kwargs_data['marker'] = '.'
        else:
            if 'markersize' not in kwargs_data:
                kwargs_data['markersize'] = 8.0
            elif 'linestyle' not in kwargs_data:
                kwargs_data['linestyle'] = 'none'
            elif 'color' not in kwargs_data:
                kwargs_data['color'] = 'b'
            elif 'alpha' not in kwargs_data:
                kwargs_data['alpha'] = 1.0
            else:
                if 'rasterized' not in kwargs_data:
                    kwargs_data['rasterized'] = True
                if kwargs_model is None:
                    kwargs_model = {}
                if 'marker' not in kwargs_model:
                    kwargs_model['marker'] = 'none'
                if 'markersize' not in kwargs_model:
                    kwargs_model['markersize'] = 0.0
                if 'linestyle' not in kwargs_model:
                    kwargs_model['linestyle'] = '-'
                if 'color' not in kwargs_model:
                    kwargs_model['color'] = 'r'
                if 'alpha' not in kwargs_model:
                    kwargs_model['alpha'] = 1.0
                if kwargs_ax is None:
                    kwargs_ax = {}
                if 'title' not in kwargs_ax:
                    kwargs_ax['title'] = None
                if 'xlabel' not in kwargs_ax:
                    kwargs_ax['xlabel'] = None
                if 'ylabel' not in kwargs_ax:
                    kwargs_ax['ylabel'] = None
                timelabel = 'Time'

                def set_title(title1):
                    if kwargs_ax['title'] is None:
                        return title1
                    return kwargs_ax['title']

                if inst in base.settings['inst_phot']:
                    key = 'flux'
                    baseline_plus = 1.0
                    if style in ('full', ):
                        ylabel = 'Relative Flux'
                    elif style in ('phase', 'phasezoom', 'phasezoom_occ', 'phase_curve'):
                        ylabel = 'Relative Flux - Baseline'
                    elif style in ('full_residuals', 'phase_residuals', 'phasezoom_residuals',
                                   'phasezoom_occ_residuals', 'phase_curve_residuals'):
                        ylabel = 'Residuals'
                elif inst in base.settings['inst_rv']:
                    key = 'rv'
                    baseline_plus = 0.0
                    if style in ('full', ):
                        ylabel = 'RV (km/s)'
                    elif style in ('phase', 'phasezoom', 'phasezoom_occ', 'phase_curve'):
                        ylabel = 'RV (km/s) - Baseline'
                    elif style in ('full_residuals', 'phase_residuals', 'phasezoom_residuals',
                                   'phasezoom_occ_residuals', 'phase_curve_residuals'):
                        ylabel = 'Residuals'
                else:
                    raise ValueError('inst should be listed in inst_phot or inst_rv...')
            if samples is not None:
                if samples.shape[0] == 1:
                    alpha = 1.0
                else:
                    alpha = 0.1
        if style in ('full', 'full_residuals'):
            x = base.data[inst]['time']
            if timelabel == 'Time_since':
                x = np.copy(x)
                objttime = Time(x, format='jd', scale='utc')
                xsave = np.copy(x)
                x -= x[0]
            else:
                y = 1.0 * base.data[inst][key]
                yerr_w = calculate_yerr_w(params_median, inst, key)
                if style in ('full_residuals', ):
                    model = calculate_model(params_median, inst, key)
                    baseline = calculate_baseline(params_median, inst, key)
                    stellar_var = calculate_stellar_var(params_median, 'all', key, xx=x)
                    y -= model + baseline + stellar_var
                ax.errorbar(x, y, yerr=yerr_w, marker=(kwargs_data['marker']), markersize=(kwargs_data['markersize']), linestyle=(kwargs_data['linestyle']), color=(kwargs_data['color']), alpha=(kwargs_data['alpha']), capsize=0, rasterized=(kwargs_data['rasterized']))
                if base.settings['color_plot']:
                    ax.scatter(x, y, c=x, marker='o', rasterized=(kwargs_data['rasterized']), cmap='inferno', zorder=11)
                if timelabel == 'Time_since':
                    ax.set(xlabel=('Time since %s [days]' % objttime[0].isot[:10]), ylabel=ylabel, title=(set_title(inst)))
                elif timelabel == 'Time':
                    ax.set(xlabel='Time (BJD)', ylabel=ylabel, title=(set_title(inst)))
            if style in ('full', ):
                if samples is not None:
                    if dt is None:
                        if x[(-1)] - x[0] < 1:
                            dt = 0.0013888888888888887
                        else:
                            dt = 0.020833333333333332
                    if key == 'flux':
                        xx_full = np.arange(x[0], x[(-1)] + dt, dt)
                        Npoints_chunk = 48
                        for i_chunk in tqdm(range(int(1.0 * len(xx_full) / Npoints_chunk) + 2)):
                            xx = xx_full[i_chunk * Npoints_chunk:(i_chunk + 1) * Npoints_chunk]
                            if len(xx) > 0 and any((x > xx[0]) & (x < xx[(-1)])):
                                for i in range(samples.shape[0]):
                                    s = samples[i, :]
                                    p = update_params(s)
                                    model = calculate_model(p, inst, key, xx=xx)
                                    baseline = calculate_baseline(p, inst, key, xx=xx)
                                    stellar_var = calculate_stellar_var(p, 'all', key, xx=xx)
                                    ax.plot(xx, (baseline + stellar_var + baseline_plus), 'k-', color='orange', alpha=alpha, zorder=12)
                                    ax.plot(xx, (model + baseline + stellar_var), 'r-', alpha=alpha, zorder=12)

                    elif key == 'rv':
                        xx = np.arange(x[0], x[(-1)] + dt, dt)
                        for i in range(samples.shape[0]):
                            s = samples[i, :]
                            p = update_params(s)
                            model = calculate_model(p, inst, key, xx=xx)
                            baseline = calculate_baseline(p, inst, key, xx=xx)
                            stellar_var = calculate_stellar_var(p, 'all', key, xx=xx)
                            ax.plot(xx, (baseline + stellar_var + baseline_plus), 'k-', color='orange', alpha=alpha, zorder=12)
                            ax.plot(xx, (model + baseline + stellar_var), 'r-', alpha=alpha, zorder=12)

            if timelabel == 'Time_since':
                x = np.copy(xsave)
        elif style in ('phase', 'phasezoom', 'phasezoom_occ', 'phase_curve', 'phase_residuals',
                       'phasezoom_residuals', 'phasezoom_occ_residuals', 'phase_curve_residuals'):
            x = 1.0 * base.data[inst]['time']
            baseline_median = calculate_baseline(params_median, inst, key)
            stellar_var_median = calculate_stellar_var(params_median, 'all', key, xx=x)
            y = base.data[inst][key] - baseline_median - stellar_var_median
            yerr_w = calculate_yerr_w(params_median, inst, key)
            if style in ('phasezoom', 'phasezoom_occ', 'phasezoom_residuals', 'phasezoom_occ_residuals'):
                zoomfactor = params_median[(companion + '_period')] * 24.0
            else:
                zoomfactor = 1.0
            if inst in base.settings['inst_rv']:
                for other_companion in base.settings['companions_rv']:
                    if companion != other_companion:
                        model = rv_fct(params_median, inst, other_companion)[0]
                        y -= model

                if style in ('phase_residuals', 'phasezoom_residuals', 'phasezoom_occ_residuals',
                             'phase_curve_residuals'):
                    model = rv_fct(params_median, inst, companion)[0]
                    y -= model
                else:
                    phase_time, phase_y, phase_y_err, _, phi = lct.phase_fold(x, y, (params_median[(companion + '_period')]), (params_median[(companion + '_epoch')]), dt=0.002, ferr_type='meansig', ferr_style='sem', sigmaclip=False)
                    if len(x) > 500:
                        ax.plot((phi * zoomfactor), y, 'k.', color='lightgrey', rasterized=(kwargs_data['rasterized']))
                        ax.errorbar((phase_time * zoomfactor), phase_y, yerr=phase_y_err, marker=(kwargs_data['marker']), markersize=(kwargs_data['markersize']), linestyle=(kwargs_data['linestyle']), color=(kwargs_data['color']), alpha=(kwargs_data['alpha']), capsize=0, rasterized=(kwargs_data['rasterized']), zorder=11)
                    else:
                        ax.errorbar((phi * zoomfactor), y, yerr=yerr_w, marker=(kwargs_data['marker']), markersize=(kwargs_data['markersize']), linestyle=(kwargs_data['linestyle']), color=(kwargs_data['color']), alpha=(kwargs_data['alpha']), capsize=0, rasterized=(kwargs_data['rasterized']), zorder=11)
                ax.set(xlabel='Phase', ylabel=ylabel, title=(set_title(inst + ', companion ' + companion + ' only')))
                if style in ('phase', 'phasezoom', 'phasezoom_occ', 'phase_curve'):
                    if samples is not None:
                        xx = np.linspace(-0.25, 0.75, 1000)
                        xx2 = params_median[(companion + '_epoch')] + np.linspace(-0.25, 0.75, 1000) * params_median[(companion + '_period')]
                        for i in range(samples.shape[0]):
                            s = samples[i, :]
                            p = update_params(s)
                            model = rv_fct(p, inst, companion, xx=xx2)[0]
                            ax.plot((xx * zoomfactor), model, 'r-', alpha=alpha, zorder=12)

                    elif inst in base.settings['inst_phot']:
                        for other_companion in base.settings['companions_phot']:
                            if companion != other_companion:
                                model = flux_fct(params_median, inst, other_companion)
                                y -= model - 1.0

                        if style in ('phase_residuals', 'phasezoom_residuals', 'phasezoom_occ_residuals',
                                     'phase_curve_residuals'):
                            model = flux_fct(params_median, inst, companion)
                            y -= model
                        elif style in ('phase', 'phase_residuals'):
                            dt = 0.002
                        elif style in ('phase_curve', 'phase_curve_residuals'):
                            dt = 0.01
                        elif style in ('phasezoom', 'phasezoom_occ', 'phasezoom_residuals',
                                       'phasezoom_occ_residuals'):
                            dt = 0.010416666666666666 / params_median[(companion + '_period')]
                        phase_time, phase_y, phase_y_err, _, phi = lct.phase_fold(x, y, (params_median[(companion + '_period')]), (params_median[(companion + '_epoch')]), dt=dt, ferr_type='meansig', ferr_style='sem', sigmaclip=False)
                        if len(x) > 500:
                            if style in ('phase_curve', 'phase_curve_residuals'):
                                ax.plot((phase_time * zoomfactor), phase_y, 'b.', color=(kwargs_data['color']), rasterized=(kwargs_data['rasterized']), zorder=11)
                    else:
                        ax.plot((phi * zoomfactor), y, 'b.', color='lightgrey', rasterized=(kwargs_data['rasterized']))
                        ax.errorbar((phase_time * zoomfactor), phase_y, yerr=phase_y_err, marker=(kwargs_data['marker']), markersize=(kwargs_data['markersize']), linestyle=(kwargs_data['linestyle']), color=(kwargs_data['color']), alpha=(kwargs_data['alpha']), capsize=0, rasterized=(kwargs_data['rasterized']), zorder=11)
            else:
                ax.errorbar((phi * zoomfactor), y, yerr=yerr_w, marker=(kwargs_data['marker']), markersize=(kwargs_data['markersize']), linestyle=(kwargs_data['linestyle']), color=(kwargs_data['color']), alpha=(kwargs_data['alpha']), capsize=0, rasterized=(kwargs_data['rasterized']), zorder=11)
            if base.settings['color_plot']:
                ax.scatter((phi * zoomfactor), y, c=x, marker='o', rasterized=(kwargs_data['rasterized']), cmap='inferno', zorder=11)
            else:
                ax.set(xlabel='Phase', ylabel=ylabel, title=(set_title(inst + ', companion ' + companion)))
                if style in ('phase', 'phasezoom', 'phasezoom_occ', 'phase_curve'):
                    if style in ('phase', 'phase_curve'):
                        xx = np.linspace(-0.25, 0.75, 1000)
                        xx2 = params_median[(companion + '_epoch')] + xx * params_median[(companion + '_period')]
                else:
                    if style in ('phasezoom', ):
                        xx = np.linspace(-10.0 / zoomfactor, 10.0 / zoomfactor, 1000)
                        xx2 = params_median[(companion + '_epoch')] + xx * params_median[(companion + '_period')]
                    elif style in ('phasezoom_occ', ):
                        e = params_median[(companion + '_f_s')] ** 2 + params_median[(companion + '_f_c')] ** 2
                        w = np.mod(np.arctan2(params_median[(companion + '_f_s')], params_median[(companion + '_f_c')]), 2 * np.pi)
                        phase_shift = 0.5 * (1.0 + 4.0 / np.pi * e * np.cos(w))
                        xx = np.linspace(-10.0 / zoomfactor + phase_shift, 10.0 / zoomfactor + phase_shift, 1000)
                        xx2 = params_median[(companion + '_epoch')] + xx * params_median[(companion + '_period')]
                    if samples is not None:
                        for i in range(samples.shape[0]):
                            s = samples[i, :]
                            p = update_params(s)
                            model = flux_fct(p, inst, companion, xx=xx2)
                            ax.plot((xx * zoomfactor), model, 'r-', alpha=alpha, zorder=12)

                    if style in ('phasezoom', 'phasezoom_residuals'):
                        ax.set(xlim=[-zoomwindow / 2.0, zoomwindow / 2.0], xlabel='$\\mathrm{ T - T_0 \\ (h) }$')
                    elif style in ('phasezoom_occ', 'phasezoom_occ_residuals'):
                        xlower = -zoomwindow / 2.0 + phase_shift * params_median[(companion + '_period')] * 24.0
                        xupper = zoomwindow / 2.0 + phase_shift * params_median[(companion + '_period')] * 24.0
                        ax.set(xlim=[xlower, xupper], xlabel='$\\mathrm{ T - T_0 \\ (h) }$')
                    elif style in ('phasezoom_occ', ):
                        ax.set(ylim=[0.999, 1.0005])
            if style in ('phase_curve', 'phase_curve_residuals'):
                ax.set(ylim=[0.999, 1.001])


def afplot_per_transit(samples, inst, companion, base=None, rasterized=True, marker='.', linestyle='none', color='b', markersize=8):
    if base == None:
        base = config.BASEMENT
    else:
        if inst in base.settings['inst_phot']:
            key = 'flux'
            ylabel = 'Realtive Flux'
            baseline_plus = 1.0
        elif inst in base.settings['inst_rv']:
            key = 'rv'
            ylabel = 'RV (km/s)'
        if samples.shape[0] == 1:
            alpha = 1.0
        else:
            alpha = 0.1
    params_median, params_ll, params_ul = get_params_from_samples(samples)
    width = 0.3333333333333333
    x = base.data[inst]['time']
    y = 1.0 * base.data[inst][key]
    yerr_w = calculate_yerr_w(params_median, inst, key)
    tmid_observed_transits = get_tmid_observed_transits(x, params_median[(companion + '_epoch')], params_median[(companion + '_period')], width)
    N_transits = len(tmid_observed_transits)
    fig, axes = plt.subplots(N_transits, 1, figsize=(6, 4 * N_transits), sharey=True)
    if N_transits > 0:
        axes = np.atleast_1d(axes)
        axes[0].set(title=inst)
        for i, t in enumerate(tmid_observed_transits):
            ax = axes[i]
            ind = np.where((x >= t - width / 2.0) & (x <= t + width / 2.0))[0]
            ax.errorbar((x[ind]), (y[ind]), yerr=(yerr_w[ind]), marker=marker, linestyle=linestyle, color=color, markersize=markersize, alpha=alpha, capsize=0, rasterized=rasterized)
            ax.set(xlabel='Time (BJD)', ylabel=ylabel)
            dt = 0.0013888888888888887
            xx = np.arange(x[ind][0], x[ind][(-1)] + dt, dt)
            for i in range(samples.shape[0]):
                s = samples[i, :]
                p = update_params(s)
                model = calculate_model(p, inst, key, xx=xx)
                baseline = calculate_baseline(p, inst, key, xx=xx)
                stellar_var = calculate_stellar_var(p, 'all', key, xx=xx)
                ax.plot(xx, (baseline + stellar_var + baseline_plus), 'k-', color='orange', alpha=alpha, zorder=12)
                ax.plot(xx, (model + baseline + stellar_var), 'r-', alpha=alpha, zorder=12)

            ax.set(xlim=[t - 0.16666666666666666, t + 0.16666666666666666])
            ax.axvline(t, color='g', lw=2, ls='--')

    else:
        warnings.warn('No transit of companion ' + companion + ' for ' + inst + '.')
    return (
     fig, axes)


def get_params_from_samples(samples):
    """
    read MCMC results and update params
    """
    theta_median = np.percentile(samples, 50, axis=0)
    theta_ul = np.percentile(samples, 84, axis=0) - theta_median
    theta_ll = theta_median - np.percentile(samples, 16, axis=0)
    params_median = update_params(theta_median)
    params_ll = update_params(theta_ll)
    params_ul = update_params(theta_ul)
    return (
     params_median, params_ll, params_ul)


def save_table(samples, mode):
    """
    Inputs:
    -------
    samples : array
        posterior samples
    mode : string
        'mcmc' or 'ns'
    """
    params, params_ll, params_ul = get_params_from_samples(samples)
    with open(os.path.join(config.BASEMENT.outdir, mode + '_table.csv'), 'w') as (f):
        f.write('#name,median,lower_error,upper_error,label,unit\n')
        f.write('#Fitted parameters,,,\n')
        for i, key in enumerate(config.BASEMENT.allkeys):
            if key not in config.BASEMENT.fitkeys:
                f.write(key + ',' + str(params[key]) + ',' + '(fixed),(fixed),' + config.BASEMENT.labels[i] + ',' + config.BASEMENT.units[i] + '\n')
            else:
                f.write(key + ',' + str(params[key]) + ',' + str(params_ll[key]) + ',' + str(params_ul[key]) + ',' + config.BASEMENT.labels[i] + ',' + config.BASEMENT.units[i] + '\n')


def save_latex_table(samples, mode):
    """
    Inputs:
    -------
    samples : array
        posterior samples
    mode : string
        'mcmc' or 'ns'
    """
    params_median, params_ll, params_ul = get_params_from_samples(samples)
    label = 'none'
    with open(os.path.join(config.BASEMENT.outdir, mode + '_latex_table.txt'), 'w') as (f):
        with open(os.path.join(config.BASEMENT.outdir, mode + '_latex_cmd.txt'), 'w') as (f_cmd):
            f.write('parameter & value & unit & fit/fixed \\\\ \n')
            f.write('\\hline \n')
            f.write('\\multicolumn{4}{c}{\\textit{Fitted parameters}} \\\\ \n')
            f.write('\\hline \n')
            for i, key in enumerate(config.BASEMENT.allkeys):
                if key not in config.BASEMENT.fitkeys:
                    value = str(params_median[key])
                    f.write(config.BASEMENT.labels[i] + ' & $' + value + '$ & ' + config.BASEMENT.units[i] + '& fixed \\\\ \n')
                    f_cmd.write('\\newcommand{\\' + key.replace('_', '') + '}{$' + value + '$} %' + label + ' = ' + value + '\n')
                else:
                    value = latex_printer.round_tex(params_median[key], params_ll[key], params_ul[key])
                    f.write(config.BASEMENT.labels[i] + ' & $' + value + '$ & ' + config.BASEMENT.units[i] + '& fit \\\\ \n')
                    f_cmd.write('\\newcommand{\\' + key.replace('_', '') + '}{$=' + value + '$} %' + label + ' = ' + value + '\n')


def show_initial_guess(datadir, do_logprint=True, do_plot=True, return_figs=False):
    config.init(datadir)
    if do_logprint:
        logprint_initial_guess()
    if do_plot:
        return plot_initial_guess(return_figs=return_figs)


def logprint_initial_guess():
    """
    Inputs:
    -------
    datadir : str
        the working directory for allesfitter
        must contain all the data files
        output directories and files will also be created inside datadir
            
    Outputs:
    --------
    This will output information into the console, 
    and create a file called datadir/results/initial_guess.pdf
    """
    logprint('\nSettings:')
    logprint('--------------------------')
    for key in config.BASEMENT.settings:
        if config.BASEMENT.settings[key] != '':
            logprint('{0: <30}'.format(key), '{0: <15}'.format(str(config.BASEMENT.settings[key])))
        else:
            logprint('\n{0: <30}'.format(key))

    logprint('\nParameters:')
    logprint('--------------------------')
    for i, key in enumerate(config.BASEMENT.params):
        if key in config.BASEMENT.fitkeys:
            ind = np.where(config.BASEMENT.fitkeys == key)[0][0]
            logprint('{0: <30}'.format(key), '{0: <15}'.format(str(config.BASEMENT.params[key])), '{0: <5}'.format('free'), '{0: <30}'.format(str(config.BASEMENT.bounds[ind])))
        elif config.BASEMENT.params[key] != '':
            logprint('{0: <30}'.format(key), '{0: <15}'.format(str(config.BASEMENT.params[key])), '{0: <5}'.format('set'))
        else:
            logprint('\n{0: <30}'.format(key))

    logprint('\nExternal priors:')
    logprint('--------------------------')
    if 'host_density' in config.BASEMENT.external_priors:
        logprint('\nStellar density prior (automatically set):', config.BASEMENT.external_priors['host_density'], '(g cm^-3)')
    else:
        logprint('No external priors defined.')
    logprint('\nndim:', config.BASEMENT.ndim)


def plot_initial_guess(return_figs=False):
    samples = draw_initial_guess_samples()
    if return_figs == False:
        for companion in config.BASEMENT.settings['companions_all']:
            fig, axes = afplot(samples, companion)
            fig.savefig((os.path.join(config.BASEMENT.outdir, 'initial_guess_' + companion + '.pdf')), bbox_inches='tight')
            plt.close(fig)

        for companion in config.BASEMENT.settings['companions_phot']:
            for inst in config.BASEMENT.settings['inst_phot']:
                try:
                    fig, axes = afplot_per_transit(samples, inst, companion)
                    fig.savefig((os.path.join(config.BASEMENT.outdir, 'initial_guess_per_transit_' + inst + '_' + companion + '.pdf')), bbox_inches='tight')
                    plt.close(fig)
                except:
                    pass

        return
    fig_list = []
    for companion in config.BASEMENT.settings['companions_all']:
        fig, axes = afplot(samples, companion)
        fig_list.append(fig)

    return fig_list


def plot_ttv_results(params_median, params_ll, params_ul):
    for companion in config.BASEMENT.settings['companions_all']:
        fig, axes = plt.subplots()
        axes.axhline(0, color='grey', linestyle='--')
        for i in range(len(config.BASEMENT.data[(companion + '_tmid_observed_transits')])):
            axes.errorbar((i + 1), (params_median[(companion + '_ttv_transit_' + str(i + 1))] * 24 * 60), yerr=(np.array([[params_ll[(companion + '_ttv_transit_' + str(i + 1))] * 24 * 60, params_ul[(companion + '_ttv_transit_' + str(i + 1))] * 24 * 60]]).T),
              color=(config.BASEMENT.settings[(companion + '_color')]),
              fmt='.')

        axes.set(xlabel='Tranist Nr.', ylabel='TTV (mins)')
        fig.savefig((os.path.join(config.BASEMENT.outdir, 'ttv_results_' + companion + '.pdf')), bbox_inches='tight')
        plt.close(fig)


def get_labels(datadir, as_type='dic'):
    config.init(datadir)
    if as_type == '2d_array':
        return config.BASEMENT.labels
    if as_type == 'dic':
        labels_dic = {}
        for key in config.BASEMENT.fitkeys:
            ind = np.where(config.BASEMENT.allkeys == key)[0]
            labels_dic[key] = config.BASEMENT.labels[ind][0]

        return labels_dic


def get_data(datadir):
    config.init(datadir)
    return config.BASEMENT.data


def get_settings(datadir):
    config.init(datadir)
    return config.BASEMENT.settings
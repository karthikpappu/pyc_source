# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/utils/utils.py
# Compiled at: 2020-05-08 05:31:08
# Size of source mod 2**32: 26501 bytes
import os, sys, logging, contextlib, time, copy, shutil, numpy as np
from scipy.integrate import cumtrapz
from scipy.interpolate import interp1d
from scipy import stats
import h5py
from tqdm import tqdm as Basetqdm
CACHE_DIR = os.path.expanduser(os.path.join('~', '.cache', 'pesummary', 'style'))

class _tqdm(Basetqdm):

    @property
    def format_dict(self):
        """Public API for read-only member access."""
        return dict(n=(self.n),
          total=(self.total),
          elapsed=(self._time() - self.start_t if hasattr(self, 'start_t') else 0),
          asctime=(time.strftime('%Y-%m-%d  %H:%M:%S')),
          ncols=(self.dynamic_ncols(self.fp) if self.dynamic_ncols else self.ncols),
          prefix=(self.desc),
          ascii=(self.ascii),
          unit=(self.unit),
          unit_scale=(self.unit_scale),
          rate=(1 / self.avg_time if self.avg_time else None),
          bar_format=(self.bar_format),
          postfix=(self.postfix),
          unit_divisor=(self.unit_divisor))


def trange(*args, **kwargs):
    """
    A shortcut for tqdm(range(*args), **kwargs).
    """
    return _tqdm(range(*args), **kwargs)


def resample_posterior_distribution(posterior, nsamples):
    """Randomly draw nsamples from the posterior distribution

    Parameters
    ----------
    posterior: ndlist
        nd list of posterior samples. If you only want to resample one
        posterior distribution then posterior=[[1., 2., 3., 4.]]. For multiple
        posterior distributions then posterior=[[1., 2., 3., 4.], [1., 2., 3.]]
    nsamples: int
        number of samples that you wish to randomly draw from the distribution
    """
    if len(posterior) == 1:
        n, bins = np.histogram(posterior, bins=50)
        n = np.array([0] + [i for i in n])
        cdf = cumtrapz(n, bins, initial=0)
        cdf /= cdf[(-1)]
        icdf = interp1d(cdf, bins)
        samples = icdf(np.random.rand(nsamples))
    else:
        posterior = np.array([i for i in posterior])
        keep_idxs = np.random.choice((len(posterior[0])),
          nsamples, replace=False)
        samples = [i[keep_idxs] for i in posterior]
    return samples


def check_file_exists_and_rename(file_name):
    """Check to see if a file exists and if it does then rename the file

    Parameters
    ----------
    file_name: str
        proposed file name to store data
    """
    if os.path.isfile(file_name):
        import shutil
        old_file = '{}_old'.format(file_name)
        while os.path.isfile(old_file):
            old_file += '_old'

        logger.warn("The file '{}' already exists. Renaming the existing file to {} and saving the data to the requested file name".format(file_name, old_file))
        shutil.move(file_name, old_file)


def check_condition(condition, error_message):
    """Raise an exception if the condition is not satisfied
    """
    if condition:
        raise Exception(error_message)


def rename_group_or_dataset_in_hf5_file(base_file, group=None, dataset=None):
    """Rename a group or dataset in an hdf5 file

    Parameters
    ----------
    group: list, optional
        a list containing the path to the group that you would like to change
        as the first argument and the new name of the group as the second
        argument
    dataset: list, optional
        a list containing the name of the dataset that you would like to change
        as the first argument and the new name of the dataset as the second
        argument
    """
    condition = not os.path.isfile(base_file)
    check_condition(condition, 'The file %s does not exist' % base_file)
    f = h5py.File(base_file, 'a')
    if group:
        f[group[1]] = f[group[0]]
        del f[group[0]]
    else:
        if dataset:
            f[dataset[1]] = f[dataset[0]]
            del f[dataset[0]]
    f.close()


def make_dir(path):
    if os.path.isdir(os.path.expanduser(path)):
        pass
    else:
        os.makedirs(os.path.expanduser(path))


def guess_url(web_dir, host, user):
    """Guess the base url from the host name

    Parameters
    ----------
    web_dir: str
        path to the web directory where you want the data to be saved
    host: str
        the host name of the machine where the python interpreter is currently
        executing
    user: str
        the user that is current executing the python interpreter
    """
    ligo_data_grid = False
    if 'public_html' in web_dir:
        ligo_data_grid = True
    else:
        if ligo_data_grid:
            path = web_dir.split('public_html')[1]
            if 'raven' in host or 'arcca' in host:
                url = 'https://geo2.arcca.cf.ac.uk/~{}'.format(user)
            else:
                if 'ligo-wa' in host:
                    url = 'https://ldas-jobs.ligo-wa.caltech.edu/~{}'.format(user)
                else:
                    if 'ligo-la' in host:
                        url = 'https://ldas-jobs.ligo-la.caltech.edu/~{}'.format(user)
                    else:
                        if 'cit' in host or 'caltech' in host:
                            url = 'https://ldas-jobs.ligo.caltech.edu/~{}'.format(user)
                        else:
                            if 'uwm' in host or 'nemo' in host:
                                url = 'https://ldas-jobs.phys.uwm.edu/~{}'.format(user)
                            else:
                                if 'phy.syr.edu' in host:
                                    url = 'https://sugar-jobs.phy.syr.edu/~{}'.format(user)
                                else:
                                    if 'vulcan' in host:
                                        url = 'https://galahad.aei.mpg.de/~{}'.format(user)
                                    else:
                                        if 'atlas' in host:
                                            url = 'https://atlas1.atlas.aei.uni-hannover.de/~{}'.format(user)
                                        else:
                                            if 'iucca' in host:
                                                url = 'https://ldas-jobs.gw.iucaa.in/~{}'.format(user)
                                            else:
                                                if 'hawk' in host:
                                                    url = 'https://ligo.gravity.cf.ac.uk/~{}'.format(user)
                                                else:
                                                    url = 'https://{}/~{}'.format(host, user)
            url += path
        else:
            url = 'https://{}'.format(web_dir)
    return url


def command_line_arguments():
    """Return the command line arguments
    """
    return sys.argv[1:]


def command_line_dict():
    """Return a dictionary of command line arguments
    """
    from pesummary.core.command_line import command_line
    from pesummary.gw.command_line import insert_gwspecific_option_group
    parser = command_line()
    insert_gwspecific_option_group(parser)
    opts = parser.parse_args()
    return vars(opts)


def gw_results_file(opts):
    """Determine if a GW results file is passed
    """
    cond1 = hasattr(opts, 'gw') and opts.gw
    cond2 = hasattr(opts, 'calibration') and opts.calibration
    cond3 = hasattr(opts, 'gracedb') and opts.gracedb
    cond4 = hasattr(opts, 'approximant') and opts.approximant
    cond5 = hasattr(opts, 'psd') and opts.psd
    if cond1 or cond2 or cond3 or cond4 or cond5:
        return True
    else:
        return False


def functions(opts):
    """Return a dictionary of functions that are either specific to GW results
    files or core.
    """
    from pesummary.core.inputs import Input
    from pesummary.gw.inputs import GWInput
    from pesummary.core.file.meta_file import MetaFile
    from pesummary.gw.file.meta_file import GWMetaFile
    from pesummary.core.finish import FinishingTouches
    from pesummary.gw.finish import GWFinishingTouches
    dictionary = {}
    dictionary['input'] = GWInput if gw_results_file(opts) else Input
    dictionary['MetaFile'] = GWMetaFile if gw_results_file(opts) else MetaFile
    dictionary['FinishingTouches'] = GWFinishingTouches if gw_results_file(opts) else FinishingTouches
    return dictionary


def _logger_format():
    return '%(asctime)s %(name)s %(levelname)-8s: %(message)s'


def setup_logger():
    """Set up the logger output.
    """
    import tempfile
    if not os.path.isdir('.tmp/pesummary'):
        os.makedirs('.tmp/pesummary')
    dirpath = tempfile.mkdtemp(dir='.tmp/pesummary')
    level = 'INFO'
    if '-v' in sys.argv or '--verbose' in sys.argv:
        level = 'DEBUG'
    FORMAT = _logger_format()
    logger = logging.getLogger('PESummary')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(('%s/pesummary.log' % dirpath), mode='w')
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel('INFO')
    formatter = logging.Formatter(FORMAT, datefmt='%Y-%m-%d  %H:%M:%S')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)


def remove_tmp_directories():
    """Remove the temporary directories created by PESummary
    """
    import shutil
    from glob import glob
    import time
    directories = glob('.tmp/pesummary/*')
    for i in directories:
        if os.path.isdir(i):
            shutil.rmtree(i)
        else:
            if os.path.isfile(i):
                os.remove(i)


def _add_existing_data(namespace):
    """Add existing data to namespace object
    """
    for num, i in enumerate(namespace.existing_labels):
        if hasattr(namespace, 'labels'):
            if i not in namespace.labels:
                namespace.labels.append(i)
            elif hasattr(namespace, 'samples'):
                if i not in list(namespace.samples.keys()):
                    namespace.samples[i] = namespace.existing_samples[i]
                elif hasattr(namespace, 'weights') and i not in list(namespace.weights.keys()):
                    if namespace.existing_weights is None:
                        namespace.weights[i] = None
                    else:
                        namespace.weights[i] = namespace.existing_weights[i]
                    if hasattr(namespace, 'injection_data'):
                        if i not in list(namespace.injection_data.keys()):
                            namespace.injection_data[i] = namespace.existing_injection_data[i]
                    if hasattr(namespace, 'file_versions'):
                        if i not in list(namespace.file_versions.keys()):
                            namespace.file_versions[i] = namespace.existing_file_version[i]
                    if hasattr(namespace, 'file_kwargs'):
                        if i not in list(namespace.file_kwargs.keys()):
                            namespace.file_kwargs[i] = namespace.existing_file_kwargs[i]
                    if hasattr(namespace, 'config'):
                        if namespace.existing_config[num] not in namespace.config:
                            namespace.config.append(namespace.existing_config[num])
                    if hasattr(namespace, 'priors'):
                        if hasattr(namespace, 'existing_priors'):
                            for key, item in namespace.existing_priors.items():
                                if key in namespace.priors.keys():
                                    for label in item.keys():
                                        if label not in namespace.priors[key].keys():
                                            namespace.priors[key][label] = item[label]

                                else:
                                    namespace.priors.update({key: item})

                    if hasattr(namespace, 'approximant'):
                        if namespace.approximant is not None:
                            if i not in list(namespace.approximant.keys()):
                                if i in list(namespace.existing_approximant.keys()):
                                    namespace.approximant[i] = namespace.existing_approximant[i]
                    if hasattr(namespace, 'psds'):
                        if namespace.psds is not None:
                            if i not in list(namespace.psds.keys()):
                                if i in list(namespace.existing_psd.keys()):
                                    namespace.psds[i] = namespace.existing_psd[i]
                                else:
                                    namespace.psds[i] = {}
                else:
                    if hasattr(namespace, 'calibration'):
                        if namespace.calibration is not None:
                            if i not in list(namespace.calibration.keys()):
                                if i in list(namespace.existing_calibration.keys()):
                                    namespace.calibration[i] = namespace.existing_calibration[i]
                                else:
                                    namespace.calibration[i] = {}
            else:
                if hasattr(namespace, 'maxL_samples'):
                    if i not in list(namespace.maxL_samples.keys()):
                        namespace.maxL_samples[i] = {key:val.maxL for key, val in namespace.samples[i].items()}
                if hasattr(namespace, 'pepredicates_probs'):
                    if i not in list(namespace.pepredicates_probs.keys()):
                        from pesummary.gw.pepredicates import get_classifications
                        namespace.pepredicates_probs[i] = get_classifications(namespace.existing_samples[i])
            if hasattr(namespace, 'pastro_probs') and i not in list(namespace.pastro_probs.keys()):
                from pesummary.gw.p_astro import get_probabilities
                em_bright = get_probabilities(namespace.existing_samples[i])
                namespace.pastro_probs[i] = {'default':em_bright[0], 
                 'population':em_bright[1]}

    if hasattr(namespace, 'result_files'):
        number = len(namespace.labels)
        while len(namespace.result_files) < number:
            namespace.result_files.append(namespace.existing_metafile)

    parameters = [list(namespace.samples[i].keys()) for i in namespace.labels]
    namespace.same_parameters = list((set.intersection)(*[set(l) for l in parameters]))
    namespace.same_samples = {param:{i:namespace.samples[i][param] for i in namespace.labels} for param in namespace.same_parameters}
    return namespace


def customwarn(message, category, filename, lineno, file=None, line=None):
    """
    """
    import sys, warnings
    sys.stdout.write(warnings.formatwarning('%s' % message, category, filename, lineno))


def determine_gps_time_and_window(maxL_samples, labels):
    """Determine the gps time and window to use in the spectrogram and
    omegascan plots
    """
    times = [maxL_samples[label]['geocent_time'] for label in labels]
    gps_time = np.mean(times)
    time_range = np.max(times) - np.min(times)
    if time_range < 4.0:
        window = 4.0
    else:
        window = time_range * 1.5
    return (
     gps_time, window)


def number_of_columns_for_legend(labels):
    """Determine the number of columns to use in a legend

    Parameters
    ----------
    labels: list
        list of labels in the legend
    """
    max_length = np.max([len(i) for i in labels]) + 5.0
    if max_length > 50.0:
        return 1
    else:
        return int(50.0 / max_length)


class RedirectLogger(object):
    __doc__ = 'Class to redirect the output from other codes to the `pesummary`\n    logger\n\n    Parameters\n    ----------\n    level: str, optional\n        the level to display the messages\n    '

    def __init__(self, code, level='Debug'):
        self.logger = logging.getLogger('PESummary')
        self.level = getattr(logging, level)
        self._redirector = contextlib.redirect_stdout(self)
        self.code = code

    def isatty(self):
        pass

    def write(self, msg):
        """Write the message to stdout

        Parameters
        ----------
        msg: str
            the message you wish to be printed to stdout
        """
        if msg:
            if not msg.isspace():
                self.logger.log(self.level, '[from %s] %s' % (self.code, msg))

    def flush(self):
        pass

    def __enter__(self):
        self._redirector.__enter__()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._redirector.__exit__(exc_type, exc_value, traceback)


def draw_conditioned_prior_samples(samples_dict, prior_samples_dict, conditioned, xlow, xhigh, N):
    """Return a prior_dict that is conditioned on certain parameters

    Parameters
    ----------
    samples_dict: pesummary.utils.samples_dict.SamplesDict
        SamplesDict containing the posterior samples
    prior_samples_dict: pesummary.utils.samples_dict.SamplesDict
        SamplesDict containing the prior samples
    conditioned: list
        list of parameters that you wish to condition your prior on
    xlow: dict
        dictionary of lower bounds for each parameter
    xhigh: dict
        dictionary of upper bounds for each parameter
    N: int
        number of points to use within the grid
    """
    for param in conditioned:
        indices = _draw_conditioned_prior_samples(prior_samples_dict[param], samples_dict[param], xlow[param], xhigh[param], N)
        for key, val in prior_samples_dict.items():
            prior_samples_dict[key] = val[indices]

    return prior_samples_dict


def _draw_conditioned_prior_samples(prior_samples, posterior_samples, xlow, xhigh, xN=1000, N=1000):
    """Return a list of indices for the conditioned prior via rejection
    sampling. The conditioned prior will then be `prior_samples[indicies]`.
    Code from Michael Puerrer.

    Parameters
    ----------
    prior_samples: np.ndarray
        array of prior samples that you wish to condition
    posterior_samples: np.ndarray
        array of posterior samples that you wish to condition on
    xlow: float
        lower bound for grid to be used
    xhigh: float
        upper bound for grid to be used
    xN: int, optional
        Number of points to use within the grid
    N: int, optional
        Number of samples to generate
    """
    from pesummary.core.plots.bounded_1d_kde import Bounded_1d_kde
    prior_KDE = Bounded_1d_kde(prior_samples)
    posterior_KDE = Bounded_1d_kde(posterior_samples)
    x = np.linspace(xlow, xhigh, xN)
    idx_nz = np.nonzero(posterior_KDE(x))
    pdf_ratio = prior_KDE(x)[idx_nz] / posterior_KDE(x)[idx_nz]
    M = 1.1 / min(pdf_ratio[np.where(pdf_ratio < 1)])
    indicies = []
    i = 0
    while i < N:
        x_i = np.random.choice(prior_samples)
        idx_i = np.argmin(np.abs(prior_samples - x_i))
        u = np.random.uniform()
        if u < posterior_KDE(x_i) / (M * prior_KDE(x_i)):
            indicies.append(idx_i)
            i += 1

    return indicies


def unzip(zip_file, outdir='.', overwrite=False):
    """Extract the data from a zipped file and save in outdir.

    Parameters
    ----------
    zip_file: str
        path to the file you wish to unzip
    outdir: str, optional
        path to the directory where you wish to save the unzipped file.
    overwrite: Bool, optional
        If True, overwrite a file that has the same name
    """
    import gzip, shutil
    from pathlib import Path
    f = Path(zip_file)
    file_name = f.stem
    out_file = os.path.join(outdir, file_name)
    if os.path.isfile(out_file):
        if not overwrite:
            raise FileExistsError("The file '{}' already exists. Not overwriting".format(out_file))
    with gzip.open(zip_file, 'rb') as (input):
        with open(out_file, 'wb') as (output):
            shutil.copyfileobj(input, output)
    return out_file


def iterator(iterable, desc='', tqdm=False, logger_output=True, total=None, logger_name='PESummary'):
    """Return either a tqdm iterator, if tqdm installed, or a simple range

    Parameters
    ----------
    iterable: func
        iterable that you wish to iterate over
    desc: str, optional
        description for the tqdm bar
    tqdm: Bool, optional
        If True, a tqdm object is used. Otherwise simply returns the iterator.
    logger_output: Bool, optional
        If True, the tqdm progress bar interacts with logger
    total: float, optional
        total length of iterable
    logger_name: str, optional
        name of the logger you wish to use
    """
    if tqdm:
        try:
            FORMAT, DESC = (None, None)
            if logger_output:
                data = {'name':logger_name, 
                 'levelname':'INFO',  'message':desc, 
                 'asctime':'{asctime}'}
                FORMAT = _logger_format() % data + ' | {percentage:3.0f}% | {n_fmt}/{total_fmt} | {elapsed}'
            else:
                if len(desc):
                    DESC = desc
            return _tqdm(iterable,
              total=total, desc=DESC, bar_format=FORMAT)
        except ImportError:
            return iterable

    else:
        return iterable


def _check_latex_install():
    from matplotlib import rcParams
    from distutils.spawn import find_executable
    original = rcParams['text.usetex']
    if find_executable('latex') is not None:
        rcParams['text.usetex'] = original
    else:
        rcParams['text.usetex'] = False


def smart_round(parameters, return_latex=False, return_latex_row=False):
    """Round a parameter according to the uncertainty. If more than one parameter
    and uncertainty is passed, each parameter is rounded according to the
    lowest uncertainty

    Parameters
    ----------
    parameter_dictionary: list/np.ndarray
        list containing the median, upper bound and lower bound for a given parameter
    return_latex: Bool, optional
        if True, return as a latex string
    return_latex_row: Bool, optional
        if True, return the rounded data as a single row in latex format

    Examples
    --------
    >>> data = [1.234, 0.2, 0.1]
    >>> smart_round(data)
    [ 1.2  0.2  0.1]
    >>> data = [
    ...     [6.093, 0.059, 0.055],
    ...     [6.104, 0.057, 0.052],
    ...     [6.08, 0.056, 0.052]
    ... ]
    >>> smart_round(data)
    [[ 6.09  0.06  0.06]
     [ 6.1   0.06  0.05]
     [ 6.08  0.06  0.05]]
    >>> smart_round(data, return_latex=True)
    6.09^{+0.06}_{-0.06}
    6.10^{+0.06}_{-0.05}
    6.08^{+0.06}_{-0.05}
    >>> data = [
    ...     [743.25, 43.6, 53.2],
    ...     [8712.5, 21.5, 35.2],
    ...     [196.46, 65.2, 12.5]
    ... ]
    >>> smart_round(data, return_latex_row=True)
    740^{+40}_{-50} & 8710^{+20}_{-40} & 200^{+70}_{-10}
    >>> data = [
    ...     [743.25, 43.6, 53.2],
    ...     [8712.5, 21.5, 35.2],
    ...     [196.46, 65.2, 8.2]
    ... ]
    >>> smart_round(data, return_latex_row=True)
    743^{+44}_{-53} & 8712^{+22}_{-35} & 196^{+65}_{-8}
    """
    rounded = copy.deepcopy(np.atleast_2d(parameters))
    lowest_uncertainty = np.min(np.abs(parameters))
    rounding = int(-1 * np.floor(np.log10(lowest_uncertainty)))
    for num, _ in enumerate(rounded):
        rounded[num] = [np.round(value, rounding) for value in rounded[num]]

    if return_latex or return_latex_row:
        if rounding > 0:
            _format = '%.{}f'.format(rounding)
        else:
            _format = '%.f'
        string = '{0}^{{+{0}}}_{{-{0}}}'.format(_format)
        latex = [string % (value[0], value[1], value[2]) for value in rounded]
        if return_latex:
            for ll in latex:
                print(ll)

        else:
            print(' & '.join(latex))
        return ''
    else:
        if np.array(parameters).ndim == 1:
            return rounded[0]
        return rounded


def gelman_rubin(samples, decimal=5):
    """Return an approximation to the Gelman-Rubin statistic (see Gelman, A. and
     Rubin, D. B., Statistical Science, Vol 7, No. 4, pp. 457--511 (1992))

    Parameters
    ----------
    samples: np.ndarray
        2d array of samples for a given parameter, one for each chain
    decimal: int
        number of decimal places to keep when rounding

    Examples
    --------
    >>> from pesummary.utils.utils import gelman_rubin
    >>> samples = [[1, 1.5, 1.2, 1.4, 1.6, 1.2], [1.5, 1.3, 1.4, 1.7]]
    >>> gelman_rubin(samples, decimal=5)
    1.2972
    """
    means = [np.mean(data) for data in samples]
    variances = [np.var(data) for data in samples]
    BoverN = np.var(means)
    W = np.mean(variances)
    sigma = W + BoverN
    m = len(samples)
    Vhat = sigma + BoverN / m
    return np.round(Vhat / W, decimal)


def kolmogorov_smirnov_test(samples, decimal=5):
    """Return the KS p value between two PDFs

    Parameters
    ----------
    samples: 2d list
        2d list containing the 2 PDFs that you wish to compare
    decimal: int
        number of decimal places to keep when rounding
    """
    return np.round((stats.ks_2samp)(*samples)[1], decimal)


def jension_shannon_divergence(samples, decimal=5):
    try:
        kernel = [stats.gaussian_kde(i) for i in samples]
    except np.linalg.LinAlgError:
        return float('nan')
    else:
        a, b = kernel
        x = np.linspace(np.min([np.min(i) for i in samples]), np.max([np.max(i) for i in samples]), 100)
        a, b = [k(x) for k in kernel]
        a = np.asarray(a)
        b = np.asarray(b)
        a /= a.sum()
        b /= b.sum()
        m = 0.5 * (a + b)
        kl_forward = stats.entropy(a, qk=m)
        kl_backward = stats.entropy(b, qk=m)
        return np.round(kl_forward / 2.0 + kl_backward / 2.0, decimal)


def make_cache_style_file(style_file):
    """Make a cache directory which stores the style file you wish to use
    when plotting

    Parameters
    ----------
    style_file: str
        path to the style file that you wish to use when plotting
    """
    make_dir(CACHE_DIR)
    shutil.copyfile(style_file, os.path.join(CACHE_DIR, 'matplotlib_rcparams.sty'))


def get_matplotlib_style_file():
    """Return the path to the matplotlib style file that you wish to use
    """
    style_file = os.path.join(CACHE_DIR, 'matplotlib_rcparams.sty')
    if not os.path.isfile(style_file):
        from pesummary import conf
        return conf.style_file
    else:
        return os.path.join(style_file)


def get_matplotlib_backend(parallel=False):
    """Return the matplotlib backend to use for the plotting modules

    Parameters
    ----------
    parallel: Bool, optional
        if True, backend is always set to 'Agg' for the multiprocessing module
    """
    try:
        os.environ['DISPLAY']
    except KeyError:
        try:
            __IPYTHON__
        except NameError:
            DISPLAY = False
        else:
            DISPLAY = True
    else:
        DISPLAY = True
    if DISPLAY:
        if not parallel:
            backend = 'TKAgg'
    else:
        backend = 'Agg'
    return backend


setup_logger()
logger = logging.getLogger('PESummary')
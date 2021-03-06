# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pesummary/utils/samples_dict.py
# Compiled at: 2020-04-21 06:57:35
# Size of source mod 2**32: 23504 bytes
import copy, numpy as np
from pesummary.utils.utils import resample_posterior_distribution, gelman_rubin as _gelman_rubin, logger

class SamplesDict(dict):
    __doc__ = 'Class to store the samples from a single run\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter\n    autoscale: Bool, optional\n        If True, the posterior samples for each parameter are scaled to the\n        same length\n\n    Attributes\n    ----------\n    maxL: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the maximum likelihood sample keyed by\n        the parameter\n    minimum: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the minimum sample for each parameter\n    maximum: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the maximum sample for each parameter\n    median: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containining the median of each marginalized\n        posterior distribution\n    mean: pesummary.utils.samples_dict.SamplesDict\n        SamplesDict object containing the mean of each marginalized posterior\n        distribution\n    number_of_samples: int\n        Number of samples stored in the SamplesDict object\n\n    Methods\n    -------\n    to_pandas:\n        Convert the SamplesDict object to a pandas DataFrame\n    to_structured_array:\n        Convert the SamplesDict object to a numpy structured array\n    pop:\n        Remove an entry from the SamplesDict object\n    downsample:\n        Downsample the samples stored in the SamplesDict object. See the\n        pesummary.utils.utils.resample_posterior_distribution method\n    discard_samples:\n        Remove the first N samples from each distribution\n\n    Examples\n    --------\n    How the initialize the SamplesDict class\n\n    >>> from pesummary.utils.samples_dict import SamplesDict\n    >>> data = {\n    ...     "a": [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...     "b": [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ... }\n    >>> dataset = SamplesDict(data)\n    >>> parameters = ["a", "b"]\n    >>> samples = [\n    ...     [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...     [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ... }\n    >>> dataset = SamplesDict(parameters, samples)\n    '

    def __init__(self, *args, logger_warn='warn', autoscale=True):
        super(SamplesDict, self).__init__()
        if len(args) == 1:
            if isinstance(args[0], dict):
                self.parameters = list(args[0].keys())
                self.samples = np.array([args[0][param] for param in self.parameters])
                for key, item in args[0].items():
                    self[key] = Array(item)

        else:
            self.parameters, self.samples = args
            lengths = [len(i) for i in self.samples]
            if len(np.unique(lengths)) > 1:
                if autoscale:
                    nsamples = np.min(lengths)
                    getattr(logger, logger_warn)('Unequal number of samples for each parameter. Restricting all posterior samples to have {} samples'.format(nsamples))
                    self.samples = [dataset[:nsamples] for dataset in self.samples]
            self.make_dictionary()

    def __getitem__(self, key):
        if isinstance(key, slice):
            return SamplesDict(self.parameters, [i[key.start:key.stop:key.step] for i in self.samples])
        else:
            if isinstance(key, str):
                if key not in self.keys():
                    raise KeyError('{} not in dictionary. The list of available keys are {}'.format(key, self.keys()))
            return super(SamplesDict, self).__getitem__(key)

    def __str__(self):
        """Print a summary of the information stored in the dictionary
        """

        def format_string(string, row):
            """Format a list into a table

            Parameters
            ----------
            string: str
                existing table
            row: list
                the row you wish to be written to a table
            """
            string += '{:<8}'.format(row[0])
            for i in range(1, len(row)):
                if isinstance(row[i], str):
                    string += '{:<15}'.format(row[i])
                else:
                    if isinstance(row[i], (float, int, np.int64, np.int32)):
                        string += '{:<15.6f}'.format(row[i])

            string += '\n'
            return string

        string = ''
        string = format_string(string, ['idx'] + list(self.keys()))
        if self.number_of_samples < 8:
            for i in range(self.number_of_samples):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

        else:
            for i in range(4):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

            for i in range(2):
                string = format_string(string, ['.'] * (len(self.keys()) + 1))

            for i in range(self.number_of_samples - 2, self.number_of_samples):
                string = format_string(string, [i] + [item[i] for key, item in self.items()])

        return string

    @property
    def maxL(self):
        return SamplesDict(self.parameters, [[item.maxL] for key, item in self.items()])

    @property
    def minimum(self):
        return SamplesDict(self.parameters, [[item.minimum] for key, item in self.items()])

    @property
    def maximum(self):
        return SamplesDict(self.parameters, [[item.maximum] for key, item in self.items()])

    @property
    def median(self):
        return SamplesDict(self.parameters, [[item.average(type='median')] for key, item in self.items()])

    @property
    def mean(self):
        return SamplesDict(self.parameters, [[item.average(type='mean')] for key, item in self.items()])

    @property
    def number_of_samples(self):
        return len(self[self.parameters[0]])

    def to_pandas(self):
        """Convert a SamplesDict object to a pandas dataframe
        """
        from pandas import DataFrame
        return DataFrame(self)

    def to_structured_array(self):
        """Convert a SamplesDict object to a structured numpy array
        """
        return self.to_pandas().to_records(index=False, column_dtypes=(np.float))

    def pop(self, parameter):
        if parameter not in self.parameters:
            logger.info('{} not in SamplesDict. Unable to remove {}'.format(parameter, parameter))
            return
        else:
            ind = self.parameters.index(parameter)
            self.parameters.remove(parameter)
            remove = self.samples[ind]
            samples = self.samples
            if isinstance(self.samples, np.ndarray):
                samples = self.samples.tolist()
                remove = self.samples[ind].tolist()
            samples.remove(remove)
            if isinstance(self.samples, np.ndarray):
                self.samples = np.array(samples)
            return super(SamplesDict, self).pop(parameter)

    def downsample(self, number):
        """Downsample the samples stored in the SamplesDict class

        Parameters
        ----------
        number: int
            Number of samples you wish to downsample to
        """
        self.samples = resample_posterior_distribution(self.samples, number)
        self.make_dictionary()
        return self

    def discard_samples(self, number):
        """Remove the first n samples

        Parameters
        ----------
        number: int
            Number of samples that you wish to remove
        """
        self.make_dictionary(discard_samples=number)
        return self

    def make_dictionary(self, discard_samples=None):
        """Add the parameters and samples to the class
        """
        if 'log_likelihood' in self.parameters:
            likelihoods = self.samples[self.parameters.index('log_likelihood')]
            likelihoods = likelihoods[discard_samples:]
        else:
            likelihoods = None
        if any(i in self.parameters for i in ('weights', 'weight')):
            ind = self.parameters.index('weights') if 'weights' in self.parameters else self.parameters.index('weight')
            weights = self.samples[ind][discard_samples:]
        else:
            weights = None
        for key, val in zip(self.parameters, self.samples):
            self[key] = Array((val[discard_samples:]),
              likelihood=likelihoods, weights=weights)


class MCMCSamplesDict(dict):
    __doc__ = 'Class to store the mcmc chains from a single run\n\n    Parameters\n    ----------\n    parameters: list\n        list of parameters\n    samples: nd list\n        list of samples for each parameter for each chain\n    transpose: Bool, optional\n        True if the input is a transposed dictionary\n\n    Attributes\n    ----------\n    T: pesummary.utils.samples_dict.MCMCSamplesDict\n        Transposed MCMCSamplesDict object keyed by parameters rather than\n        chain\n    average: pesummary.utils.samples_dict.SamplesDict\n        The mean of each sample across multiple chains. If the chains are of\n        different lengths, all chains are resized to the minimum number of\n        samples\n    nchains: int\n        Total number of chains stored in the MCMCSamplesDict object\n    number_of_samples: dict\n        Number of samples stored in the MCMCSamplesDict for each chain\n    total_number_of_samples: int\n        Total number of samples stored across the multiple chains\n    minimum_number_of_samples: int\n        The number of samples in the smallest chain\n\n    Methods\n    -------\n    discard_samples:\n        Discard the first N samples for each chain\n    burnin:\n        Remove the first N samples as burnin. For different algorithms\n        see pesummary.core.file.mcmc.algorithms\n    gelman_rubin: float\n        Return the Gelman-Rubin statistic between the chains for a given\n        parameter. See pesummary.utils.utils.gelman_rubin\n\n    Examples\n    --------\n    Initializing the MCMCSamplesDict class\n\n    >>> from pesummary.utils.samplesdict import MCMCSamplesDict\n    >>> data = {\n    ...     "chain_0": {\n    ...         "a": [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...         "b": [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ...     },\n    ...     "chain_1": {\n    ...         "a": [0.8, 0.5, 1.7, 1.4, 1.2, 1.7, 0.9],\n    ...         "b": [10, 10.5, 10.4, 9.6, 8.6, 11.6, 16.2]\n    ...     }\n    ... }\n    >>> dataset = MCMCSamplesDict(data)\n    >>> parameters = ["a", "b"]\n    >>> samples = [\n    ...     [\n    ...         [1, 1.2, 1.7, 1.1, 1.4, 0.8, 1.6],\n    ...         [10.2, 11.3, 11.6, 9.5, 8.6, 10.8, 10.9]\n    ...     ], [\n    ...         [0.8, 0.5, 1.7, 1.4, 1.2, 1.7, 0.9],\n    ...         [10, 10.5, 10.4, 9.6, 8.6, 11.6, 16.2]\n    ...     ]\n    ... ]\n    >>> dataset = MCMCSamplesDict(parameter, samples)\n    '

    def __init__(self, *args, transpose=False):
        super(MCMCSamplesDict, self).__init__()
        single_chain_error = 'This class requires more than one mcmc chain to be passed. As only one dataset is available, please use the SamplesDict class.'
        self.transpose = transpose
        if len(args) == 1 and isinstance(args[0], dict):
            if transpose:
                parameters = list(args[0].keys())
                chains = list(args[0][parameters[0]].keys())
                outer_iterator, inner_iterator = parameters, chains
            else:
                chains = list(args[0].keys())
                parameters = list(args[0][chains[0]].keys())
                outer_iterator, inner_iterator = chains, parameters
            if len(chains) == 1:
                raise ValueError(single_chain_error)
            for num, dataset in enumerate(outer_iterator):
                samples = np.array([args[0][dataset][param] for param in inner_iterator])
                if transpose:
                    desc = parameters[num]
                    self[desc] = SamplesDict(chains,
                      samples, logger_warn='debug', autoscale=False)
                else:
                    desc = 'chain_{}'.format(num)
                    self[desc] = SamplesDict(parameters, samples)

        else:
            parameters, chains = args
            if len(chains) == 1:
                raise ValueError(single_chain_error)
            for num, dataset in enumerate(chains):
                self['chain_{}'.format(num)] = SamplesDict(parameters, dataset)

        self.chains = ['chain_{}'.format(num) for num, _ in enumerate(chains)]
        self.parameters = parameters

    @property
    def T(self):
        return MCMCSamplesDict({param:{chain:dataset[param] for chain, dataset in self.items()} for param in self[self.chains[0]].keys()},
          transpose=True)

    @property
    def average(self):
        if self.transpose:
            data = SamplesDict({param:np.mean([self[param][key][:self.minimum_number_of_samples] for key in self[param].keys()],
              axis=0) for param in self.parameters},
              logger_warn='debug')
        else:
            data = SamplesDict({param:np.mean([self[key][param][:self.minimum_number_of_samples] for key in self.keys()],
              axis=0) for param in self.parameters},
              logger_warn='debug')
        return data

    @property
    def nchains(self):
        if self.transpose:
            parameters = list(self.keys())
            return len(self[parameters[0]])
        else:
            return len(self)

    @property
    def number_of_samples(self):
        if self.transpose:
            return {chain:len(self[iterator][chain]) for iterator, chain in zip(self.keys(), self.chains)}
        else:
            return {chain:self[iterator].number_of_samples for iterator, chain in zip(self.keys(), self.chains)}

    @property
    def total_number_of_samples(self):
        return np.sum([length for length in self.number_of_samples.values()])

    @property
    def minimum_number_of_samples(self):
        return np.min([length for length in self.number_of_samples.values()])

    def discard_samples(self, number):
        """Remove the first n samples

        Parameters
        ----------
        number: int/dict
            Number of samples that you wish to remove across all chains or a
            dictionary containing the number of samples to remove per chain
        """
        if isinstance(number, int):
            number = {chain:number for chain in self.keys()}
        for chain in self.keys():
            self[chain].discard_samples(number[chain])

        return self

    def burnin(self, *args, algorithm='burnin_by_step_number', **kwargs):
        """Remove the first N samples as burnin

        Parameters
        ----------
        algorithm: str, optional
            The algorithm you wish to use to remove samples as burnin. Default
            is 'burnin_by_step_number'. See
            `pesummary.core.file.mcmc.algorithms` for list of available
            algorithms
        """
        from pesummary.core.file import mcmc
        if algorithm not in mcmc.algorithms:
            raise ValueError('{} is not a valid algorithm for removing samples as burnin'.format(algorithm))
        arguments = [self] + [i for i in args]
        return (getattr(mcmc, algorithm))(*arguments, **kwargs)

    def gelman_rubin(self, parameter, decimal=5):
        """Return the gelman rubin statistic between chains for a given
        parameter

        Parameters
        ----------
        parameter: str
            name of the parameter you wish to return the gelman rubin statistic
            for
        decimal: int
            number of decimal places to keep when rounding
        """
        from pesummary.utils.utils import gelman_rubin
        if self.transpose:
            samples = [self[parameter][chain] for chain in self.chains]
        else:
            samples = [self[chain][parameter] for chain in self.chains]
        return _gelman_rubin(samples, decimal=decimal)


class Array(np.ndarray):
    __doc__ = 'Class to add extra functions and methods to np.ndarray\n\n    Parameters\n    ----------\n    input_aray: list/array\n        input list/array\n\n    Attributes\n    ----------\n    median: float\n        median of the input array\n    mean: float\n        mean of the input array\n    '
    __slots__ = ['standard_deviation', 'minimum', 'maximum', 'maxL', 'weights']

    def __new__(cls, input_array, likelihood=None, weights=None):
        obj = np.asarray(input_array).view(cls)
        obj.standard_deviation = np.std(obj)
        obj.minimum = np.min(obj)
        obj.maximum = np.max(obj)
        obj.maxL = cls._maxL(obj, likelihood)
        obj.weights = weights
        return obj

    def __reduce__(self):
        pickled_state = super(Array, self).__reduce__()
        new_state = pickled_state[2] + tuple([getattr(self, i) for i in self.__slots__])
        return (
         pickled_state[0], pickled_state[1], new_state)

    def __setstate__(self, state):
        self.standard_deviation = state[(-5)]
        self.minimum = state[(-4)]
        self.maximum = state[(-3)]
        self.maxL = state[(-2)]
        self.weights = state[(-1)]
        super(Array, self).__setstate__(state[0:-5])

    def average(self, type='mean'):
        """Return the average of the array

        Parameters
        ----------
        type: str
            the method to average the array
        """
        if type == 'mean':
            return self._mean(self, weights=(self.weights))
        else:
            if type == 'median':
                return self._median(self, weights=(self.weights))
            return

    @staticmethod
    def _mean(array, weights=None):
        """Compute the mean from a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        """
        if weights is None:
            return np.mean(array)
        else:
            weights = np.array(weights).flatten() / float(sum(weights))
            return float(np.dot(np.array(array), weights))

    @staticmethod
    def _median(array, weights=None):
        """Compute the median from a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        """
        if weights is None:
            return np.median(array)
        else:
            return Array.percentile(array, weights=weights, percentile=0.5)

    @staticmethod
    def _maxL(array, likelihood=None):
        """Return the maximum likelihood value of the array

        Parameters
        ----------
        array: np.ndarray
            input array
        likelihood: np.ndarray, optional
            likelihoods associated with each sample
        """
        if likelihood is not None:
            likelihood = list(likelihood)
            ind = likelihood.index(np.max(likelihood))
            return array[ind]

    @staticmethod
    def percentile(array, weights=None, percentile=None):
        """Compute the Nth percentile of a set of weighted samples

        Parameters
        ----------
        array: np.ndarray
            input array
        weights: np.ndarray, optional
            list of weights associated with each sample
        percentile: float, list
            list of percentiles to compute
        """
        if weights is None:
            return np.percentile(array, percentile)
        else:
            array, weights = np.array(array), np.array(weights)
            percentile_type = percentile
            if not isinstance(percentile, (list, np.ndarray)):
                percentile = [
                 float(percentile)]
            percentile = np.array([float(i) for i in percentile])
            if not all(i < 1 for i in percentile):
                percentile *= 0.01
            ind_sorted = np.argsort(array)
            sorted_data = array[ind_sorted]
            sorted_weights = weights[ind_sorted]
            Sn = np.cumsum(sorted_weights)
            Pn = (Sn - 0.5 * sorted_weights) / Sn[(-1)]
            data = np.interp(percentile, Pn, sorted_data)
            if isinstance(percentile_type, (int, float, np.float64, np.float32)):
                return float(data[0])
            return data

    def confidence_interval(self, percentile=None):
        """Return the confidence interval of the array

        Parameters
        ----------
        percentile: int/list, optional
            Percentile or sequence of percentiles to compute, which must be
            between 0 and 100 inclusive
        """
        if percentile is not None:
            if isinstance(percentile, int):
                return self.percentile(self, self.weights, percentile)
            return np.array([self.percentile(self, self.weights, i) for i in percentile])
        else:
            return np.array([self.percentile(self, self.weights, i) for i in (5, 95)])

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self.standard_deviation = getattr(obj, 'standard_deviation', None)
        self.minimum = getattr(obj, 'minimum', None)
        self.maximum = getattr(obj, 'maximum', None)
        self.maxL = getattr(obj, 'maxL', None)
        self.weights = getattr(obj, 'weights', None)
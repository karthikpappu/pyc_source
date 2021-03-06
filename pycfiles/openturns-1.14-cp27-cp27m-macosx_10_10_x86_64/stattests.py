# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/stattests.py
# Compiled at: 2019-11-13 10:35:53
"""Statistical tests."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _stattests
else:
    import _stattests
try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_repr(self):
    try:
        strthis = 'proxy of ' + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ''

    return '<%s.%s; %s >' % (self.__class__.__module__, self.__class__.__name__, strthis)


def _swig_setattr_nondynamic_instance_variable(set):

    def set_instance_attr(self, name, value):
        if name == 'thisown':
            self.this.own(value)
        elif name == 'this':
            set(self, name, value)
        elif hasattr(self, name) and isinstance(getattr(type(self), name), property):
            set(self, name, value)
        else:
            raise AttributeError('You cannot add instance attributes to %s' % self)

    return set_instance_attr


def _swig_setattr_nondynamic_class_variable(set):

    def set_class_attr(cls, name, value):
        if hasattr(cls, name) and not isinstance(getattr(cls, name), property):
            set(cls, name, value)
        else:
            raise AttributeError('You cannot add class attributes to %s' % cls)

    return set_class_attr


def _swig_add_metaclass(metaclass):
    """Class decorator for adding a metaclass to a SWIG wrapped class - a slimmed down version of six.add_metaclass"""

    def wrapper(cls):
        return metaclass(cls.__name__, cls.__bases__, cls.__dict__.copy())

    return wrapper


class _SwigNonDynamicMeta(type):
    """Meta class to enforce nondynamic attributes (no new attributes) for a class"""
    __setattr__ = _swig_setattr_nondynamic_class_variable(type.__setattr__)


class SwigPyIterator(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined - class is abstract')

    __repr__ = _swig_repr
    __swig_destroy__ = _stattests.delete_SwigPyIterator

    def value(self):
        return _stattests.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _stattests.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _stattests.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _stattests.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _stattests.SwigPyIterator_equal(self, x)

    def copy(self):
        return _stattests.SwigPyIterator_copy(self)

    def next(self):
        return _stattests.SwigPyIterator_next(self)

    def __next__(self):
        return _stattests.SwigPyIterator___next__(self)

    def previous(self):
        return _stattests.SwigPyIterator_previous(self)

    def advance(self, n):
        return _stattests.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _stattests.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _stattests.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _stattests.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _stattests.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _stattests.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _stattests.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_stattests.SwigPyIterator_swigregister(SwigPyIterator)

class TestFailed():
    """TestFailed is used to raise an uniform exception in tests."""
    __type = 'TestFailed'

    def __init__(self, reason=''):
        self.reason = reason

    def type(self):
        return TestFailed.__type

    def what(self):
        return self.reason

    def __str__(self):
        return TestFailed.__type + ': ' + self.reason

    def __lshift__(self, ch):
        self.reason += ch
        return self


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo, openturns.model_copula

class FittingTest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    @staticmethod
    def BestModelBIC(*args):
        """
        Select the best model according to the Bayesian information criterion.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distributions.

        Returns
        -------
        best_model : :class:`~openturns.Distribution`
            The best distribution for the sample according to Bayesian information
            criterion.
            This may raise a warning if the best model does not perform well.
        best_bic : float
            The Bayesian information criterion with the best model.

        See Also
        --------
        FittingTest_BIC

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> tested_distributions = [ot.ExponentialFactory(), ot.NormalFactory()]
        >>> best_model, best_bic = ot.FittingTest.BestModelBIC(sample, tested_distributions)
        >>> print(best_model)
        Normal(mu = -0.0944924, sigma = 0.989808)
        """
        return _stattests.FittingTest_BestModelBIC(*args)

    @staticmethod
    def BestModelKolmogorov(*args):
        """
        Select the best model according to the Kolmogorov goodness-of-fit test.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distributions.

        Returns
        -------
        best_model : :class:`~openturns.Distribution`
            The best distribution for the sample according to Bayesian information
            criterion.
            This may raise a warning if the best model does not perform well.
        best_result : :class:`~openturns.TestResult`
            Best test result.

        See Also
        --------
        FittingTest_Kolmogorov

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> tested_distributions = [ot.ExponentialFactory(), ot.NormalFactory()]
        >>> best_model, best_result = ot.FittingTest.BestModelKolmogorov(sample, tested_distributions)
        >>> print(best_model)
        Normal(mu = -0.0944924, sigma = 0.989808)
        """
        return _stattests.FittingTest_BestModelKolmogorov(*args)

    @staticmethod
    def BestModelChiSquared(*args):
        r"""
        Select the best model according to the :math:`\chi^2` goodness-of-fit test.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distributions.

        Returns
        -------
        best_model : :class:`~openturns.Distribution`
            The best distribution for the sample according to Bayesian information
            criterion.
            This may raise a warning if the best model does not perform well.
        best_result : :class:`~openturns.TestResult`
            Best test result.

        See Also
        --------
        FittingTest_ChiSquared

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Poisson()
        >>> sample = distribution.getSample(30)
        >>> tested_distributions = [ot.PoissonFactory(), ot.UserDefinedFactory()]
        >>> best_model, best_bic = ot.FittingTest.BestModelBIC(sample, tested_distributions)
        >>> print(best_model)
        Poisson(lambda = 1.06667)
        """
        return _stattests.FittingTest_BestModelChiSquared(*args)

    @staticmethod
    def BIC(*args):
        r"""
        Compute the Bayesian information criterion.

        Refer to :ref:`bic`.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distribution.
        n_parameters : int, :math:`0 \leq k`, optional
            The number of parameters in the distribution that have been estimated from
            the sample.
            This parameter must not be provided if a :class:`~openturns.DistributionFactory`
            was provided as the second argument (it will internally be set to the
            number of parameters estimated by the :class:`~openturns.DistributionFactory`).
            It can be specified if  a :class:`~openturns.Distribution` was provided
            as the second argument, but if it is not, it will be set equal to 0.

        Returns
        -------
        estimatedDist : :class:`~openturns.Distribution`
            Estimated distribution (case factory as argument)
        BIC : float
            The Bayesian information criterion.

        Notes
        -----
        This is used for model selection.
        In case we set a factory argument, the method returns both the estimated distribution and BIC value.
        Otherwise it returns only the BIC value.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> ot.FittingTest.BIC(sample, distribution)
        2.793869...
        >>> ot.FittingTest.BIC(sample, distribution, 2)
        3.020615...
        >>> fitted_dist, bic = ot.FittingTest.BIC(sample, ot.NormalFactory())
        >>> bic
        3.010802...
        """
        return _stattests.FittingTest_BIC(*args)

    @staticmethod
    def Kolmogorov(*args):
        r"""
        Perform a Kolmogorov goodness-of-fit test for 1-d continuous distributions.

        Refer to :ref:`kolmogorov_smirnov_test`.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distribution.
        level : float, :math:`0 \leq \alpha \leq 1`, optional
            This is the risk :math:`\alpha` of committing a Type I error,
            that is an incorrect rejection of a true null hypothesis.
        n_parameters : int, :math:`0 \leq k`, optional
            The number of parameters in the distribution that have been estimated from
            the sample.
            This parameter must not be provided if a :class:`~openturns.DistributionFactory`
            was provided as the second argument (it will internally be set to the
            number of parameters estimated by the :class:`~openturns.DistributionFactory`).
            It can be specified if a :class:`~openturns.Distribution` was provided
            as the second argument, but if it is not, it will be set equal to 0.

        Returns
        -------
        fitted_dist : :class:`~openturns.Distribution`
            Estilmated distribution (if model is of type :class:`~openturns.DistributionFactory`).
        test_result : :class:`~openturns.TestResult`
            Test result.

        Raises
        ------
        TypeError : If the distribution is not continuous or if the sample is
            multivariate.

        Notes
        -----
        The present implementation of the Kolmogorov goodness-of-fit test is
        two-sided. This uses an external C implementation of the Kolmogorov cumulative
        distribution function by [simard2011]_.
        If it is called with a distribution, it is supposed to be fully specified ie no parameter has been estimated from the given sample. Otherwise, the distribution is estimated using the given factory based on the given sample and the distribution of the test statistics is estimated using a Monte Carlo approach (see the *FittingTest-KolmogorovSamplingSize* key in :class:`~openturns.ResourceMap`).

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> fitted_dist, test_result = ot.FittingTest.Kolmogorov(sample, ot.NormalFactory(), 0.01)
        >>> test_result
        class=TestResult name=Unnamed type=Kolmogorov Normal binaryQualityMeasure=true p-value threshold=0.01 p-value=0.7 statistic=0.106933 description=[Normal(mu = -0.0944924, sigma = 0.989808) vs sample Normal]
        """
        return _stattests.FittingTest_Kolmogorov(*args)

    @staticmethod
    def ComputeKolmogorovStatistics(sample, distribution):
        """
        Compute the unscaled Kolmogorov distance between a sample and a distribution.

        The distance is the maximum absolute deviation between the empirical CDF of the
        given sample and the CDF of the given distribution.

        Parameters
        ----------
        sample : 2-d float array
            A continuous 1D distribution sample.
        distribution : :class:`~openturns.Distribution`
            A continuous 1D distribution.

        Returns
        -------
        distance : float
            The Kolmogorov distance.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(20)
        >>> ot.FittingTest.ComputeKolmogorovStatistics(sample, distribution)
        0.14727...
        """
        return _stattests.FittingTest_ComputeKolmogorovStatistics(sample, distribution)

    @staticmethod
    def ChiSquared(*args):
        r"""
        Perform a :math:`\chi^2` goodness-of-fit test for 1-d discrete distributions.

        Refer to :ref:`chi2_fitting_test`.

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
            Tested distribution.
        level : float, :math:`0 \leq \alpha \leq 1`, optional
            This is the risk :math:`\alpha` of committing a Type I error,
            that is an incorrect rejection of a true null hypothesis.
        n_parameters : int, :math:`0 \leq k`, optional
            The number of parameters in the distribution that have been estimated from
            the sample.
            This parameter must not be provided if a :class:`~openturns.DistributionFactory`
            was provided as the second argument (it will internally be set to the
            number of parameters estimated by the :class:`~openturns.DistributionFactory`).
            It can be specified if  a :class:`~openturns.Distribution` was provided
            as the second argument, but if it is not, it will be set equal to 0.

        Returns
        -------
        fitted_dist : :class:`~openturns.Distribution`
            Estilmated distribution (if model is of type :class:`~openturns.DistributionFactory`).
        test_result : :class:`~openturns.TestResult`
            Test result.

        Raises
        ------
        TypeError : If the distribution is not discrete or if the sample is
            multivariate.

        Notes
        -----
        This is an interface to the `chisq.test function from the
        'stats' R package <http://stat.ethz.ch/R-manual/R-patched/library/stats/html/chisq.test.html>`_.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Poisson()
        >>> sample = distribution.getSample(30)
        >>> fitted_dist, test_result = ot.FittingTest.ChiSquared(sample, ot.PoissonFactory(), 0.01)
        >>> test_result
        class=TestResult name=Unnamed type=ChiSquared Poisson binaryQualityMeasure=true p-value threshold=0.01 p-value=0.698061 statistic=0.150497 description=[Poisson(lambda = 1.06667) vs sample Poisson]
        """
        return _stattests.FittingTest_ChiSquared(*args)

    __swig_destroy__ = _stattests.delete_FittingTest


_stattests.FittingTest_swigregister(FittingTest)

def FittingTest_BestModelBIC(*args):
    """
    Select the best model according to the Bayesian information criterion.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distributions.

    Returns
    -------
    best_model : :class:`~openturns.Distribution`
        The best distribution for the sample according to Bayesian information
        criterion.
        This may raise a warning if the best model does not perform well.
    best_bic : float
        The Bayesian information criterion with the best model.

    See Also
    --------
    FittingTest_BIC

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> tested_distributions = [ot.ExponentialFactory(), ot.NormalFactory()]
    >>> best_model, best_bic = ot.FittingTest.BestModelBIC(sample, tested_distributions)
    >>> print(best_model)
    Normal(mu = -0.0944924, sigma = 0.989808)
    """
    return _stattests.FittingTest_BestModelBIC(*args)


def FittingTest_BestModelKolmogorov(*args):
    """
    Select the best model according to the Kolmogorov goodness-of-fit test.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distributions.

    Returns
    -------
    best_model : :class:`~openturns.Distribution`
        The best distribution for the sample according to Bayesian information
        criterion.
        This may raise a warning if the best model does not perform well.
    best_result : :class:`~openturns.TestResult`
        Best test result.

    See Also
    --------
    FittingTest_Kolmogorov

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> tested_distributions = [ot.ExponentialFactory(), ot.NormalFactory()]
    >>> best_model, best_result = ot.FittingTest.BestModelKolmogorov(sample, tested_distributions)
    >>> print(best_model)
    Normal(mu = -0.0944924, sigma = 0.989808)
    """
    return _stattests.FittingTest_BestModelKolmogorov(*args)


def FittingTest_BestModelChiSquared(*args):
    r"""
    Select the best model according to the :math:`\chi^2` goodness-of-fit test.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    models : list of :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distributions.

    Returns
    -------
    best_model : :class:`~openturns.Distribution`
        The best distribution for the sample according to Bayesian information
        criterion.
        This may raise a warning if the best model does not perform well.
    best_result : :class:`~openturns.TestResult`
        Best test result.

    See Also
    --------
    FittingTest_ChiSquared

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Poisson()
    >>> sample = distribution.getSample(30)
    >>> tested_distributions = [ot.PoissonFactory(), ot.UserDefinedFactory()]
    >>> best_model, best_bic = ot.FittingTest.BestModelBIC(sample, tested_distributions)
    >>> print(best_model)
    Poisson(lambda = 1.06667)
    """
    return _stattests.FittingTest_BestModelChiSquared(*args)


def FittingTest_BIC(*args):
    r"""
    Compute the Bayesian information criterion.

    Refer to :ref:`bic`.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distribution.
    n_parameters : int, :math:`0 \leq k`, optional
        The number of parameters in the distribution that have been estimated from
        the sample.
        This parameter must not be provided if a :class:`~openturns.DistributionFactory`
        was provided as the second argument (it will internally be set to the
        number of parameters estimated by the :class:`~openturns.DistributionFactory`).
        It can be specified if  a :class:`~openturns.Distribution` was provided
        as the second argument, but if it is not, it will be set equal to 0.

    Returns
    -------
    estimatedDist : :class:`~openturns.Distribution`
        Estimated distribution (case factory as argument)
    BIC : float
        The Bayesian information criterion.

    Notes
    -----
    This is used for model selection.
    In case we set a factory argument, the method returns both the estimated distribution and BIC value.
    Otherwise it returns only the BIC value.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> ot.FittingTest.BIC(sample, distribution)
    2.793869...
    >>> ot.FittingTest.BIC(sample, distribution, 2)
    3.020615...
    >>> fitted_dist, bic = ot.FittingTest.BIC(sample, ot.NormalFactory())
    >>> bic
    3.010802...
    """
    return _stattests.FittingTest_BIC(*args)


def FittingTest_Kolmogorov(*args):
    r"""
    Perform a Kolmogorov goodness-of-fit test for 1-d continuous distributions.

    Refer to :ref:`kolmogorov_smirnov_test`.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distribution.
    level : float, :math:`0 \leq \alpha \leq 1`, optional
        This is the risk :math:`\alpha` of committing a Type I error,
        that is an incorrect rejection of a true null hypothesis.
    n_parameters : int, :math:`0 \leq k`, optional
        The number of parameters in the distribution that have been estimated from
        the sample.
        This parameter must not be provided if a :class:`~openturns.DistributionFactory`
        was provided as the second argument (it will internally be set to the
        number of parameters estimated by the :class:`~openturns.DistributionFactory`).
        It can be specified if a :class:`~openturns.Distribution` was provided
        as the second argument, but if it is not, it will be set equal to 0.

    Returns
    -------
    fitted_dist : :class:`~openturns.Distribution`
        Estilmated distribution (if model is of type :class:`~openturns.DistributionFactory`).
    test_result : :class:`~openturns.TestResult`
        Test result.

    Raises
    ------
    TypeError : If the distribution is not continuous or if the sample is
        multivariate.

    Notes
    -----
    The present implementation of the Kolmogorov goodness-of-fit test is
    two-sided. This uses an external C implementation of the Kolmogorov cumulative
    distribution function by [simard2011]_.
    If it is called with a distribution, it is supposed to be fully specified ie no parameter has been estimated from the given sample. Otherwise, the distribution is estimated using the given factory based on the given sample and the distribution of the test statistics is estimated using a Monte Carlo approach (see the *FittingTest-KolmogorovSamplingSize* key in :class:`~openturns.ResourceMap`).

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> fitted_dist, test_result = ot.FittingTest.Kolmogorov(sample, ot.NormalFactory(), 0.01)
    >>> test_result
    class=TestResult name=Unnamed type=Kolmogorov Normal binaryQualityMeasure=true p-value threshold=0.01 p-value=0.7 statistic=0.106933 description=[Normal(mu = -0.0944924, sigma = 0.989808) vs sample Normal]
    """
    return _stattests.FittingTest_Kolmogorov(*args)


def FittingTest_ComputeKolmogorovStatistics(sample, distribution):
    """
    Compute the unscaled Kolmogorov distance between a sample and a distribution.

    The distance is the maximum absolute deviation between the empirical CDF of the
    given sample and the CDF of the given distribution.

    Parameters
    ----------
    sample : 2-d float array
        A continuous 1D distribution sample.
    distribution : :class:`~openturns.Distribution`
        A continuous 1D distribution.

    Returns
    -------
    distance : float
        The Kolmogorov distance.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(20)
    >>> ot.FittingTest.ComputeKolmogorovStatistics(sample, distribution)
    0.14727...
    """
    return _stattests.FittingTest_ComputeKolmogorovStatistics(sample, distribution)


def FittingTest_ChiSquared(*args):
    r"""
    Perform a :math:`\chi^2` goodness-of-fit test for 1-d discrete distributions.

    Refer to :ref:`chi2_fitting_test`.

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    model : :class:`~openturns.Distribution` or :class:`~openturns.DistributionFactory`
        Tested distribution.
    level : float, :math:`0 \leq \alpha \leq 1`, optional
        This is the risk :math:`\alpha` of committing a Type I error,
        that is an incorrect rejection of a true null hypothesis.
    n_parameters : int, :math:`0 \leq k`, optional
        The number of parameters in the distribution that have been estimated from
        the sample.
        This parameter must not be provided if a :class:`~openturns.DistributionFactory`
        was provided as the second argument (it will internally be set to the
        number of parameters estimated by the :class:`~openturns.DistributionFactory`).
        It can be specified if  a :class:`~openturns.Distribution` was provided
        as the second argument, but if it is not, it will be set equal to 0.

    Returns
    -------
    fitted_dist : :class:`~openturns.Distribution`
        Estilmated distribution (if model is of type :class:`~openturns.DistributionFactory`).
    test_result : :class:`~openturns.TestResult`
        Test result.

    Raises
    ------
    TypeError : If the distribution is not discrete or if the sample is
        multivariate.

    Notes
    -----
    This is an interface to the `chisq.test function from the
    'stats' R package <http://stat.ethz.ch/R-manual/R-patched/library/stats/html/chisq.test.html>`_.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Poisson()
    >>> sample = distribution.getSample(30)
    >>> fitted_dist, test_result = ot.FittingTest.ChiSquared(sample, ot.PoissonFactory(), 0.01)
    >>> test_result
    class=TestResult name=Unnamed type=ChiSquared Poisson binaryQualityMeasure=true p-value threshold=0.01 p-value=0.698061 statistic=0.150497 description=[Poisson(lambda = 1.06667) vs sample Poisson]
    """
    return _stattests.FittingTest_ChiSquared(*args)


class HypothesisTest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    @staticmethod
    def ChiSquared(firstSample, secondSample, level=0.05):
        """
        Test whether two discrete samples are independent.

        **Available usages**:

            HypothesisTest.ChiSquared(*firstSample, secondSample*)

            HypothesisTest.ChiSquared(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension 1.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Pearson, HypothesisTest_Spearman

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distCol = [ot.Poisson(3), ot.Binomial(10, 0.3)]
        >>> distribution = ot.ComposedDistribution(distCol)
        >>> sample = distribution.getSample(30)
        >>> test_result = ot.HypothesisTest.ChiSquared(sample[:,0], sample[:,1])
        >>> print(test_result)
        class=TestResult name=Unnamed type=ChiSquared binaryQualityMeasure=true p-value threshold=0.05 p-value=0.855945 statistic=4.74502 description=[]

        """
        return _stattests.HypothesisTest_ChiSquared(firstSample, secondSample, level)

    @staticmethod
    def Pearson(firstSample, secondSample, level=0.05):
        r"""
        Test whether two discrete samples are independent.

        Refer to :ref:`pearson_test`.

        **Available usages**:

            HypothesisTest.Pearson(*firstSample, secondSample*)

            HypothesisTest.Pearson(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Spearman

        Notes
        -----
        The Pearson Test is used to check whether two samples which are assumed to form
        a gaussian vector are independent (based on the evaluation of the linear
        correlation coefficient).

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distCol = [ot.Normal(), ot.Normal()]
        >>> firstSample = ot.Normal().getSample(30)
        >>> secondSample = ot.Normal().getSample(30)
        >>> test_result = ot.HypothesisTest.Pearson(firstSample, secondSample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.984737 statistic=0.019302 description=[]

        """
        return _stattests.HypothesisTest_Pearson(firstSample, secondSample, level)

    @staticmethod
    def TwoSamplesKolmogorov(sample1, sample2, level=0.05):
        r"""
        Test whether two samples follows the same distribution.

        If the p-value is high, then we cannot reject the hypothesis that the
        distributions of the two samples are the same.

        Parameters
        ----------
        sample1 : 2-d float array
            A continuous distribution sample.
        sample2 : 2-d float array
            Another continuous distribution sample, can be of different size.
        level : float, :math:`0 \leq \alpha \leq 1`, optional
            This is the risk :math:`\alpha` of committing a Type I error,
            that is an incorrect rejection of a true null hypothesis.
            Default value is 0.05

        Returns
        -------
        test_result : :class:`~openturns.TestResult`
            Test result.

        Notes
        -----
        This statistical test might be used to compare two samples :math:`\{x_1, \ldots, x_N\}`
        and :math:`\{x^{'}_1, \ldots, x^{'}_M\}` (of sizes not necessarily equal).
        The goal is to determine whether these two samples come from
        the same probability distribution or not. (without any information of the underlying
        distribution under the null hypothesis)

        As application, if null hypothesis could not be rejected, the two samples could be
        be aggregated in order to increase the robustness of further statistical analysis.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> sample1 = ot.Normal().getSample(20)
        >>> sample2 = ot.Normal(0.1, 1.1).getSample(30)
        >>> ot.HypothesisTest.TwoSamplesKolmogorov(sample1, sample2)
        class=TestResult name=Unnamed type=TwoSamplesKolmogorov binaryQualityMeasure=true p-value threshold=0.05 p-value=0.554765 statistic=0.216667 description=[sampleNormal vs sample Normal]
        """
        return _stattests.HypothesisTest_TwoSamplesKolmogorov(sample1, sample2, level)

    @staticmethod
    def Spearman(firstSample, secondSample, level=0.05):
        r"""
        Test whether two samples have no rank correlation.

        Refer to :ref:`spearman_test`.

        **Available usages**:

            HypothesisTest.Spearman(*firstSample, secondSample*)

            HypothesisTest.Spearman(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Pearson

        Notes
        -----
        The Spearman Test is used to check whether two samples of dimension 1
        have no rank correlation.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> firstSample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction(['x'], ['x^2'])
        >>> secondSample = func(firstSample)
        >>> test_result = ot.HypothesisTest.Spearman(firstSample, secondSample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.442067 statistic=-0.774521 description=[]

        """
        return _stattests.HypothesisTest_Spearman(firstSample, secondSample, level)

    @staticmethod
    def PartialPearson(firstSample, secondSample, selection, level=0.05):
        r"""
        Test whether two discrete samples are independent.

        **Available usages**:

            HypothesisTest.PartialPearson(*firstSample, secondSample, selection*)

            HypothesisTest.PartialPearson(*firstSample, secondSample, selection, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        selection : sequence of integers, maximum integer value :math:`< n`
            List of indices selecting which subsets of the first sample will successively
            be tested with the second sample through the Pearson test.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Pearson, HypothesisTest_FullPearson

        Notes
        -----
        The Partial Pearson Test is used to check the independence between two samples:
        *firstSample* of dimension *n* and *secondSample* of dimension 1. The parameter
        *selection* enables to select specific subsets of the *firstSample* to be tested.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distCol = [ot.Normal(), ot.Normal(), ot.Normal(), ot.Normal()]
        >>> S = ot.CorrelationMatrix(4)
        >>> S[0, 3] = 0.9
        >>> copula = ot.NormalCopula(S)
        >>> distribution = ot.ComposedDistribution(distCol, copula)
        >>> sample = distribution.getSample(30)
        >>> firstSample = sample[:, :3]
        >>> secondSample = sample[:, 3]
        >>> test_result = ot.HypothesisTest.PartialPearson(firstSample, secondSample, [0, 2])
        >>> print(test_result)
        [class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=false p-value threshold=0.05 p-value=1.17002e-10 statistic=9.91178 description=[],class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.19193 statistic=-1.33717 description=[]]

        """
        return _stattests.HypothesisTest_PartialPearson(firstSample, secondSample, selection, level)

    @staticmethod
    def PartialSpearman(firstSample, secondSample, selection, level=0.05):
        r"""
        Test whether two sample have no rank correlation.

        **Available usages**:

        HypothesisTest_PartialSpearman(*firstSample, secondSample, selection*)

        HypothesisTest_PartialSpearman(*firstSample, secondSample, selection, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        selection : sequence of integers, maximum integer value :math:`< n`
            List of indices selecting which subsets of the first sample will successively
            be tested with the second sample through the Spearman test.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Spearman, HypothesisTest_FullSpearman

        Notes
        -----
        The Partial Spearman Test is used to check hypothesis of no rank correlation
        between two samples: *firstSample* of dimension :math:`n` and *secondSample* of
        dimension 1. The parameter *selection* enables to select specific subsets of
        marginals of *firstSample* to be tested.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction(['x'], ['x', 'x^2', 'x^3', 'sin(5*x)'])
        >>> testedSample = func(sample)
        >>> test_result = ot.HypothesisTest.PartialSpearman(testedSample, sample, [0,3])
        >>> print(test_result)
        [class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=false p-value threshold=0.05 p-value=0 statistic=1.79769e+308 description=[],class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.570533 statistic=-0.569502 description=[]]

        """
        return _stattests.HypothesisTest_PartialSpearman(firstSample, secondSample, selection, level)

    @staticmethod
    def FullPearson(firstSample, secondSample, level=0.05):
        r"""
        Test whether two discrete samples are independent.

        **Available usages**:

            HypothesisTest.FullPearson(*firstSample, secondSample*)

            HypothesisTest.FullPearson(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            First tested sample, of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Second tested sample, of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        HypothesisTest_Pearson, HypothesisTest_PartialPearson

        Notes
        -----
        The Full Pearson Test is the independence Pearson test between 2 samples :
        *firstSample* of dimension *n* and *secondSample* of dimension 1. If
        *firstSample[i]* is the sample extracted from *firstSample*
        (:math:`i^{th}` coordinate of each point of the sample), FullPearson
        performs the independence Pearson test simultaneously on *firstSample[i]* and 
        secondSample. For all *i*, it is supposed that the couple (*firstSample[i]* and
        *secondSample*) is issued from a gaussian vector.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distCol = [ot.Normal()] * 3
        >>> S = ot.CorrelationMatrix(3)
        >>> S[0, 2] = 0.9
        >>> copula = ot.NormalCopula(S)
        >>> distribution = ot.ComposedDistribution(distCol, copula)
        >>> sample = distribution.getSample(30)
        >>> firstSample = sample[:, :2]
        >>> secondSample = sample[:, 2]
        >>> test_result = ot.HypothesisTest.FullPearson(firstSample, secondSample)
        >>> print(test_result)
        [class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=false p-value threshold=0.05 p-value=7.23...e-14 statistic=13.61 description=[],class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.895124 statistic=-0.133027 description=[]]

        """
        return _stattests.HypothesisTest_FullPearson(firstSample, secondSample, level)

    @staticmethod
    def FullSpearman(firstSample, secondSample, level=0.05):
        r"""
        Test whether two samples have no rank correlation.

        **Available usages**:

            HypothesisTest.FullSpearman(*firstSample, secondSample*)

            HypothesisTest.FullSpearman(*firstSample, secondSample, level*)

        Parameters
        ----------
        firstSample : 2-d sequence of float
            Sample of dimension :math:`n \geq 1`.
        secondSample : 2-d sequence of float
            Sample of dimension 1.
        level : positive float :math:`< 1`
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResultCollection`
            Collection of :class:`~openturns.TestResult` of size :math:`n`, one result per component of the first sample.

        See Also
        --------
        HypothesisTest_Spearman, HypothesisTest_PartialSpearman

        Notes
        -----
        The Full Spearman Test is used to check the hypothesis of no rank correlation
        between two samples: *firstSample* of dimension :math:`n` and *secondSample* of
        dimension 1. The test is done marginal by marginal on the first sample.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> func = ot.SymbolicFunction(['x'], ['x', 'x^2'])
        >>> testedSample = func(sample)
        >>> test_result = ot.HypothesisTest.FullSpearman(testedSample, sample, 0.05)
        >>> print(test_result)
        [class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=false p-value threshold=0.05 p-value=0 statistic=1.79769e+308 description=[],class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.442067 statistic=-0.774521 description=[]]

        """
        return _stattests.HypothesisTest_FullSpearman(firstSample, secondSample, level)

    __swig_destroy__ = _stattests.delete_HypothesisTest


_stattests.HypothesisTest_swigregister(HypothesisTest)

def HypothesisTest_ChiSquared(firstSample, secondSample, level=0.05):
    """
    Test whether two discrete samples are independent.

    **Available usages**:

        HypothesisTest.ChiSquared(*firstSample, secondSample*)

        HypothesisTest.ChiSquared(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension 1.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Pearson, HypothesisTest_Spearman

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distCol = [ot.Poisson(3), ot.Binomial(10, 0.3)]
    >>> distribution = ot.ComposedDistribution(distCol)
    >>> sample = distribution.getSample(30)
    >>> test_result = ot.HypothesisTest.ChiSquared(sample[:,0], sample[:,1])
    >>> print(test_result)
    class=TestResult name=Unnamed type=ChiSquared binaryQualityMeasure=true p-value threshold=0.05 p-value=0.855945 statistic=4.74502 description=[]

    """
    return _stattests.HypothesisTest_ChiSquared(firstSample, secondSample, level)


def HypothesisTest_Pearson(firstSample, secondSample, level=0.05):
    r"""
    Test whether two discrete samples are independent.

    Refer to :ref:`pearson_test`.

    **Available usages**:

        HypothesisTest.Pearson(*firstSample, secondSample*)

        HypothesisTest.Pearson(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Spearman

    Notes
    -----
    The Pearson Test is used to check whether two samples which are assumed to form
    a gaussian vector are independent (based on the evaluation of the linear
    correlation coefficient).

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distCol = [ot.Normal(), ot.Normal()]
    >>> firstSample = ot.Normal().getSample(30)
    >>> secondSample = ot.Normal().getSample(30)
    >>> test_result = ot.HypothesisTest.Pearson(firstSample, secondSample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.984737 statistic=0.019302 description=[]

    """
    return _stattests.HypothesisTest_Pearson(firstSample, secondSample, level)


def HypothesisTest_TwoSamplesKolmogorov(sample1, sample2, level=0.05):
    r"""
    Test whether two samples follows the same distribution.

    If the p-value is high, then we cannot reject the hypothesis that the
    distributions of the two samples are the same.

    Parameters
    ----------
    sample1 : 2-d float array
        A continuous distribution sample.
    sample2 : 2-d float array
        Another continuous distribution sample, can be of different size.
    level : float, :math:`0 \leq \alpha \leq 1`, optional
        This is the risk :math:`\alpha` of committing a Type I error,
        that is an incorrect rejection of a true null hypothesis.
        Default value is 0.05

    Returns
    -------
    test_result : :class:`~openturns.TestResult`
        Test result.

    Notes
    -----
    This statistical test might be used to compare two samples :math:`\{x_1, \ldots, x_N\}`
    and :math:`\{x^{'}_1, \ldots, x^{'}_M\}` (of sizes not necessarily equal).
    The goal is to determine whether these two samples come from
    the same probability distribution or not. (without any information of the underlying
    distribution under the null hypothesis)

    As application, if null hypothesis could not be rejected, the two samples could be
    be aggregated in order to increase the robustness of further statistical analysis.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> sample1 = ot.Normal().getSample(20)
    >>> sample2 = ot.Normal(0.1, 1.1).getSample(30)
    >>> ot.HypothesisTest.TwoSamplesKolmogorov(sample1, sample2)
    class=TestResult name=Unnamed type=TwoSamplesKolmogorov binaryQualityMeasure=true p-value threshold=0.05 p-value=0.554765 statistic=0.216667 description=[sampleNormal vs sample Normal]
    """
    return _stattests.HypothesisTest_TwoSamplesKolmogorov(sample1, sample2, level)


def HypothesisTest_Spearman(firstSample, secondSample, level=0.05):
    r"""
    Test whether two samples have no rank correlation.

    Refer to :ref:`spearman_test`.

    **Available usages**:

        HypothesisTest.Spearman(*firstSample, secondSample*)

        HypothesisTest.Spearman(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Pearson

    Notes
    -----
    The Spearman Test is used to check whether two samples of dimension 1
    have no rank correlation.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> firstSample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction(['x'], ['x^2'])
    >>> secondSample = func(firstSample)
    >>> test_result = ot.HypothesisTest.Spearman(firstSample, secondSample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.442067 statistic=-0.774521 description=[]

    """
    return _stattests.HypothesisTest_Spearman(firstSample, secondSample, level)


def HypothesisTest_PartialPearson(firstSample, secondSample, selection, level=0.05):
    r"""
    Test whether two discrete samples are independent.

    **Available usages**:

        HypothesisTest.PartialPearson(*firstSample, secondSample, selection*)

        HypothesisTest.PartialPearson(*firstSample, secondSample, selection, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    selection : sequence of integers, maximum integer value :math:`< n`
        List of indices selecting which subsets of the first sample will successively
        be tested with the second sample through the Pearson test.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Pearson, HypothesisTest_FullPearson

    Notes
    -----
    The Partial Pearson Test is used to check the independence between two samples:
    *firstSample* of dimension *n* and *secondSample* of dimension 1. The parameter
    *selection* enables to select specific subsets of the *firstSample* to be tested.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distCol = [ot.Normal(), ot.Normal(), ot.Normal(), ot.Normal()]
    >>> S = ot.CorrelationMatrix(4)
    >>> S[0, 3] = 0.9
    >>> copula = ot.NormalCopula(S)
    >>> distribution = ot.ComposedDistribution(distCol, copula)
    >>> sample = distribution.getSample(30)
    >>> firstSample = sample[:, :3]
    >>> secondSample = sample[:, 3]
    >>> test_result = ot.HypothesisTest.PartialPearson(firstSample, secondSample, [0, 2])
    >>> print(test_result)
    [class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=false p-value threshold=0.05 p-value=1.17002e-10 statistic=9.91178 description=[],class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.19193 statistic=-1.33717 description=[]]

    """
    return _stattests.HypothesisTest_PartialPearson(firstSample, secondSample, selection, level)


def HypothesisTest_PartialSpearman(firstSample, secondSample, selection, level=0.05):
    r"""
    Test whether two sample have no rank correlation.

    **Available usages**:

    HypothesisTest_PartialSpearman(*firstSample, secondSample, selection*)

    HypothesisTest_PartialSpearman(*firstSample, secondSample, selection, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    selection : sequence of integers, maximum integer value :math:`< n`
        List of indices selecting which subsets of the first sample will successively
        be tested with the second sample through the Spearman test.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Spearman, HypothesisTest_FullSpearman

    Notes
    -----
    The Partial Spearman Test is used to check hypothesis of no rank correlation
    between two samples: *firstSample* of dimension :math:`n` and *secondSample* of
    dimension 1. The parameter *selection* enables to select specific subsets of
    marginals of *firstSample* to be tested.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction(['x'], ['x', 'x^2', 'x^3', 'sin(5*x)'])
    >>> testedSample = func(sample)
    >>> test_result = ot.HypothesisTest.PartialSpearman(testedSample, sample, [0,3])
    >>> print(test_result)
    [class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=false p-value threshold=0.05 p-value=0 statistic=1.79769e+308 description=[],class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.570533 statistic=-0.569502 description=[]]

    """
    return _stattests.HypothesisTest_PartialSpearman(firstSample, secondSample, selection, level)


def HypothesisTest_FullPearson(firstSample, secondSample, level=0.05):
    r"""
    Test whether two discrete samples are independent.

    **Available usages**:

        HypothesisTest.FullPearson(*firstSample, secondSample*)

        HypothesisTest.FullPearson(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        First tested sample, of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Second tested sample, of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    HypothesisTest_Pearson, HypothesisTest_PartialPearson

    Notes
    -----
    The Full Pearson Test is the independence Pearson test between 2 samples :
    *firstSample* of dimension *n* and *secondSample* of dimension 1. If
    *firstSample[i]* is the sample extracted from *firstSample*
    (:math:`i^{th}` coordinate of each point of the sample), FullPearson
    performs the independence Pearson test simultaneously on *firstSample[i]* and 
    secondSample. For all *i*, it is supposed that the couple (*firstSample[i]* and
    *secondSample*) is issued from a gaussian vector.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distCol = [ot.Normal()] * 3
    >>> S = ot.CorrelationMatrix(3)
    >>> S[0, 2] = 0.9
    >>> copula = ot.NormalCopula(S)
    >>> distribution = ot.ComposedDistribution(distCol, copula)
    >>> sample = distribution.getSample(30)
    >>> firstSample = sample[:, :2]
    >>> secondSample = sample[:, 2]
    >>> test_result = ot.HypothesisTest.FullPearson(firstSample, secondSample)
    >>> print(test_result)
    [class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=false p-value threshold=0.05 p-value=7.23...e-14 statistic=13.61 description=[],class=TestResult name=Unnamed type=Pearson binaryQualityMeasure=true p-value threshold=0.05 p-value=0.895124 statistic=-0.133027 description=[]]

    """
    return _stattests.HypothesisTest_FullPearson(firstSample, secondSample, level)


def HypothesisTest_FullSpearman(firstSample, secondSample, level=0.05):
    r"""
    Test whether two samples have no rank correlation.

    **Available usages**:

        HypothesisTest.FullSpearman(*firstSample, secondSample*)

        HypothesisTest.FullSpearman(*firstSample, secondSample, level*)

    Parameters
    ----------
    firstSample : 2-d sequence of float
        Sample of dimension :math:`n \geq 1`.
    secondSample : 2-d sequence of float
        Sample of dimension 1.
    level : positive float :math:`< 1`
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResultCollection`
        Collection of :class:`~openturns.TestResult` of size :math:`n`, one result per component of the first sample.

    See Also
    --------
    HypothesisTest_Spearman, HypothesisTest_PartialSpearman

    Notes
    -----
    The Full Spearman Test is used to check the hypothesis of no rank correlation
    between two samples: *firstSample* of dimension :math:`n` and *secondSample* of
    dimension 1. The test is done marginal by marginal on the first sample.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> func = ot.SymbolicFunction(['x'], ['x', 'x^2'])
    >>> testedSample = func(sample)
    >>> test_result = ot.HypothesisTest.FullSpearman(testedSample, sample, 0.05)
    >>> print(test_result)
    [class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=false p-value threshold=0.05 p-value=0 statistic=1.79769e+308 description=[],class=TestResult name=Unnamed type=Spearman binaryQualityMeasure=true p-value threshold=0.05 p-value=0.442067 statistic=-0.774521 description=[]]

    """
    return _stattests.HypothesisTest_FullSpearman(firstSample, secondSample, level)


class NormalityTest(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def __init__(self, *args, **kwargs):
        raise AttributeError('No constructor defined')

    __repr__ = _swig_repr

    @staticmethod
    def AndersonDarlingNormal(sample, level=0.05):
        """
        Evaluate whether a sample follows a normal distribution.

        Refer to :ref:`anderson_darling_test`.

        **Available usages**:

            NormalityTest.AndersonDarlingNormal(*sample*)

            NormalityTest.AndersonDarlingNormal(*sample, level*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        level : positive float
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        NormalityTest_CramerVonMisesNormal

        Notes
        -----
        The test is used to check whether the sample follows a normal distribution. This
        test gives more importance to extreme values.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> test_result = ot.NormalityTest.AndersonDarlingNormal(sample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=AndersonDarlingNormal binaryQualityMeasure=true p-value threshold=0.05 p-value=0.7268 statistic=0.255405 description=[]

        """
        return _stattests.NormalityTest_AndersonDarlingNormal(sample, level)

    @staticmethod
    def CramerVonMisesNormal(sample, level=0.05):
        """
        Evaluate whether a sample follows a normal distribution.

        Refer to :ref:`cramer_vonmises_test`.

        **Available usages**:

            NormalityTest.CramerVonMisesNormal(*sample*)

            NormalityTest.CramerVonMisesNormal(*sample, level*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Tested sample.
        level : positive float
            Threshold p-value of the test (= first kind risk), it must be
            :math:`< 1`, equal to 0.05 by default.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Structure containing the result of the test.

        See Also
        --------
        NormalityTest_AndersonDarlingNormal

        Notes
        -----
        The test is used to check whether the sample follows a normal distribution. The 
        test concerns the deviation squared and integrated over the entire variation
        domain, it often appears to be more robust than the Kolmogorov-Smirnov test.

        Examples
        --------
        >>> import openturns as ot
        >>> ot.RandomGenerator.SetSeed(0)
        >>> distribution = ot.Normal()
        >>> sample = distribution.getSample(30)
        >>> test_result = ot.NormalityTest.CramerVonMisesNormal(sample)
        >>> print(test_result)
        class=TestResult name=Unnamed type=CramerVonMisesNormal binaryQualityMeasure=true p-value threshold=0.05 p-value=0.682524 statistic=0.0399704 description=[]

        """
        return _stattests.NormalityTest_CramerVonMisesNormal(sample, level)

    __swig_destroy__ = _stattests.delete_NormalityTest


_stattests.NormalityTest_swigregister(NormalityTest)

def NormalityTest_AndersonDarlingNormal(sample, level=0.05):
    """
    Evaluate whether a sample follows a normal distribution.

    Refer to :ref:`anderson_darling_test`.

    **Available usages**:

        NormalityTest.AndersonDarlingNormal(*sample*)

        NormalityTest.AndersonDarlingNormal(*sample, level*)

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    level : positive float
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    NormalityTest_CramerVonMisesNormal

    Notes
    -----
    The test is used to check whether the sample follows a normal distribution. This
    test gives more importance to extreme values.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> test_result = ot.NormalityTest.AndersonDarlingNormal(sample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=AndersonDarlingNormal binaryQualityMeasure=true p-value threshold=0.05 p-value=0.7268 statistic=0.255405 description=[]

    """
    return _stattests.NormalityTest_AndersonDarlingNormal(sample, level)


def NormalityTest_CramerVonMisesNormal(sample, level=0.05):
    """
    Evaluate whether a sample follows a normal distribution.

    Refer to :ref:`cramer_vonmises_test`.

    **Available usages**:

        NormalityTest.CramerVonMisesNormal(*sample*)

        NormalityTest.CramerVonMisesNormal(*sample, level*)

    Parameters
    ----------
    sample : 2-d sequence of float
        Tested sample.
    level : positive float
        Threshold p-value of the test (= first kind risk), it must be
        :math:`< 1`, equal to 0.05 by default.

    Returns
    -------
    testResult : :class:`~openturns.TestResult`
        Structure containing the result of the test.

    See Also
    --------
    NormalityTest_AndersonDarlingNormal

    Notes
    -----
    The test is used to check whether the sample follows a normal distribution. The 
    test concerns the deviation squared and integrated over the entire variation
    domain, it often appears to be more robust than the Kolmogorov-Smirnov test.

    Examples
    --------
    >>> import openturns as ot
    >>> ot.RandomGenerator.SetSeed(0)
    >>> distribution = ot.Normal()
    >>> sample = distribution.getSample(30)
    >>> test_result = ot.NormalityTest.CramerVonMisesNormal(sample)
    >>> print(test_result)
    class=TestResult name=Unnamed type=CramerVonMisesNormal binaryQualityMeasure=true p-value threshold=0.05 p-value=0.682524 statistic=0.0399704 description=[]

    """
    return _stattests.NormalityTest_CramerVonMisesNormal(sample, level)


class DickeyFullerTest(openturns.common.PersistentObject):
    """
    The Dickey-Fuller stationarity test.

    Refer to :ref:`dickey_fuller`.

    Notes
    -----
    The Dickey-Fuller test checks the stationarity of a scalar time series using one time series.

    Examples
    --------
    Create an ARMA process and generate a time series:

    >>> import openturns as ot
    >>> arcoefficients = ot.ARMACoefficients([0.3])
    >>> macoefficients = ot.ARMACoefficients(0)
    >>> timeGrid = ot.RegularGrid(0.0, 0.1, 10)
    >>> whiteNoise = ot.WhiteNoise(ot.Normal(), timeGrid)
    >>> myARMA = ot.ARMA(arcoefficients, macoefficients, whiteNoise)

    >>> realization = ot.TimeSeries(myARMA.getRealization())
    >>> test = ot.DickeyFullerTest(realization)

    Test the stationarity of the data without any asumption on the model:

    >>> globalRes = test.runStrategy()

    Test the stationarity knowing you have a drift and linear trend model:

    >>> res1 = test.testUnitRootInDriftAndLinearTrendModel(0.95)

    Test the stationarity knowing you have a drift model:

    >>> res2 = test.testUnitRootInDriftModel(0.95)

    Test the stationarity knowing you have an AR1 model:

    >>> res3 = test.testUnitRootInAR1Model(0.95)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _stattests.DickeyFullerTest_getClassName(self)

    def testUnitRootInDriftAndLinearTrendModel(self, level=0.05):
        r"""
        Test for unit root in model with drift and trend.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestModel1`.

        """
        return _stattests.DickeyFullerTest_testUnitRootInDriftAndLinearTrendModel(self, level)

    def testUnitRootInDriftModel(self, level=0.05):
        r"""
        Test for unit root in model with drift.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestModel2`.

        """
        return _stattests.DickeyFullerTest_testUnitRootInDriftModel(self, level)

    def testUnitRootInAR1Model(self, level=0.05):
        r"""
        Test for unit root in AR1 model.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestModel3`.

        """
        return _stattests.DickeyFullerTest_testUnitRootInAR1Model(self, level)

    def runStrategy(self, level=0.05):
        r"""
        Test the stationarity without any assumption on the model.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the tests. The strategy if the one described above.

        """
        return _stattests.DickeyFullerTest_runStrategy(self, level)

    def testUnitRootAndNoLinearTrendInDriftAndLinearTrendModel(self, level=0.05):
        r"""
        Test for linear trend in model with unit root.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestSousModele1_2`.

        """
        return _stattests.DickeyFullerTest_testUnitRootAndNoLinearTrendInDriftAndLinearTrendModel(self, level)

    def testNoUnitRootAndNoLinearTrendInDriftAndLinearTrendModel(self, level=0.05):
        r"""
        Test for trend in model without unit root.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestSousModele1_1`.

        """
        return _stattests.DickeyFullerTest_testNoUnitRootAndNoLinearTrendInDriftAndLinearTrendModel(self, level)

    def testUnitRootAndNoDriftInDriftModel(self, level=0.05):
        r"""
        Test for null drift in model with unit root.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestSousModele2_2`.

        """
        return _stattests.DickeyFullerTest_testUnitRootAndNoDriftInDriftModel(self, level)

    def testNoUnitRootAndNoDriftInDriftModel(self, level=0.05):
        r"""
        Test for null drift in model without unit root.

        Parameters
        ----------
        alpha : float, :math:`0 < \alpha < 1`
            The first kind risk of the test.

            By default, :math:`\alpha=0.05`.

        Returns
        -------
        testResult : :class:`~openturns.TestResult`
            Results container of the test detailed in :eq:`TestSousModele2_1`.

        """
        return _stattests.DickeyFullerTest_testNoUnitRootAndNoDriftInDriftModel(self, level)

    def setVerbose(self, verbose):
        return _stattests.DickeyFullerTest_setVerbose(self, verbose)

    def getVerbose(self):
        return _stattests.DickeyFullerTest_getVerbose(self)

    def __init__(self, *args):
        _stattests.DickeyFullerTest_swiginit(self, _stattests.new_DickeyFullerTest(*args))

    __swig_destroy__ = _stattests.delete_DickeyFullerTest


_stattests.DickeyFullerTest_swigregister(DickeyFullerTest)
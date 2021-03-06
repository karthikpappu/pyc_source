# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/model_copula.py
# Compiled at: 2019-11-13 10:35:53
"""Copulas."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _model_copula
else:
    import _model_copula
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
    __swig_destroy__ = _model_copula.delete_SwigPyIterator

    def value(self):
        return _model_copula.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _model_copula.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _model_copula.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _model_copula.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _model_copula.SwigPyIterator_equal(self, x)

    def copy(self):
        return _model_copula.SwigPyIterator_copy(self)

    def next(self):
        return _model_copula.SwigPyIterator_next(self)

    def __next__(self):
        return _model_copula.SwigPyIterator___next__(self)

    def previous(self):
        return _model_copula.SwigPyIterator_previous(self)

    def advance(self, n):
        return _model_copula.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _model_copula.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _model_copula.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _model_copula.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _model_copula.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _model_copula.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _model_copula.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_model_copula.SwigPyIterator_swigregister(SwigPyIterator)

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


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo

class DistributionImplementation(openturns.common.PersistentObject):
    """
    Base class for probability distributions.

    Notes
    -----
    In OpenTURNS a :class:`~openturns.Distribution` maps the concept of *probability distribution*.
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionImplementation_getClassName(self)

    def __eq__(self, other):
        return _model_copula.DistributionImplementation___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.DistributionImplementation___ne__(self, other)

    def __truediv__(self, *args):
        return _model_copula.DistributionImplementation___truediv__(self, *args)

    __div__ = __truediv__

    def cos(self):
        """
        Transform distribution by cosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_cos(self)

    def sin(self):
        """
        Transform distribution by sine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_sin(self)

    def tan(self):
        """
        Transform distribution by tangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_tan(self)

    def acos(self):
        """
        Transform distribution by arccosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_acos(self)

    def asin(self):
        """
        Transform distribution by arcsine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_asin(self)

    def atan(self):
        """
        Transform distribution by arctangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_atan(self)

    def cosh(self):
        """
        Transform distribution by cosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_cosh(self)

    def sinh(self):
        """
        Transform distribution by sinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_sinh(self)

    def tanh(self):
        """
        Transform distribution by tanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_tanh(self)

    def acosh(self):
        """
        Transform distribution by acosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_acosh(self)

    def asinh(self):
        """
        Transform distribution by asinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_asinh(self)

    def atanh(self):
        """
        Transform distribution by atanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_atanh(self)

    def exp(self):
        """
        Transform distribution by exponential function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_exp(self)

    def log(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_log(self)

    def ln(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_ln(self)

    def inverse(self):
        """
        Transform distribution by inverse function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_inverse(self)

    def sqr(self):
        """
        Transform distribution by square function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_sqr(self)

    def sqrt(self):
        """
        Transform distribution by square root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_sqrt(self)

    def cbrt(self):
        """
        Transform distribution by cubic root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_cbrt(self)

    def abs(self):
        """
        Transform distribution by absolute value function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementation_abs(self)

    def __repr__(self):
        return _model_copula.DistributionImplementation___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionImplementation___str__(self, *args)

    def getDimension(self):
        """
        Accessor to the dimension of the distribution.

        Returns
        -------
        n : int
            The number of components in the distribution.
        """
        return _model_copula.DistributionImplementation_getDimension(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.DistributionImplementation_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.DistributionImplementation_getSample(self, size)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementation_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementation_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _model_copula.DistributionImplementation_computeLogPDF(self, *args)

    def computeInverseSurvivalFunction(self, point):
        r"""
        Compute the inverse survival function.

        Parameters
        ----------
        p : float, :math:`p \in [0; 1]`
            Level of the survival function.

        Returns
        -------
        x : :class:`~openturns.Point`
            Point :math:`\vect{x}` such that :math:`S_{\vect{X}}(\vect{x}) = p` with iso-quantile components.

        Notes
        -----
        The inverse survival function writes: :math:`S^{-1}(p)  =  \vect{x}^p` where :math:`S( \vect{x}^p) = \Prob{\bigcap_{i=1}^d X_i > x_i^p}`. OpenTURNS returns the point :math:`\vect{x}^p` such that 
        :math:`\Prob{ X_1 > x_1^p}   =  \dots = \Prob{ X_d > x_d^p}`.

        See Also
        --------
        computeQuantile, computeSurvivalFunction
        """
        return _model_copula.DistributionImplementation_computeInverseSurvivalFunction(self, point)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.DistributionImplementation_computeSurvivalFunction(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementation_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _model_copula.DistributionImplementation_computeComplementaryCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.DistributionImplementation_computeProbability(self, interval)

    def computeCharacteristicFunction(self, *args):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _model_copula.DistributionImplementation_computeCharacteristicFunction(self, *args)

    def computeLogCharacteristicFunction(self, *args):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _model_copula.DistributionImplementation_computeLogCharacteristicFunction(self, *args)

    def computeGeneratingFunction(self, *args):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _model_copula.DistributionImplementation_computeGeneratingFunction(self, *args)

    def computeLogGeneratingFunction(self, *args):
        """
        Compute the logarithm of the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        lg : float
            Logarithm of the probability-generating function value at input :math:`X`.

        Notes
        -----
        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete, computeGeneratingFunction
        """
        return _model_copula.DistributionImplementation_computeLogGeneratingFunction(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.DistributionImplementation_computeEntropy(self)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementation_computePDFGradient(self, *args)

    def computeLogPDFGradient(self, *args):
        """
        Compute the gradient of the log probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the logPDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementation_computeLogPDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementation_computeCDFGradient(self, *args)

    def computeScalarQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function for univariate distributions.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : float
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_X(p) = F_X^{-1}(p), \quad p \in [0; 1]

        See Also
        --------
        computeQuantile
        """
        return _model_copula.DistributionImplementation_computeScalarQuantile(self, prob, tail)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.DistributionImplementation_computeQuantile(self, *args)

    def computeMinimumVolumeInterval(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`[a_i, b_i]   = \argmin_{I \in \Rset \, | \, \mu_i(I) = \beta} \lambda_i(I)` and :math:`\mu(I^*_{\alpha})  =  \alpha` with :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. 

        This problem resorts to solving :math:`d` univariate non linear equations: for a fixed value :math:`\beta`, we find each intervals :math:`[a_i, b_i]` such that:

        .. math::
            :nowrap:

            \begin{eqnarray*}
            F_i(b_i) - F_i(a_i) & = & \beta \\
            p_i(b_i) & = & p_i(a_i)
            \end{eqnarray*}

        which consists of finding the bound :math:`a_i` such that:

        .. math::

            p_i(a_i) =  p_i(F_i^{-1}(\beta + F_i(a_i)))

        To find :math:`\beta`, we use the Brent algorithm:  :math:`\mu([\vect{a}(\beta); \vect{b}(\beta)] = g(\beta) = \alpha` with :math:`g` a non linear function.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt = paramDist.computeMinimumVolumeInterval(0.9)

        """
        return _model_copula.DistributionImplementation_computeMinimumVolumeInterval(self, prob)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _model_copula.DistributionImplementation_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeBilateralConfidenceInterval(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The bilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`a_i = F_i^{-1}((1-\beta)/2)` and :math:`b_i = F_i^{-1}((1+\beta)/2)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeBilateralConfidenceInterval(0.9)
        """
        return _model_copula.DistributionImplementation_computeBilateralConfidenceInterval(self, prob)

    def computeBilateralConfidenceIntervalWithMarginalProbability(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Refer to :func:`computeBilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9 with marginal probability:

        >>> confInt, marginalProb = paramDist.computeBilateralConfidenceIntervalWithMarginalProbability(0.9)
        """
        return _model_copula.DistributionImplementation_computeBilateralConfidenceIntervalWithMarginalProbability(self, prob)

    def computeUnilateralConfidenceInterval(self, prob, tail=False):
        r"""
        Compute a unilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu`.

        The left unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]-\infty, b_1] \times \dots \times ]-\infty, b_d]` where :math:`b_i = F_i^{-1}(\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`\vect{b}` is the quantile of level :math:`\alpha` of the measure :math:`\mu`, with iso-quantile components.

        The right unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]a_1; +\infty[ \times \dots \times ]a_d; +\infty[` where :math:`a_i = F_i^{-1}(1-\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`S_{\mu}^{-1}(\vect{a}) = \alpha` with iso-quantile components, where :math:`S_{\mu}` is the survival function of the measure :math:`\mu`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9, True)

        """
        return _model_copula.DistributionImplementation_computeUnilateralConfidenceInterval(self, prob, tail)

    def computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail):
        r"""
        Compute a unilateral confidence interval.

        Refer to :func:`computeUnilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, False)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, True)

        """
        return _model_copula.DistributionImplementation_computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail)

    def computeMinimumVolumeLevelSet(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence domain :math:`A^*_{\alpha}` is the set of minimum volume and which measure is at least :math:`\alpha`. It is defined by:

        .. math::

            A^*_{\alpha} = \argmin_{A \in \Rset^d\, | \, \mu(A) \geq \alpha} \lambda(A)

        where :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. Under some general conditions on :math:`\mu` (for example, no flat regions), the set  :math:`A^*_{\alpha}` is unique and realises the minimum: :math:`\mu(A^*_{\alpha}) = \alpha`. We show that :math:`A^*_{\alpha}` writes:

        .. math::

            A^*_{\alpha} = \{ \vect{x} \in \Rset^d \, | \, p(\vect{x}) \geq p_{\alpha} \}

        for a certain :math:`p_{\alpha} >0`.

        If we consider the random variable :math:`Y = p(\vect{X})`, with cumulative distribution function :math:`F_Y`, then :math:`p_{\alpha}` is defined by:

        .. math::

            1-F_Y(p_{\alpha}) = \alpha

        Thus the minimum volume domain of confidence :math:`\alpha` is the interior of the domain which frontier is the :math:`1-\alpha` quantile of :math:`Y`. It can be determined with simulations of :math:`Y`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9:

        >>> levelSet = paramDist.computeMinimumVolumeLevelSet(0.9)

        """
        return _model_copula.DistributionImplementation_computeMinimumVolumeLevelSet(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _model_copula.DistributionImplementation_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def getRange(self):
        """
        Accessor to the range of the distribution.

        Returns
        -------
        range : :class:`~openturns.Interval`
            Range of the distribution.

        Notes
        -----
        The *mathematical* range is the smallest closed interval outside of which the
        PDF is zero. The *numerical* range is the interval outside of which the PDF is
        rounded to zero in double precision.

        See Also
        --------
        getSupport
        """
        return _model_copula.DistributionImplementation_getRange(self)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _model_copula.DistributionImplementation_getRoughness(self)

    def getMean(self):
        r"""
        Accessor to the mean.

        Returns
        -------
        k : :class:`~openturns.Point`
            Mean.

        Notes
        -----
        The mean is the first-order moment:

        .. math::

            \vect{\mu} = \Tr{\left(\Expect{X_i}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementation_getMean(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.DistributionImplementation_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementation_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementation_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _model_copula.DistributionImplementation_getStandardMoment(self, n)

    def getMoment(self, n):
        r"""
        Accessor to the componentwise moments.

        Parameters
        ----------
        k : int
            The order of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise moment of order :math:`k`.

        Notes
        -----
        The componentwise moment of order :math:`k` is defined as:

        .. math::

            \vect{m}^{(k)} = \Tr{\left(\Expect{X_i^k}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementation_getMoment(self, n)

    def getCenteredMoment(self, n):
        r"""
        Accessor to the componentwise centered moments.

        Parameters
        ----------
        k : int
            The order of the centered moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        Centered moments are centered with respect to the first-order moment:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - \mu_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment
        """
        return _model_copula.DistributionImplementation_getCenteredMoment(self, n)

    def getShiftedMoment(self, n, shift):
        r"""
        Accessor to the componentwise shifted moments.

        Parameters
        ----------
        k : int
            The order of the shifted moment.
        shift : sequence of float
            The shift of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        The moments are centered with respect to the given shift :\math:`\vect{s}`:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - s_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment, getCenteredMoment
        """
        return _model_copula.DistributionImplementation_getShiftedMoment(self, n, shift)

    def getCovariance(self):
        r"""
        Accessor to the covariance matrix.

        Returns
        -------
        Sigma : :class:`~openturns.CovarianceMatrix`
            Covariance matrix.

        Notes
        -----
        The covariance is the second-order centered moment. It is defined as:

        .. math::

            \mat{\Sigma} & = \Cov{\vect{X}} \\
                         & = \Expect{\left(\vect{X} - \vect{\mu}\right)
                                     \Tr{\left(\vect{X} - \vect{\mu}\right)}}
        """
        return _model_copula.DistributionImplementation_getCovariance(self)

    def getCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.DistributionImplementation_getCorrelation(self)

    def getLinearCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.DistributionImplementation_getLinearCorrelation(self)

    def getPearsonCorrelation(self):
        r"""
        Accessor to the Pearson correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Pearson's correlation matrix.

        See Also
        --------
        getCovariance

        Notes
        -----
        Pearson's correlation is defined as the normalized covariance matrix:

        .. math::

            \mat{\rho} & = \left[\frac{\Cov{X_i, X_j}}{\sqrt{\Var{X_i}\Var{X_j}}},
                                 \quad i,j = 1, \ldots, n\right] \\
                       & = \left[\frac{\Sigma_{i,j}}{\sqrt{\Sigma_{i,i}\Sigma_{j,j}}},
                                 \quad i,j = 1, \ldots, n\right]
        """
        return _model_copula.DistributionImplementation_getPearsonCorrelation(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.DistributionImplementation_getSpearmanCorrelation(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.DistributionImplementation_getKendallTau(self)

    def getShapeMatrix(self):
        """
        Accessor to the shape matrix of the underlying copula if it is elliptical.

        Returns
        -------
        shape : :class:`~openturns.CorrelationMatrix`
            Shape matrix of the elliptical copula of a distribution.

        Notes
        -----
        This is not the Pearson correlation matrix.

        See Also
        --------
        getPearsonCorrelation
        """
        return _model_copula.DistributionImplementation_getShapeMatrix(self)

    def getCholesky(self):
        """
        Accessor to the Cholesky factor of the covariance matrix.

        Returns
        -------
        L : :class:`~openturns.SquareMatrix`
            Cholesky factor of the covariance matrix.

        See Also
        --------
        getCovariance
        """
        return _model_copula.DistributionImplementation_getCholesky(self)

    def getInverseCholesky(self):
        """
        Accessor to the inverse Cholesky factor of the covariance matrix.

        Returns
        -------
        Linv : :class:`~openturns.SquareMatrix`
            Inverse Cholesky factor of the covariance matrix.

        See also
        --------
        getCholesky
        """
        return _model_copula.DistributionImplementation_getInverseCholesky(self)

    def isCopula(self):
        """
        Test whether the distribution is a copula or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A copula is a distribution with uniform margins on [0; 1].
        """
        return _model_copula.DistributionImplementation_isCopula(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.DistributionImplementation_isElliptical(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementation_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementation_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementation_isIntegral(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.DistributionImplementation_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementation_hasIndependentCopula(self)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _model_copula.DistributionImplementation_getSupport(self, *args)

    def getProbabilities(self):
        """
        Accessor to the discrete probability levels.

        Returns
        -------
        probabilities : :class:`~openturns.Point`
            The probability levels of a discrete distribution.
        """
        return _model_copula.DistributionImplementation_getProbabilities(self)

    def getSingularities(self):
        """
        Accessor to the singularities of the PDF function.

        It is defined for univariate distributions only, and gives all the singularities (ie discontinuities of any order) strictly inside of the range of the distribution.

        Returns
        -------
        singularities : :class:`~openturns.Point`
            The singularities of the PDF of an univariate distribution.
        """
        return _model_copula.DistributionImplementation_getSingularities(self)

    def computeDensityGenerator(self, betaSquare):
        r"""
        Compute the probability density function of the characteristic generator.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator value at input :math:`X`.

        Notes
        -----
        This is the function :math:`\phi` such that the probability density function
        rewrites:

        .. math::

            f_{\vect{X}}(\vect{x}) =
                \phi\left(\Tr{\left(\vect{x} - \vect{\mu}\right)}
                              \mat{\Sigma}^{-1}
                              \left(\vect{x} - \vect{\mu}\right)
                    \right),
                \quad \vect{x} \in \supp{\vect{X}}

        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computePDF
        """
        return _model_copula.DistributionImplementation_computeDensityGenerator(self, betaSquare)

    def computeDensityGeneratorDerivative(self, betaSquare):
        """
        Compute the first-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator first-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.DistributionImplementation_computeDensityGeneratorDerivative(self, betaSquare)

    def computeDensityGeneratorSecondDerivative(self, betaSquare):
        """
        Compute the second-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator second-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.DistributionImplementation_computeDensityGeneratorSecondDerivative(self, betaSquare)

    def computeRadialDistributionCDF(self, radius, tail=False):
        r"""
        Compute the cumulative distribution function of the squared radius.

        For the underlying standard spherical distribution (for elliptical
        distributions only).

        Parameters
        ----------
        r2 : float, :math:`0 \leq r^2`
            Squared radius.

        Returns
        -------
        F : float
            CDF value at input :math:`r^2`.

        Notes
        -----
        This is the CDF of the sum of the squared independent, standard, identically
        distributed components:

        .. math::

            R^2 = \sqrt{\sum\limits_{i=1}^n U_i^2}
        """
        return _model_copula.DistributionImplementation_computeRadialDistributionCDF(self, radius, tail)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.DistributionImplementation_getMarginal(self, *args)

    def getCopula(self):
        """
        Accessor to the copula of the distribution.

        Returns
        -------
        C : :class:`~openturns.Distribution`
            Copula of the distribution.

        See Also
        --------
        ComposedDistribution
        """
        return _model_copula.DistributionImplementation_getCopula(self)

    def computeConditionalDDF(self, x, y):
        """
        Compute the conditional derivative density function of the last component.

        With respect to the other fixed components.

        Parameters
        ----------
        Xn : float
            Conditional DDF input (last component).
        Xcond : sequence of float with dimension :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        d : float
            Conditional DDF value at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computeDDF, computeConditionalCDF
        """
        return _model_copula.DistributionImplementation_computeConditionalDDF(self, x, y)

    def computeSequentialConditionalDDF(self, x):
        r"""
        Compute the sequential conditional derivative density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the DDF.

        Returns
        -------
        ddf : sequence of float
            Conditional DDF values at input.

        Notes
        -----
        The sequential conditional derivative density function is defined as follows:

        .. math::

            ddf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d^2}{d\,x_n^2}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional DDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d^2}{d\,x_1^2}\Prob{X_1 \leq x_1}`, ie the DDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementation_computeSequentialConditionalDDF(self, x)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementation_computeSequentialConditionalPDF(self, x)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.DistributionImplementation_computeConditionalPDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementation_computeSequentialConditionalCDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.DistributionImplementation_computeConditionalCDF(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.DistributionImplementation_computeSequentialConditionalQuantile(self, q)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.DistributionImplementation_computeConditionalQuantile(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.DistributionImplementation_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.DistributionImplementation_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.DistributionImplementation_getStandardDistribution(self)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _model_copula.DistributionImplementation_getStandardRepresentative(self)

    def getIntegrationNodesNumber(self):
        """
        Accessor to the number of Gauss integration points.

        Returns
        -------
        N : int
            Number of integration points.
        """
        return _model_copula.DistributionImplementation_getIntegrationNodesNumber(self)

    def setIntegrationNodesNumber(self, integrationNodesNumber):
        """
        Accessor to the number of Gauss integration points.

        Parameters
        ----------
        N : int
            Number of integration points.
        """
        return _model_copula.DistributionImplementation_setIntegrationNodesNumber(self, integrationNodesNumber)

    def drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF of the requested margin.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of probability density function.

        Available constructors:
            drawPDF(*x_min, x_max, pointNumber, logScale*)

            drawPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computePDF, viewer.View, ResourceMap

        Examples
        --------
        View the PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawPDF()
        >>> graph.setLegends(['normal pdf'])

        View the iso-lines PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementation_drawPDF(self, *args)

    def drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal PDF of the requested couple of
            margins.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the log-probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF of the requested margin.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DLogPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawLogPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of log-probability density function.

        Available constructors:
            drawLogPDF(*x_min, x_max, pointNumber, logScale*)

            drawLogPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawLogPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeLogPDF, viewer.View, ResourceMap

        Examples
        --------
        View the log-PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawLogPDF()
        >>> graph.setLegends(['normal log-pdf'])

        View the iso-lines log-PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawLogPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawLogPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementation_drawLogPDF(self, *args)

    def drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the log-probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal log-PDF of the requested couple of
            margins.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DLogPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawCDF(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawCDF(*x_min, x_max, pointNumber, logScale*)

            drawCDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawCDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeCDF, viewer.View, ResourceMap

        Examples
        --------
        View the CDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawCDF()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines CDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawCDF()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawCDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementation_drawCDF(self, *args)

    def drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF of the requested margin.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DCDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal CDF of the requested couple of
            margins.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DCDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawSurvivalFunction(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawSurvivalFunction(*x_min, x_max, pointNumber, logScale*)

            drawSurvivalFunction(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawSurvivalFunction(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeSurvivalFunction, viewer.View, ResourceMap

        Examples
        --------
        View the SurvivalFunction of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawSurvivalFunction()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines SurvivalFunction of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawSurvivalFunction()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawSurvivalFunction([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementation_drawSurvivalFunction(self, *args)

    def drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction of the requested margin.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DSurvivalFunction(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal SurvivalFunction of the requested couple of
            margins.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DSurvivalFunction(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawQuantile(self, *args):
        """
        Draw the quantile function.

        Parameters
        ----------
        q_min : float, in :math:`[0,1]`
            The min value of the mesh of the x-axis.
        q_max : float, in :math:`[0,1]`
            The max value of the mesh of the x-axis.
        n_points : int, optional
            The number of points that is used for meshing the quantile curve.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the quantile function.

        Notes
        -----
        This is implemented for univariate and bivariate distributions only.
        In the case of bivariate distributions, defined by its CDF :math:`F` and its marginals :math:`(F_1, F_2)`, the quantile of order :math:`q` is the point :math:`(F_1(u),F_2(u))` defined by

        .. math::

            F(F_1(u), F_2(u)) = q

        See Also
        --------
        computeQuantile, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal()
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        >>> distribution = ot.ComposedDistribution([ot.Normal(), ot.Exponential(1.0)], ot.ClaytonCopula(0.5))
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementation_drawQuantile(self, *args)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.DistributionImplementation_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.DistributionImplementation_setParametersCollection(self, *args)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.DistributionImplementation_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.DistributionImplementation_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.DistributionImplementation_getParameterDescription(self)

    def getParameterDimension(self):
        """
        Accessor to the number of parameters in the distribution.

        Returns
        -------
        n_parameters : int
            Number of parameters in the distribution.

        See Also
        --------
        getParametersCollection
        """
        return _model_copula.DistributionImplementation_getParameterDimension(self)

    def setDescription(self, description):
        """
        Accessor to the componentwise description.

        Parameters
        ----------
        description : sequence of str
            Description of the components of the distribution.
        """
        return _model_copula.DistributionImplementation_setDescription(self, description)

    def getDescription(self):
        """
        Accessor to the componentwise description.

        Returns
        -------
        description : :class:`~openturns.Description`
            Description of the components of the distribution.

        See Also
        --------
        setDescription
        """
        return _model_copula.DistributionImplementation_getDescription(self)

    def getPDFEpsilon(self):
        """
        Accessor to the PDF computation precision.

        Returns
        -------
        PDFEpsilon : float
            PDF computation precision.
        """
        return _model_copula.DistributionImplementation_getPDFEpsilon(self)

    def getCDFEpsilon(self):
        """
        Accessor to the CDF computation precision.

        Returns
        -------
        CDFEpsilon : float
            CDF computation precision.
        """
        return _model_copula.DistributionImplementation_getCDFEpsilon(self)

    def getPositionIndicator(self):
        """
        Position indicator accessor.

        Defines a generic metric of the position. When the mean is not defined it falls
        back to the median.
        Available only for 1-d distributions.

        Returns
        -------
        position : float
            Mean or median of the distribution.
        """
        return _model_copula.DistributionImplementation_getPositionIndicator(self)

    def getDispersionIndicator(self):
        """
        Dispersion indicator accessor.

        Defines a generic metric of the dispersion. When the standard deviation is not
        defined it falls back to the interquartile.
        Only available for 1-d distributions.

        Returns
        -------
        dispersion : float
            Standard deviation or interquartile.
        """
        return _model_copula.DistributionImplementation_getDispersionIndicator(self)

    def __init__(self, *args):
        _model_copula.DistributionImplementation_swiginit(self, _model_copula.new_DistributionImplementation(*args))

    def __rtruediv__(self, s):
        return _model_copula.DistributionImplementation___rtruediv__(self, s)

    def __rdiv__(self, s):
        return _model_copula.DistributionImplementation___rdiv__(self, s)

    def __pow__(self, *args):
        return _model_copula.DistributionImplementation___pow__(self, *args)

    def __sub__(self, *args):
        return _model_copula.DistributionImplementation___sub__(self, *args)

    def __rsub__(self, s):
        return _model_copula.DistributionImplementation___rsub__(self, s)

    def __neg__(self):
        return _model_copula.DistributionImplementation___neg__(self)

    def __add__(self, *args):
        return _model_copula.DistributionImplementation___add__(self, *args)

    def __radd__(self, s):
        return _model_copula.DistributionImplementation___radd__(self, s)

    def __mul__(self, *args):
        return _model_copula.DistributionImplementation___mul__(self, *args)

    def __rmul__(self, s):
        return _model_copula.DistributionImplementation___rmul__(self, s)

    __swig_destroy__ = _model_copula.delete_DistributionImplementation


_model_copula.DistributionImplementation_swigregister(DistributionImplementation)

def maximum(*args):
    return _model_copula.maximum(*args)


from openturns.typ import Interval

class PythonDistribution(object):
    """
    Allow to override Distribution from Python.

    Parameters
    ----------
    dim : positive int
        the distribution dimension

    Examples
    --------
    Not useful on its own, see the examples section on how to inherit from it.
    """

    def __init__(self, dim=0):
        """
        Constructor.
        """
        self.__dim = dim

    def __str__(self):
        return 'PythonDistribution -> #%d' % self.__dim

    def __repr__(self):
        return self.__str__()

    def getDimension(self):
        """
        Dimension accessor.
        """
        return self.__dim

    def computeCDF(self, X):
        """
        CDF accessor.
        """
        raise RuntimeError('You must define a method computeCDF(x) -> cdf, where cdf is a float')


class SciPyDistribution(PythonDistribution):
    """
    Allow to override Distribution from a scipy distribution.

    Parameters
    ----------
    dist : a scipy.stats distribution
        The distribution to wrap

    Examples
    --------
    >>> import openturns as ot
    >>> import scipy.stats as st
    >>> scipy_dist = st.johnsonsu(2.55, 2.25)  # doctest: +SKIP
    >>> distribution = ot.Distribution(ot.SciPyDistribution(scipy_dist))  # doctest: +SKIP
    >>> distribution.getRealization()  # doctest: +SKIP
    """

    def __init__(self, dist):
        super(SciPyDistribution, self).__init__(1)
        if dist.__class__.__name__ != 'rv_frozen':
            raise TypeError('Argument is not a scipy distribution')
        self._dist = dist
        from openturns import ResourceMap
        cdf_epsilon = ResourceMap.GetAsScalar('Distribution-DefaultCDFEpsilon')
        lb = dist.ppf(0.0)
        ub = dist.ppf(1.0)
        flb = lb != float('-inf')
        fub = ub != float('+inf')
        if not flb:
            lb = dist.ppf(cdf_epsilon)
        if not fub:
            ub = dist.ppf(1.0 - cdf_epsilon)
        self.__range = Interval([lb], [ub])
        self.__range.setFiniteLowerBound([int(flb)])
        self.__range.setFiniteUpperBound([int(fub)])

    def getRange(self):
        return self.__range

    def getRealization(self):
        rvs = self._dist.rvs()
        return [rvs]

    def getSample(self, size):
        rvs = self._dist.rvs(size)
        return rvs.reshape(size, 1)

    def computePDF(self, X):
        pdf = self._dist.pdf(X[0])
        return pdf

    def computeCDF(self, X):
        cdf = self._dist.cdf(X[0])
        return cdf

    def getMean(self):
        mean = float(self._dist.stats('m'))
        return [mean]

    def getStandardDeviation(self):
        var = float(self._dist.stats('v'))
        std = var ** 0.5
        return [std]

    def getSkewness(self):
        skewness = float(self._dist.stats('s'))
        return [skewness]

    def getKurtosis(self):
        kurtosis = float(self._dist.stats('k')) + 3.0
        return [kurtosis]

    def getMoment(self, n):
        moment = self._dist.moment(n)
        return [moment]

    def computeScalarQuantile(self, p, tail=False):
        q = self._dist.ppf(1.0 - p if tail else p)
        return q

    def computeQuantile(self, prob, tail=False):
        p = 1.0 - prob if tail else prob
        q = self._dist.ppf(p)
        return [q]

    def getParameter(self):
        return self._dist.args

    def setParameter(self, params):
        size = len(self._dist.args)
        if len(params) != size:
            raise ValueError('Parameter must be of size %d' % size)
        self._dist.args = params

    def getParameterDescription(self):
        size = len(self._dist.args)
        return [ 'parameter' + str(i + 1) for i in range(size) ]


class ChaospyDistribution(PythonDistribution):
    """
    Allow to override Distribution from a chaospy distribution.

    Parameters
    ----------
    dist : a chaospy.stats distribution
        The distribution to wrap. It is currently limited to stochastically
        independent distributions as chaopy distributions doesn't implement CDF
        computation for dependencies.

    Examples
    --------
    >>> import openturns as ot
    >>> import chaospy as cp  # doctest: +SKIP
    >>> chaospy_dist = cp.J(cp.Triangular(1.0, 2.0, 3.0), cp.F(4.0, 5.0))  # doctest: +SKIP
    >>> distribution = ot.Distribution(ot.ChaospyDistribution(chaospy_dist))  # doctest: +SKIP
    >>> distribution.getRealization()  # doctest: +SKIP
    """

    def __init__(self, dist):
        super(ChaospyDistribution, self).__init__(len(dist))
        from chaospy import Iid, J, get_dependencies
        independent = len(dist) == 1
        independent |= isinstance(dist, Iid)
        independent |= isinstance(dist, J) and not get_dependencies(*dist)
        if not independent:
            raise Exception("Dependent chaospy distributions doesn't implement CDF computation")
        self._dist = dist
        bounds = dist.range()
        self.__range = Interval(bounds[0], bounds[1])

    def getRange(self):
        return self.__range

    def getRealization(self):
        rvs = self._dist.sample(1).flatten()
        return rvs

    def getSample(self, size):
        rvs = self._dist.sample(size).T
        return rvs.reshape(size, len(self._dist))

    def computePDF(self, X):
        pdf = self._dist.pdf(X)
        return pdf

    def computeCDF(self, X):
        cdf = self._dist.cdf(X)
        return cdf

    def computeScalarQuantile(self, p, tail=False):
        if len(self._dist) > 1:
            raise Exception("Multivariate distribution doesn't implement scalar quantile")
        q = self._dist.inv(1 - p if tail else p)
        return float(q)

    def computeQuantile(self, prob, tail=False):
        p = 1.0 - prob if tail else prob
        q = self._dist.inv(p).flatten()
        return q


class DistributionImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _model_copula.DistributionImplementationTypedInterfaceObject_swiginit(self, _model_copula.new_DistributionImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _model_copula.DistributionImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _model_copula.DistributionImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.DistributionImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _model_copula.delete_DistributionImplementationTypedInterfaceObject


_model_copula.DistributionImplementationTypedInterfaceObject_swigregister(DistributionImplementationTypedInterfaceObject)

class DistributionCollection(object):
    """
    Collection.

    Examples
    --------
    >>> import openturns as ot

    - Collection of **real values**:

    >>> ot.ScalarCollection(2)
    [0,0]
    >>> ot.ScalarCollection(2, 3.25)
    [3.25,3.25]
    >>> vector = ot.ScalarCollection([2.0, 1.5, 2.6])
    >>> vector
    [2,1.5,2.6]
    >>> vector[1] = 4.2
    >>> vector
    [2,4.2,2.6]
    >>> vector.add(3.8)
    >>> vector
    [2,4.2,2.6,3.8]

    - Collection of **complex values**:

    >>> ot.ComplexCollection(2)
    [(0,0),(0,0)]
    >>> ot.ComplexCollection(2, 3+4j)
    [(3,4),(3,4)]
    >>> vector = ot.ComplexCollection([2+3j, 1-4j, 3.0])
    >>> vector
    [(2,3),(1,-4),(3,0)]
    >>> vector[1] = 4+3j
    >>> vector
    [(2,3),(4,3),(3,0)]
    >>> vector.add(5+1j)
    >>> vector
    [(2,3),(4,3),(3,0),(5,1)]

    - Collection of **booleans**:

    >>> ot.BoolCollection(3)
    [0,0,0]
    >>> ot.BoolCollection(3, 1)
    [1,1,1]
    >>> vector = ot.BoolCollection([0, 1, 0])
    >>> vector
    [0,1,0]
    >>> vector[1] = 0
    >>> vector
    [0,0,0]
    >>> vector.add(1)
    >>> vector
    [0,0,0,1]

    - Collection of **distributions**:

    >>> print(ot.DistributionCollection(2))
    [Uniform(a = -1, b = 1),Uniform(a = -1, b = 1)]
    >>> print(ot.DistributionCollection(2, ot.Gamma(2.75, 1.0)))
    [Gamma(k = 2.75, lambda = 1, gamma = 0),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    >>> vector = ot.DistributionCollection([ot.Normal(), ot.Uniform()])
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -1, b = 1)]
    >>> vector[1] = ot.Uniform(-0.5, 1)
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1)]
    >>> vector.add(ot.Gamma(2.75, 1.0))
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __swig_destroy__ = _model_copula.delete_DistributionCollection

    def clear(self):
        """
        Reset the collection to zero dimension.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.clear()
        >>> x
        class=Point name=Unnamed dimension=0 values=[]
        """
        return _model_copula.DistributionCollection_clear(self)

    def __len__(self):
        return _model_copula.DistributionCollection___len__(self)

    def __eq__(self, rhs):
        return _model_copula.DistributionCollection___eq__(self, rhs)

    def __contains__(self, val):
        return _model_copula.DistributionCollection___contains__(self, val)

    def __getitem__(self, i):
        return _model_copula.DistributionCollection___getitem__(self, i)

    def __setitem__(self, i, val):
        return _model_copula.DistributionCollection___setitem__(self, i, val)

    def __delitem__(self, i):
        return _model_copula.DistributionCollection___delitem__(self, i)

    def at(self, *args):
        """
        Access to an element of the collection.

        Parameters
        ----------
        index : positive int
            Position of the element to access.

        Returns
        -------
        element : type depends on the type of the collection
            Element of the collection at the position *index*.
        """
        return _model_copula.DistributionCollection_at(self, *args)

    def add(self, *args):
        """
        Append a component (in-place).

        Parameters
        ----------
        value : type depends on the type of the collection.
            The component to append.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.add(1.)
        >>> print(x)
        [0,0,1]
        """
        return _model_copula.DistributionCollection_add(self, *args)

    def getSize(self):
        """
        Get the collection's dimension (or size).

        Returns
        -------
        n : int
            The number of components in the collection.
        """
        return _model_copula.DistributionCollection_getSize(self)

    def resize(self, newSize):
        """
        Change the size of the collection.

        Parameters
        ----------
        newSize : positive int
            New size of the collection.

        Notes
        -----
        If the new size is smaller than the older one, the last elements are thrown
        away, else the new elements are set to the default value of the element type.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2, 4)
        >>> print(x)
        [4,4]
        >>> x.resize(1)
        >>> print(x)
        [4]
        >>> x.resize(4)
        >>> print(x)
        [4,0,0,0]
        """
        return _model_copula.DistributionCollection_resize(self, newSize)

    def isEmpty(self):
        """
        Tell if the collection is empty.

        Returns
        -------
        isEmpty : bool
            *True* if there is no element in the collection.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.isEmpty()
        False
        >>> x.clear()
        >>> x.isEmpty()
        True
        """
        return _model_copula.DistributionCollection_isEmpty(self)

    def __repr__(self):
        return _model_copula.DistributionCollection___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionCollection___str__(self, *args)

    def __init__(self, *args):
        _model_copula.DistributionCollection_swiginit(self, _model_copula.new_DistributionCollection(*args))


_model_copula.DistributionCollection_swigregister(DistributionCollection)

class Distribution(DistributionImplementationTypedInterfaceObject):
    """
    Base class for probability distributions.

    Notes
    -----
    In OpenTURNS a :class:`~openturns.Distribution` maps the concept of *probability distribution*.
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.Distribution_getClassName(self)

    def __eq__(self, other):
        return _model_copula.Distribution___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.Distribution___ne__(self, other)

    def __truediv__(self, *args):
        return _model_copula.Distribution___truediv__(self, *args)

    __div__ = __truediv__

    def cos(self):
        """
        Transform distribution by cosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_cos(self)

    def sin(self):
        """
        Transform distribution by sine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_sin(self)

    def tan(self):
        """
        Transform distribution by tangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_tan(self)

    def acos(self):
        """
        Transform distribution by arccosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_acos(self)

    def asin(self):
        """
        Transform distribution by arcsine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_asin(self)

    def atan(self):
        """
        Transform distribution by arctangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_atan(self)

    def cosh(self):
        """
        Transform distribution by cosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_cosh(self)

    def sinh(self):
        """
        Transform distribution by sinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_sinh(self)

    def tanh(self):
        """
        Transform distribution by tanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_tanh(self)

    def acosh(self):
        """
        Transform distribution by acosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_acosh(self)

    def asinh(self):
        """
        Transform distribution by asinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_asinh(self)

    def atanh(self):
        """
        Transform distribution by atanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_atanh(self)

    def exp(self):
        """
        Transform distribution by exponential function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_exp(self)

    def log(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_log(self)

    def ln(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_ln(self)

    def inverse(self):
        """
        Transform distribution by inverse function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_inverse(self)

    def sqr(self):
        """
        Transform distribution by square function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_sqr(self)

    def sqrt(self):
        """
        Transform distribution by square root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_sqrt(self)

    def cbrt(self):
        """
        Transform distribution by cubic root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_cbrt(self)

    def abs(self):
        """
        Transform distribution by absolute value function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.Distribution_abs(self)

    def __repr__(self):
        return _model_copula.Distribution___repr__(self)

    def __str__(self, *args):
        return _model_copula.Distribution___str__(self, *args)

    def getDimension(self):
        """
        Accessor to the dimension of the distribution.

        Returns
        -------
        n : int
            The number of components in the distribution.
        """
        return _model_copula.Distribution_getDimension(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.Distribution_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.Distribution_getSample(self, size)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.Distribution_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.Distribution_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _model_copula.Distribution_computeLogPDF(self, *args)

    def computeInverseSurvivalFunction(self, prob):
        r"""
        Compute the inverse survival function.

        Parameters
        ----------
        p : float, :math:`p \in [0; 1]`
            Level of the survival function.

        Returns
        -------
        x : :class:`~openturns.Point`
            Point :math:`\vect{x}` such that :math:`S_{\vect{X}}(\vect{x}) = p` with iso-quantile components.

        Notes
        -----
        The inverse survival function writes: :math:`S^{-1}(p)  =  \vect{x}^p` where :math:`S( \vect{x}^p) = \Prob{\bigcap_{i=1}^d X_i > x_i^p}`. OpenTURNS returns the point :math:`\vect{x}^p` such that 
        :math:`\Prob{ X_1 > x_1^p}   =  \dots = \Prob{ X_d > x_d^p}`.

        See Also
        --------
        computeQuantile, computeSurvivalFunction
        """
        return _model_copula.Distribution_computeInverseSurvivalFunction(self, prob)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.Distribution_computeSurvivalFunction(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.Distribution_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _model_copula.Distribution_computeComplementaryCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.Distribution_computeProbability(self, interval)

    def computeCharacteristicFunction(self, x):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _model_copula.Distribution_computeCharacteristicFunction(self, x)

    def computeLogCharacteristicFunction(self, x):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _model_copula.Distribution_computeLogCharacteristicFunction(self, x)

    def computeGeneratingFunction(self, *args):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _model_copula.Distribution_computeGeneratingFunction(self, *args)

    def computeLogGeneratingFunction(self, *args):
        """
        Compute the logarithm of the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        lg : float
            Logarithm of the probability-generating function value at input :math:`X`.

        Notes
        -----
        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete, computeGeneratingFunction
        """
        return _model_copula.Distribution_computeLogGeneratingFunction(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.Distribution_computeEntropy(self)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.Distribution_computePDFGradient(self, *args)

    def computeLogPDFGradient(self, *args):
        """
        Compute the gradient of the log probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the logPDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.Distribution_computeLogPDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.Distribution_computeCDFGradient(self, *args)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.Distribution_computeQuantile(self, *args)

    def computeScalarQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function for univariate distributions.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : float
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_X(p) = F_X^{-1}(p), \quad p \in [0; 1]

        See Also
        --------
        computeQuantile
        """
        return _model_copula.Distribution_computeScalarQuantile(self, prob, tail)

    def computeMinimumVolumeInterval(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`[a_i, b_i]   = \argmin_{I \in \Rset \, | \, \mu_i(I) = \beta} \lambda_i(I)` and :math:`\mu(I^*_{\alpha})  =  \alpha` with :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. 

        This problem resorts to solving :math:`d` univariate non linear equations: for a fixed value :math:`\beta`, we find each intervals :math:`[a_i, b_i]` such that:

        .. math::
            :nowrap:

            \begin{eqnarray*}
            F_i(b_i) - F_i(a_i) & = & \beta \\
            p_i(b_i) & = & p_i(a_i)
            \end{eqnarray*}

        which consists of finding the bound :math:`a_i` such that:

        .. math::

            p_i(a_i) =  p_i(F_i^{-1}(\beta + F_i(a_i)))

        To find :math:`\beta`, we use the Brent algorithm:  :math:`\mu([\vect{a}(\beta); \vect{b}(\beta)] = g(\beta) = \alpha` with :math:`g` a non linear function.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt = paramDist.computeMinimumVolumeInterval(0.9)

        """
        return _model_copula.Distribution_computeMinimumVolumeInterval(self, prob)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _model_copula.Distribution_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeBilateralConfidenceInterval(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The bilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`a_i = F_i^{-1}((1-\beta)/2)` and :math:`b_i = F_i^{-1}((1+\beta)/2)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeBilateralConfidenceInterval(0.9)
        """
        return _model_copula.Distribution_computeBilateralConfidenceInterval(self, prob)

    def computeBilateralConfidenceIntervalWithMarginalProbability(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Refer to :func:`computeBilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9 with marginal probability:

        >>> confInt, marginalProb = paramDist.computeBilateralConfidenceIntervalWithMarginalProbability(0.9)
        """
        return _model_copula.Distribution_computeBilateralConfidenceIntervalWithMarginalProbability(self, prob)

    def computeUnilateralConfidenceInterval(self, prob, tail=False):
        r"""
        Compute a unilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu`.

        The left unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]-\infty, b_1] \times \dots \times ]-\infty, b_d]` where :math:`b_i = F_i^{-1}(\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`\vect{b}` is the quantile of level :math:`\alpha` of the measure :math:`\mu`, with iso-quantile components.

        The right unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]a_1; +\infty[ \times \dots \times ]a_d; +\infty[` where :math:`a_i = F_i^{-1}(1-\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`S_{\mu}^{-1}(\vect{a}) = \alpha` with iso-quantile components, where :math:`S_{\mu}` is the survival function of the measure :math:`\mu`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9, True)

        """
        return _model_copula.Distribution_computeUnilateralConfidenceInterval(self, prob, tail)

    def computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail):
        r"""
        Compute a unilateral confidence interval.

        Refer to :func:`computeUnilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, False)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, True)

        """
        return _model_copula.Distribution_computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail)

    def computeMinimumVolumeLevelSet(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence domain :math:`A^*_{\alpha}` is the set of minimum volume and which measure is at least :math:`\alpha`. It is defined by:

        .. math::

            A^*_{\alpha} = \argmin_{A \in \Rset^d\, | \, \mu(A) \geq \alpha} \lambda(A)

        where :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. Under some general conditions on :math:`\mu` (for example, no flat regions), the set  :math:`A^*_{\alpha}` is unique and realises the minimum: :math:`\mu(A^*_{\alpha}) = \alpha`. We show that :math:`A^*_{\alpha}` writes:

        .. math::

            A^*_{\alpha} = \{ \vect{x} \in \Rset^d \, | \, p(\vect{x}) \geq p_{\alpha} \}

        for a certain :math:`p_{\alpha} >0`.

        If we consider the random variable :math:`Y = p(\vect{X})`, with cumulative distribution function :math:`F_Y`, then :math:`p_{\alpha}` is defined by:

        .. math::

            1-F_Y(p_{\alpha}) = \alpha

        Thus the minimum volume domain of confidence :math:`\alpha` is the interior of the domain which frontier is the :math:`1-\alpha` quantile of :math:`Y`. It can be determined with simulations of :math:`Y`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9:

        >>> levelSet = paramDist.computeMinimumVolumeLevelSet(0.9)

        """
        return _model_copula.Distribution_computeMinimumVolumeLevelSet(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _model_copula.Distribution_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def getRange(self):
        """
        Accessor to the range of the distribution.

        Returns
        -------
        range : :class:`~openturns.Interval`
            Range of the distribution.

        Notes
        -----
        The *mathematical* range is the smallest closed interval outside of which the
        PDF is zero. The *numerical* range is the interval outside of which the PDF is
        rounded to zero in double precision.

        See Also
        --------
        getSupport
        """
        return _model_copula.Distribution_getRange(self)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _model_copula.Distribution_getRoughness(self)

    def getMean(self):
        r"""
        Accessor to the mean.

        Returns
        -------
        k : :class:`~openturns.Point`
            Mean.

        Notes
        -----
        The mean is the first-order moment:

        .. math::

            \vect{\mu} = \Tr{\left(\Expect{X_i}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.Distribution_getMean(self)

    def getCovariance(self):
        r"""
        Accessor to the covariance matrix.

        Returns
        -------
        Sigma : :class:`~openturns.CovarianceMatrix`
            Covariance matrix.

        Notes
        -----
        The covariance is the second-order centered moment. It is defined as:

        .. math::

            \mat{\Sigma} & = \Cov{\vect{X}} \\
                         & = \Expect{\left(\vect{X} - \vect{\mu}\right)
                                     \Tr{\left(\vect{X} - \vect{\mu}\right)}}
        """
        return _model_copula.Distribution_getCovariance(self)

    def getCholesky(self):
        """
        Accessor to the Cholesky factor of the covariance matrix.

        Returns
        -------
        L : :class:`~openturns.SquareMatrix`
            Cholesky factor of the covariance matrix.

        See Also
        --------
        getCovariance
        """
        return _model_copula.Distribution_getCholesky(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _model_copula.Distribution_getStandardMoment(self, n)

    def getMoment(self, n):
        r"""
        Accessor to the componentwise moments.

        Parameters
        ----------
        k : int
            The order of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise moment of order :math:`k`.

        Notes
        -----
        The componentwise moment of order :math:`k` is defined as:

        .. math::

            \vect{m}^{(k)} = \Tr{\left(\Expect{X_i^k}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.Distribution_getMoment(self, n)

    def getCenteredMoment(self, n):
        r"""
        Accessor to the componentwise centered moments.

        Parameters
        ----------
        k : int
            The order of the centered moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        Centered moments are centered with respect to the first-order moment:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - \mu_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment
        """
        return _model_copula.Distribution_getCenteredMoment(self, n)

    def getShiftedMoment(self, n, shift):
        r"""
        Accessor to the componentwise shifted moments.

        Parameters
        ----------
        k : int
            The order of the shifted moment.
        shift : sequence of float
            The shift of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        The moments are centered with respect to the given shift :\math:`\vect{s}`:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - s_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment, getCenteredMoment
        """
        return _model_copula.Distribution_getShiftedMoment(self, n, shift)

    def getInverseCholesky(self):
        """
        Accessor to the inverse Cholesky factor of the covariance matrix.

        Returns
        -------
        Linv : :class:`~openturns.SquareMatrix`
            Inverse Cholesky factor of the covariance matrix.

        See also
        --------
        getCholesky
        """
        return _model_copula.Distribution_getInverseCholesky(self)

    def getCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.Distribution_getCorrelation(self)

    def getLinearCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.Distribution_getLinearCorrelation(self)

    def getPearsonCorrelation(self):
        r"""
        Accessor to the Pearson correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Pearson's correlation matrix.

        See Also
        --------
        getCovariance

        Notes
        -----
        Pearson's correlation is defined as the normalized covariance matrix:

        .. math::

            \mat{\rho} & = \left[\frac{\Cov{X_i, X_j}}{\sqrt{\Var{X_i}\Var{X_j}}},
                                 \quad i,j = 1, \ldots, n\right] \\
                       & = \left[\frac{\Sigma_{i,j}}{\sqrt{\Sigma_{i,i}\Sigma_{j,j}}},
                                 \quad i,j = 1, \ldots, n\right]
        """
        return _model_copula.Distribution_getPearsonCorrelation(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.Distribution_getSpearmanCorrelation(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.Distribution_getKendallTau(self)

    def getShapeMatrix(self):
        """
        Accessor to the shape matrix of the underlying copula if it is elliptical.

        Returns
        -------
        shape : :class:`~openturns.CorrelationMatrix`
            Shape matrix of the elliptical copula of a distribution.

        Notes
        -----
        This is not the Pearson correlation matrix.

        See Also
        --------
        getPearsonCorrelation
        """
        return _model_copula.Distribution_getShapeMatrix(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.Distribution_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.Distribution_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.Distribution_getKurtosis(self)

    def getImplementation(self):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _model_copula.Distribution_getImplementation(self)

    def isCopula(self):
        """
        Test whether the distribution is a copula or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A copula is a distribution with uniform margins on [0; 1].
        """
        return _model_copula.Distribution_isCopula(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.Distribution_isElliptical(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.Distribution_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.Distribution_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.Distribution_isIntegral(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.Distribution_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.Distribution_hasIndependentCopula(self)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _model_copula.Distribution_getSupport(self, *args)

    def getProbabilities(self):
        """
        Accessor to the discrete probability levels.

        Returns
        -------
        probabilities : :class:`~openturns.Point`
            The probability levels of a discrete distribution.
        """
        return _model_copula.Distribution_getProbabilities(self)

    def getSingularities(self):
        """
        Accessor to the singularities of the PDF function.

        It is defined for univariate distributions only, and gives all the singularities (ie discontinuities of any order) strictly inside of the range of the distribution.

        Returns
        -------
        singularities : :class:`~openturns.Point`
            The singularities of the PDF of an univariate distribution.
        """
        return _model_copula.Distribution_getSingularities(self)

    def computeDensityGenerator(self, betaSquare):
        r"""
        Compute the probability density function of the characteristic generator.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator value at input :math:`X`.

        Notes
        -----
        This is the function :math:`\phi` such that the probability density function
        rewrites:

        .. math::

            f_{\vect{X}}(\vect{x}) =
                \phi\left(\Tr{\left(\vect{x} - \vect{\mu}\right)}
                              \mat{\Sigma}^{-1}
                              \left(\vect{x} - \vect{\mu}\right)
                    \right),
                \quad \vect{x} \in \supp{\vect{X}}

        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computePDF
        """
        return _model_copula.Distribution_computeDensityGenerator(self, betaSquare)

    def computeDensityGeneratorDerivative(self, betaSquare):
        """
        Compute the first-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator first-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.Distribution_computeDensityGeneratorDerivative(self, betaSquare)

    def computeDensityGeneratorSecondDerivative(self, betaSquare):
        """
        Compute the second-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator second-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.Distribution_computeDensityGeneratorSecondDerivative(self, betaSquare)

    def computeRadialDistributionCDF(self, radius, tail=False):
        r"""
        Compute the cumulative distribution function of the squared radius.

        For the underlying standard spherical distribution (for elliptical
        distributions only).

        Parameters
        ----------
        r2 : float, :math:`0 \leq r^2`
            Squared radius.

        Returns
        -------
        F : float
            CDF value at input :math:`r^2`.

        Notes
        -----
        This is the CDF of the sum of the squared independent, standard, identically
        distributed components:

        .. math::

            R^2 = \sqrt{\sum\limits_{i=1}^n U_i^2}
        """
        return _model_copula.Distribution_computeRadialDistributionCDF(self, radius, tail)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.Distribution_getMarginal(self, *args)

    def getCopula(self):
        """
        Accessor to the copula of the distribution.

        Returns
        -------
        C : :class:`~openturns.Distribution`
            Copula of the distribution.

        See Also
        --------
        ComposedDistribution
        """
        return _model_copula.Distribution_getCopula(self)

    def computeConditionalDDF(self, x, y):
        """
        Compute the conditional derivative density function of the last component.

        With respect to the other fixed components.

        Parameters
        ----------
        Xn : float
            Conditional DDF input (last component).
        Xcond : sequence of float with dimension :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        d : float
            Conditional DDF value at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computeDDF, computeConditionalCDF
        """
        return _model_copula.Distribution_computeConditionalDDF(self, x, y)

    def computeSequentialConditionalDDF(self, x):
        r"""
        Compute the sequential conditional derivative density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the DDF.

        Returns
        -------
        ddf : sequence of float
            Conditional DDF values at input.

        Notes
        -----
        The sequential conditional derivative density function is defined as follows:

        .. math::

            ddf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d^2}{d\,x_n^2}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional DDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d^2}{d\,x_1^2}\Prob{X_1 \leq x_1}`, ie the DDF of the first component at :math:`x_1`.
        """
        return _model_copula.Distribution_computeSequentialConditionalDDF(self, x)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.Distribution_computeSequentialConditionalPDF(self, x)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.Distribution_computeConditionalPDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.Distribution_computeSequentialConditionalCDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.Distribution_computeConditionalCDF(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.Distribution_computeSequentialConditionalQuantile(self, q)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.Distribution_computeConditionalQuantile(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.Distribution_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.Distribution_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.Distribution_getStandardDistribution(self)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _model_copula.Distribution_getStandardRepresentative(self)

    def drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF of the requested margin.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of probability density function.

        Available constructors:
            drawPDF(*x_min, x_max, pointNumber, logScale*)

            drawPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computePDF, viewer.View, ResourceMap

        Examples
        --------
        View the PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawPDF()
        >>> graph.setLegends(['normal pdf'])

        View the iso-lines PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.Distribution_drawPDF(self, *args)

    def drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal PDF of the requested couple of
            margins.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the log-probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF of the requested margin.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DLogPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawLogPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of log-probability density function.

        Available constructors:
            drawLogPDF(*x_min, x_max, pointNumber, logScale*)

            drawLogPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawLogPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeLogPDF, viewer.View, ResourceMap

        Examples
        --------
        View the log-PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawLogPDF()
        >>> graph.setLegends(['normal log-pdf'])

        View the iso-lines log-PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawLogPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawLogPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.Distribution_drawLogPDF(self, *args)

    def drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the log-probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal log-PDF of the requested couple of
            margins.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DLogPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawCDF(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawCDF(*x_min, x_max, pointNumber, logScale*)

            drawCDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawCDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeCDF, viewer.View, ResourceMap

        Examples
        --------
        View the CDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawCDF()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines CDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawCDF()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawCDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.Distribution_drawCDF(self, *args)

    def drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF of the requested margin.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DCDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal CDF of the requested couple of
            margins.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DCDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawSurvivalFunction(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawSurvivalFunction(*x_min, x_max, pointNumber, logScale*)

            drawSurvivalFunction(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawSurvivalFunction(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeSurvivalFunction, viewer.View, ResourceMap

        Examples
        --------
        View the SurvivalFunction of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawSurvivalFunction()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines SurvivalFunction of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawSurvivalFunction()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawSurvivalFunction([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.Distribution_drawSurvivalFunction(self, *args)

    def drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction of the requested margin.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DSurvivalFunction(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal SurvivalFunction of the requested couple of
            margins.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DSurvivalFunction(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawQuantile(self, *args):
        """
        Draw the quantile function.

        Parameters
        ----------
        q_min : float, in :math:`[0,1]`
            The min value of the mesh of the x-axis.
        q_max : float, in :math:`[0,1]`
            The max value of the mesh of the x-axis.
        n_points : int, optional
            The number of points that is used for meshing the quantile curve.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the quantile function.

        Notes
        -----
        This is implemented for univariate and bivariate distributions only.
        In the case of bivariate distributions, defined by its CDF :math:`F` and its marginals :math:`(F_1, F_2)`, the quantile of order :math:`q` is the point :math:`(F_1(u),F_2(u))` defined by

        .. math::

            F(F_1(u), F_2(u)) = q

        See Also
        --------
        computeQuantile, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal()
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        >>> distribution = ot.ComposedDistribution([ot.Normal(), ot.Exponential(1.0)], ot.ClaytonCopula(0.5))
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.Distribution_drawQuantile(self, *args)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.Distribution_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.Distribution_setParametersCollection(self, *args)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.Distribution_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.Distribution_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.Distribution_getParameterDescription(self)

    def getParameterDimension(self):
        """
        Accessor to the number of parameters in the distribution.

        Returns
        -------
        n_parameters : int
            Number of parameters in the distribution.

        See Also
        --------
        getParametersCollection
        """
        return _model_copula.Distribution_getParameterDimension(self)

    def setDescription(self, description):
        """
        Accessor to the componentwise description.

        Parameters
        ----------
        description : sequence of str
            Description of the components of the distribution.
        """
        return _model_copula.Distribution_setDescription(self, description)

    def getDescription(self):
        """
        Accessor to the componentwise description.

        Returns
        -------
        description : :class:`~openturns.Description`
            Description of the components of the distribution.

        See Also
        --------
        setDescription
        """
        return _model_copula.Distribution_getDescription(self)

    def getPDFEpsilon(self):
        """
        Accessor to the PDF computation precision.

        Returns
        -------
        PDFEpsilon : float
            PDF computation precision.
        """
        return _model_copula.Distribution_getPDFEpsilon(self)

    def getCDFEpsilon(self):
        """
        Accessor to the CDF computation precision.

        Returns
        -------
        CDFEpsilon : float
            CDF computation precision.
        """
        return _model_copula.Distribution_getCDFEpsilon(self)

    def getPositionIndicator(self):
        """
        Position indicator accessor.

        Defines a generic metric of the position. When the mean is not defined it falls
        back to the median.
        Available only for 1-d distributions.

        Returns
        -------
        position : float
            Mean or median of the distribution.
        """
        return _model_copula.Distribution_getPositionIndicator(self)

    def getDispersionIndicator(self):
        """
        Dispersion indicator accessor.

        Defines a generic metric of the dispersion. When the standard deviation is not
        defined it falls back to the interquartile.
        Only available for 1-d distributions.

        Returns
        -------
        dispersion : float
            Standard deviation or interquartile.
        """
        return _model_copula.Distribution_getDispersionIndicator(self)

    def __init__(self, *args):
        _model_copula.Distribution_swiginit(self, _model_copula.new_Distribution(*args))

    def __add__(self, *args):
        return _model_copula.Distribution___add__(self, *args)

    def __radd__(self, s):
        return _model_copula.Distribution___radd__(self, s)

    def __sub__(self, *args):
        return _model_copula.Distribution___sub__(self, *args)

    def __rsub__(self, s):
        return _model_copula.Distribution___rsub__(self, s)

    def __mul__(self, *args):
        return _model_copula.Distribution___mul__(self, *args)

    def __rmul__(self, s):
        return _model_copula.Distribution___rmul__(self, s)

    def __div__(self, s):
        return _model_copula.Distribution___div__(self, s)

    __swig_destroy__ = _model_copula.delete_Distribution


_model_copula.Distribution_swigregister(Distribution)

class DistributionFactoryResult(openturns.common.PersistentObject):
    """
    Results of distribution estimation.

    This class is the result of a distribution estimation through a
    :class:`~openturns.DistributionFactory`.

    Parameters
    ----------
    distribution : :class:`~openturns.Distribution`
        The estimated distribution.
    parameterDistribution : :class:`~openturns.Distribution`
        The distribution of the parameter.

    See also
    --------
    DistributionFactory

    Examples
    --------
    We demonstrate the method on a Beta Distribution.

    Create a sample from a Beta distribution:

    >>> import openturns as ot
    >>> sample = ot.Beta().getSample(10)
    >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

    Fit a Beta distribution and create a :class:`~openturns.DistributionFactory`: 

    >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

    Get the fitted Beta distribution and its parameters:

    >>> fittedBeta =  fittedRes.getDistribution()

    Get the asymptotic parameters distribution: 

    >>> paramDist = fittedRes.getParameterDistribution()
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionFactoryResult_getClassName(self)

    def setDistribution(self, distribution):
        """
        Accessor to the estimated distribution.

        Parameters
        ----------
        distribution : :class:`~openturns.Distribution`
            The estimated distribution.
        """
        return _model_copula.DistributionFactoryResult_setDistribution(self, distribution)

    def getDistribution(self):
        """
        Accessor to the estimated distribution.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The estimated distribution.
        """
        return _model_copula.DistributionFactoryResult_getDistribution(self)

    def setParameterDistribution(self, parameterDistribution):
        """
        Accessor to the distribution of the parameter.

        Parameters
        ----------
        parameterDistribution : :class:`~openturns.Distribution`
            The distribution of the parameter.
        """
        return _model_copula.DistributionFactoryResult_setParameterDistribution(self, parameterDistribution)

    def getParameterDistribution(self):
        """
        Accessor to the distribution of the parameter.

        Returns
        -------
        parameterDistribution : :class:`~openturns.Distribution`
            The distribution of the parameter.
        """
        return _model_copula.DistributionFactoryResult_getParameterDistribution(self)

    def __repr__(self):
        return _model_copula.DistributionFactoryResult___repr__(self)

    def __init__(self, *args):
        _model_copula.DistributionFactoryResult_swiginit(self, _model_copula.new_DistributionFactoryResult(*args))

    __swig_destroy__ = _model_copula.delete_DistributionFactoryResult


_model_copula.DistributionFactoryResult_swigregister(DistributionFactoryResult)

class DistributionParametersImplementation(openturns.common.PersistentObject):
    """
    Define a distribution with particular parameters.

    This class enables to create a set of non-native parameters in order to
    define distribution.

    A *DistributionParameters* object can be used through its derived classes:

    - :class:`~openturns.ArcsineMuSigma`
    - :class:`~openturns.BetaMuSigma`
    - :class:`~openturns.GammaMuSigma`
    - :class:`~openturns.GumbelMuSigma`
    - :class:`~openturns.GumbelAB`
    - :class:`~openturns.LogNormalMuSigma`
    - :class:`~openturns.LogNormalMuSigmaOverMu`
    - :class:`~openturns.WeibullMinMuSigma`

    See also
    --------
    ParametrizedDistribution, Distribution
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionParametersImplementation_getClassName(self)

    def __repr__(self):
        return _model_copula.DistributionParametersImplementation___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionParametersImplementation___str__(self, *args)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _model_copula.DistributionParametersImplementation_getDistribution(self)

    def evaluate(self):
        """
        Compute native parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            The native parameter values.
        """
        return _model_copula.DistributionParametersImplementation_evaluate(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _model_copula.DistributionParametersImplementation_gradient(self)

    def __call__(self, inP):
        return _model_copula.DistributionParametersImplementation___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _model_copula.DistributionParametersImplementation_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _model_copula.DistributionParametersImplementation_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _model_copula.DistributionParametersImplementation_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _model_copula.DistributionParametersImplementation_getDescription(self)

    def __init__(self, *args):
        _model_copula.DistributionParametersImplementation_swiginit(self, _model_copula.new_DistributionParametersImplementation(*args))

    __swig_destroy__ = _model_copula.delete_DistributionParametersImplementation


_model_copula.DistributionParametersImplementation_swigregister(DistributionParametersImplementation)

class DistributionParametersImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _model_copula.DistributionParametersImplementationTypedInterfaceObject_swiginit(self, _model_copula.new_DistributionParametersImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _model_copula.DistributionParametersImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionParametersImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionParametersImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _model_copula.DistributionParametersImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.DistributionParametersImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _model_copula.delete_DistributionParametersImplementationTypedInterfaceObject


_model_copula.DistributionParametersImplementationTypedInterfaceObject_swigregister(DistributionParametersImplementationTypedInterfaceObject)

class DistributionParameters(DistributionParametersImplementationTypedInterfaceObject):
    """
    Define a distribution with particular parameters.

    This class enables to create a set of non-native parameters in order to
    define distribution.

    A *DistributionParameters* object can be used through its derived classes:

    - :class:`~openturns.ArcsineMuSigma`
    - :class:`~openturns.BetaMuSigma`
    - :class:`~openturns.GammaMuSigma`
    - :class:`~openturns.GumbelMuSigma`
    - :class:`~openturns.GumbelAB`
    - :class:`~openturns.LogNormalMuSigma`
    - :class:`~openturns.LogNormalMuSigmaOverMu`
    - :class:`~openturns.WeibullMinMuSigma`

    See also
    --------
    ParametrizedDistribution, Distribution
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionParameters_getClassName(self)

    def getDistribution(self):
        """
        Build a distribution based on a set of native parameters.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            Distribution built with the native parameters.
        """
        return _model_copula.DistributionParameters_getDistribution(self)

    def evaluate(self):
        """
        Compute native parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            The native parameter values.
        """
        return _model_copula.DistributionParameters_evaluate(self)

    def gradient(self):
        r"""
        Get the gradient.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            The gradient of the transformation of the native parameters into the new
            parameters.

        Notes
        -----

        If we note :math:`(p_1, \dots, p_q)` the native parameters and :math:`(p'_1, \dots, p'_q)` the new ones, then the gradient matrix is :math:`\left( \dfrac{\partial p'_i}{\partial p_j} \right)_{1 \leq i,j \leq  q}`.
        """
        return _model_copula.DistributionParameters_gradient(self)

    def __call__(self, inP):
        return _model_copula.DistributionParameters___call__(self, inP)

    def inverse(self, inP):
        """
        Convert to native parameters.

        Parameters
        ----------
        inP : sequence of float
            The non-native parameters.

        Returns
        -------
        outP : :class:`~openturns.Point`
            The native parameters.
        """
        return _model_copula.DistributionParameters_inverse(self, inP)

    def setValues(self, values):
        """
        Accessor to the parameters values.

        Parameters
        ----------
        values : sequence of float
            List of parameters values.
        """
        return _model_copula.DistributionParameters_setValues(self, values)

    def getValues(self):
        """
        Accessor to the parameters values.

        Returns
        -------
        values : :class:`~openturns.Point`
            List of parameters values.
        """
        return _model_copula.DistributionParameters_getValues(self)

    def getDescription(self):
        """
        Get the description of the parameters.

        Returns
        -------
        collection : :class:`~openturns.Description`
            List of parameters names.
        """
        return _model_copula.DistributionParameters_getDescription(self)

    def __repr__(self):
        return _model_copula.DistributionParameters___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionParameters___str__(self, *args)

    def __init__(self, *args):
        _model_copula.DistributionParameters_swiginit(self, _model_copula.new_DistributionParameters(*args))

    __swig_destroy__ = _model_copula.delete_DistributionParameters


_model_copula.DistributionParameters_swigregister(DistributionParameters)

class DistributionFactoryImplementation(openturns.common.PersistentObject):
    """
    Base class for probability distribution factories.

    Notes
    -----
    This class generally describes the factory mechanism of each OpenTURNS
    distribution. Refer to :ref:`parametric_estimation` for information on the specific
    estimators used for each distribution.

    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionFactoryImplementation_getClassName(self)

    def __repr__(self):
        return _model_copula.DistributionFactoryImplementation___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionFactoryImplementation___str__(self, *args)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.DistributionFactoryImplementation_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _model_copula.DistributionFactoryImplementation_buildEstimator(self, *args)

    def getBootstrapSize(self):
        """
        Accessor to the bootstrap size.

        Returns
        -------
        size : integer
            Size of the bootstrap.
        """
        return _model_copula.DistributionFactoryImplementation_getBootstrapSize(self)

    def setBootstrapSize(self, bootstrapSize):
        """
        Accessor to the bootstrap size.

        Parameters
        ----------
        size : integer
            Size of the bootstrap.
        """
        return _model_copula.DistributionFactoryImplementation_setBootstrapSize(self, bootstrapSize)

    def __init__(self, *args):
        _model_copula.DistributionFactoryImplementation_swiginit(self, _model_copula.new_DistributionFactoryImplementation(*args))

    __swig_destroy__ = _model_copula.delete_DistributionFactoryImplementation


_model_copula.DistributionFactoryImplementation_swigregister(DistributionFactoryImplementation)

class DistributionFactoryImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _model_copula.DistributionFactoryImplementationTypedInterfaceObject_swiginit(self, _model_copula.new_DistributionFactoryImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _model_copula.DistributionFactoryImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionFactoryImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionFactoryImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _model_copula.DistributionFactoryImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.DistributionFactoryImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _model_copula.delete_DistributionFactoryImplementationTypedInterfaceObject


_model_copula.DistributionFactoryImplementationTypedInterfaceObject_swigregister(DistributionFactoryImplementationTypedInterfaceObject)

class DistributionFactoryCollection(object):
    """
    Collection.

    Examples
    --------
    >>> import openturns as ot

    - Collection of **real values**:

    >>> ot.ScalarCollection(2)
    [0,0]
    >>> ot.ScalarCollection(2, 3.25)
    [3.25,3.25]
    >>> vector = ot.ScalarCollection([2.0, 1.5, 2.6])
    >>> vector
    [2,1.5,2.6]
    >>> vector[1] = 4.2
    >>> vector
    [2,4.2,2.6]
    >>> vector.add(3.8)
    >>> vector
    [2,4.2,2.6,3.8]

    - Collection of **complex values**:

    >>> ot.ComplexCollection(2)
    [(0,0),(0,0)]
    >>> ot.ComplexCollection(2, 3+4j)
    [(3,4),(3,4)]
    >>> vector = ot.ComplexCollection([2+3j, 1-4j, 3.0])
    >>> vector
    [(2,3),(1,-4),(3,0)]
    >>> vector[1] = 4+3j
    >>> vector
    [(2,3),(4,3),(3,0)]
    >>> vector.add(5+1j)
    >>> vector
    [(2,3),(4,3),(3,0),(5,1)]

    - Collection of **booleans**:

    >>> ot.BoolCollection(3)
    [0,0,0]
    >>> ot.BoolCollection(3, 1)
    [1,1,1]
    >>> vector = ot.BoolCollection([0, 1, 0])
    >>> vector
    [0,1,0]
    >>> vector[1] = 0
    >>> vector
    [0,0,0]
    >>> vector.add(1)
    >>> vector
    [0,0,0,1]

    - Collection of **distributions**:

    >>> print(ot.DistributionCollection(2))
    [Uniform(a = -1, b = 1),Uniform(a = -1, b = 1)]
    >>> print(ot.DistributionCollection(2, ot.Gamma(2.75, 1.0)))
    [Gamma(k = 2.75, lambda = 1, gamma = 0),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    >>> vector = ot.DistributionCollection([ot.Normal(), ot.Uniform()])
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -1, b = 1)]
    >>> vector[1] = ot.Uniform(-0.5, 1)
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1)]
    >>> vector.add(ot.Gamma(2.75, 1.0))
    >>> print(vector)
    [Normal(mu = 0, sigma = 1),Uniform(a = -0.5, b = 1),Gamma(k = 2.75, lambda = 1, gamma = 0)]
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __swig_destroy__ = _model_copula.delete_DistributionFactoryCollection

    def clear(self):
        """
        Reset the collection to zero dimension.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.clear()
        >>> x
        class=Point name=Unnamed dimension=0 values=[]
        """
        return _model_copula.DistributionFactoryCollection_clear(self)

    def __len__(self):
        return _model_copula.DistributionFactoryCollection___len__(self)

    def __eq__(self, rhs):
        return _model_copula.DistributionFactoryCollection___eq__(self, rhs)

    def __contains__(self, val):
        return _model_copula.DistributionFactoryCollection___contains__(self, val)

    def __getitem__(self, i):
        return _model_copula.DistributionFactoryCollection___getitem__(self, i)

    def __setitem__(self, i, val):
        return _model_copula.DistributionFactoryCollection___setitem__(self, i, val)

    def __delitem__(self, i):
        return _model_copula.DistributionFactoryCollection___delitem__(self, i)

    def at(self, *args):
        """
        Access to an element of the collection.

        Parameters
        ----------
        index : positive int
            Position of the element to access.

        Returns
        -------
        element : type depends on the type of the collection
            Element of the collection at the position *index*.
        """
        return _model_copula.DistributionFactoryCollection_at(self, *args)

    def add(self, *args):
        """
        Append a component (in-place).

        Parameters
        ----------
        value : type depends on the type of the collection.
            The component to append.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.add(1.)
        >>> print(x)
        [0,0,1]
        """
        return _model_copula.DistributionFactoryCollection_add(self, *args)

    def getSize(self):
        """
        Get the collection's dimension (or size).

        Returns
        -------
        n : int
            The number of components in the collection.
        """
        return _model_copula.DistributionFactoryCollection_getSize(self)

    def resize(self, newSize):
        """
        Change the size of the collection.

        Parameters
        ----------
        newSize : positive int
            New size of the collection.

        Notes
        -----
        If the new size is smaller than the older one, the last elements are thrown
        away, else the new elements are set to the default value of the element type.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2, 4)
        >>> print(x)
        [4,4]
        >>> x.resize(1)
        >>> print(x)
        [4]
        >>> x.resize(4)
        >>> print(x)
        [4,0,0,0]
        """
        return _model_copula.DistributionFactoryCollection_resize(self, newSize)

    def isEmpty(self):
        """
        Tell if the collection is empty.

        Returns
        -------
        isEmpty : bool
            *True* if there is no element in the collection.

        Examples
        --------
        >>> import openturns as ot
        >>> x = ot.Point(2)
        >>> x.isEmpty()
        False
        >>> x.clear()
        >>> x.isEmpty()
        True
        """
        return _model_copula.DistributionFactoryCollection_isEmpty(self)

    def __repr__(self):
        return _model_copula.DistributionFactoryCollection___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionFactoryCollection___str__(self, *args)

    def __init__(self, *args):
        _model_copula.DistributionFactoryCollection_swiginit(self, _model_copula.new_DistributionFactoryCollection(*args))


_model_copula.DistributionFactoryCollection_swigregister(DistributionFactoryCollection)

class DistributionFactory(DistributionFactoryImplementationTypedInterfaceObject):
    """
    Base class for probability distribution factories.

    Notes
    -----
    This class generally describes the factory mechanism of each OpenTURNS
    distribution. Refer to :ref:`parametric_estimation` for information on the specific
    estimators used for each distribution.

    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionFactory_getClassName(self)

    def __repr__(self):
        return _model_copula.DistributionFactory___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionFactory___str__(self, *args)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.DistributionFactory_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _model_copula.DistributionFactory_buildEstimator(self, *args)

    @staticmethod
    def GetContinuousUniVariateFactories():
        """
        Accessor to the list of continuous univariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid continuous univariate factories.
        """
        return _model_copula.DistributionFactory_GetContinuousUniVariateFactories()

    @staticmethod
    def GetContinuousMultiVariateFactories():
        """
        Accessor to the list of continuous multivariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid continuous multivariate factories.
        """
        return _model_copula.DistributionFactory_GetContinuousMultiVariateFactories()

    @staticmethod
    def GetDiscreteUniVariateFactories():
        """
        Accessor to the list of discrete univariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid discrete univariate factories.
        """
        return _model_copula.DistributionFactory_GetDiscreteUniVariateFactories()

    @staticmethod
    def GetDiscreteMultiVariateFactories():
        """
        Accessor to the list of discrete multivariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid discrete multivariate factories.
        """
        return _model_copula.DistributionFactory_GetDiscreteMultiVariateFactories()

    @staticmethod
    def GetUniVariateFactories():
        """
        Accessor to the list of univariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid univariate factories.
        """
        return _model_copula.DistributionFactory_GetUniVariateFactories()

    @staticmethod
    def GetMultiVariateFactories():
        """
        Accessor to the list of multivariate factories.

        Returns
        -------
        listFactories : collection of :class:`~openturns.DistributionFactory`
            All the valid multivariate factories.
        """
        return _model_copula.DistributionFactory_GetMultiVariateFactories()

    def __init__(self, *args):
        _model_copula.DistributionFactory_swiginit(self, _model_copula.new_DistributionFactory(*args))

    __swig_destroy__ = _model_copula.delete_DistributionFactory


_model_copula.DistributionFactory_swigregister(DistributionFactory)

def DistributionFactory_GetContinuousUniVariateFactories():
    """
    Accessor to the list of continuous univariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid continuous univariate factories.
    """
    return _model_copula.DistributionFactory_GetContinuousUniVariateFactories()


def DistributionFactory_GetContinuousMultiVariateFactories():
    """
    Accessor to the list of continuous multivariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid continuous multivariate factories.
    """
    return _model_copula.DistributionFactory_GetContinuousMultiVariateFactories()


def DistributionFactory_GetDiscreteUniVariateFactories():
    """
    Accessor to the list of discrete univariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid discrete univariate factories.
    """
    return _model_copula.DistributionFactory_GetDiscreteUniVariateFactories()


def DistributionFactory_GetDiscreteMultiVariateFactories():
    """
    Accessor to the list of discrete multivariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid discrete multivariate factories.
    """
    return _model_copula.DistributionFactory_GetDiscreteMultiVariateFactories()


def DistributionFactory_GetUniVariateFactories():
    """
    Accessor to the list of univariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid univariate factories.
    """
    return _model_copula.DistributionFactory_GetUniVariateFactories()


def DistributionFactory_GetMultiVariateFactories():
    """
    Accessor to the list of multivariate factories.

    Returns
    -------
    listFactories : collection of :class:`~openturns.DistributionFactory`
        All the valid multivariate factories.
    """
    return _model_copula.DistributionFactory_GetMultiVariateFactories()


class ContinuousDistribution(DistributionImplementation):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.ContinuousDistribution_getClassName(self)

    def __init__(self):
        _model_copula.ContinuousDistribution_swiginit(self, _model_copula.new_ContinuousDistribution())

    def __eq__(self, other):
        return _model_copula.ContinuousDistribution___eq__(self, other)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ContinuousDistribution_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ContinuousDistribution_computeCDF(self, *args)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.ContinuousDistribution_computeSurvivalFunction(self, *args)

    def __repr__(self):
        return _model_copula.ContinuousDistribution___repr__(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ContinuousDistribution_isContinuous(self)

    __swig_destroy__ = _model_copula.delete_ContinuousDistribution


_model_copula.ContinuousDistribution_swigregister(ContinuousDistribution)

class EllipticalDistribution(ContinuousDistribution):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.EllipticalDistribution_getClassName(self)

    def __repr__(self):
        return _model_copula.EllipticalDistribution___repr__(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.EllipticalDistribution_isElliptical(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.EllipticalDistribution_hasEllipticalCopula(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.EllipticalDistribution_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.EllipticalDistribution_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _model_copula.EllipticalDistribution_computeLogPDF(self, *args)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.EllipticalDistribution_computePDFGradient(self, *args)

    def computeDensityGenerator(self, betaSquare):
        r"""
        Compute the probability density function of the characteristic generator.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator value at input :math:`X`.

        Notes
        -----
        This is the function :math:`\phi` such that the probability density function
        rewrites:

        .. math::

            f_{\vect{X}}(\vect{x}) =
                \phi\left(\Tr{\left(\vect{x} - \vect{\mu}\right)}
                              \mat{\Sigma}^{-1}
                              \left(\vect{x} - \vect{\mu}\right)
                    \right),
                \quad \vect{x} \in \supp{\vect{X}}

        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computePDF
        """
        return _model_copula.EllipticalDistribution_computeDensityGenerator(self, betaSquare)

    def computeLogDensityGenerator(self, betaSquare):
        return _model_copula.EllipticalDistribution_computeLogDensityGenerator(self, betaSquare)

    def computeDensityGeneratorDerivative(self, betaSquare):
        """
        Compute the first-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator first-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.EllipticalDistribution_computeDensityGeneratorDerivative(self, betaSquare)

    def computeDensityGeneratorSecondDerivative(self, betaSquare):
        """
        Compute the second-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator second-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.EllipticalDistribution_computeDensityGeneratorSecondDerivative(self, betaSquare)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.EllipticalDistribution_computeSurvivalFunction(self, *args)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _model_copula.EllipticalDistribution_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def setMean(self, mean):
        return _model_copula.EllipticalDistribution_setMean(self, mean)

    def setSigma(self, sigma):
        return _model_copula.EllipticalDistribution_setSigma(self, sigma)

    def getSigma(self):
        return _model_copula.EllipticalDistribution_getSigma(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.EllipticalDistribution_getStandardDeviation(self)

    def setCorrelation(self, R):
        return _model_copula.EllipticalDistribution_setCorrelation(self, R)

    def getCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.EllipticalDistribution_getCorrelation(self)

    def normalize(self, x):
        return _model_copula.EllipticalDistribution_normalize(self, x)

    def denormalize(self, u):
        return _model_copula.EllipticalDistribution_denormalize(self, u)

    def getInverseCorrelation(self):
        return _model_copula.EllipticalDistribution_getInverseCorrelation(self)

    def getCholesky(self):
        """
        Accessor to the Cholesky factor of the covariance matrix.

        Returns
        -------
        L : :class:`~openturns.SquareMatrix`
            Cholesky factor of the covariance matrix.

        See Also
        --------
        getCovariance
        """
        return _model_copula.EllipticalDistribution_getCholesky(self)

    def getInverseCholesky(self):
        """
        Accessor to the inverse Cholesky factor of the covariance matrix.

        Returns
        -------
        Linv : :class:`~openturns.SquareMatrix`
            Inverse Cholesky factor of the covariance matrix.

        See also
        --------
        getCholesky
        """
        return _model_copula.EllipticalDistribution_getInverseCholesky(self)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.EllipticalDistribution_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.EllipticalDistribution_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.EllipticalDistribution_getStandardDistribution(self)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.EllipticalDistribution_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.EllipticalDistribution_setParametersCollection(self, *args)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.EllipticalDistribution_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.EllipticalDistribution_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.EllipticalDistribution_getParameterDescription(self)

    def __init__(self, *args):
        _model_copula.EllipticalDistribution_swiginit(self, _model_copula.new_EllipticalDistribution(*args))

    __swig_destroy__ = _model_copula.delete_EllipticalDistribution


_model_copula.EllipticalDistribution_swigregister(EllipticalDistribution)

class DiscreteDistribution(DistributionImplementation):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DiscreteDistribution_getClassName(self)

    def __init__(self):
        _model_copula.DiscreteDistribution_swiginit(self, _model_copula.new_DiscreteDistribution())

    def __eq__(self, other):
        return _model_copula.DiscreteDistribution___eq__(self, other)

    def __repr__(self):
        return _model_copula.DiscreteDistribution___repr__(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DiscreteDistribution_computePDF(self, *args)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DiscreteDistribution_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DiscreteDistribution_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DiscreteDistribution_isIntegral(self)

    def setSupportEpsilon(self, epsilon):
        return _model_copula.DiscreteDistribution_setSupportEpsilon(self, epsilon)

    def getSupportEpsilon(self):
        return _model_copula.DiscreteDistribution_getSupportEpsilon(self)

    __swig_destroy__ = _model_copula.delete_DiscreteDistribution


_model_copula.DiscreteDistribution_swigregister(DiscreteDistribution)

class CopulaImplementation(DistributionImplementation):
    r"""
    Base class for copulas.

    Notes
    -----
    To define the joined probability density function of the random input vector
    :math:`\vect{X}` by composition, one needs:

    - the specification of the copula of interest :math:`C` with its parameters,
    - the specification of the :math:`n_X` marginal laws of interest :math:`F_{X_i}`
      of the :math:`n_X` input variables :math:`X_i`.

    The joined cumulative density function is therefore defined by :

    .. math::

      \Prob{X^1 \leq x^1, X^2 \leq x^2, \cdots, X^{n_X} \leq x^{n_X}}
          = C\left( F_{X^1}(x^1),F_{X^2}(x^2),\cdots,F_{X^{n_X}}(x^{n_X}) \right)

    Copulas allow to represent the part of the joined cumulative density function
    which is not described by the marginal laws. It enables to represent the
    dependence structure of the input variables. A copula is a special cumulative
    density function defined on :math:`[0,1]^{n_X}` whose marginal distributions
    are uniform on :math:`[0,1]`. The choice of the dependence structure is
    disconnected from the choice of the marginal distributions.

    A copula, restricted to :math:`[0,1]^{n_X}` is a :math:`n_U`-dimensional
    cumulative density function with uniform marginals such as:

    - :math:`C(\vect{u}) \geq 0, \forall \vect{u} \in [0,1]^{n_U}`
    - :math:`C(\vect{u}) = u_i, \forall \vect{u}=(1,\ldots,1,u_i,1,\ldots,1)`
    - For all :math:`N`-box 
      :math:`\cB = [a_1,b_1] \times \cdots \times [a_{n_U},b_{n_U}] \in [0,1]^{n_U}`,
      we have :math:`\cV_C(\cB) \geq 0`, where :

      - :math:`\cV_C(\cB) = \sum_{i=1,\cdots, 2^{n_U}} sign(\vect{v}_i) \times C(\vect{v}_i)`,
        the summation being made over the :math:`2^{n_U}` vertices :math:`\vect{v}_i` of :math:`\cB`.
      - :math:`sign(\vect{v}_i)= +1` if :math:`v_i^k = a_k` for an even number of
        :math:`k`'s, :math:`sign(\vect{v}_i)= -1` otherwise.

    See also
    --------
    ArchimedeanCopula, NormalCopula, ComposedCopula, SklarCopula
    IndependentCopula, MinCopula, OrdinalSumCopula, FarlieGumbelMorgensternCopula
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.CopulaImplementation_getClassName(self)

    def __eq__(self, other):
        return _model_copula.CopulaImplementation___eq__(self, other)

    def computeSurvivalFunction(self, point):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.CopulaImplementation_computeSurvivalFunction(self, point)

    def getMean(self):
        r"""
        Accessor to the mean.

        Returns
        -------
        k : :class:`~openturns.Point`
            Mean.

        Notes
        -----
        The mean is the first-order moment:

        .. math::

            \vect{\mu} = \Tr{\left(\Expect{X_i}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.CopulaImplementation_getMean(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.CopulaImplementation_getSpearmanCorrelation(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.CopulaImplementation_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.CopulaImplementation_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.CopulaImplementation_getKurtosis(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.CopulaImplementation_getMarginal(self, *args)

    def getCopula(self):
        """
        Accessor to the copula of the distribution.

        Returns
        -------
        C : :class:`~openturns.Distribution`
            Copula of the distribution.

        See Also
        --------
        ComposedDistribution
        """
        return _model_copula.CopulaImplementation_getCopula(self)

    def __repr__(self):
        return _model_copula.CopulaImplementation___repr__(self)

    def computeQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.CopulaImplementation_computeQuantile(self, prob, tail)

    def __init__(self, *args):
        _model_copula.CopulaImplementation_swiginit(self, _model_copula.new_CopulaImplementation(*args))

    __swig_destroy__ = _model_copula.delete_CopulaImplementation


_model_copula.CopulaImplementation_swigregister(CopulaImplementation)

class ArchimedeanCopula(CopulaImplementation):
    r"""
    Base class for bivariate Archimedean copulas.

    Notes
    -----
    The bivariate Archimedean copulas are defined by:

    .. math::

        C(u_1, u_2; \theta) = \varphi^{-1}(\varphi(u_1; \theta) + \varphi(u_2; \theta); \theta)

    where :math:`\varphi` is the generator of the copula, a continous, strictly
    decreasing and convex function from :math:`[0, 1]\times \theta` to
    :math:`[0, \infty)` such that :math:`\varphi(1; \theta)=0`. :math:`\varphi^{-1}`
    is the pseudo-inverse of the generator function defined by:

    .. math::

        \varphi^{-1}(t; \theta) = \left\{
                          \begin{array}{ll}
                          \displaystyle \varphi^{-1}(t; \theta)
                              & \text{ if } 0 \leq t \leq \varphi(0; \theta)\\
                          \displaystyle 0 & \text{ if } \varphi(0; \theta) \leq t \leq \infty
                          \end{array}
                                  \right.

    An ArchimedeanCopula object can be used only through its derived classes:

    - :class:`~openturns.AliMikhailHaqCopula`
    - :class:`~openturns.ClaytonCopula`
    - :class:`~openturns.FrankCopula`
    - :class:`~openturns.GumbelCopula`

    See also
    --------
    Distribution
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.ArchimedeanCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.ArchimedeanCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.ArchimedeanCopula___repr__(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ArchimedeanCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ArchimedeanCopula_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _model_copula.ArchimedeanCopula_computeComplementaryCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.ArchimedeanCopula_computeProbability(self, interval)

    def computeConditionalPDF(self, x, y):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.ArchimedeanCopula_computeConditionalPDF(self, x, y)

    def computeArchimedeanGenerator(self, t):
        r"""
        Compute the Archimedean generator :math:`\varphi`.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ArchimedeanCopula_computeArchimedeanGenerator(self, t)

    def computeInverseArchimedeanGenerator(self, t):
        r"""
        Compute the inverse of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
             :math:`\varphi^{-1}` the inverse of the Archimedean generator.
        """
        return _model_copula.ArchimedeanCopula_computeInverseArchimedeanGenerator(self, t)

    def computeArchimedeanGeneratorDerivative(self, t):
        r"""
        Compute the derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ArchimedeanCopula_computeArchimedeanGeneratorDerivative(self, t)

    def computeArchimedeanGeneratorSecondDerivative(self, t):
        r"""
        Compute the seconde derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The seconde derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ArchimedeanCopula_computeArchimedeanGeneratorSecondDerivative(self, t)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.ArchimedeanCopula_getMarginal(self, *args)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.ArchimedeanCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ArchimedeanCopula_hasIndependentCopula(self)

    def __init__(self, *args):
        _model_copula.ArchimedeanCopula_swiginit(self, _model_copula.new_ArchimedeanCopula(*args))

    __swig_destroy__ = _model_copula.delete_ArchimedeanCopula


_model_copula.ArchimedeanCopula_swigregister(ArchimedeanCopula)

class SklarCopula(CopulaImplementation):
    r"""
    Sklar copula.

    Available constructor:
        SklarCopula(*distribution*)

    Parameters
    ----------
    distribution : :class:`~openturns.Distribution`
        Distribution, whatever its type : UsualDistribution, ComposedDistribution,
        KernelMixture, Mixture, RandomMixture, ...).

    Notes
    -----
    The Sklar copula is obtained directly from the expression of the
    :math:`n`-dimensional distribution which cumulative distribution function is
    :math:`F` with :math:`F_i` its marginals :

    .. math::

        C(u_1, \cdots, u_n) = F(F_1^{-1}(u_1), \cdots, F_n^{-1}(u_n))

    for :math:`u_i \in [0, 1]`

    See also
    --------
    MaximumEntropyOrderStatisticsCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> R = ot.CorrelationMatrix(3)
    >>> R[0, 1] = 0.25
    >>> R[1, 2] = 0.25
    >>> copula = ot.SklarCopula(ot.Normal([1.0, 2.0, 3.0], [2.0, 3.0, 1.0], R))

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.SklarCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.SklarCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.SklarCopula___repr__(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.SklarCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.SklarCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.SklarCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.SklarCopula_computeCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.SklarCopula_computeProbability(self, interval)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.SklarCopula_computeSurvivalFunction(self, *args)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.SklarCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.SklarCopula_computeCDFGradient(self, point)

    def computeQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.SklarCopula_computeQuantile(self, prob, tail)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.SklarCopula_computeConditionalPDF(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.SklarCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.SklarCopula_computeConditionalQuantile(self, *args)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.SklarCopula_getMarginal(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.SklarCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.SklarCopula_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.SklarCopula_getStandardDistribution(self)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.SklarCopula_getParametersCollection(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.SklarCopula_setParameter(self, parameters)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.SklarCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.SklarCopula_getParameterDescription(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.SklarCopula_hasIndependentCopula(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.SklarCopula_hasEllipticalCopula(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.SklarCopula_getKendallTau(self)

    def setDistribution(self, distribution):
        """
        Set the distribution.

        Parameters
        ----------
        distribution : :class:`~openturns.Distribution`
            A distribution, whatever its type : UsualDistribution,
            ComposedDistribution, KernelMixture, Mixture, RandomMixture, ...)
            from which the copula is built.
        """
        return _model_copula.SklarCopula_setDistribution(self, distribution)

    def getDistribution(self):
        """
        Get the distribution.

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The distribution from which the copula is built.
        """
        return _model_copula.SklarCopula_getDistribution(self)

    def __init__(self, *args):
        _model_copula.SklarCopula_swiginit(self, _model_copula.new_SklarCopula(*args))

    __swig_destroy__ = _model_copula.delete_SklarCopula


_model_copula.SklarCopula_swigregister(SklarCopula)

class AliMikhailHaqCopula(ArchimedeanCopula):
    r"""
    AliMikhailHaq copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`-1 \leq \theta \leq 1`. Default is :math:`\theta=1`.

    Notes
    -----
    The AliMikhailHaq copula is a bivariate Archimedean copula defined by:

    .. math::

        C(u_1, u_2) = \frac{u_1 u_2}{1- \theta (1 - u_1)(1 - u_2)}

    for :math:`(u_1, u_2) \in [0, 1]^2`

    And its generator is:

    .. math::

        \varphi(t) = \log \left( \frac{1-\theta(1-t)}{t} \right)

    See also
    --------
    ArchimedeanCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.AliMikhailHaqCopula(0.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.AliMikhailHaqCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.AliMikhailHaqCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.AliMikhailHaqCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.AliMikhailHaqCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.AliMikhailHaqCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.AliMikhailHaqCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.AliMikhailHaqCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.AliMikhailHaqCopula_computeCDF(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.AliMikhailHaqCopula_getKendallTau(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.AliMikhailHaqCopula_getSpearmanCorrelation(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.AliMikhailHaqCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.AliMikhailHaqCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.AliMikhailHaqCopula_computeQuantile(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.AliMikhailHaqCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.AliMikhailHaqCopula_computeConditionalQuantile(self, *args)

    def computeArchimedeanGenerator(self, t):
        r"""
        Compute the Archimedean generator :math:`\varphi`.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The Archimedean generator :math:`\varphi`.
        """
        return _model_copula.AliMikhailHaqCopula_computeArchimedeanGenerator(self, t)

    def computeInverseArchimedeanGenerator(self, t):
        r"""
        Compute the inverse of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
             :math:`\varphi^{-1}` the inverse of the Archimedean generator.
        """
        return _model_copula.AliMikhailHaqCopula_computeInverseArchimedeanGenerator(self, t)

    def computeArchimedeanGeneratorDerivative(self, t):
        r"""
        Compute the derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.AliMikhailHaqCopula_computeArchimedeanGeneratorDerivative(self, t)

    def computeArchimedeanGeneratorSecondDerivative(self, t):
        r"""
        Compute the seconde derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The seconde derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.AliMikhailHaqCopula_computeArchimedeanGeneratorSecondDerivative(self, t)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.AliMikhailHaqCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.AliMikhailHaqCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.AliMikhailHaqCopula_getParameterDescription(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.AliMikhailHaqCopula_hasIndependentCopula(self)

    def setTheta(self, theta):
        r"""
        Set the parameter :math:`\theta`.

        Parameters
        ----------
        theta : float, :math:`-1 \leq \theta \leq 1`
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.AliMikhailHaqCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the parameter :math:`\theta`.

        Returns
        -------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.AliMikhailHaqCopula_getTheta(self)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.AliMikhailHaqCopula_computeEntropy(self)

    def __init__(self, *args):
        _model_copula.AliMikhailHaqCopula_swiginit(self, _model_copula.new_AliMikhailHaqCopula(*args))

    __swig_destroy__ = _model_copula.delete_AliMikhailHaqCopula


_model_copula.AliMikhailHaqCopula_swigregister(AliMikhailHaqCopula)

class AliMikhailHaqCopulaFactory(DistributionFactoryImplementation):
    r"""
    AliMikhailHaq copula factory.

    We note :math:`\Hat{\tau}_n` the Kendall-\ :math:`\tau` of the sample.

    The parameter :math:`\Hat{\theta}_n` is solution of

    .. math::

        \displaystyle \Hat{\tau}_n = \displaystyle \frac{3\theta-2}{3\theta} - \frac{2(1-\theta)^2\ln(1-\theta)}{3\theta^2}

    See also
    --------
    DistributionFactory, AliMikhailHaqCopula
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
        return _model_copula.AliMikhailHaqCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.AliMikhailHaqCopulaFactory_build(self, *args)

    def buildAsAliMikhailHaqCopula(self, *args):
        return _model_copula.AliMikhailHaqCopulaFactory_buildAsAliMikhailHaqCopula(self, *args)

    def __init__(self, *args):
        _model_copula.AliMikhailHaqCopulaFactory_swiginit(self, _model_copula.new_AliMikhailHaqCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_AliMikhailHaqCopulaFactory


_model_copula.AliMikhailHaqCopulaFactory_swigregister(AliMikhailHaqCopulaFactory)

class IndependentCopula(CopulaImplementation):
    r"""
    Independent copula.

    Parameters
    ----------
    n : int
        Dimension of the copula, :math:`n \geq 1`. Default is :math:`n=2`.

    Notes
    -----
    The Independent copula is defined by :

    .. math::

        C(u_1, \cdots, u_n) = \prod_{i=1}^n u_i

    for :math:`u_i \in [0, 1]`

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.IndependentCopula(3)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.IndependentCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.IndependentCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.IndependentCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.IndependentCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.IndependentCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.IndependentCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.IndependentCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.IndependentCopula_computeCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.IndependentCopula_computeProbability(self, interval)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.IndependentCopula_computeSurvivalFunction(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.IndependentCopula_computeEntropy(self)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _model_copula.IndependentCopula_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeBilateralConfidenceIntervalWithMarginalProbability(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Refer to :func:`computeBilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9 with marginal probability:

        >>> confInt, marginalProb = paramDist.computeBilateralConfidenceIntervalWithMarginalProbability(0.9)
        """
        return _model_copula.IndependentCopula_computeBilateralConfidenceIntervalWithMarginalProbability(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _model_copula.IndependentCopula_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.IndependentCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.IndependentCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.IndependentCopula_computeQuantile(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.IndependentCopula_getKendallTau(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.IndependentCopula_getMarginal(self, *args)

    def computeConditionalDDF(self, x, y):
        """
        Compute the conditional derivative density function of the last component.

        With respect to the other fixed components.

        Parameters
        ----------
        Xn : float
            Conditional DDF input (last component).
        Xcond : sequence of float with dimension :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        d : float
            Conditional DDF value at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computeDDF, computeConditionalCDF
        """
        return _model_copula.IndependentCopula_computeConditionalDDF(self, x, y)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.IndependentCopula_computeConditionalPDF(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.IndependentCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.IndependentCopula_computeConditionalQuantile(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.IndependentCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.IndependentCopula_getInverseIsoProbabilisticTransformation(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.IndependentCopula_isElliptical(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.IndependentCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.IndependentCopula_hasIndependentCopula(self)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.IndependentCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.IndependentCopula_getParameterDescription(self)

    def __init__(self, *args):
        _model_copula.IndependentCopula_swiginit(self, _model_copula.new_IndependentCopula(*args))

    __swig_destroy__ = _model_copula.delete_IndependentCopula


_model_copula.IndependentCopula_swigregister(IndependentCopula)

class MinCopula(CopulaImplementation):
    r"""
    MinCopula.

    Available constructor:
        MinCopula(*n=2*)

    Parameters
    ----------
    n : int
        Dimension of the copula, :math:`n \geq 1`. Default is :math:`n=2`.

    Notes
    -----
    The Min Copula is defined by:

    .. math::

        C(u_1, \cdots, u_n) = \min_{i=1, \cdots, n} u_i

    for :math:`u_i \in [0, 1]`

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.MinCopula(2)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.MinCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.MinCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.MinCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.MinCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.MinCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.MinCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.MinCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.MinCopula_computeCDF(self, *args)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.MinCopula_computeQuantile(self, *args)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.MinCopula_computeSurvivalFunction(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.MinCopula_computeEntropy(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.MinCopula_getKendallTau(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.MinCopula_getMarginal(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.MinCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.MinCopula_getInverseIsoProbabilisticTransformation(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.MinCopula_isElliptical(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.MinCopula_isContinuous(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.MinCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.MinCopula_hasIndependentCopula(self)

    def __init__(self, *args):
        _model_copula.MinCopula_swiginit(self, _model_copula.new_MinCopula(*args))

    __swig_destroy__ = _model_copula.delete_MinCopula


_model_copula.MinCopula_swigregister(MinCopula)

class NormalCopula(CopulaImplementation):
    r"""
    Normal copula.

    Available constructor:
        NormalCopula(*n=1*)

        NormalCopula(*R*)

    Parameters
    ----------
    n : int, :math:`n \geq 1`
        Dimension of the copula.
    R : :class:`~openturns.CorrelationMatrix`
        Shape matrix :math:`\mat{R}` of the copula, ie the correlation matrix of
        any normal distribution with this copula (it is not the Kendall nor the
        Spearman rank correlation matrix of the distribution).

    Notes
    -----
    The Normal copula is defined by :

    .. math::

        C(u_1, \cdots, u_n) = \Phi_{\mat{R}}^n(\Phi^{-1}(u_1), \cdots, \Phi^{-1}(u_n))

    where :math:`\Phi_{\mat{R}}^n` is the cumulative distribution function of the
    normal distribution with zero mean, unit marginal variances and correlation :math:`R`:

    .. math::

        \Phi_{\mat{R}}^n(\vect{x}) = \int_{-\infty}^{x_1} \ldots
                                       \int_{-\infty}^{x_n}
                                       \frac{1}
                                            {{(2\pi\det{\mat{R}})}^{\frac{n}{2}}}
                                     \exp \left(-\frac{\Tr{\vect{u}}\mat{R}\vect{u}}{2} \right)\di{\vect{u}}

    with :math:`\Phi` given by:

    .. math::

          \Phi(x) = \int_{-\infty}^x \frac{1}{\sqrt{2\pi}} e^{-\frac{t^2}{2}}\di{t}

    The correlation matrix :math:`\mat{R}` is linked to the Spearman correlation
    and the Kendall concordance through the following relations:      

    - From the Spearman correlation matrix:

      .. math ::

          \mat{R}_{ij} = 2 \sin \left( \frac{\pi}{6}\rho_{ij}^S \right)

      where :math:`\rho_{ij}^S = \rho^S(X_i,X_j) = \rho^P(F_{X_i}(X_i),F_{X_j}(X_j))`

    - From the Kendall concordance matrix:

      .. math::

          \mat{R}_{ij} = \sin \left( \frac{\pi}{2} \tau_{ij} \right)

      with

      .. math::

          \tau_{ij} = \tau(X_i,X_j)
                    = \Prob{(X_{i_1} - X_{i_2})(X_{j_1} - X_{j_2}) > 0} -
                      \Prob{(X_{i_1} - X_{i_2})(X_{j_1} - X_{j_2}) < 0}

      where :math:`(X_{i_1},X_{j_1}` and :math:`(X_{i_2},X_{j_2})` follow the
      distribution of :math:`(X_i,X_j)`.

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> R = ot.CorrelationMatrix(3)
    >>> R[0, 1] = 0.25
    >>> R[1, 2] = 0.25
    >>> copula = ot.NormalCopula(R)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.NormalCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.NormalCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.NormalCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.NormalCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.NormalCopula_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.NormalCopula_getSample(self, size)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.NormalCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.NormalCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.NormalCopula_computeCDF(self, *args)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.NormalCopula_computeSurvivalFunction(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.NormalCopula_computeProbability(self, interval)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.NormalCopula_computeEntropy(self)

    def getShapeMatrix(self):
        """
        Accessor to the shape matrix of the underlying copula if it is elliptical.

        Returns
        -------
        shape : :class:`~openturns.CorrelationMatrix`
            Shape matrix of the elliptical copula of a distribution.

        Notes
        -----
        This is not the Pearson correlation matrix.

        See Also
        --------
        getPearsonCorrelation
        """
        return _model_copula.NormalCopula_getShapeMatrix(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.NormalCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.NormalCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.NormalCopula_computeCDFGradient(self, point)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.NormalCopula_computeConditionalPDF(self, *args)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.NormalCopula_computeSequentialConditionalPDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.NormalCopula_computeConditionalCDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.NormalCopula_computeSequentialConditionalCDF(self, x)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.NormalCopula_computeConditionalQuantile(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.NormalCopula_computeSequentialConditionalQuantile(self, q)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.NormalCopula_getMarginal(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.NormalCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.NormalCopula_getInverseIsoProbabilisticTransformation(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.NormalCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.NormalCopula_hasIndependentCopula(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.NormalCopula_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.NormalCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.NormalCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.NormalCopula_getParameterDescription(self)

    @staticmethod
    def GetCorrelationFromSpearmanCorrelation(matrix):
        r"""
        Get the correlation matrix from the Spearman correlation matrix.

        Parameters
        ----------
        S : :class:`~openturns.CorrelationMatrix`
            Spearman correlation matrix :math:`S` of the considered random vector.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Correlation matrix :math:`\mat{R}` of the normal copula evaluated from
            the Spearman correlation matrix :math:`S`.
        """
        return _model_copula.NormalCopula_GetCorrelationFromSpearmanCorrelation(matrix)

    @staticmethod
    def GetCorrelationFromKendallCorrelation(matrix):
        r"""
        Get the correlation matrix from the Kendall correlation matrix.

        Parameters
        ----------
        K : :class:`~openturns.CorrelationMatrix`
            Kendall correlation matrix of the considered random vector.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Correlation matrix :math:`\mat{R}` of the normal copula evaluated from
            the Kendall correlation matrix :math:`K`.
        """
        return _model_copula.NormalCopula_GetCorrelationFromKendallCorrelation(matrix)

    def __init__(self, *args):
        _model_copula.NormalCopula_swiginit(self, _model_copula.new_NormalCopula(*args))

    __swig_destroy__ = _model_copula.delete_NormalCopula


_model_copula.NormalCopula_swigregister(NormalCopula)

def NormalCopula_GetCorrelationFromSpearmanCorrelation(matrix):
    r"""
    Get the correlation matrix from the Spearman correlation matrix.

    Parameters
    ----------
    S : :class:`~openturns.CorrelationMatrix`
        Spearman correlation matrix :math:`S` of the considered random vector.

    Returns
    -------
    R : :class:`~openturns.CorrelationMatrix`
        Correlation matrix :math:`\mat{R}` of the normal copula evaluated from
        the Spearman correlation matrix :math:`S`.
    """
    return _model_copula.NormalCopula_GetCorrelationFromSpearmanCorrelation(matrix)


def NormalCopula_GetCorrelationFromKendallCorrelation(matrix):
    r"""
    Get the correlation matrix from the Kendall correlation matrix.

    Parameters
    ----------
    K : :class:`~openturns.CorrelationMatrix`
        Kendall correlation matrix of the considered random vector.

    Returns
    -------
    R : :class:`~openturns.CorrelationMatrix`
        Correlation matrix :math:`\mat{R}` of the normal copula evaluated from
        the Kendall correlation matrix :math:`K`.
    """
    return _model_copula.NormalCopula_GetCorrelationFromKendallCorrelation(matrix)


class NormalCopulaFactory(DistributionFactoryImplementation):
    r"""
    Normal Copula factory.

    We note :math:`\Hat{\tau}_n` the Kendall-\ :math:`\tau` of the sample.

    The correlation matrix :math:`\mat{R}` is estimated by:

    .. math::

        R_{ij} = sin(\frac{\pi}{2}\Hat{\tau}_{n,ij})_{\strut}

    See also
    --------
    DistributionFactory, NormalCopula
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
        return _model_copula.NormalCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.NormalCopulaFactory_build(self, *args)

    def buildAsNormalCopula(self, *args):
        return _model_copula.NormalCopulaFactory_buildAsNormalCopula(self, *args)

    def __init__(self, *args):
        _model_copula.NormalCopulaFactory_swiginit(self, _model_copula.new_NormalCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_NormalCopulaFactory


_model_copula.NormalCopulaFactory_swigregister(NormalCopulaFactory)

class FarlieGumbelMorgensternCopula(CopulaImplementation):
    r"""
    FarlieGumbelMorgenstern copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`-1 \leq \theta \leq 1`. Default is :math:`\theta=1`.

    Notes
    -----
    The FarlieGumbelMorgenstern copula is defined by :

    .. math::

        C(u_1, u_2) = u_1 u_2 (1- \theta (1 - u_1)(1 - u_2))

    for :math:`(u_1, u_2) \in [0, 1]^2`

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.FarlieGumbelMorgensternCopula(0.7)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.FarlieGumbelMorgensternCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.FarlieGumbelMorgensternCopula___repr__(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeCDF(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeCDFGradient(self, point)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeConditionalQuantile(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getParameterDescription(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.FarlieGumbelMorgensternCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.FarlieGumbelMorgensternCopula_hasIndependentCopula(self)

    def setTheta(self, theta):
        return _model_copula.FarlieGumbelMorgensternCopula_setTheta(self, theta)

    def getTheta(self):
        return _model_copula.FarlieGumbelMorgensternCopula_getTheta(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.FarlieGumbelMorgensternCopula_getMarginal(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.FarlieGumbelMorgensternCopula_computeEntropy(self)

    def __init__(self, *args):
        _model_copula.FarlieGumbelMorgensternCopula_swiginit(self, _model_copula.new_FarlieGumbelMorgensternCopula(*args))

    __swig_destroy__ = _model_copula.delete_FarlieGumbelMorgensternCopula


_model_copula.FarlieGumbelMorgensternCopula_swigregister(FarlieGumbelMorgensternCopula)

class FarlieGumbelMorgensternCopulaFactory(DistributionFactoryImplementation):
    r"""
    Farlie Gumbel Morgenstern Copula factory.

    We note :math:`\Hat{\tau}_n` the Kendall-\ :math:`\tau` of the sample
    and :math:`\Hat{\rho}_n` its Spearman correlation coefficient.

    We use the following estimators:

    .. math::

        \Hat{\theta}_n = \displaystyle \frac{9}{2}\Hat{\tau}_n^{\strut}` 

    if :math:`|\Hat{\theta}_n|<1`.

    Otherwise

    .. math::

        \Hat{\theta}_n = \displaystyle 3\Hat{\rho}_n^{\strut}`

    if :math:`|\Hat{\theta}_n|<1`.

    Otherwise, the estimation is not possible.

    See also
    --------
    DistributionFactory, FarlieGumbelMorgensternCopula
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
        return _model_copula.FarlieGumbelMorgensternCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.FarlieGumbelMorgensternCopulaFactory_build(self, *args)

    def buildAsFarlieGumbelMorgensternCopula(self, *args):
        return _model_copula.FarlieGumbelMorgensternCopulaFactory_buildAsFarlieGumbelMorgensternCopula(self, *args)

    def __init__(self, *args):
        _model_copula.FarlieGumbelMorgensternCopulaFactory_swiginit(self, _model_copula.new_FarlieGumbelMorgensternCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_FarlieGumbelMorgensternCopulaFactory


_model_copula.FarlieGumbelMorgensternCopulaFactory_swigregister(FarlieGumbelMorgensternCopulaFactory)

class FrankCopula(ArchimedeanCopula):
    r"""
    Frank copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`\theta \in \Rset`. Default is :math:`\theta=2`.

    Notes
    -----
    The Frank copula is a bivariate symmetric Archimedean copula defined by:

    .. math::

        C(u_1, u_2) = -\frac{1}{\theta}
                      log \left( 1 +
                                 \frac{(e^{-\theta u_1} - 1)(e^{-\theta u_2} - 1)}
                                      {e^{-\theta} - 1}
                          \right)

    for :math:`(u_1, u_2) \in [0, 1]^2`

    And its generator is:

    .. math::

        \varphi(t) = -\log \left( \frac{e^{-\theta t}-1}{e^{-\theta}-1} \right)

    See also
    --------
    ArchimedeanCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.FrankCopula(2.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.FrankCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.FrankCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.FrankCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.FrankCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.FrankCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FrankCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FrankCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.FrankCopula_computeCDF(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.FrankCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.FrankCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.FrankCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.FrankCopula_computeQuantile(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.FrankCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.FrankCopula_computeConditionalQuantile(self, *args)

    def computeArchimedeanGenerator(self, t):
        r"""
        Compute the Archimedean generator :math:`\varphi`.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The Archimedean generator :math:`\varphi`.
        """
        return _model_copula.FrankCopula_computeArchimedeanGenerator(self, t)

    def computeInverseArchimedeanGenerator(self, t):
        r"""
        Compute the inverse of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
             :math:`\varphi^{-1}` the inverse of the Archimedean generator.
        """
        return _model_copula.FrankCopula_computeInverseArchimedeanGenerator(self, t)

    def computeArchimedeanGeneratorDerivative(self, t):
        r"""
        Compute the derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.FrankCopula_computeArchimedeanGeneratorDerivative(self, t)

    def computeArchimedeanGeneratorSecondDerivative(self, t):
        r"""
        Compute the seconde derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The seconde derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.FrankCopula_computeArchimedeanGeneratorSecondDerivative(self, t)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.FrankCopula_hasIndependentCopula(self)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.FrankCopula_computeEntropy(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.FrankCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.FrankCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.FrankCopula_getParameterDescription(self)

    def setTheta(self, theta):
        r"""
        Set the parameter :math:`\theta`.

        Parameters
        ----------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.FrankCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the parameter :math:`\theta`.

        Returns
        -------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.FrankCopula_getTheta(self)

    def __init__(self, *args):
        _model_copula.FrankCopula_swiginit(self, _model_copula.new_FrankCopula(*args))

    __swig_destroy__ = _model_copula.delete_FrankCopula


_model_copula.FrankCopula_swigregister(FrankCopula)

class FrankCopulaFactory(DistributionFactoryImplementation):
    r"""
    Frank Copula factory.

    The paramters are estimated using the follwing equations:

    :math:`\Hat{\theta}_n` is solution of

    .. math::

        \displaystyle \Hat{\tau}_n = 1-4\left( \frac{1-D(\Hat{\theta}_n, 1)^{\strut}}{\theta} \right)

    where :math:`D` is the Debye function defined as

    .. math::

        \displaystyle D(x, n)=\frac{n}{x^n}\int_0^x \frac{t^n}{e^t-1_{\strut}} dt

    See also
    --------
    DistributionFactory, FrankCopula
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
        return _model_copula.FrankCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.FrankCopulaFactory_build(self, *args)

    def buildAsFrankCopula(self, *args):
        return _model_copula.FrankCopulaFactory_buildAsFrankCopula(self, *args)

    def __init__(self, *args):
        _model_copula.FrankCopulaFactory_swiginit(self, _model_copula.new_FrankCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_FrankCopulaFactory


_model_copula.FrankCopulaFactory_swigregister(FrankCopulaFactory)

class ClaytonCopula(ArchimedeanCopula):
    r"""
    Clayton copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`\theta \geq -1`. Default is :math:`\theta=2`.

    Notes
    -----
    The Clayton copula is a bivariate asymmmetric Archimedean copula, exhibiting
    greater dependence in the negative tail than in the positive. It is defined by:

    .. math::

        C(u_1, u_2) = (u_1^{-\theta} + u_2^{-\theta} - 1)^{-1/\theta}

    for :math:`(u_1, u_2) \in [0, 1]^2`

    And its generator is:

    .. math::

        \varphi(t) = \frac{1}{\theta} (t^{-\theta} - 1)

    The support of the copula is :math:`\{ (u,v)\in [0,1]^2, u^{-\theta} +  v^{-\theta} \geq 1 \}`. 

    If :math:`\theta <0`, the support is strictly included in :math:`[0,1]^2` and the frontier defined by :math:`\{ (u,v)\in [0,1]^2, u^{-\theta} +  v^{-\theta} = 1 \}` has a mass not equal to zero. In that case, the copula is a non strict archimedean copula.

    See also
    --------
    ArchimedeanCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.ClaytonCopula(2.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.ClaytonCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.ClaytonCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.ClaytonCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.ClaytonCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.ClaytonCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ClaytonCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ClaytonCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ClaytonCopula_computeCDF(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.ClaytonCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ClaytonCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ClaytonCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.ClaytonCopula_computeQuantile(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.ClaytonCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.ClaytonCopula_computeConditionalQuantile(self, *args)

    def computeArchimedeanGenerator(self, t):
        r"""
        Compute the Archimedean generator :math:`\varphi`.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ClaytonCopula_computeArchimedeanGenerator(self, t)

    def computeInverseArchimedeanGenerator(self, t):
        r"""
        Compute the inverse of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
             :math:`\varphi^{-1}` the inverse of the Archimedean generator.
        """
        return _model_copula.ClaytonCopula_computeInverseArchimedeanGenerator(self, t)

    def computeArchimedeanGeneratorDerivative(self, t):
        r"""
        Compute the derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ClaytonCopula_computeArchimedeanGeneratorDerivative(self, t)

    def computeArchimedeanGeneratorSecondDerivative(self, t):
        r"""
        Compute the seconde derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The seconde derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.ClaytonCopula_computeArchimedeanGeneratorSecondDerivative(self, t)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.ClaytonCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.ClaytonCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.ClaytonCopula_getParameterDescription(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ClaytonCopula_hasIndependentCopula(self)

    def setTheta(self, theta):
        r"""
        Set the parameter :math:`\theta`.

        Parameters
        ----------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.ClaytonCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the parameter :math:`\theta`.

        Returns
        -------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.ClaytonCopula_getTheta(self)

    def __init__(self, *args):
        _model_copula.ClaytonCopula_swiginit(self, _model_copula.new_ClaytonCopula(*args))

    __swig_destroy__ = _model_copula.delete_ClaytonCopula


_model_copula.ClaytonCopula_swigregister(ClaytonCopula)

class ClaytonCopulaFactory(DistributionFactoryImplementation):
    r"""
    Clayton Copula factory.

    We use the following estimator:

    .. math::

        \displaystyle\Hat{\theta}_n=\frac{2\Hat{\tau}_n^{\strut}}{1_{\strut} - \Hat{\tau}_n}

    See also
    --------
    DistributionFactory, ClaytonCopula
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
        return _model_copula.ClaytonCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.ClaytonCopulaFactory_build(self, *args)

    def buildAsClaytonCopula(self, *args):
        return _model_copula.ClaytonCopulaFactory_buildAsClaytonCopula(self, *args)

    def __init__(self, *args):
        _model_copula.ClaytonCopulaFactory_swiginit(self, _model_copula.new_ClaytonCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_ClaytonCopulaFactory


_model_copula.ClaytonCopulaFactory_swigregister(ClaytonCopulaFactory)

class GumbelCopula(ArchimedeanCopula):
    r"""
    Gumbel copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`\theta \geq 1`. Default is :math:`\theta=2`.

    Notes
    -----
    The Gumbel copula is a bivariate asymmetric Archimedean copula, exhibiting
    greater dependence in the positive tail than in the negative. It is defined by:

    .. math::

        C(u_1, u_2) = \exp(-((-log(u_1))^{\theta} + (-log(u_2))^{\theta}))^{1/\theta})

    for :math:`(u_1, u_2) \in [0, 1]^2`

    And its generator is:

    .. math::

        \varphi(t) = (-\log(t))^{\theta}

    See also
    --------
    ArchimedeanCopula

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.GumbelCopula(2.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.GumbelCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.GumbelCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.GumbelCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.GumbelCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.GumbelCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.GumbelCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.GumbelCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.GumbelCopula_computeCDF(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.GumbelCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.GumbelCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.GumbelCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.GumbelCopula_computeQuantile(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.GumbelCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.GumbelCopula_computeConditionalQuantile(self, *args)

    def computeArchimedeanGenerator(self, t):
        r"""
        Compute the Archimedean generator :math:`\varphi`.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The Archimedean generator :math:`\varphi`.
        """
        return _model_copula.GumbelCopula_computeArchimedeanGenerator(self, t)

    def computeInverseArchimedeanGenerator(self, t):
        r"""
        Compute the inverse of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
             :math:`\varphi^{-1}` the inverse of the Archimedean generator.
        """
        return _model_copula.GumbelCopula_computeInverseArchimedeanGenerator(self, t)

    def computeArchimedeanGeneratorDerivative(self, t):
        r"""
        Compute the derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.GumbelCopula_computeArchimedeanGeneratorDerivative(self, t)

    def computeArchimedeanGeneratorSecondDerivative(self, t):
        r"""
        Compute the seconde derivative of the Archimedean generator.

        Parameters
        ----------
        t : float

        Returns
        -------
        result : float
            The seconde derivative of the Archimedean generator :math:`\varphi`.
        """
        return _model_copula.GumbelCopula_computeArchimedeanGeneratorSecondDerivative(self, t)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.GumbelCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.GumbelCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.GumbelCopula_getParameterDescription(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.GumbelCopula_hasIndependentCopula(self)

    def setTheta(self, theta):
        r"""
        Set the parameter :math:`\theta`.

        Parameters
        ----------
        theta : float, :math:`\theta \geq 1`
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.GumbelCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the parameter :math:`\theta`.

        Returns
        -------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.GumbelCopula_getTheta(self)

    def __init__(self, *args):
        _model_copula.GumbelCopula_swiginit(self, _model_copula.new_GumbelCopula(*args))

    __swig_destroy__ = _model_copula.delete_GumbelCopula


_model_copula.GumbelCopula_swigregister(GumbelCopula)

class GumbelCopulaFactory(DistributionFactoryImplementation):
    r"""
    Gumbel Copula factory.

    We note :math:`\Hat{\tau}_n` the Kendall-\ :math:`\tau` of the sample.

    We use the following estimator:

    .. math::
        :nowrap:

        \begin{eqnarray*}
          \displaystyle \Hat{\theta}_n=\frac{1^{\strut}}{1 - \Hat{\tau}_{n_{\strut}}}
        \end{eqnarray*}

    See also
    --------
    DistributionFactory, GumbelCopula
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
        return _model_copula.GumbelCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.GumbelCopulaFactory_build(self, *args)

    def buildAsGumbelCopula(self, *args):
        return _model_copula.GumbelCopulaFactory_buildAsGumbelCopula(self, *args)

    def __init__(self, *args):
        _model_copula.GumbelCopulaFactory_swiginit(self, _model_copula.new_GumbelCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_GumbelCopulaFactory


_model_copula.GumbelCopulaFactory_swigregister(GumbelCopulaFactory)

class ComposedDistribution(DistributionImplementation):
    r"""
    Composed distribution.

    Available constructors:
        ComposedDistribution(*distributions, copula=ot.IndependentCopula(n)*)

    Parameters
    ----------
    distributions : list of :class:`~openturns.Distribution`
        List of :math:`n` marginals of the distribution. Each marginal must be of
        dimension 1.
    copula : :class:`~openturns.Distribution`
        A copula. If not mentioned, the copula is set to an
        :class:`~openturns.IndependentCopula` with the same dimension as
        *distributions*.

    Notes
    -----
    A ComposedDistribution is a :math:`n`-dimensional distribution which can be
    written in terms of 1-d marginal distribution functions and a copula :math:`C`
    which describes the dependence structure between the variables.
    Its cumulative distribution function :math:`F` is defined by its marginal
    distributions :math:`F_i` and the copula :math:`C` through the relation:

    .. math::

        F(x_1, \cdots, x_n) = C(F_1(x_1), \cdots, F_n(x_n))

    See also
    --------
    SklarCopula

    Examples
    --------
    >>> import openturns as ot
    >>> copula = ot.GumbelCopula(2.0)
    >>> marginals = [ot.Uniform(1.0, 2.0), ot.Normal(2.0, 3.0)]
    >>> distribution = ot.ComposedDistribution(marginals, copula)

    Draw a sample:

    >>> sample = distribution.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.ComposedDistribution_getClassName(self)

    def __eq__(self, other):
        return _model_copula.ComposedDistribution___eq__(self, other)

    def __repr__(self):
        return _model_copula.ComposedDistribution___repr__(self)

    def __str__(self, *args):
        return _model_copula.ComposedDistribution___str__(self, *args)

    def setDistributionCollection(self, coll):
        """
        Set the marginals of the distribution.

        Parameters
        ----------
        distributions : list of :class:`~openturns.Distribution`
            List of the marginals of the distribution.
        """
        return _model_copula.ComposedDistribution_setDistributionCollection(self, coll)

    def getDistributionCollection(self):
        """
        Get the marginals of the distribution.

        Returns
        -------
        distributions : list of :class:`~openturns.Distribution`
            List of the marginals of the distribution.
        """
        return _model_copula.ComposedDistribution_getDistributionCollection(self)

    def setCopula(self, copula):
        """
        Set the copula of the distribution.

        Parameters
        ----------
        copula : :class:`~openturns.Distribution`
            Copula of the distribution.
        """
        return _model_copula.ComposedDistribution_setCopula(self, copula)

    def getCopula(self):
        """
        Accessor to the copula of the distribution.

        Returns
        -------
        C : :class:`~openturns.Distribution`
            Copula of the distribution.

        See Also
        --------
        ComposedDistribution
        """
        return _model_copula.ComposedDistribution_getCopula(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.ComposedDistribution_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.ComposedDistribution_getSample(self, size)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedDistribution_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedDistribution_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedDistribution_computeCDF(self, *args)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.ComposedDistribution_computeSurvivalFunction(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.ComposedDistribution_computeProbability(self, interval)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ComposedDistribution_computePDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ComposedDistribution_computeCDFGradient(self, *args)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.ComposedDistribution_computeQuantile(self, *args)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.ComposedDistribution_computeConditionalPDF(self, *args)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.ComposedDistribution_computeSequentialConditionalPDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.ComposedDistribution_computeConditionalCDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.ComposedDistribution_computeSequentialConditionalCDF(self, x)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.ComposedDistribution_computeConditionalQuantile(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.ComposedDistribution_computeSequentialConditionalQuantile(self, q)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.ComposedDistribution_computeEntropy(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.ComposedDistribution_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.ComposedDistribution_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.ComposedDistribution_getKurtosis(self)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.ComposedDistribution_getMarginal(self, *args)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.ComposedDistribution_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.ComposedDistribution_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.ComposedDistribution_getStandardDistribution(self)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.ComposedDistribution_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.ComposedDistribution_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.ComposedDistribution_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.ComposedDistribution_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.ComposedDistribution_getParameterDescription(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ComposedDistribution_hasIndependentCopula(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.ComposedDistribution_hasEllipticalCopula(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.ComposedDistribution_isElliptical(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ComposedDistribution_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ComposedDistribution_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ComposedDistribution_isIntegral(self)

    def __init__(self, *args):
        _model_copula.ComposedDistribution_swiginit(self, _model_copula.new_ComposedDistribution(*args))

    __swig_destroy__ = _model_copula.delete_ComposedDistribution


_model_copula.ComposedDistribution_swigregister(ComposedDistribution)

class CumulativeDistributionNetwork(DistributionImplementation):
    r"""
    Composed distribution.

    Parameters
    ----------
    distributions : list of :class:`~openturns.Distribution`
        List of :math:`n` distributions associated to the red nodes of a bipartite graph.
    graph : :class:`~openturns.BipartiteGraph`
        A bipartite graph. It must have :math:`n` red nodes, and the red node :math:`i` must have a clique of size the dimension of the :math:`i` th distribution.

    Notes
    -----
    A cumulative distribution network (CDN) is a :math:`p`-dimensional distribution which cumulative distribution function is given as a product of lower dimensional cumulative distribution functions:

    .. math::

        F(x_1, \cdots, x_p) = \prod_{i=1}^n(F_i(\vect{x}_i))

    Where :math:`\vect{x}_i` is the vector :math:`(x_{j}, j\in J_i)`, :math:`J_i` being the clique of black nodes linked to the red node :math:`i`.

    The dimension :math:`p` is the cardinal of the union of the cliques, ie the number of black nodes in the bipartite graph.

    Examples
    --------
    >>> import openturns as ot
    >>> graph = ot.BipartiteGraph([[0, 1], [1, 2], [2, 0]])
    >>> distribution = ot.CumulativeDistributionNetwork([ot.Normal(2)]*3, graph)

    Compute the CDF:

    >>> print('%.6f' % distribution.computeCDF([1.0, 2.0, -0.5]))
    0.064354
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.CumulativeDistributionNetwork_getClassName(self)

    def __eq__(self, other):
        return _model_copula.CumulativeDistributionNetwork___eq__(self, other)

    def __repr__(self):
        return _model_copula.CumulativeDistributionNetwork___repr__(self)

    def __str__(self, *args):
        return _model_copula.CumulativeDistributionNetwork___str__(self, *args)

    def setDistributionCollection(self, coll):
        """
        Set the distributions defining the CDN.

        Parameters
        ----------
        distributions : list of :class:`~openturns.Distribution`
            List of the distributions in the CDN.
        """
        return _model_copula.CumulativeDistributionNetwork_setDistributionCollection(self, coll)

    def getDistributionCollection(self):
        """
        Get the distributions defining the CDN.

        Returns
        -------
        distributions : list of :class:`~openturns.Distribution`
            List of the distributions in the CDN.
        """
        return _model_copula.CumulativeDistributionNetwork_getDistributionCollection(self)

    def setGraph(self, graph):
        """
        Set the bipartite graph defining the CDN.

        Parameters
        ----------
        graph : a :class:`~openturns.BipartiteGraph`
            The bipartite graph defining the CDN.
        """
        return _model_copula.CumulativeDistributionNetwork_setGraph(self, graph)

    def getGraph(self):
        """
        Get the bipartite graph defining the CDN.

        Returns
        -------
        graph : a :class:`~openturns.BipartiteGraph`
            The bipartite graph defining the CDN.
        """
        return _model_copula.CumulativeDistributionNetwork_getGraph(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.CumulativeDistributionNetwork_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.CumulativeDistributionNetwork_getSample(self, size)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.CumulativeDistributionNetwork_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.CumulativeDistributionNetwork_computeCDF(self, *args)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.CumulativeDistributionNetwork_getMarginal(self, *args)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.CumulativeDistributionNetwork_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.CumulativeDistributionNetwork_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.CumulativeDistributionNetwork_isIntegral(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.CumulativeDistributionNetwork_hasIndependentCopula(self)

    def __init__(self, *args):
        _model_copula.CumulativeDistributionNetwork_swiginit(self, _model_copula.new_CumulativeDistributionNetwork(*args))

    __swig_destroy__ = _model_copula.delete_CumulativeDistributionNetwork


_model_copula.CumulativeDistributionNetwork_swigregister(CumulativeDistributionNetwork)

class ComposedCopula(CopulaImplementation):
    r"""
    Merge of a collection of independent copulas.

    Parameters
    ----------
    copulas : list of copulas.
        The collection of copulas to be merged.

    Notes
    -----
    Let's :math:`(C_1\, \dots, C_K)` a collection of :math:`K` copulas respectively defined on :math:`[0,1]^{n_i}` with :math:`n_1 + \dots + n_K = d`.

    The  merged copula :math:`C` is defined on :math:`[0,1]^d` by:

    .. math::

        C(u_1, \dots, u_d) = C_1(u_1, \dots, u_{n_1}) C_2(u_{n_1+1}, \dots, u_{n_2}) \dots C_K(u_{n_1+\dots + n_{K-1}+1}, \dots, u_d) 

    It means that the  subvectors :math:`(u_{n_{i-1}+1}, \dots, u_{n_i})_i` are independent.

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> R = ot.CorrelationMatrix(3)
    >>> R[0, 1] = 0.5
    >>> R[0, 2] = 0.25
    >>> collection = [ot.FrankCopula(3.0), ot.NormalCopula(R), ot.ClaytonCopula(2.0)]
    >>> copula = ot.ComposedCopula(collection)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.ComposedCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.ComposedCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.ComposedCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.ComposedCopula___str__(self, *args)

    def setCopulaCollection(self, coll):
        """
        Accessor to the list of the copulas.

        Parameters
        ----------
        copulas : list of copulas
            The collection of copulas to be merged.
        """
        return _model_copula.ComposedCopula_setCopulaCollection(self, coll)

    def getCopulaCollection(self):
        """
        Accessor to the list of the copulas.

        Returns
        -------
        copulas : list of copulas
            The collection of the copulas to be merged.
        """
        return _model_copula.ComposedCopula_getCopulaCollection(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.ComposedCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedCopula_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _model_copula.ComposedCopula_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.ComposedCopula_computeCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.ComposedCopula_computeProbability(self, interval)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.ComposedCopula_computeSurvivalFunction(self, *args)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.ComposedCopula_getKendallTau(self)

    def getShapeMatrix(self):
        """
        Accessor to the shape matrix of the underlying copula if it is elliptical.

        Returns
        -------
        shape : :class:`~openturns.CorrelationMatrix`
            Shape matrix of the elliptical copula of a distribution.

        Notes
        -----
        This is not the Pearson correlation matrix.

        See Also
        --------
        getPearsonCorrelation
        """
        return _model_copula.ComposedCopula_getShapeMatrix(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ComposedCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.ComposedCopula_computeCDFGradient(self, point)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.ComposedCopula_getMarginal(self, *args)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.ComposedCopula_computeConditionalPDF(self, *args)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.ComposedCopula_computeSequentialConditionalPDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.ComposedCopula_computeConditionalCDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.ComposedCopula_computeSequentialConditionalCDF(self, x)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.ComposedCopula_computeConditionalQuantile(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.ComposedCopula_computeSequentialConditionalQuantile(self, q)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.ComposedCopula_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.ComposedCopula_setParametersCollection(self, *args)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.ComposedCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.ComposedCopula_hasIndependentCopula(self)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.ComposedCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.ComposedCopula_getInverseIsoProbabilisticTransformation(self)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.ComposedCopula_computeEntropy(self)

    def __init__(self, *args):
        _model_copula.ComposedCopula_swiginit(self, _model_copula.new_ComposedCopula(*args))

    __swig_destroy__ = _model_copula.delete_ComposedCopula


_model_copula.ComposedCopula_swigregister(ComposedCopula)

class MarshallOlkinCopula(CopulaImplementation):
    r"""
    MarshallOlkin copula.

    Parameters
    ----------
    alpha : float
        Parameter :math:`\alpha`, :math:`0 \leq \alpha \leq 1`. Default is :math:`\alpha=0.5`.

    beta : float
        Parameter :math:`\beta`, :math:`0 \leq \beta \leq 1`. Default is :math:`\beta=0.5`.

    Notes
    -----
    The MarshallOlkin copula is a bivariate copula defined by:

    .. math::

        C(u_1, u_2) = 
        \begin{cases}
        u_1^{1-\alpha} u_2, \textrm{ if } u_1^{1-\alpha} \geq u_2^{1-\beta} \\
        u_1 u_2^{1-\beta}, \textrm{ otherwise.}
        \end{cases}

    for :math:`(u_1, u_2) \in [0, 1]^2`. 

    This copula is also known as the generalized Cuadras-Auge copula. 

    Independence corresponds to :math:`\alpha = 0` or :math:`\beta = 0`.

    The minimum copula corresponds to :math:`\alpha = \beta = 1`.

    More details on this copula can be found in [nelsen2006]_, 
    chapter 3, section 3.1.1, page 52.

    Examples
    --------
    Create a Marshall-Olkin copula with default parameters:

    >>> import openturns as ot
    >>> copula = ot.MarshallOlkinCopula()

    Create a Marshall-Olkin copula:

    >>> import openturns as ot
    >>> copula = ot.MarshallOlkinCopula(0.3,0.7)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.MarshallOlkinCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.MarshallOlkinCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.MarshallOlkinCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.MarshallOlkinCopula___str__(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.MarshallOlkinCopula_computeCDF(self, *args)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.MarshallOlkinCopula_hasIndependentCopula(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.MarshallOlkinCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.MarshallOlkinCopula_getParameter(self)

    def setAlpha(self, alpha):
        r"""
        Set the parameter :math:`\alpha`.

        Parameters
        ----------
        alpha : float, :math:`0 \leq \alpha \leq 1`
            Parameter :math:`\alpha` of the copula.
        """
        return _model_copula.MarshallOlkinCopula_setAlpha(self, alpha)

    def getAlpha(self):
        r"""
        Get the parameter :math:`\alpha`.

        Returns
        -------
        alpha : float
            Parameter :math:`\alpha` of the copula.
        """
        return _model_copula.MarshallOlkinCopula_getAlpha(self)

    def setBeta(self, beta):
        r"""
        Set the parameter :math:`\beta`.

        Parameters
        ----------
        beta : float, :math:`0 \leq \beta \leq 1`
            Parameter :math:`\beta` of the copula.
        """
        return _model_copula.MarshallOlkinCopula_setBeta(self, beta)

    def getBeta(self):
        r"""
        Get the parameter :math:`\beta`.

        Returns
        -------
        beta : float
            Parameter :math:`\beta` of the copula.
        """
        return _model_copula.MarshallOlkinCopula_getBeta(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.MarshallOlkinCopula_getKendallTau(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.MarshallOlkinCopula_getSpearmanCorrelation(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.MarshallOlkinCopula_getRealization(self)

    def __init__(self, *args):
        _model_copula.MarshallOlkinCopula_swiginit(self, _model_copula.new_MarshallOlkinCopula(*args))

    __swig_destroy__ = _model_copula.delete_MarshallOlkinCopula


_model_copula.MarshallOlkinCopula_swigregister(MarshallOlkinCopula)

class OrdinalSumCopula(CopulaImplementation):
    r"""
    Copula built as an ordinal sum of copulas.

    Parameters
    ----------
    collCopula : list of :class:`~openturns.Distribution`
        The collection :math:`(C_1, \dots, C_n)` of :math:`n` copulas of dimension :math:`d`.

    bounds : sequence of float, of size :math:`n-1` and :math:`0 \leq \alpha_1 \leq \dots \leq \alpha_{n-1} \leq 1`
        The bounds :math:`\alpha_i` are such that the copula :math:`C_i` is
        squeezed into :math:`[\alpha_i, \alpha_{i+1}]`.

    Notes
    -----
    The ordinal sum of the :math:`n` copulas :math:`(C_1, \dots, C_n)`, each one
    being squeezed into the interval :math:`[\alpha_i, \alpha_{i+1}], i=1 \dots n-1`,
    writes:

    .. math::

        C(\vect{u}) = \left\{
        \begin{array}{ll}
           \alpha_i+C_i \left( \dfrac{u_1-\alpha_i}{\alpha_{i+1} - \alpha_i}, \dot,  \dfrac{u_d-\alpha_i}{\alpha_{i+1} - \alpha_i} \right)
               & \mbox{ if } \vect{u} \in [\alpha_i, \alpha_{i+1}[^d \\
           M_d(\vect{u}) & \mbox{ else }
        \end{array}
        \right.

    with :math:`M_d` the Min-copula: :math:`M_d(\vect{u}) = \min_{k=1 \dots d} u_k`
    and where, for convenience, we noted :math:`\alpha_0=0` and :math:`\alpha_n=1`.

    Note that if  :math:`\alpha_i=\alpha_{i+1}` then the copula :math:`C_{i+1}` is
    erased from the list, for :math:`i=0 \dots n-1`.

    See also
    --------
    Distribution

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> ordinalSumCop = ot.OrdinalSumCopula([ot.GumbelCopula(2), ot.NormalCopula(2)], [0.3])
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.OrdinalSumCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.OrdinalSumCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.OrdinalSumCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.OrdinalSumCopula___str__(self, *args)

    def setCopulaCollection(self, coll):
        """
        Accessor to the collection of copulas.

        Parameters
        ----------
        copColl : list of :class:`~openturns.Distribution` with the same dimension
            List of copulas that build the ordinal sum.
        """
        return _model_copula.OrdinalSumCopula_setCopulaCollection(self, coll)

    def getCopulaCollection(self):
        """
        Accessor to the collection of copulas.

        Returns
        -------
        copColl : list of :class:`~openturns.Distribution` with the same dimension
            List of copulas that build the ordinal sum.
        """
        return _model_copula.OrdinalSumCopula_getCopulaCollection(self)

    def setBounds(self, bounds):
        """
        Accessor to the collection of bounds.

        Parameters
        ----------
        bounds : sequence of float
            Bounds defining the intervals on whch the copulas of the collection are
            squeezed.
        """
        return _model_copula.OrdinalSumCopula_setBounds(self, bounds)

    def getBounds(self):
        """
        Accessor to the collection of bounds.

        Returns
        -------
        bounds : :class:`~openturns.Point`
            Bounds defining the intervals on which the copulas of the collection are
            squeezed.
        """
        return _model_copula.OrdinalSumCopula_getBounds(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.OrdinalSumCopula_getRealization(self)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.OrdinalSumCopula_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.OrdinalSumCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.OrdinalSumCopula_computeCDF(self, *args)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.OrdinalSumCopula_computeProbability(self, interval)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.OrdinalSumCopula_getKendallTau(self)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.OrdinalSumCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.OrdinalSumCopula_computeCDFGradient(self, point)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.OrdinalSumCopula_getMarginal(self, *args)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.OrdinalSumCopula_computeConditionalPDF(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.OrdinalSumCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.OrdinalSumCopula_computeConditionalQuantile(self, *args)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.OrdinalSumCopula_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.OrdinalSumCopula_setParametersCollection(self, *args)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.OrdinalSumCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.OrdinalSumCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.OrdinalSumCopula_getParameterDescription(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.OrdinalSumCopula_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.OrdinalSumCopula_hasIndependentCopula(self)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.OrdinalSumCopula_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.OrdinalSumCopula_getInverseIsoProbabilisticTransformation(self)

    def __init__(self, *args):
        _model_copula.OrdinalSumCopula_swiginit(self, _model_copula.new_OrdinalSumCopula(*args))

    __swig_destroy__ = _model_copula.delete_OrdinalSumCopula


_model_copula.OrdinalSumCopula_swigregister(OrdinalSumCopula)

class PlackettCopula(CopulaImplementation):
    r"""
    Plackett copula.

    Parameters
    ----------
    theta : float
        Parameter :math:`\theta`, :math:`\theta \geq 0`. Default is :math:`\theta=2`.

    Notes
    -----
    The Plackett copula is a bivariate symmetric copula defined by:

    .. math::

        C(u_1, u_2) = \frac{\left[1+(\theta-1)(u_1+u_2)\right]-
                      \sqrt{\left[1+(\theta-1)(u_1+u_2)\right]^2-
                      4u_1u_2\theta(\theta-1)}}{2(\theta-1)}

    for :math:`(u_1, u_2) \in [0, 1]^2`

    This copula is the only copula with constant *odd ratio* :math:`\theta\geq 0`:

    .. math::

       \theta = \frac{\Prob{U_1\leq u_1,U_2\leq u_2}\Prob{U_1>u_1,U_2>u_2}}{\Prob{U_1\leq u_1,U_2>u_2}\Prob{U_1>u_1,U_2\leq u_2}} = \frac{C(u_1,u_2)\left[1-u_1-u_2+C(u_1,u_2)\right]}{\left[u_1-C(u_1,u_2)\right]\left[u_2-C(u_1,u_2)\right]}

    This is a *comprehensive family* of copulas as it contains:

    - the Frechet lower bound :math:`W(u_1,u_2)=\max(0,u_1+u_2-1)=\lim_{\theta\rightarrow\infty}C(u_1,u_2)`,
    - the Frechet upper bound :math:`M(u_1,u_2)=\min(u_1,u_2)=C_0(u_1,u_2)`
    - the independent copula :math:`\Pi(u_1,u_2)=u_1u_2=C_1(u_1,u_2)`.

    Examples
    --------
    Create a distribution:

    >>> import openturns as ot
    >>> copula = ot.PlackettCopula(2.5)

    Draw a sample:

    >>> sample = copula.getSample(5)
    """
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.PlackettCopula_getClassName(self)

    def __eq__(self, other):
        return _model_copula.PlackettCopula___eq__(self, other)

    def __repr__(self):
        return _model_copula.PlackettCopula___repr__(self)

    def __str__(self, *args):
        return _model_copula.PlackettCopula___str__(self, *args)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.PlackettCopula_getRealization(self)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.PlackettCopula_computePDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.PlackettCopula_computeCDF(self, *args)

    def computePDFGradient(self, point):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.PlackettCopula_computePDFGradient(self, point)

    def computeCDFGradient(self, point):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.PlackettCopula_computeCDFGradient(self, point)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.PlackettCopula_computeQuantile(self, *args)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.PlackettCopula_computeConditionalCDF(self, *args)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.PlackettCopula_computeConditionalQuantile(self, *args)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.PlackettCopula_getMarginal(self, *args)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.PlackettCopula_hasIndependentCopula(self)

    def setParameter(self, parameter):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.PlackettCopula_setParameter(self, parameter)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.PlackettCopula_getParameter(self)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.PlackettCopula_getParameterDescription(self)

    def setTheta(self, theta):
        r"""
        Set the parameter :math:`\theta`.

        Parameters
        ----------
        theta : float
            Parameter :math:`\theta\geq 0` of the copula.
        """
        return _model_copula.PlackettCopula_setTheta(self, theta)

    def getTheta(self):
        r"""
        Get the parameter :math:`\theta`.

        Returns
        -------
        theta : float
            Parameter :math:`\theta` of the copula.
        """
        return _model_copula.PlackettCopula_getTheta(self)

    def __init__(self, *args):
        _model_copula.PlackettCopula_swiginit(self, _model_copula.new_PlackettCopula(*args))

    __swig_destroy__ = _model_copula.delete_PlackettCopula


_model_copula.PlackettCopula_swigregister(PlackettCopula)

class PlackettCopulaFactory(DistributionFactoryImplementation):
    r"""
    Plackett Copula factory.

    The parameter is estimated using the follwing equation:

    :math:`\Hat{\theta}_n` is solution of

    .. math::

        \displaystyle \Hat{\tau}_n = \frac{4m_n^2}{(1-2m_n)^2}

    where :math:`m_n` is the value of the empirical CDF :math:`F_n` at the median point :math:`({U_1}_{\lceil n/2 \rceil},{U_2}_{\lceil n/2 \rceil})` of the sample :math:`({U_1}_k,{U_2}_k)_{k\in\{1,\dots,n\}}`.

    See also
    --------
    DistributionFactory, PlackettCopula
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
        return _model_copula.PlackettCopulaFactory_getClassName(self)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.PlackettCopulaFactory_build(self, *args)

    def buildAsPlackettCopula(self, *args):
        return _model_copula.PlackettCopulaFactory_buildAsPlackettCopula(self, *args)

    def __init__(self, *args):
        _model_copula.PlackettCopulaFactory_swiginit(self, _model_copula.new_PlackettCopulaFactory(*args))

    __swig_destroy__ = _model_copula.delete_PlackettCopulaFactory


_model_copula.PlackettCopulaFactory_swigregister(PlackettCopulaFactory)

class DistributionFactoryImplementationPointer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    ptr_ = property(_model_copula.DistributionFactoryImplementationPointer_ptr__get, _model_copula.DistributionFactoryImplementationPointer_ptr__set)

    def __init__(self, *args):
        _model_copula.DistributionFactoryImplementationPointer_swiginit(self, _model_copula.new_DistributionFactoryImplementationPointer(*args))

    __swig_destroy__ = _model_copula.delete_DistributionFactoryImplementationPointer

    def reset(self):
        return _model_copula.DistributionFactoryImplementationPointer_reset(self)

    def __ref__(self, *args):
        return _model_copula.DistributionFactoryImplementationPointer___ref__(self, *args)

    def __deref__(self, *args):
        return _model_copula.DistributionFactoryImplementationPointer___deref__(self, *args)

    def isNull(self):
        return _model_copula.DistributionFactoryImplementationPointer_isNull(self)

    def __nonzero__(self):
        return _model_copula.DistributionFactoryImplementationPointer___nonzero__(self)

    __bool__ = __nonzero__

    def get(self):
        return _model_copula.DistributionFactoryImplementationPointer_get(self)

    def getImplementation(self):
        return _model_copula.DistributionFactoryImplementationPointer_getImplementation(self)

    def unique(self):
        return _model_copula.DistributionFactoryImplementationPointer_unique(self)

    def use_count(self):
        return _model_copula.DistributionFactoryImplementationPointer_use_count(self)

    def swap(self, other):
        return _model_copula.DistributionFactoryImplementationPointer_swap(self, other)

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionFactoryImplementationPointer_getClassName(self)

    def __repr__(self):
        return _model_copula.DistributionFactoryImplementationPointer___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionFactoryImplementationPointer___str__(self, *args)

    def build(self, *args):
        """
        Build the distribution.

        **Available usages**:

            build(*sample*)

            build(*param*)

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        param : Collection of :class:`~openturns.PointWithDescription`
            A vector of parameters of the distribution.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The built distribution.
        """
        return _model_copula.DistributionFactoryImplementationPointer_build(self, *args)

    def buildEstimator(self, *args):
        r"""
        Build the distribution and the parameter distribution.

        Parameters
        ----------
        sample : 2-d sequence of float
            Sample from which the distribution parameters are estimated.
        parameters : :class:`~openturns.DistributionParameters`
            Optional, the parametrization.

        Returns
        -------
        resDist : :class:`~openturns.DistributionFactoryResult`
            The results.

        Notes
        -----
        According to the way the native parameters of the distribution are estimated, the parameters distribution differs:

            - Moments method: the asymptotic parameters distribution is normal and estimated by Bootstrap on the initial data;
            - Maximum likelihood method with a regular model: the asymptotic parameters distribution is normal and its covariance matrix is the inverse Fisher information matrix;
            - Other methods: the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting (see :class:`~openturns.KernelSmoothing`).

        If another set of parameters is specified, the native parameters distribution is first estimated and the new distribution is determined from it:

            - if the native parameters distribution is normal and the transformation regular at the estimated parameters values: the asymptotic parameters distribution is normal and its covariance matrix determined from the inverse Fisher information matrix of the native parameters and the transformation;
            - in the other cases, the asymptotic parameters distribution is estimated by Bootstrap on the initial data and kernel fitting.

        Examples
        --------
        Create a sample from a Beta distribution:

        >>> import openturns as ot
        >>> sample = ot.Beta().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Beta distribution in the native parameters and create a :class:`~openturns.DistributionFactory`:

        >>> fittedRes = ot.BetaFactory().buildEstimator(sample)

        Fit a Beta distribution  in the alternative parametrization :math:`(\mu, \sigma, a, b)`:

        >>> fittedRes2 = ot.BetaFactory().buildEstimator(sample, ot.BetaMuSigma())
        """
        return _model_copula.DistributionFactoryImplementationPointer_buildEstimator(self, *args)

    def getBootstrapSize(self):
        """
        Accessor to the bootstrap size.

        Returns
        -------
        size : integer
            Size of the bootstrap.
        """
        return _model_copula.DistributionFactoryImplementationPointer_getBootstrapSize(self)

    def setBootstrapSize(self, bootstrapSize):
        """
        Accessor to the bootstrap size.

        Parameters
        ----------
        size : integer
            Size of the bootstrap.
        """
        return _model_copula.DistributionFactoryImplementationPointer_setBootstrapSize(self, bootstrapSize)

    def __eq__(self, arg2):
        return _model_copula.DistributionFactoryImplementationPointer___eq__(self, arg2)

    def __ne__(self, other):
        return _model_copula.DistributionFactoryImplementationPointer___ne__(self, other)

    def getId(self):
        """
        Accessor to the object's id.

        Returns
        -------
        id : int
           Internal unique identifier.
        """
        return _model_copula.DistributionFactoryImplementationPointer_getId(self)

    def setShadowedId(self, id):
        """
        Accessor to the object's shadowed id.

        Parameters
        ----------
        id : int
            Internal unique identifier.
        """
        return _model_copula.DistributionFactoryImplementationPointer_setShadowedId(self, id)

    def getShadowedId(self):
        """
        Accessor to the object's shadowed id.

        Returns
        -------
        id : int
            Internal unique identifier.
        """
        return _model_copula.DistributionFactoryImplementationPointer_getShadowedId(self)

    def setVisibility(self, visible):
        """
        Accessor to the object's visibility state.

        Parameters
        ----------
        visible : bool
            Visibility flag.
        """
        return _model_copula.DistributionFactoryImplementationPointer_setVisibility(self, visible)

    def getVisibility(self):
        """
        Accessor to the object's visibility state.

        Returns
        -------
        visible : bool
            Visibility flag.
        """
        return _model_copula.DistributionFactoryImplementationPointer_getVisibility(self)

    def hasName(self):
        """
        Test if the object is named.

        Returns
        -------
        hasName : bool
            True if the name is not empty.
        """
        return _model_copula.DistributionFactoryImplementationPointer_hasName(self)

    def hasVisibleName(self):
        """
        Test if the object has a distinguishable name.

        Returns
        -------
        hasVisibleName : bool
            True if the name is not empty and not the default one.
        """
        return _model_copula.DistributionFactoryImplementationPointer_hasVisibleName(self)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionFactoryImplementationPointer_getName(self)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionFactoryImplementationPointer_setName(self, name)


_model_copula.DistributionFactoryImplementationPointer_swigregister(DistributionFactoryImplementationPointer)

class DistributionImplementationPointer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    ptr_ = property(_model_copula.DistributionImplementationPointer_ptr__get, _model_copula.DistributionImplementationPointer_ptr__set)

    def __init__(self, *args):
        _model_copula.DistributionImplementationPointer_swiginit(self, _model_copula.new_DistributionImplementationPointer(*args))

    __swig_destroy__ = _model_copula.delete_DistributionImplementationPointer

    def reset(self):
        return _model_copula.DistributionImplementationPointer_reset(self)

    def __ref__(self, *args):
        return _model_copula.DistributionImplementationPointer___ref__(self, *args)

    def __deref__(self, *args):
        return _model_copula.DistributionImplementationPointer___deref__(self, *args)

    def isNull(self):
        return _model_copula.DistributionImplementationPointer_isNull(self)

    def __nonzero__(self):
        return _model_copula.DistributionImplementationPointer___nonzero__(self)

    __bool__ = __nonzero__

    def get(self):
        return _model_copula.DistributionImplementationPointer_get(self)

    def getImplementation(self):
        return _model_copula.DistributionImplementationPointer_getImplementation(self)

    def unique(self):
        return _model_copula.DistributionImplementationPointer_unique(self)

    def use_count(self):
        return _model_copula.DistributionImplementationPointer_use_count(self)

    def swap(self, other):
        return _model_copula.DistributionImplementationPointer_swap(self, other)

    def getClassName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        class_name : str
            The object class name (`object.__class__.__name__`).
        """
        return _model_copula.DistributionImplementationPointer_getClassName(self)

    def __eq__(self, other):
        return _model_copula.DistributionImplementationPointer___eq__(self, other)

    def __ne__(self, other):
        return _model_copula.DistributionImplementationPointer___ne__(self, other)

    def __add__(self, *args):
        return _model_copula.DistributionImplementationPointer___add__(self, *args)

    def __sub__(self, *args):
        return _model_copula.DistributionImplementationPointer___sub__(self, *args)

    def __mul__(self, *args):
        return _model_copula.DistributionImplementationPointer___mul__(self, *args)

    def __truediv__(self, *args):
        return _model_copula.DistributionImplementationPointer___truediv__(self, *args)

    __div__ = __truediv__

    def cos(self):
        """
        Transform distribution by cosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_cos(self)

    def sin(self):
        """
        Transform distribution by sine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_sin(self)

    def tan(self):
        """
        Transform distribution by tangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_tan(self)

    def acos(self):
        """
        Transform distribution by arccosine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_acos(self)

    def asin(self):
        """
        Transform distribution by arcsine function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_asin(self)

    def atan(self):
        """
        Transform distribution by arctangent function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_atan(self)

    def cosh(self):
        """
        Transform distribution by cosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_cosh(self)

    def sinh(self):
        """
        Transform distribution by sinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_sinh(self)

    def tanh(self):
        """
        Transform distribution by tanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_tanh(self)

    def acosh(self):
        """
        Transform distribution by acosh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_acosh(self)

    def asinh(self):
        """
        Transform distribution by asinh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_asinh(self)

    def atanh(self):
        """
        Transform distribution by atanh function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_atanh(self)

    def exp(self):
        """
        Transform distribution by exponential function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_exp(self)

    def log(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_log(self)

    def ln(self):
        """
        Transform distribution by natural logarithm function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_ln(self)

    def inverse(self):
        """
        Transform distribution by inverse function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_inverse(self)

    def sqr(self):
        """
        Transform distribution by square function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_sqr(self)

    def sqrt(self):
        """
        Transform distribution by square root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_sqrt(self)

    def cbrt(self):
        """
        Transform distribution by cubic root function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_cbrt(self)

    def abs(self):
        """
        Transform distribution by absolute value function.

        Returns
        -------
        dist : :class:`~openturns.Distribution`
            The transformed distribution.
        """
        return _model_copula.DistributionImplementationPointer_abs(self)

    def __repr__(self):
        return _model_copula.DistributionImplementationPointer___repr__(self)

    def __str__(self, *args):
        return _model_copula.DistributionImplementationPointer___str__(self, *args)

    def getDimension(self):
        """
        Accessor to the dimension of the distribution.

        Returns
        -------
        n : int
            The number of components in the distribution.
        """
        return _model_copula.DistributionImplementationPointer_getDimension(self)

    def getRealization(self):
        """
        Accessor to a pseudo-random realization from the distribution.

        Refer to :ref:`distribution_realization`.

        Returns
        -------
        point : :class:`~openturns.Point`
            A pseudo-random realization of the distribution.

        See Also
        --------
        getSample, RandomGenerator
        """
        return _model_copula.DistributionImplementationPointer_getRealization(self)

    def getSample(self, size):
        """
        Accessor to a pseudo-random sample from the distribution.

        Parameters
        ----------
        size : int
            Sample size.

        Returns
        -------
        sample : :class:`~openturns.Sample`
            A pseudo-random sample of the distribution.

        See Also
        --------
        getRealization, RandomGenerator
        """
        return _model_copula.DistributionImplementationPointer_getSample(self, size)

    def computeDDF(self, *args):
        r"""
        Compute the derivative density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        d : :class:`~openturns.Point`, :class:`~openturns.Sample`
            DDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The derivative density function is the gradient of the probability density
        function with respect to :math:`\vect{x}`:

        .. math::

            \vect{\nabla}_{\vect{x}} f_{\vect{X}}(\vect{x}) =
                \Tr{\left(\frac{\partial f_{\vect{X}}(\vect{x})}{\partial x_i},
                          \quad i = 1, \ldots, n\right)},
                \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementationPointer_computeDDF(self, *args)

    def computePDF(self, *args):
        r"""
        Compute the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            PDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The probability density function is defined as follows:

        .. math::

            f_{\vect{X}}(\vect{x}) = \frac{\partial^n F_{\vect{X}}(\vect{x})}
                                          {\prod_{i=1}^n \partial x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementationPointer_computePDF(self, *args)

    def computeLogPDF(self, *args):
        """
        Compute the logarithm of the probability density function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            PDF input(s).

        Returns
        -------
        f : float, :class:`~openturns.Point`
            Logarithm of the PDF value(s) at input(s) :math:`X`.
        """
        return _model_copula.DistributionImplementationPointer_computeLogPDF(self, *args)

    def computeCDF(self, *args):
        r"""
        Compute the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            CDF input(s).

        Returns
        -------
        F : float, :class:`~openturns.Point`
            CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The cumulative distribution function is defined as:

        .. math::

            F_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^n X_i \leq x_i},
                                     \quad \vect{x} \in \supp{\vect{X}}
        """
        return _model_copula.DistributionImplementationPointer_computeCDF(self, *args)

    def computeComplementaryCDF(self, *args):
        r"""
        Compute the complementary cumulative distribution function.

        Parameters
        ----------
        X : sequence of float, 2-d sequence of float
            Complementary CDF input(s).

        Returns
        -------
        C : float, :class:`~openturns.Point`
            Complementary CDF value(s) at input(s) :math:`X`.

        Notes
        -----
        The complementary cumulative distribution function.

        .. math::

            1 - F_{\vect{X}}(\vect{x}) = 1 - \Prob{\bigcap_{i=1}^n X_i \leq x_i}, \quad \vect{x} \in \supp{\vect{X}}

        .. warning::
            This is not the survival function (except for 1-dimensional
            distributions).

        See Also
        --------
        computeSurvivalFunction
        """
        return _model_copula.DistributionImplementationPointer_computeComplementaryCDF(self, *args)

    def computeSurvivalFunction(self, *args):
        r"""
        Compute the survival function.

        Parameters
        ----------
        x : sequence of float, 2-d sequence of float
            Survival function input(s).

        Returns
        -------
        S : float, :class:`~openturns.Point`
            Survival function value(s) at input(s) `x`.

        Notes
        -----
        The survival function of the random vector :math:`\vect{X}` is defined as follows:

        .. math::

            S_{\vect{X}}(\vect{x}) = \Prob{\bigcap_{i=1}^d X_i > x_i}
                     \quad \forall \vect{x} \in \Rset^d

        .. warning::

            This is not the complementary cumulative distribution function (except for
            1-dimensional distributions).

        See Also
        --------
        computeComplementaryCDF
        """
        return _model_copula.DistributionImplementationPointer_computeSurvivalFunction(self, *args)

    def computeInverseSurvivalFunction(self, point):
        r"""
        Compute the inverse survival function.

        Parameters
        ----------
        p : float, :math:`p \in [0; 1]`
            Level of the survival function.

        Returns
        -------
        x : :class:`~openturns.Point`
            Point :math:`\vect{x}` such that :math:`S_{\vect{X}}(\vect{x}) = p` with iso-quantile components.

        Notes
        -----
        The inverse survival function writes: :math:`S^{-1}(p)  =  \vect{x}^p` where :math:`S( \vect{x}^p) = \Prob{\bigcap_{i=1}^d X_i > x_i^p}`. OpenTURNS returns the point :math:`\vect{x}^p` such that 
        :math:`\Prob{ X_1 > x_1^p}   =  \dots = \Prob{ X_d > x_d^p}`.

        See Also
        --------
        computeQuantile, computeSurvivalFunction
        """
        return _model_copula.DistributionImplementationPointer_computeInverseSurvivalFunction(self, point)

    def computeProbability(self, interval):
        r"""
        Compute the interval probability.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval, possibly multivariate.

        Returns
        -------
        P : float
            Interval probability.

        Notes
        -----
        This computes the probability that the random vector :math:`\vect{X}` lies in
        the hyper-rectangular region formed by the vectors :math:`\vect{a}` and
        :math:`\vect{b}`:

        .. math::

            \Prob{\bigcap\limits_{i=1}^n a_i < X_i \leq b_i} =
                \sum\limits_{\vect{c}} (-1)^{n(\vect{c})}
                    F_{\vect{X}}\left(\vect{c}\right)

        where the sum runs over the :math:`2^n` vectors such that
        :math:`\vect{c} = \Tr{(c_i, i = 1, \ldots, n)}` with :math:`c_i \in [a_i, b_i]`,
        and :math:`n(\vect{c})` is the number of components in
        :math:`\vect{c}` such that :math:`c_i = a_i`.
        """
        return _model_copula.DistributionImplementationPointer_computeProbability(self, interval)

    def computeCharacteristicFunction(self, *args):
        r"""
        Compute the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Characteristic function value at input :math:`t`.

        Notes
        -----
        The characteristic function is defined as:

        .. math::
            \phi_X(t) = \mathbb{E}\left[\exp(- i t X)\right],
                        \quad t \in \Rset

        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.
        """
        return _model_copula.DistributionImplementationPointer_computeCharacteristicFunction(self, *args)

    def computeLogCharacteristicFunction(self, *args):
        """
        Compute the logarithm of the characteristic function.

        Parameters
        ----------
        t : float
            Characteristic function input.

        Returns
        -------
        phi : complex
            Logarithm of the characteristic function value at input :math:`t`.

        Notes
        -----
        OpenTURNS features a generic implementation of the characteristic function for
        all its univariate distributions (both continuous and discrete). This default
        implementation might be time consuming, especially as the modulus of :math:`t` gets
        high. Only some univariate distributions benefit from dedicated more efficient
        implementations.

        See Also
        --------
        computeCharacteristicFunction
        """
        return _model_copula.DistributionImplementationPointer_computeLogCharacteristicFunction(self, *args)

    def computeGeneratingFunction(self, *args):
        r"""
        Compute the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        g : float
            Probability-generating function value at input :math:`X`.

        Notes
        -----
        The probability-generating function is defined as follows:

        .. math::

            G_X(z) = \Expect{z^X}, \quad z \in \Cset

        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete
        """
        return _model_copula.DistributionImplementationPointer_computeGeneratingFunction(self, *args)

    def computeLogGeneratingFunction(self, *args):
        """
        Compute the logarithm of the probability-generating function.

        Parameters
        ----------
        z : float or complex
            Probability-generating function input.

        Returns
        -------
        lg : float
            Logarithm of the probability-generating function value at input :math:`X`.

        Notes
        -----
        This function only exists for discrete distributions. OpenTURNS implements
        this method for univariate distributions only.

        See Also
        --------
        isDiscrete, computeGeneratingFunction
        """
        return _model_copula.DistributionImplementationPointer_computeLogGeneratingFunction(self, *args)

    def computeEntropy(self):
        r"""
        Compute the entropy of the distribution.

        Returns
        -------
        e : float
            Entropy of the distribution.

        Notes
        -----
        The entropy of a distribution is defined by:

        .. math::

            \cE_X = \Expect{-\log(p_X(\vect{X}))}

        Where the random vector :math:`\vect{X}` follows the probability
        distribution of interest, and :math:`p_X` is either the *probability
        density function* of :math:`\vect{X}` if it is continuous or the
        *probability distribution function* if it is discrete.

        """
        return _model_copula.DistributionImplementationPointer_computeEntropy(self)

    def computePDFGradient(self, *args):
        """
        Compute the gradient of the probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the PDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementationPointer_computePDFGradient(self, *args)

    def computeLogPDFGradient(self, *args):
        """
        Compute the gradient of the log probability density function.

        Parameters
        ----------
        X : sequence of float
            PDF input.

        Returns
        -------
        dfdtheta : :class:`~openturns.Point`
            Partial derivatives of the logPDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementationPointer_computeLogPDFGradient(self, *args)

    def computeCDFGradient(self, *args):
        """
        Compute the gradient of the cumulative distribution function.

        Parameters
        ----------
        X : sequence of float
            CDF input.

        Returns
        -------
        dFdtheta : :class:`~openturns.Point`
            Partial derivatives of the CDF with respect to the distribution
            parameters at input :math:`X`.
        """
        return _model_copula.DistributionImplementationPointer_computeCDFGradient(self, *args)

    def computeQuantile(self, *args):
        r"""
        Compute the quantile function.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : :class:`~openturns.Point`
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_{\vect{X}}(p) = F_{\vect{X}}^{-1}(p),
                              \quad p \in [0; 1]
        """
        return _model_copula.DistributionImplementationPointer_computeQuantile(self, *args)

    def computeScalarQuantile(self, prob, tail=False):
        r"""
        Compute the quantile function for univariate distributions.

        Parameters
        ----------
        p : float, :math:`0 < p < 1`
            Quantile function input (a probability).

        Returns
        -------
        X : float
            Quantile at probability level :math:`p`.

        Notes
        -----
        The quantile function is also known as the inverse cumulative distribution
        function:

        .. math::

            Q_X(p) = F_X^{-1}(p), \quad p \in [0; 1]

        See Also
        --------
        computeQuantile
        """
        return _model_copula.DistributionImplementationPointer_computeScalarQuantile(self, prob, tail)

    def computeMinimumVolumeInterval(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`[a_i, b_i]   = \argmin_{I \in \Rset \, | \, \mu_i(I) = \beta} \lambda_i(I)` and :math:`\mu(I^*_{\alpha})  =  \alpha` with :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. 

        This problem resorts to solving :math:`d` univariate non linear equations: for a fixed value :math:`\beta`, we find each intervals :math:`[a_i, b_i]` such that:

        .. math::
            :nowrap:

            \begin{eqnarray*}
            F_i(b_i) - F_i(a_i) & = & \beta \\
            p_i(b_i) & = & p_i(a_i)
            \end{eqnarray*}

        which consists of finding the bound :math:`a_i` such that:

        .. math::

            p_i(a_i) =  p_i(F_i^{-1}(\beta + F_i(a_i)))

        To find :math:`\beta`, we use the Brent algorithm:  :math:`\mu([\vect{a}(\beta); \vect{b}(\beta)] = g(\beta) = \alpha` with :math:`g` a non linear function.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt = paramDist.computeMinimumVolumeInterval(0.9)

        """
        return _model_copula.DistributionImplementationPointer_computeMinimumVolumeInterval(self, prob)

    def computeMinimumVolumeIntervalWithMarginalProbability(self, prob):
        r"""
        Compute the confidence interval with minimum volume.

        Refer to :func:`computeMinimumVolumeInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence interval of the native parameters at level 0.9 with minimum volume:

        >>> ot.ResourceMap.SetAsUnsignedInteger('Distribution-MinimumVolumeLevelSetSamplingSize', 1000)
        >>> confInt, marginalProb = paramDist.computeMinimumVolumeIntervalWithMarginalProbability(0.9)

        """
        return _model_copula.DistributionImplementationPointer_computeMinimumVolumeIntervalWithMarginalProbability(self, prob)

    def computeBilateralConfidenceInterval(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The bilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = [a_1, b_1] \times \dots \times [a_d, b_d]` where :math:`a_i = F_i^{-1}((1-\beta)/2)` and :math:`b_i = F_i^{-1}((1+\beta)/2)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeBilateralConfidenceInterval(0.9)
        """
        return _model_copula.DistributionImplementationPointer_computeBilateralConfidenceInterval(self, prob)

    def computeBilateralConfidenceIntervalWithMarginalProbability(self, prob):
        r"""
        Compute a bilateral confidence interval.

        Refer to :func:`computeBilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the bilateral confidence interval at level 0.9 with marginal probability:

        >>> confInt, marginalProb = paramDist.computeBilateralConfidenceIntervalWithMarginalProbability(0.9)
        """
        return _model_copula.DistributionImplementationPointer_computeBilateralConfidenceIntervalWithMarginalProbability(self, prob)

    def computeUnilateralConfidenceInterval(self, prob, tail=False):
        r"""
        Compute a unilateral confidence interval.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu`.

        The left unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]-\infty, b_1] \times \dots \times ]-\infty, b_d]` where :math:`b_i = F_i^{-1}(\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`\vect{b}` is the quantile of level :math:`\alpha` of the measure :math:`\mu`, with iso-quantile components.

        The right unilateral confidence interval :math:`I^*_{\alpha}` is the cartesian product :math:`I^*_{\alpha} = ]a_1; +\infty[ \times \dots \times ]a_d; +\infty[` where :math:`a_i = F_i^{-1}(1-\beta)` for all :math:`i` and which verifies :math:`\mu(I^*_{\alpha}) = \alpha`. 
        It means that :math:`S_{\mu}^{-1}(\vect{a}) = \alpha` with iso-quantile components, where :math:`S_{\mu}` is the survival function of the measure :math:`\mu`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt = paramDist.computeUnilateralConfidenceInterval(0.9, True)

        """
        return _model_copula.DistributionImplementationPointer_computeUnilateralConfidenceInterval(self, prob, tail)

    def computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail):
        r"""
        Compute a unilateral confidence interval.

        Refer to :func:`computeUnilateralConfidenceInterval()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.
        tail : boolean
            `True` indicates the interval is bounded by an lower value.
            `False` indicates the interval is bounded by an upper value.
            Default value is `False`.

        Returns
        -------
        confInterval : :class:`~openturns.Interval`
            The unilateral confidence interval of level :math:`\alpha`.
        marginalProb : float
            The value :math:`\beta` which is the common marginal probability of each marginal interval.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution: 

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the right unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, False)

        Determine the left unilateral confidence interval at level 0.9:

        >>> confInt, marginalProb = paramDist.computeUnilateralConfidenceIntervalWithMarginalProbability(0.9, True)

        """
        return _model_copula.DistributionImplementationPointer_computeUnilateralConfidenceIntervalWithMarginalProbability(self, prob, tail)

    def computeMinimumVolumeLevelSet(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.

        Notes
        -----
        We consider an absolutely continuous measure :math:`\mu` with density function :math:`p`. 

        The minimum volume confidence domain :math:`A^*_{\alpha}` is the set of minimum volume and which measure is at least :math:`\alpha`. It is defined by:

        .. math::

            A^*_{\alpha} = \argmin_{A \in \Rset^d\, | \, \mu(A) \geq \alpha} \lambda(A)

        where :math:`\lambda` is the Lebesgue measure on :math:`\Rset^d`. Under some general conditions on :math:`\mu` (for example, no flat regions), the set  :math:`A^*_{\alpha}` is unique and realises the minimum: :math:`\mu(A^*_{\alpha}) = \alpha`. We show that :math:`A^*_{\alpha}` writes:

        .. math::

            A^*_{\alpha} = \{ \vect{x} \in \Rset^d \, | \, p(\vect{x}) \geq p_{\alpha} \}

        for a certain :math:`p_{\alpha} >0`.

        If we consider the random variable :math:`Y = p(\vect{X})`, with cumulative distribution function :math:`F_Y`, then :math:`p_{\alpha}` is defined by:

        .. math::

            1-F_Y(p_{\alpha}) = \alpha

        Thus the minimum volume domain of confidence :math:`\alpha` is the interior of the domain which frontier is the :math:`1-\alpha` quantile of :math:`Y`. It can be determined with simulations of :math:`Y`.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9:

        >>> levelSet = paramDist.computeMinimumVolumeLevelSet(0.9)

        """
        return _model_copula.DistributionImplementationPointer_computeMinimumVolumeLevelSet(self, prob)

    def computeMinimumVolumeLevelSetWithThreshold(self, prob):
        r"""
        Compute the confidence domain with minimum volume.

        Refer to :func:`computeMinimumVolumeLevelSet()`

        Parameters
        ----------
        alpha : float, :math:`\alpha \in [0,1]`
            The confidence level.

        Returns
        -------
        levelSet : :class:`~openturns.LevelSet`
            The minimum volume domain of measure :math:`\alpha`.
        level : float
            The value :math:`p_{\alpha}` of the density function defining the frontier of the domain.

        Examples
        --------
        Create a sample from a Normal distribution:

        >>> import openturns as ot
        >>> sample = ot.Normal().getSample(10)
        >>> ot.ResourceMap.SetAsUnsignedInteger('DistributionFactory-DefaultBootstrapSize', 100)

        Fit a Normal distribution and extract the asymptotic parameters distribution:

        >>> fittedRes = ot.NormalFactory().buildEstimator(sample)
        >>> paramDist = fittedRes.getParameterDistribution()

        Determine the confidence region of minimum volume of the native parameters at level 0.9 with PDF threshold:

        >>> levelSet, threshold = paramDist.computeMinimumVolumeLevelSetWithThreshold(0.9)

        """
        return _model_copula.DistributionImplementationPointer_computeMinimumVolumeLevelSetWithThreshold(self, prob)

    def getRange(self):
        """
        Accessor to the range of the distribution.

        Returns
        -------
        range : :class:`~openturns.Interval`
            Range of the distribution.

        Notes
        -----
        The *mathematical* range is the smallest closed interval outside of which the
        PDF is zero. The *numerical* range is the interval outside of which the PDF is
        rounded to zero in double precision.

        See Also
        --------
        getSupport
        """
        return _model_copula.DistributionImplementationPointer_getRange(self)

    def getRoughness(self):
        r"""
        Accessor to roughness of the distribution.

        Returns
        -------
        r : float
            Roughness of the distribution.

        Notes
        -----
        The roughness of the distribution is defined as the :math:`\cL^2`-norm of its
        PDF:

        .. math::

            r = \int_{\supp{\vect{X}}} f_{\vect{X}}(\vect{x})^2 \di{\vect{x}}

        See Also
        --------
        computePDF
        """
        return _model_copula.DistributionImplementationPointer_getRoughness(self)

    def getMean(self):
        r"""
        Accessor to the mean.

        Returns
        -------
        k : :class:`~openturns.Point`
            Mean.

        Notes
        -----
        The mean is the first-order moment:

        .. math::

            \vect{\mu} = \Tr{\left(\Expect{X_i}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementationPointer_getMean(self)

    def getStandardDeviation(self):
        """
        Accessor to the componentwise standard deviation.

        The standard deviation is the square root of the variance.

        Returns
        -------
        sigma : :class:`~openturns.Point`
            Componentwise standard deviation.

        See Also
        --------
        getCovariance
        """
        return _model_copula.DistributionImplementationPointer_getStandardDeviation(self)

    def getSkewness(self):
        r"""
        Accessor to the componentwise skewness.

        Returns
        -------
        d : :class:`~openturns.Point`
            Componentwise skewness.

        Notes
        -----
        The skewness is the third-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\delta} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^3},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementationPointer_getSkewness(self)

    def getKurtosis(self):
        r"""
        Accessor to the componentwise kurtosis.

        Returns
        -------
        k : :class:`~openturns.Point`
            Componentwise kurtosis.

        Notes
        -----
        The kurtosis is the fourth-order centered moment standardized by the standard deviation:

        .. math::

            \vect{\kappa} = \Tr{\left(\Expect{\left(\frac{X_i - \mu_i}
                                                         {\sigma_i}\right)^4},
                                      \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementationPointer_getKurtosis(self)

    def getStandardMoment(self, n):
        """
        Accessor to the componentwise standard moments.

        Parameters
        ----------
        k : int
            The order of the standard moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise standard moment of order :math:`k`.

        Notes
        -----
        Standard moments are the raw moments of the standard representative of the parametric family of distributions.

        See Also
        --------
        getStandardRepresentative
        """
        return _model_copula.DistributionImplementationPointer_getStandardMoment(self, n)

    def getMoment(self, n):
        r"""
        Accessor to the componentwise moments.

        Parameters
        ----------
        k : int
            The order of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise moment of order :math:`k`.

        Notes
        -----
        The componentwise moment of order :math:`k` is defined as:

        .. math::

            \vect{m}^{(k)} = \Tr{\left(\Expect{X_i^k}, \quad i = 1, \ldots, n\right)}
        """
        return _model_copula.DistributionImplementationPointer_getMoment(self, n)

    def getCenteredMoment(self, n):
        r"""
        Accessor to the componentwise centered moments.

        Parameters
        ----------
        k : int
            The order of the centered moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        Centered moments are centered with respect to the first-order moment:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - \mu_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment
        """
        return _model_copula.DistributionImplementationPointer_getCenteredMoment(self, n)

    def getShiftedMoment(self, n, shift):
        r"""
        Accessor to the componentwise shifted moments.

        Parameters
        ----------
        k : int
            The order of the shifted moment.
        shift : sequence of float
            The shift of the moment.

        Returns
        -------
        m : :class:`~openturns.Point`
            Componentwise centered moment of order :math:`k`.

        Notes
        -----
        The moments are centered with respect to the given shift :\math:`\vect{s}`:

        .. math::

            \vect{m}^{(k)}_0 = \Tr{\left(\Expect{\left(X_i - s_i\right)^k},
                                         \quad i = 1, \ldots, n\right)}

        See Also
        --------
        getMoment, getCenteredMoment
        """
        return _model_copula.DistributionImplementationPointer_getShiftedMoment(self, n, shift)

    def getCovariance(self):
        r"""
        Accessor to the covariance matrix.

        Returns
        -------
        Sigma : :class:`~openturns.CovarianceMatrix`
            Covariance matrix.

        Notes
        -----
        The covariance is the second-order centered moment. It is defined as:

        .. math::

            \mat{\Sigma} & = \Cov{\vect{X}} \\
                         & = \Expect{\left(\vect{X} - \vect{\mu}\right)
                                     \Tr{\left(\vect{X} - \vect{\mu}\right)}}
        """
        return _model_copula.DistributionImplementationPointer_getCovariance(self)

    def getCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.DistributionImplementationPointer_getCorrelation(self)

    def getLinearCorrelation(self):
        """**(ditch me?)**"""
        return _model_copula.DistributionImplementationPointer_getLinearCorrelation(self)

    def getPearsonCorrelation(self):
        r"""
        Accessor to the Pearson correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Pearson's correlation matrix.

        See Also
        --------
        getCovariance

        Notes
        -----
        Pearson's correlation is defined as the normalized covariance matrix:

        .. math::

            \mat{\rho} & = \left[\frac{\Cov{X_i, X_j}}{\sqrt{\Var{X_i}\Var{X_j}}},
                                 \quad i,j = 1, \ldots, n\right] \\
                       & = \left[\frac{\Sigma_{i,j}}{\sqrt{\Sigma_{i,i}\Sigma_{j,j}}},
                                 \quad i,j = 1, \ldots, n\right]
        """
        return _model_copula.DistributionImplementationPointer_getPearsonCorrelation(self)

    def getSpearmanCorrelation(self):
        r"""
        Accessor to the Spearman correlation matrix.

        Returns
        -------
        R : :class:`~openturns.CorrelationMatrix`
            Spearman's correlation matrix.

        Notes
        -----
        Spearman's (rank) correlation is defined as the normalized covariance matrix
        of the copula (ie that of the uniform margins):

        .. math::

            \mat{\rho_S} = \left[\frac{\Cov{F_{X_i}(X_i), F_{X_j}(X_j)}}
                                      {\sqrt{\Var{F_{X_i}(X_i)} \Var{F_{X_j}(X_j)}}},
                                 \quad i,j = 1, \ldots, n\right]

        See Also
        --------
        getKendallTau
        """
        return _model_copula.DistributionImplementationPointer_getSpearmanCorrelation(self)

    def getKendallTau(self):
        r"""
        Accessor to the Kendall coefficients matrix.

        Returns
        -------
        tau: :class:`~openturns.SquareMatrix`
            Kendall coefficients matrix.

        Notes
        -----
        The Kendall coefficients matrix is defined as:

        .. math::

            \mat{\tau} = \Big[& \Prob{X_i < x_i \cap X_j < x_j
                                      \cup
                                      X_i > x_i \cap X_j > x_j} \\
                              & - \Prob{X_i < x_i \cap X_j > x_j
                                        \cup
                                        X_i > x_i \cap X_j < x_j},
                              \quad i,j = 1, \ldots, n\Big]

        See Also
        --------
        getSpearmanCorrelation
        """
        return _model_copula.DistributionImplementationPointer_getKendallTau(self)

    def getShapeMatrix(self):
        """
        Accessor to the shape matrix of the underlying copula if it is elliptical.

        Returns
        -------
        shape : :class:`~openturns.CorrelationMatrix`
            Shape matrix of the elliptical copula of a distribution.

        Notes
        -----
        This is not the Pearson correlation matrix.

        See Also
        --------
        getPearsonCorrelation
        """
        return _model_copula.DistributionImplementationPointer_getShapeMatrix(self)

    def getCholesky(self):
        """
        Accessor to the Cholesky factor of the covariance matrix.

        Returns
        -------
        L : :class:`~openturns.SquareMatrix`
            Cholesky factor of the covariance matrix.

        See Also
        --------
        getCovariance
        """
        return _model_copula.DistributionImplementationPointer_getCholesky(self)

    def getInverseCholesky(self):
        """
        Accessor to the inverse Cholesky factor of the covariance matrix.

        Returns
        -------
        Linv : :class:`~openturns.SquareMatrix`
            Inverse Cholesky factor of the covariance matrix.

        See also
        --------
        getCholesky
        """
        return _model_copula.DistributionImplementationPointer_getInverseCholesky(self)

    def isCopula(self):
        """
        Test whether the distribution is a copula or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A copula is a distribution with uniform margins on [0; 1].
        """
        return _model_copula.DistributionImplementationPointer_isCopula(self)

    def isElliptical(self):
        r"""
        Test whether the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        Notes
        -----
        A multivariate distribution is said to be *elliptical* if its characteristic
        function is of the form:

        .. math::

            \phi(\vect{t}) = \exp\left(i \Tr{\vect{t}} \vect{\mu}\right)
                             \Psi\left(\Tr{\vect{t}} \mat{\Sigma} \vect{t}\right),
                             \quad \vect{t} \in \Rset^n

        for specified vector :math:`\vect{\mu}` and positive-definite matrix
        :math:`\mat{\Sigma}`. The function :math:`\Psi` is known as the
        *characteristic generator* of the elliptical distribution.
        """
        return _model_copula.DistributionImplementationPointer_isElliptical(self)

    def isContinuous(self):
        """
        Test whether the distribution is continuous or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementationPointer_isContinuous(self)

    def isDiscrete(self):
        """
        Test whether the distribution is discrete or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementationPointer_isDiscrete(self)

    def isIntegral(self):
        """
        Test whether the distribution is integer-valued or not.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementationPointer_isIntegral(self)

    def hasEllipticalCopula(self):
        """
        Test whether the copula of the distribution is elliptical or not.

        Returns
        -------
        test : bool
            Answer.

        See Also
        --------
        isElliptical
        """
        return _model_copula.DistributionImplementationPointer_hasEllipticalCopula(self)

    def hasIndependentCopula(self):
        """
        Test whether the copula of the distribution is the independent one.

        Returns
        -------
        test : bool
            Answer.
        """
        return _model_copula.DistributionImplementationPointer_hasIndependentCopula(self)

    def getSupport(self, *args):
        r"""
        Accessor to the support of the distribution.

        Parameters
        ----------
        interval : :class:`~openturns.Interval`
            An interval to intersect with the support of the discrete part of the distribution.

        Returns
        -------
        support : :class:`~openturns.Interval`
            The intersection of the support of the discrete part of the distribution with the given `interval`.

        Notes
        -----
        The mathematical support :math:`\supp{\vect{X}}` of the discrete part of a distribution is the collection of points with nonzero probability.

        This is yet implemented for discrete distributions only.

        See Also
        --------
        getRange
        """
        return _model_copula.DistributionImplementationPointer_getSupport(self, *args)

    def getProbabilities(self):
        """
        Accessor to the discrete probability levels.

        Returns
        -------
        probabilities : :class:`~openturns.Point`
            The probability levels of a discrete distribution.
        """
        return _model_copula.DistributionImplementationPointer_getProbabilities(self)

    def getSingularities(self):
        """
        Accessor to the singularities of the PDF function.

        It is defined for univariate distributions only, and gives all the singularities (ie discontinuities of any order) strictly inside of the range of the distribution.

        Returns
        -------
        singularities : :class:`~openturns.Point`
            The singularities of the PDF of an univariate distribution.
        """
        return _model_copula.DistributionImplementationPointer_getSingularities(self)

    def computeDensityGenerator(self, betaSquare):
        r"""
        Compute the probability density function of the characteristic generator.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator value at input :math:`X`.

        Notes
        -----
        This is the function :math:`\phi` such that the probability density function
        rewrites:

        .. math::

            f_{\vect{X}}(\vect{x}) =
                \phi\left(\Tr{\left(\vect{x} - \vect{\mu}\right)}
                              \mat{\Sigma}^{-1}
                              \left(\vect{x} - \vect{\mu}\right)
                    \right),
                \quad \vect{x} \in \supp{\vect{X}}

        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computePDF
        """
        return _model_copula.DistributionImplementationPointer_computeDensityGenerator(self, betaSquare)

    def computeDensityGeneratorDerivative(self, betaSquare):
        """
        Compute the first-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator first-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.DistributionImplementationPointer_computeDensityGeneratorDerivative(self, betaSquare)

    def computeDensityGeneratorSecondDerivative(self, betaSquare):
        """
        Compute the second-order derivative of the probability density function.

        PDF of the characteristic generator of the elliptical distribution.

        Parameters
        ----------
        beta2 : float
            Density generator input.

        Returns
        -------
        p : float
            Density generator second-order derivative value at input :math:`X`.

        Notes
        -----
        This function only exists for elliptical distributions.

        See Also
        --------
        isElliptical, computeDensityGenerator
        """
        return _model_copula.DistributionImplementationPointer_computeDensityGeneratorSecondDerivative(self, betaSquare)

    def computeRadialDistributionCDF(self, radius, tail=False):
        r"""
        Compute the cumulative distribution function of the squared radius.

        For the underlying standard spherical distribution (for elliptical
        distributions only).

        Parameters
        ----------
        r2 : float, :math:`0 \leq r^2`
            Squared radius.

        Returns
        -------
        F : float
            CDF value at input :math:`r^2`.

        Notes
        -----
        This is the CDF of the sum of the squared independent, standard, identically
        distributed components:

        .. math::

            R^2 = \sqrt{\sum\limits_{i=1}^n U_i^2}
        """
        return _model_copula.DistributionImplementationPointer_computeRadialDistributionCDF(self, radius, tail)

    def getMarginal(self, *args):
        r"""
        Accessor to marginal distributions.

        Parameters
        ----------
        i : int or list of ints, :math:`1 \leq i \leq n`
            Component(s) indice(s).

        Returns
        -------
        distribution : :class:`~openturns.Distribution`
            The marginal distribution of the selected component(s).
        """
        return _model_copula.DistributionImplementationPointer_getMarginal(self, *args)

    def getCopula(self):
        """
        Accessor to the copula of the distribution.

        Returns
        -------
        C : :class:`~openturns.Distribution`
            Copula of the distribution.

        See Also
        --------
        ComposedDistribution
        """
        return _model_copula.DistributionImplementationPointer_getCopula(self)

    def computeConditionalDDF(self, x, y):
        """
        Compute the conditional derivative density function of the last component.

        With respect to the other fixed components.

        Parameters
        ----------
        Xn : float
            Conditional DDF input (last component).
        Xcond : sequence of float with dimension :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        d : float
            Conditional DDF value at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computeDDF, computeConditionalCDF
        """
        return _model_copula.DistributionImplementationPointer_computeConditionalDDF(self, x, y)

    def computeSequentialConditionalDDF(self, x):
        r"""
        Compute the sequential conditional derivative density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the DDF.

        Returns
        -------
        ddf : sequence of float
            Conditional DDF values at input.

        Notes
        -----
        The sequential conditional derivative density function is defined as follows:

        .. math::

            ddf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d^2}{d\,x_n^2}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional DDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d^2}{d\,x_1^2}\Prob{X_1 \leq x_1}`, ie the DDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementationPointer_computeSequentialConditionalDDF(self, x)

    def computeConditionalPDF(self, *args):
        """
        Compute the conditional probability density function.

        Conditional PDF of the last component with respect to the other fixed components.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional PDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional PDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        See Also
        --------
        computePDF, computeConditionalCDF
        """
        return _model_copula.DistributionImplementationPointer_computeConditionalPDF(self, *args)

    def computeSequentialConditionalPDF(self, x):
        r"""
        Compute the sequential conditional probability density function.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the PDF.

        Returns
        -------
        pdf : sequence of float
            Conditional PDF values at input.

        Notes
        -----
        The sequential conditional density function is defined as follows:

        .. math::

            pdf^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\dfrac{d}{d\,x_n}\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional PDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\dfrac{d}{d\,x_1}\Prob{X_1 \leq x_1}`, ie the PDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementationPointer_computeSequentialConditionalPDF(self, x)

    def computeConditionalCDF(self, *args):
        r"""
        Compute the conditional cumulative distribution function.

        Parameters
        ----------
        Xn : float, sequence of float
            Conditional CDF input (last component).
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        F : float, sequence of float
            Conditional CDF value(s) at input :math:`X_n`, :math:`X_{cond}`.

        Notes
        -----
        The conditional cumulative distribution function of the last component with
        respect to the other fixed components is defined as follows:

        .. math::

            F_{X_n \mid X_1, \ldots, X_{n - 1}}(x_n) =
                \Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}},
                \quad x_n \in \supp{X_n}
        """
        return _model_copula.DistributionImplementationPointer_computeConditionalCDF(self, *args)

    def computeSequentialConditionalCDF(self, x):
        r"""
        Compute the sequential conditional cumulative distribution functions.

        Parameters
        ----------
        X : sequence of float, with size :math:`d`
            Values to be taken sequentially as argument and conditioning part of the CDF.

        Returns
        -------
        F : sequence of float
            Conditional CDF values at input.

        Notes
        -----
        The sequential conditional cumulative distribution function is defined as follows:

        .. math::

            F^{seq}_{X_1,\ldots,X_d}(x_1,\ldots,x_d) = \left(\Prob{X_n \leq x_n \mid X_1=x_1, \ldots, X_{n-1}=x_{n-1}}\right)_{i=1,\ldots,d}

        ie its :math:`n`-th component is the conditional CDF of :math:`X_n` at :math:`x_n` given that :math:`X_1=x_1,\ldots,X_{n-1}=x_{n-1}`. For :math:`n=1` it reduces to :math:`\Prob{X_1 \leq x_1}`, ie the CDF of the first component at :math:`x_1`.
        """
        return _model_copula.DistributionImplementationPointer_computeSequentialConditionalCDF(self, x)

    def computeConditionalQuantile(self, *args):
        """
        Compute the conditional quantile function of the last component.

        Conditional quantile with respect to the other fixed components.

        Parameters
        ----------
        p : float, sequence of float, :math:`0 < p < 1`
            Conditional quantile function input.
        Xcond : sequence of float, 2-d sequence of float with size :math:`n-1`
            Conditionning values for the other components.

        Returns
        -------
        X1 : float
            Conditional quantile at input :math:`p`, :math:`X_{cond}`.

        See Also
        --------
        computeQuantile, computeConditionalCDF
        """
        return _model_copula.DistributionImplementationPointer_computeConditionalQuantile(self, *args)

    def computeSequentialConditionalQuantile(self, q):
        r"""
        Compute the conditional quantile function of the last component.

        Parameters
        ----------
        q : sequence of float in :math:`[0,1]`, with size :math:`d`
            Values to be taken sequentially as the argument of the conditional quantile.

        Returns
        -------
        Q : sequence of float
            Conditional quantiles values at input.

        Notes
        -----
        The sequential conditional quantile function is defined as follows:

        .. math::

            Q^{seq}_{X_1,\ldots,X_d}(q_1,\ldots,q_d) = \left(F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1}\right)_{i=1,\ldots,d}

        where :math:`x_1,\ldots,x_{n-1}` are defined recursively as :math:`x_1=F_1^{-1}(q_1)` and given :math:`(x_i)_{i=1,\ldots,n-1}`, :math:`x_n=F^{-1}(q_n|X_1=x_1,\ldots,X_{n-1}=x_{n_1})`: the conditioning part is the set of already computed conditional quantiles.
        """
        return _model_copula.DistributionImplementationPointer_computeSequentialConditionalQuantile(self, q)

    def getIsoProbabilisticTransformation(self):
        r"""
        Accessor to the iso-probabilistic transformation.

        Refer to :ref:`isoprobabilistic_transformation`.

        Returns
        -------
        T : :class:`~openturns.Function`
            Iso-probabilistic transformation.

        Notes
        -----
        The iso-probabilistic transformation is defined as follows:

        .. math::

            T: \left|\begin{array}{rcl}
                    \supp{\vect{X}} & \rightarrow & \Rset^n \\
                    \vect{x} & \mapsto & \vect{u}
               \end{array}\right.

        An iso-probabilistic transformation is a *diffeomorphism* [#diff]_ from
        :math:`\supp{\vect{X}}` to :math:`\Rset^d` that maps realizations
        :math:`\vect{x}` of a random vector :math:`\vect{X}` into realizations
        :math:`\vect{y}` of another random vector :math:`\vect{Y}` while
        preserving probabilities. It is hence defined so that it satisfies:

        .. math::
            :nowrap:

            \begin{eqnarray*}
                \Prob{\bigcap_{i=1}^d X_i \leq x_i}
                    & = & \Prob{\bigcap_{i=1}^d Y_i \leq y_i} \\
                F_{\vect{X}}(\vect{x})
                    & = & F_{\vect{Y}}(\vect{y})
            \end{eqnarray*}

        **The present** implementation of the iso-probabilistic transformation maps
        realizations :math:`\vect{x}` into realizations :math:`\vect{u}` of a
        random vector :math:`\vect{U}` with *spherical distribution* [#spherical]_.
        To be more specific:

            - if the distribution is elliptical, then the transformed distribution is
              simply made spherical using the **Nataf (linear) transformation**.
            - if the distribution has an elliptical Copula, then the transformed
              distribution is made spherical using the **generalized Nataf
              transformation**.
            - otherwise, the transformed distribution is the standard multivariate
              Normal distribution and is obtained by means of the **Rosenblatt
              transformation**.

        .. [#diff] A differentiable map :math:`f` is called a *diffeomorphism* if it
            is a bijection and its inverse :math:`f^{-1}` is differentiable as well.
            Hence, the iso-probabilistic transformation implements a gradient (and
            even a Hessian).

        .. [#spherical] A distribution is said to be *spherical* if it is invariant by
            rotation. Mathematically, :math:`\vect{U}` has a spherical distribution
            if:

            .. math::

                \mat{Q}\,\vect{U} \sim \vect{U},
                \quad \forall \mat{Q} \in \cO_n(\Rset)

        See also
        --------
        getInverseIsoProbabilisticTransformation, isElliptical, hasEllipticalCopula
        """
        return _model_copula.DistributionImplementationPointer_getIsoProbabilisticTransformation(self)

    def getInverseIsoProbabilisticTransformation(self):
        r"""
        Accessor to the inverse iso-probabilistic transformation.

        Returns
        -------
        Tinv : :class:`~openturns.Function`
            Inverse iso-probabilistic transformation.

        Notes
        -----
        The inverse iso-probabilistic transformation is defined as follows:

        .. math::

            T^{-1}: \left|\begin{array}{rcl}
                        \Rset^n & \rightarrow & \supp{\vect{X}} \\
                        \vect{u} & \mapsto & \vect{x}
                    \end{array}\right.

        See also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.DistributionImplementationPointer_getInverseIsoProbabilisticTransformation(self)

    def getStandardDistribution(self):
        """
        Accessor to the standard distribution.

        Returns
        -------
        standard_distribution : :class:`~openturns.Distribution`
            Standard distribution.

        Notes
        -----
        The standard distribution is determined according to the distribution
        properties. This is the target distribution achieved by the iso-probabilistic
        transformation.

        See Also
        --------
        getIsoProbabilisticTransformation
        """
        return _model_copula.DistributionImplementationPointer_getStandardDistribution(self)

    def getStandardRepresentative(self):
        """
        Accessor to the standard representative distribution in the parametric family.

        Returns
        -------
        std_repr_dist : :class:`~openturns.Distribution`
            Standard representative distribution.

        Notes
        -----
        The standard representative distribution is defined on a distribution by distribution basis, most of the time by scaling the distribution with bounded support to :math:`[0,1]` or by standardizing (ie zero mean, unit variance) the distributions with unbounded support. It is the member of the family for which orthonormal polynomials will be built using generic algorithms of orthonormalization.
        """
        return _model_copula.DistributionImplementationPointer_getStandardRepresentative(self)

    def getIntegrationNodesNumber(self):
        """
        Accessor to the number of Gauss integration points.

        Returns
        -------
        N : int
            Number of integration points.
        """
        return _model_copula.DistributionImplementationPointer_getIntegrationNodesNumber(self)

    def setIntegrationNodesNumber(self, integrationNodesNumber):
        """
        Accessor to the number of Gauss integration points.

        Parameters
        ----------
        N : int
            Number of integration points.
        """
        return _model_copula.DistributionImplementationPointer_setIntegrationNodesNumber(self, integrationNodesNumber)

    def drawPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of probability density function.

        Available constructors:
            drawPDF(*x_min, x_max, pointNumber, logScale*)

            drawPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computePDF, viewer.View, ResourceMap

        Examples
        --------
        View the PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawPDF()
        >>> graph.setLegends(['normal pdf'])

        View the iso-lines PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementationPointer_drawPDF(self, *args)

    def drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the PDF of the requested margin.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal1DPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal PDF of the requested couple of
            margins.

        See Also
        --------
        computePDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal2DPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawLogPDF(self, *args):
        r"""
        Draw the graph or of iso-lines of log-probability density function.

        Available constructors:
            drawLogPDF(*x_min, x_max, pointNumber, logScale*)

            drawLogPDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawLogPDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF or its iso_lines.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeLogPDF, viewer.View, ResourceMap

        Examples
        --------
        View the log-PDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawLogPDF()
        >>> graph.setLegends(['normal log-pdf'])

        View the iso-lines log-PDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawLogPDF()
        >>> graph2.setLegends(['iso- normal pdf'])
        >>> graph3 = dist.drawLogPDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementationPointer_drawLogPDF(self, *args)

    def drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the log-probability density function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the log-PDF of the requested margin.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DLogPDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal1DLogPDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the log-probability density function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal log-PDF of the requested couple of
            margins.

        See Also
        --------
        computeLogPDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DLogPDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal2DLogPDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawCDF(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawCDF(*x_min, x_max, pointNumber, logScale*)

            drawCDF(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawCDF(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeCDF, viewer.View, ResourceMap

        Examples
        --------
        View the CDF of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawCDF()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines CDF of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawCDF()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawCDF([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementationPointer_drawCDF(self, *args)

    def drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the CDF of the requested margin.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DCDF(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal1DCDF(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal CDF of the requested couple of
            margins.

        See Also
        --------
        computeCDF, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DCDF(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal2DCDF(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawSurvivalFunction(self, *args):
        r"""
        Draw the cumulative distribution function.

        Available constructors:
            drawSurvivalFunction(*x_min, x_max, pointNumber, logScale*)

            drawSurvivalFunction(*lowerCorner, upperCorner, pointNbrInd, logScaleX, logScaleY*)

            drawSurvivalFunction(*lowerCorner, upperCorner*)

        Parameters
        ----------
        x_min : float, optional
            The min-value of the mesh of the x-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMin` from the :class:`~openturns.ResourceMap`.
        x_max : float, optional, :math:`x_{\max} > x_{\min}`
            The max-value of the mesh of the y-axis.
            Defaults uses the quantile associated to the probability level
            `Distribution-QMax` from the :class:`~openturns.ResourceMap`.
        pointNumber : int
            The number of points that is used for meshing each axis.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.
        lowerCorner : sequence of float, of dimension 2, optional
            The lower corner :math:`[x_{min}, y_{min}]`.
        upperCorner : sequence of float, of dimension 2, optional
            The upper corner :math:`[x_{max}, y_{max}]`.
        pointNbrInd : :class:`~openturns.Indices`, of dimension 2
            Number of points that is used for meshing each axis.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction.

        Notes
        -----
        Only valid for univariate and bivariate distributions.

        See Also
        --------
        computeSurvivalFunction, viewer.View, ResourceMap

        Examples
        --------
        View the SurvivalFunction of a univariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal()
        >>> graph = dist.drawSurvivalFunction()
        >>> graph.setLegends(['normal cdf'])

        View the iso-lines SurvivalFunction of a bivariate distribution:

        >>> import openturns as ot
        >>> dist = ot.Normal(2)
        >>> graph2 = dist.drawSurvivalFunction()
        >>> graph2.setLegends(['iso- normal cdf'])
        >>> graph3 = dist.drawSurvivalFunction([-10, -5],[5, 10], [511, 511])

        """
        return _model_copula.DistributionImplementationPointer_drawSurvivalFunction(self, *args)

    def drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale=False):
        r"""
        Draw the cumulative distribution function of a margin.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the margin of interest.
        x_min : float
            The starting value that is used for meshing the x-axis.
        x_max : float, :math:`x_{\max} > x_{\min}`
            The ending value that is used for meshing the x-axis.
        n_points : int
            The number of points that is used for meshing the x-axis.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the SurvivalFunction of the requested margin.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------

        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal1DSurvivalFunction(2, -6.0, 6.0, 100)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal1DSurvivalFunction(self, marginalIndex, xMin, xMax, pointNumber, logScale)

    def drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX=False, logScaleY=False):
        r"""
        Draw the cumulative distribution function of a couple of margins.

        Parameters
        ----------
        i : int, :math:`1 \leq i \leq n`
            The index of the first margin of interest.
        j : int, :math:`1 \leq i \neq j \leq n`
            The index of the second margin of interest.
        x_min : list of 2 floats
            The starting values that are used for meshing the x- and y- axes.
        x_max : list of 2 floats, :math:`x_{\max} > x_{\min}`
            The ending values that are used for meshing the x- and y- axes.
        n_points : list of 2 ints
            The number of points that are used for meshing the x- and y- axes.
        logScaleX : bool
            Flag to tell if the plot is done on a logarithmic scale for X. Default is *False*.
        logScaleY : bool
            Flag to tell if the plot is done on a logarithmic scale for Y. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the marginal SurvivalFunction of the requested couple of
            margins.

        See Also
        --------
        computeSurvivalFunction, getMarginal, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal(10)
        >>> graph = distribution.drawMarginal2DSurvivalFunction(2, 3, [-6.0] * 2, [6.0] * 2, [100] * 2)
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawMarginal2DSurvivalFunction(self, firstMarginal, secondMarginal, xMin, xMax, pointNumber, logScaleX, logScaleY)

    def drawQuantile(self, *args):
        """
        Draw the quantile function.

        Parameters
        ----------
        q_min : float, in :math:`[0,1]`
            The min value of the mesh of the x-axis.
        q_max : float, in :math:`[0,1]`
            The max value of the mesh of the x-axis.
        n_points : int, optional
            The number of points that is used for meshing the quantile curve.
            Defaults uses `DistributionImplementation-DefaultPointNumber` from the
            :class:`~openturns.ResourceMap`.
        logScale : bool
            Flag to tell if the plot is done on a logarithmic scale. Default is *False*.

        Returns
        -------
        graph : :class:`~openturns.Graph`
            A graphical representation of the quantile function.

        Notes
        -----
        This is implemented for univariate and bivariate distributions only.
        In the case of bivariate distributions, defined by its CDF :math:`F` and its marginals :math:`(F_1, F_2)`, the quantile of order :math:`q` is the point :math:`(F_1(u),F_2(u))` defined by

        .. math::

            F(F_1(u), F_2(u)) = q

        See Also
        --------
        computeQuantile, viewer.View, ResourceMap

        Examples
        --------
        >>> import openturns as ot
        >>> from openturns.viewer import View
        >>> distribution = ot.Normal()
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        >>> distribution = ot.ComposedDistribution([ot.Normal(), ot.Exponential(1.0)], ot.ClaytonCopula(0.5))
        >>> graph = distribution.drawQuantile()
        >>> view = View(graph)
        >>> view.show()
        """
        return _model_copula.DistributionImplementationPointer_drawQuantile(self, *args)

    def getParametersCollection(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.DistributionImplementationPointer_getParametersCollection(self)

    def setParametersCollection(self, *args):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameters : :class:`~openturns.PointWithDescription`
            Dictionary-like object with parameters names and values.
        """
        return _model_copula.DistributionImplementationPointer_setParametersCollection(self, *args)

    def getParameter(self):
        """
        Accessor to the parameter of the distribution.

        Returns
        -------
        parameter : :class:`~openturns.Point`
            Parameter values.
        """
        return _model_copula.DistributionImplementationPointer_getParameter(self)

    def setParameter(self, parameters):
        """
        Accessor to the parameter of the distribution.

        Parameters
        ----------
        parameter : sequence of float
            Parameter values.
        """
        return _model_copula.DistributionImplementationPointer_setParameter(self, parameters)

    def getParameterDescription(self):
        """
        Accessor to the parameter description of the distribution.

        Returns
        -------
        description : :class:`~openturns.Description`
            Parameter names.
        """
        return _model_copula.DistributionImplementationPointer_getParameterDescription(self)

    def getParameterDimension(self):
        """
        Accessor to the number of parameters in the distribution.

        Returns
        -------
        n_parameters : int
            Number of parameters in the distribution.

        See Also
        --------
        getParametersCollection
        """
        return _model_copula.DistributionImplementationPointer_getParameterDimension(self)

    def setDescription(self, description):
        """
        Accessor to the componentwise description.

        Parameters
        ----------
        description : sequence of str
            Description of the components of the distribution.
        """
        return _model_copula.DistributionImplementationPointer_setDescription(self, description)

    def getDescription(self):
        """
        Accessor to the componentwise description.

        Returns
        -------
        description : :class:`~openturns.Description`
            Description of the components of the distribution.

        See Also
        --------
        setDescription
        """
        return _model_copula.DistributionImplementationPointer_getDescription(self)

    def getPDFEpsilon(self):
        """
        Accessor to the PDF computation precision.

        Returns
        -------
        PDFEpsilon : float
            PDF computation precision.
        """
        return _model_copula.DistributionImplementationPointer_getPDFEpsilon(self)

    def getCDFEpsilon(self):
        """
        Accessor to the CDF computation precision.

        Returns
        -------
        CDFEpsilon : float
            CDF computation precision.
        """
        return _model_copula.DistributionImplementationPointer_getCDFEpsilon(self)

    def getPositionIndicator(self):
        """
        Position indicator accessor.

        Defines a generic metric of the position. When the mean is not defined it falls
        back to the median.
        Available only for 1-d distributions.

        Returns
        -------
        position : float
            Mean or median of the distribution.
        """
        return _model_copula.DistributionImplementationPointer_getPositionIndicator(self)

    def getDispersionIndicator(self):
        """
        Dispersion indicator accessor.

        Defines a generic metric of the dispersion. When the standard deviation is not
        defined it falls back to the interquartile.
        Only available for 1-d distributions.

        Returns
        -------
        dispersion : float
            Standard deviation or interquartile.
        """
        return _model_copula.DistributionImplementationPointer_getDispersionIndicator(self)

    def __rtruediv__(self, s):
        return _model_copula.DistributionImplementationPointer___rtruediv__(self, s)

    def __rdiv__(self, s):
        return _model_copula.DistributionImplementationPointer___rdiv__(self, s)

    def __pow__(self, *args):
        return _model_copula.DistributionImplementationPointer___pow__(self, *args)

    def __rsub__(self, s):
        return _model_copula.DistributionImplementationPointer___rsub__(self, s)

    def __neg__(self):
        return _model_copula.DistributionImplementationPointer___neg__(self)

    def __radd__(self, s):
        return _model_copula.DistributionImplementationPointer___radd__(self, s)

    def __rmul__(self, s):
        return _model_copula.DistributionImplementationPointer___rmul__(self, s)

    def getId(self):
        """
        Accessor to the object's id.

        Returns
        -------
        id : int
           Internal unique identifier.
        """
        return _model_copula.DistributionImplementationPointer_getId(self)

    def setShadowedId(self, id):
        """
        Accessor to the object's shadowed id.

        Parameters
        ----------
        id : int
            Internal unique identifier.
        """
        return _model_copula.DistributionImplementationPointer_setShadowedId(self, id)

    def getShadowedId(self):
        """
        Accessor to the object's shadowed id.

        Returns
        -------
        id : int
            Internal unique identifier.
        """
        return _model_copula.DistributionImplementationPointer_getShadowedId(self)

    def setVisibility(self, visible):
        """
        Accessor to the object's visibility state.

        Parameters
        ----------
        visible : bool
            Visibility flag.
        """
        return _model_copula.DistributionImplementationPointer_setVisibility(self, visible)

    def getVisibility(self):
        """
        Accessor to the object's visibility state.

        Returns
        -------
        visible : bool
            Visibility flag.
        """
        return _model_copula.DistributionImplementationPointer_getVisibility(self)

    def hasName(self):
        """
        Test if the object is named.

        Returns
        -------
        hasName : bool
            True if the name is not empty.
        """
        return _model_copula.DistributionImplementationPointer_hasName(self)

    def hasVisibleName(self):
        """
        Test if the object has a distinguishable name.

        Returns
        -------
        hasVisibleName : bool
            True if the name is not empty and not the default one.
        """
        return _model_copula.DistributionImplementationPointer_hasVisibleName(self)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionImplementationPointer_getName(self)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _model_copula.DistributionImplementationPointer_setName(self, name)


_model_copula.DistributionImplementationPointer_swigregister(DistributionImplementationPointer)

class RandomVectorImplementationPointer(object):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr
    ptr_ = property(_model_copula.RandomVectorImplementationPointer_ptr__get, _model_copula.RandomVectorImplementationPointer_ptr__set)

    def __init__(self, *args):
        _model_copula.RandomVectorImplementationPointer_swiginit(self, _model_copula.new_RandomVectorImplementationPointer(*args))

    __swig_destroy__ = _model_copula.delete_RandomVectorImplementationPointer

    def reset(self):
        return _model_copula.RandomVectorImplementationPointer_reset(self)

    def __ref__(self, *args):
        return _model_copula.RandomVectorImplementationPointer___ref__(self, *args)

    def __deref__(self, *args):
        return _model_copula.RandomVectorImplementationPointer___deref__(self, *args)

    def isNull(self):
        return _model_copula.RandomVectorImplementationPointer_isNull(self)

    def __nonzero__(self):
        return _model_copula.RandomVectorImplementationPointer___nonzero__(self)

    __bool__ = __nonzero__

    def get(self):
        return _model_copula.RandomVectorImplementationPointer_get(self)

    def getImplementation(self):
        return _model_copula.RandomVectorImplementationPointer_getImplementation(self)

    def unique(self):
        return _model_copula.RandomVectorImplementationPointer_unique(self)

    def use_count(self):
        return _model_copula.RandomVectorImplementationPointer_use_count(self)

    def swap(self, other):
        return _model_copula.RandomVectorImplementationPointer_swap(self, other)


_model_copula.RandomVectorImplementationPointer_swigregister(RandomVectorImplementationPointer)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/classification.py
# Compiled at: 2019-11-13 10:35:17
"""Classification algorithms."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _classification
else:
    import _classification
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
    __swig_destroy__ = _classification.delete_SwigPyIterator

    def value(self):
        return _classification.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _classification.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _classification.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _classification.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _classification.SwigPyIterator_equal(self, x)

    def copy(self):
        return _classification.SwigPyIterator_copy(self)

    def next(self):
        return _classification.SwigPyIterator_next(self)

    def __next__(self):
        return _classification.SwigPyIterator___next__(self)

    def previous(self):
        return _classification.SwigPyIterator_previous(self)

    def advance(self, n):
        return _classification.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _classification.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _classification.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _classification.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _classification.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _classification.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _classification.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_classification.SwigPyIterator_swigregister(SwigPyIterator)

class TestFailed:
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


import openturns.base, openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom, openturns.diff, openturns.optim, openturns.experiment, openturns.solver, openturns.algo, openturns.model_copula, openturns.dist_bundle1, openturns.dist_bundle2

class MixtureClassifier(openturns.algo.ClassifierImplementation):
    r"""
    Particular classifier based on a mixture distribution.

    Available constructors:
        MixtureClassifier(*mixtDist*)

    Parameters
    ----------
    mixtDist : :class:`~openturns.Mixture`
        A mixture distribution.

    See also
    --------
    Classifier, ExpertMixture

    Notes
    -----
    This implements a mixture classifier which is a particular classifier based on
    a mixture distribution:

    .. math::

        p( \vect{x} ) = \sum_{i=1}^N w_i p_i ( \vect{x} )

    The classifier proposes :math:`N` classes. The rule to assign a point 
    :math:`\vect{x}` to a class :math:`i` is defined as follows: 

    .. math::

        i = \argmax_k \log w_k p_k( \vect{x} )

    See useful methods :meth:`classify` and :meth:`grade`.
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
        return _classification.MixtureClassifier_getClassName(self)

    def __repr__(self):
        return _classification.MixtureClassifier___repr__(self)

    def getNumberOfClasses(self):
        """
        Accessor to the number of classes.

        Returns
        -------
        n_classes : int
            The number of classes
        """
        return _classification.MixtureClassifier_getNumberOfClasses(self)

    def classify(self, *args):
        r"""
        Classify points according to the classifier.

        **Available usages**:

            classify(*inputPoint*)

            classify(*inputSample*)

        Parameters
        ----------
        inputPoint : sequence of float
            A point to classify.
        inputSample : 2-d a sequence of float
            A set of point to classify.

        Notes
        -----
        The classifier proposes :math:`N` classes where :math:`N` is the dimension of
        the mixture distribution *mixtDist*. The rule to assign a point :math:`\vect{x}`
        to a class :math:`i` is defined as follows: 

        .. math::

            i = \argmax_k \log w_k p_k( \vect{x} )

        In the first usage, it returns an integer which corresponds to the class where
        *inputPoint* has been assigned.

        In the second usage, it returns an :class:`~openturns.Indices` that collects the
        class of each point of *inputSample*.
        """
        return _classification.MixtureClassifier_classify(self, *args)

    def grade(self, inP, outC):
        r"""
        Grade points according to the classifier.

        **Available usages**:

            grade(*inputPoint, k*)

            grade(*inputSample, classList*)

        Parameters
        ----------
        inputPoint : sequence of float
            A point to grade.
        inputSample : 2-d a sequence of float
            A set of point to grade.
        k : integer
            The class number.
        classList : sequence of integer
            The list of class number.

        Notes
        -----
        The grade of :math:`\vect{x}` with respect to the class *k* is
        :math:`log w_k p_k ( \vect{x} )`.

        In the first usage, it returns a real that grades *inputPoint* with respect to
        the class *k*. The greatest, the best.

        In the second usage, it returns an :class:`~openturns.Indices` that collects the
        grades of the :math:`i^{th}` point of *inputSample* with respect to the
        :math:`i^{th}` class of *classList*.
        """
        return _classification.MixtureClassifier_grade(self, inP, outC)

    def getMixture(self):
        """
        Accessor to the mixture distribution.

        Returns
        -------
        mixtDist : :class:`~openturns.Mixture`
            The mixture distribution.
        """
        return _classification.MixtureClassifier_getMixture(self)

    def setMixture(self, mixture):
        """
        Accessor to the mixture distribution.

        Parameters
        ----------
        mixtDist : :class:`~openturns.Mixture`
            The mixture distribution.
        """
        return _classification.MixtureClassifier_setMixture(self, mixture)

    def getDimension(self):
        """
        Accessor to the dimension.

        Returns
        -------
        dim : int
            The dimension of the classifier.
        """
        return _classification.MixtureClassifier_getDimension(self)

    def __init__(self, *args):
        _classification.MixtureClassifier_swiginit(self, _classification.new_MixtureClassifier(*args))

    __swig_destroy__ = _classification.delete_MixtureClassifier


_classification.MixtureClassifier_swigregister(MixtureClassifier)
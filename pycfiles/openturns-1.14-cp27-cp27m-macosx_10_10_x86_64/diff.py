# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: lib/python2.7/site-packages/openturns/diff.py
# Compiled at: 2019-11-13 10:36:56
"""Differential algorithms."""
from sys import version_info as _swig_python_version_info
if _swig_python_version_info < (2, 7, 0):
    raise RuntimeError('Python 2.7 or later required')
if __package__ or '.' in __name__:
    from . import _diff
else:
    import _diff
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
    __swig_destroy__ = _diff.delete_SwigPyIterator

    def value(self):
        return _diff.SwigPyIterator_value(self)

    def incr(self, n=1):
        return _diff.SwigPyIterator_incr(self, n)

    def decr(self, n=1):
        return _diff.SwigPyIterator_decr(self, n)

    def distance(self, x):
        return _diff.SwigPyIterator_distance(self, x)

    def equal(self, x):
        return _diff.SwigPyIterator_equal(self, x)

    def copy(self):
        return _diff.SwigPyIterator_copy(self)

    def next(self):
        return _diff.SwigPyIterator_next(self)

    def __next__(self):
        return _diff.SwigPyIterator___next__(self)

    def previous(self):
        return _diff.SwigPyIterator_previous(self)

    def advance(self, n):
        return _diff.SwigPyIterator_advance(self, n)

    def __eq__(self, x):
        return _diff.SwigPyIterator___eq__(self, x)

    def __ne__(self, x):
        return _diff.SwigPyIterator___ne__(self, x)

    def __iadd__(self, n):
        return _diff.SwigPyIterator___iadd__(self, n)

    def __isub__(self, n):
        return _diff.SwigPyIterator___isub__(self, n)

    def __add__(self, n):
        return _diff.SwigPyIterator___add__(self, n)

    def __sub__(self, *args):
        return _diff.SwigPyIterator___sub__(self, *args)

    def __iter__(self):
        return self


_diff.SwigPyIterator_swigregister(SwigPyIterator)

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


import openturns.common, openturns.typ, openturns.statistics, openturns.graph, openturns.func, openturns.geom

class FiniteDifferenceStepImplementation(openturns.common.PersistentObject):
    """
    Base class to define finite difference steps.

    Available constructors:
        FiniteDifferenceStep(*epsilon=[1.0]*)

    Parameters
    ----------
    epsilon : sequence of float
        Finite difference steps for each dimension.

    Notes
    -----
    Base class to define how finite difference steps are computed.
    Using *FiniteDifferenceStep* is equivalent to use its derived class
    :class:`~openturns.ConstantStep`. Another way to compute steps
    is through its second derived class :class:`~openturns.BlendedStep`.
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
        return _diff.FiniteDifferenceStepImplementation_getClassName(self)

    def __repr__(self):
        return _diff.FiniteDifferenceStepImplementation___repr__(self)

    def setEpsilon(self, epsilon):
        """
        Set the finite difference steps.

        Parameters
        ----------
        epsilon : sequence of float
            If :class:`~openturns.ConstantStep` : Finite difference steps for each
            dimension.

            If :class:`~openturns.BlendedStep` : Finite difference step factors for
            each dimension.
        """
        return _diff.FiniteDifferenceStepImplementation_setEpsilon(self, epsilon)

    def getEpsilon(self):
        """
        Get the finite difference steps.

        Returns
        -------
        epsilon : :class:`~openturns.Point`
            If :class:`~openturns.ConstantStep` : Finite difference steps for each
            dimension.

            If :class:`~openturns.BlendedStep` : Finite difference step factors for
            each dimension.
        """
        return _diff.FiniteDifferenceStepImplementation_getEpsilon(self)

    def __call__(self, inP):
        return _diff.FiniteDifferenceStepImplementation___call__(self, inP)

    def __init__(self, *args):
        _diff.FiniteDifferenceStepImplementation_swiginit(self, _diff.new_FiniteDifferenceStepImplementation(*args))

    __swig_destroy__ = _diff.delete_FiniteDifferenceStepImplementation


_diff.FiniteDifferenceStepImplementation_swigregister(FiniteDifferenceStepImplementation)

class FiniteDifferenceStepImplementationTypedInterfaceObject(openturns.common.InterfaceObject):
    thisown = property(lambda x: x.this.own(), lambda x, v: x.this.own(v), doc='The membership flag')
    __repr__ = _swig_repr

    def __init__(self, *args):
        _diff.FiniteDifferenceStepImplementationTypedInterfaceObject_swiginit(self, _diff.new_FiniteDifferenceStepImplementationTypedInterfaceObject(*args))

    def getImplementation(self, *args):
        """
        Accessor to the underlying implementation.

        Returns
        -------
        impl : Implementation
            The implementation class.
        """
        return _diff.FiniteDifferenceStepImplementationTypedInterfaceObject_getImplementation(self, *args)

    def setName(self, name):
        """
        Accessor to the object's name.

        Parameters
        ----------
        name : str
            The name of the object.
        """
        return _diff.FiniteDifferenceStepImplementationTypedInterfaceObject_setName(self, name)

    def getName(self):
        """
        Accessor to the object's name.

        Returns
        -------
        name : str
            The name of the object.
        """
        return _diff.FiniteDifferenceStepImplementationTypedInterfaceObject_getName(self)

    def __eq__(self, other):
        return _diff.FiniteDifferenceStepImplementationTypedInterfaceObject___eq__(self, other)

    def __ne__(self, other):
        return _diff.FiniteDifferenceStepImplementationTypedInterfaceObject___ne__(self, other)

    __swig_destroy__ = _diff.delete_FiniteDifferenceStepImplementationTypedInterfaceObject


_diff.FiniteDifferenceStepImplementationTypedInterfaceObject_swigregister(FiniteDifferenceStepImplementationTypedInterfaceObject)

class FiniteDifferenceStep(FiniteDifferenceStepImplementationTypedInterfaceObject):
    """
    Base class to define finite difference steps.

    Available constructors:
        FiniteDifferenceStep(*epsilon=[1.0]*)

    Parameters
    ----------
    epsilon : sequence of float
        Finite difference steps for each dimension.

    Notes
    -----
    Base class to define how finite difference steps are computed.
    Using *FiniteDifferenceStep* is equivalent to use its derived class
    :class:`~openturns.ConstantStep`. Another way to compute steps
    is through its second derived class :class:`~openturns.BlendedStep`.
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
        return _diff.FiniteDifferenceStep_getClassName(self)

    def __repr__(self):
        return _diff.FiniteDifferenceStep___repr__(self)

    def setEpsilon(self, epsilon):
        """
        Set the finite difference steps.

        Parameters
        ----------
        epsilon : sequence of float
            If :class:`~openturns.ConstantStep` : Finite difference steps for each
            dimension.

            If :class:`~openturns.BlendedStep` : Finite difference step factors for
            each dimension.
        """
        return _diff.FiniteDifferenceStep_setEpsilon(self, epsilon)

    def getEpsilon(self):
        """
        Get the finite difference steps.

        Returns
        -------
        epsilon : :class:`~openturns.Point`
            If :class:`~openturns.ConstantStep` : Finite difference steps for each
            dimension.

            If :class:`~openturns.BlendedStep` : Finite difference step factors for
            each dimension.
        """
        return _diff.FiniteDifferenceStep_getEpsilon(self)

    def __call__(self, inP):
        return _diff.FiniteDifferenceStep___call__(self, inP)

    def __init__(self, *args):
        _diff.FiniteDifferenceStep_swiginit(self, _diff.new_FiniteDifferenceStep(*args))

    __swig_destroy__ = _diff.delete_FiniteDifferenceStep


_diff.FiniteDifferenceStep_swigregister(FiniteDifferenceStep)

class ConstantStep(FiniteDifferenceStepImplementation):
    """
    Constant step.

    Available constructors:
        ConstantStep(*epsilon=[1.0]*)

    Parameters
    ----------
    epsilon : sequence of float
        Finite difference steps for each dimension.

    Notes
    -----
    *ConstantStep* defines a list of constant finite difference steps equal to
    *epsilon*.

    See also
    --------
    BlendedStep

    Examples
    --------
    >>> import openturns as ot
    >>> epsilon = [1e-4, 2e-4]
    >>> steps = ot.ConstantStep(epsilon)
    >>> print(steps([2.0]*2))
    [0.0001,0.0002]
    >>> print(steps([0.0, 3.0]))
    [0.0001,0.0002]
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
        return _diff.ConstantStep_getClassName(self)

    def __repr__(self):
        return _diff.ConstantStep___repr__(self)

    def __call__(self, inP):
        return _diff.ConstantStep___call__(self, inP)

    def __init__(self, *args):
        _diff.ConstantStep_swiginit(self, _diff.new_ConstantStep(*args))

    __swig_destroy__ = _diff.delete_ConstantStep


_diff.ConstantStep_swigregister(ConstantStep)

class BlendedStep(FiniteDifferenceStepImplementation):
    """
    Blended step.

    Available constructors:
        BlendedStep(*epsilon, eta=1.0*)

    Parameters
    ----------
    epsilon : sequence of float
        Finite difference step factors for each dimension.
    eta : positive float, sequence of positive float with the same dimension as *epsilon*
        Finite difference step offsets for each dimension.

    Notes
    -----
    *BlendedStep* defines a list of finite difference steps equal to:
    *epsilon (|x| + eta)*.

    See also
    --------
    ConstantStep

    Examples
    --------
    >>> import openturns as ot
    >>> epsilon = [1e-4, 2e-4]
    >>> x = [2.0]*2
    >>> steps = ot.BlendedStep(epsilon)
    >>> print(steps(x))
    [0.0003,0.0006]
    >>> steps = ot.BlendedStep(epsilon, 0.0)
    >>> print(steps(x))
    [0.0002,0.0004]
    >>> steps = ot.BlendedStep(epsilon, [1.0, 2.0])
    >>> print(steps(x))
    [0.0003,0.0008]
    >>> steps = ot.BlendedStep(epsilon, 2.0)
    >>> print(steps(x))
    [0.0004,0.0008]
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
        return _diff.BlendedStep_getClassName(self)

    def __repr__(self):
        return _diff.BlendedStep___repr__(self)

    def __call__(self, inP):
        return _diff.BlendedStep___call__(self, inP)

    def setEta(self, eta):
        """
        Set the finite difference step offsets.

        Parameters
        ----------
        eta : sequence of positive float
            Finite difference step offsets for each dimension.
        """
        return _diff.BlendedStep_setEta(self, eta)

    def getEta(self):
        """
        Get the finite difference step offsets.

        Returns
        -------
        eta : :class:`~openturns.Point`
            Finite difference step offsets for each dimension.
        """
        return _diff.BlendedStep_getEta(self)

    def __init__(self, *args):
        _diff.BlendedStep_swiginit(self, _diff.new_BlendedStep(*args))

    __swig_destroy__ = _diff.delete_BlendedStep


_diff.BlendedStep_swigregister(BlendedStep)

class FiniteDifferenceGradient(openturns.func.GradientImplementation):
    """
    Base class for first order finite-difference schemes.

    Available constructors:
        FiniteDifferenceGradient(*epsilon, evalImpl*)

        FiniteDifferenceGradient(*step, evalImpl*)

    Parameters
    ----------
    evalImpl : :class:`~openturns.EvaluationImplementation`
        Implementation of the evaluation of a function.
    epsilon : float, sequence of float
        Finite difference steps for each dimension.
    step : :class:`~openturns.FiniteDifferenceStep`
        Defines how finite difference steps values are computed.

    Notes
    -----
    Base class to define first order finite-difference schemes. The gradient
    can be computed only through its derived classes:

    - :class:`~openturns.CenteredFiniteDifferenceGradient`,

    - :class:`~openturns.NonCenteredFiniteDifferenceGradient`.
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
        return _diff.FiniteDifferenceGradient_getClassName(self)

    def __eq__(self, other):
        return _diff.FiniteDifferenceGradient___eq__(self, other)

    def __repr__(self):
        return _diff.FiniteDifferenceGradient___repr__(self)

    def getInputDimension(self):
        """
        Get the input dimension.

        Returns
        -------
        dimension : int
            Input dimension.
        """
        return _diff.FiniteDifferenceGradient_getInputDimension(self)

    def getOutputDimension(self):
        """
        Get the output dimension.

        Returns
        -------
        dimension : int
            Output dimension.
        """
        return _diff.FiniteDifferenceGradient_getOutputDimension(self)

    def getEpsilon(self):
        """
        Get the finite difference steps.

        Returns
        -------
        epsilon : :class:`~openturns.Point`
            Finite difference steps for each dimension.
        """
        return _diff.FiniteDifferenceGradient_getEpsilon(self)

    def getEvaluation(self):
        """
        Get the implementation of the evaluation of the function.

        Returns
        -------
        evalImpl : :class:`~openturns.EvaluationImplementation`
            Implementation of the evaluation of a function.
        """
        return _diff.FiniteDifferenceGradient_getEvaluation(self)

    def setFiniteDifferenceStep(self, finiteDifferenceStep):
        """
        Set the finite difference step.

        Parameters
        ----------
        step : :class:`~openturns.FiniteDifferenceStep`
            Defines how finite difference steps values are computed.
        """
        return _diff.FiniteDifferenceGradient_setFiniteDifferenceStep(self, finiteDifferenceStep)

    def getFiniteDifferenceStep(self):
        """
        Get the finite difference step.

        Returns
        -------
        step : :class:`~openturns.FiniteDifferenceStep`
            Defines how finite difference steps values are computed.
        """
        return _diff.FiniteDifferenceGradient_getFiniteDifferenceStep(self)

    def gradient(self, inP):
        """
        Get the gradient at some point.

        Parameters
        ----------
        point : sequence of float
            Point where the gradient is computed.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Transposed Jacobian matrix evaluated at *point*.
        """
        return _diff.FiniteDifferenceGradient_gradient(self, inP)

    def __init__(self, *args):
        _diff.FiniteDifferenceGradient_swiginit(self, _diff.new_FiniteDifferenceGradient(*args))

    __swig_destroy__ = _diff.delete_FiniteDifferenceGradient


_diff.FiniteDifferenceGradient_swigregister(FiniteDifferenceGradient)

class FiniteDifferenceHessian(openturns.func.HessianImplementation):
    """
    Base class for second order centered finite-difference scheme.

    Available constructors:
        FiniteDifferenceHessian(*epsilon, evalImpl*)

        FiniteDifferenceHessian(*step, evalImpl*)

    Parameters
    ----------
    evalImpl : :class:`~openturns.EvaluationImplementation`
        Implementation of the evaluation of a function.
    epsilon : float, sequence of float
        Finite difference steps for each dimension.
    step : :class:`~openturns.FiniteDifferenceStep`
        Defines how finite difference steps values are computed.

    Notes
    -----
    Base class to define second order finite-difference scheme. The hessian
    can be computed only through its derived class:

    - :class:`~openturns.CenteredFiniteDifferenceHessian`.
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
        return _diff.FiniteDifferenceHessian_getClassName(self)

    def __eq__(self, other):
        return _diff.FiniteDifferenceHessian___eq__(self, other)

    def __repr__(self):
        return _diff.FiniteDifferenceHessian___repr__(self)

    def getInputDimension(self):
        """
        Get the input dimension.

        Returns
        -------
        dimension : int
            Input dimension.
        """
        return _diff.FiniteDifferenceHessian_getInputDimension(self)

    def getOutputDimension(self):
        """
        Get the output dimension.

        Returns
        -------
        dimension : int
            Output dimension.
        """
        return _diff.FiniteDifferenceHessian_getOutputDimension(self)

    def getEpsilon(self):
        """
        Get the finite difference steps.

        Returns
        -------
        epsilon : :class:`~openturns.Point`
            Finite difference steps for each dimension.
        """
        return _diff.FiniteDifferenceHessian_getEpsilon(self)

    def getEvaluation(self):
        """
        Get the implementation of the evaluation of the function.

        Returns
        -------
        evalImpl : :class:`~openturns.EvaluationImplementation`
            Implementation of the evaluation of a function.
        """
        return _diff.FiniteDifferenceHessian_getEvaluation(self)

    def setFiniteDifferenceStep(self, finiteDifferenceStep):
        """
        Set the finite difference step.

        Parameters
        ----------
        step : :class:`~openturns.FiniteDifferenceStep`
            Defines how finite difference steps values are computed.
        """
        return _diff.FiniteDifferenceHessian_setFiniteDifferenceStep(self, finiteDifferenceStep)

    def getFiniteDifferenceStep(self):
        """
        Get the finite difference step.

        Returns
        -------
        step : :class:`~openturns.FiniteDifferenceStep`
            Defines how finite difference steps values are computed.
        """
        return _diff.FiniteDifferenceHessian_getFiniteDifferenceStep(self)

    def hessian(self, inP):
        """
        Get the hessian at some point.

        Parameters
        ----------
        point : sequence of float
            Point where the hessian is computed.

        Returns
        -------
        hessian : :class:`~openturns.SymmetricTensor`
            Hessian evaluated at *point*.
        """
        return _diff.FiniteDifferenceHessian_hessian(self, inP)

    def __init__(self, *args):
        _diff.FiniteDifferenceHessian_swiginit(self, _diff.new_FiniteDifferenceHessian(*args))

    __swig_destroy__ = _diff.delete_FiniteDifferenceHessian


_diff.FiniteDifferenceHessian_swigregister(FiniteDifferenceHessian)

class CenteredFiniteDifferenceGradient(FiniteDifferenceGradient):
    r"""
    First order centered finite-difference scheme.

    Available constructors:
        CenteredFiniteDifferenceGradient(*epsilon, evalImpl*)

        CenteredFiniteDifferenceGradient(*step, evalImpl*)

    Parameters
    ----------
    evalImpl : :class:`~openturns.EvaluationImplementation`
        Implementation of the evaluation of a function.
    epsilon : float, sequence of float
        Finite difference steps for each dimension.
    step : :class:`~openturns.FiniteDifferenceStep`
        Defines how finite difference steps values are computed.

    Notes
    -----
    *CenteredFiniteDifferenceGradient* provides a first order centered finite-
    difference scheme:

    .. math::

      \frac{\partial f_j}{\partial x_i} \approx \frac{f_j(x + \epsilon_i) - f_j(x - \epsilon_i)}
                                                     {2 \epsilon_i}

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> epsilon = [0.01]*2
    >>> myGradient = ot.CenteredFiniteDifferenceGradient(epsilon, myFunc.getEvaluation())
    >>> inPoint = [1.]*2
    >>> print(myGradient.gradient(inPoint))
    [[  0.841471 -0.909282  0.735771 ]
     [  0.540293 -0.909282 -1.10366  ]]
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
        return _diff.CenteredFiniteDifferenceGradient_getClassName(self)

    def __repr__(self):
        return _diff.CenteredFiniteDifferenceGradient___repr__(self)

    def __str__(self, *args):
        return _diff.CenteredFiniteDifferenceGradient___str__(self, *args)

    def gradient(self, inP):
        """
        Get the gradient at some point.

        Parameters
        ----------
        point : sequence of float
            Point where the gradient is computed.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Transposed Jacobian matrix evaluated at *point*.
        """
        return _diff.CenteredFiniteDifferenceGradient_gradient(self, inP)

    def __init__(self, *args):
        _diff.CenteredFiniteDifferenceGradient_swiginit(self, _diff.new_CenteredFiniteDifferenceGradient(*args))

    __swig_destroy__ = _diff.delete_CenteredFiniteDifferenceGradient


_diff.CenteredFiniteDifferenceGradient_swigregister(CenteredFiniteDifferenceGradient)

class CenteredFiniteDifferenceHessian(FiniteDifferenceHessian):
    r"""
    Second order centered finite-difference scheme.

    Available constructors:
        CenteredFiniteDifferenceHessian(*epsilon, evalImpl*)

        CenteredFiniteDifferenceHessian(*step, evalImpl*)

    Parameters
    ----------
    evalImpl : :class:`~openturns.EvaluationImplementation`
        Implementation of the evaluation of a function.
    epsilon : float, sequence of float
        Finite difference steps for each dimension.
    step : :class:`~openturns.FiniteDifferenceStep`
        Defines how finite difference steps values are computed.

    Notes
    -----
    *CenteredFiniteDifferenceHessian* provides a second order centered finite-
    difference scheme:

    .. math::

      \frac{\partial^2 f_k}{\partial x_i \partial x_j} \approx
                                         \frac{
                                            f_k(x + \epsilon_i + \epsilon_j) -
                                            f_k(x + \epsilon_i - \epsilon_j) +
                                            f_k(x - \epsilon_i - \epsilon_j) -
                                            f_k(x - \epsilon_i + \epsilon_j)}
                                         {4 \epsilon_i \epsilon_j}

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> epsilon = [0.01]*2
    >>> myHessian = ot.CenteredFiniteDifferenceHessian(epsilon, myFunc.getEvaluation())
    >>> inPoint = [1.0]*2
    >>> print(myHessian.hessian(inPoint))
    sheet #0
    [[  0         0.540293 ]
     [  0.540293 -0.841443 ]]
    sheet #1
    [[  0.416133  0.416133 ]
     [  0.416133  0.416133 ]]
    sheet #2
    [[  0.735783 -1.10368  ]
     [ -1.10368   1.47152  ]]
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
        return _diff.CenteredFiniteDifferenceHessian_getClassName(self)

    def __eq__(self, other):
        return _diff.CenteredFiniteDifferenceHessian___eq__(self, other)

    def __repr__(self):
        return _diff.CenteredFiniteDifferenceHessian___repr__(self)

    def __str__(self, *args):
        return _diff.CenteredFiniteDifferenceHessian___str__(self, *args)

    def hessian(self, inP):
        """
        Get the hessian at some point.

        Parameters
        ----------
        point : sequence of float
            Point where the hessian is computed.

        Returns
        -------
        hessian : :class:`~openturns.SymmetricTensor`
            Hessian evaluated at *point*.
        """
        return _diff.CenteredFiniteDifferenceHessian_hessian(self, inP)

    def __init__(self, *args):
        _diff.CenteredFiniteDifferenceHessian_swiginit(self, _diff.new_CenteredFiniteDifferenceHessian(*args))

    __swig_destroy__ = _diff.delete_CenteredFiniteDifferenceHessian


_diff.CenteredFiniteDifferenceHessian_swigregister(CenteredFiniteDifferenceHessian)

class NonCenteredFiniteDifferenceGradient(FiniteDifferenceGradient):
    r"""
    First order non-centered finite-difference scheme.

    Available constructors:
        NonCenteredFiniteDifferenceGradient(*epsilon, evalImpl*)

        NonCenteredFiniteDifferenceGradient(*step, evalImpl*)

    Parameters
    ----------
    evalImpl : :class:`~openturns.EvaluationImplementation`
        Implementation of the evaluation of a function.
    epsilon : float, sequence of float
        Finite difference steps for each dimension.
    step : :class:`~openturns.FiniteDifferenceStep`
        Defines how finite difference steps values are computed.

    Notes
    -----
    *NonCenteredFiniteDifferenceGradient* provides a first order non-centered
    finite-difference scheme:

    .. math::

        \frac{\partial f_j}{\partial x_i} \approx \frac{f_j(x + \epsilon_i) - f_j(x)}
                                                       {\epsilon_i}

    Examples
    --------
    >>> import openturns as ot
    >>> formulas = ['x1 * sin(x2)', 'cos(x1 + x2)', '(x2 + 1) * exp(x1 - 2 * x2)']
    >>> myFunc = ot.SymbolicFunction(['x1', 'x2'], formulas)
    >>> epsilon = [0.01]*2
    >>> myGradient = ot.NonCenteredFiniteDifferenceGradient(epsilon, myFunc.getEvaluation())
    >>> inPoint = [1.0]*2
    >>> print(myGradient.gradient(inPoint))
    [[  0.841471 -0.907202  0.73945  ]
     [  0.536086 -0.907202 -1.09631  ]]
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
        return _diff.NonCenteredFiniteDifferenceGradient_getClassName(self)

    def __repr__(self):
        return _diff.NonCenteredFiniteDifferenceGradient___repr__(self)

    def __str__(self, *args):
        return _diff.NonCenteredFiniteDifferenceGradient___str__(self, *args)

    def gradient(self, inP):
        """
        Get the gradient at some point.

        Parameters
        ----------
        point : sequence of float
            Point where the gradient is computed.

        Returns
        -------
        gradient : :class:`~openturns.Matrix`
            Transposed Jacobian matrix evaluated at *point*.
        """
        return _diff.NonCenteredFiniteDifferenceGradient_gradient(self, inP)

    def __init__(self, *args):
        _diff.NonCenteredFiniteDifferenceGradient_swiginit(self, _diff.new_NonCenteredFiniteDifferenceGradient(*args))

    __swig_destroy__ = _diff.delete_NonCenteredFiniteDifferenceGradient


_diff.NonCenteredFiniteDifferenceGradient_swigregister(NonCenteredFiniteDifferenceGradient)
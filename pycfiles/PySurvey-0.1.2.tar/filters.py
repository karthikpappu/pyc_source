# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jonathanfriedman/Dropbox/python_dev_library/PySurvey/pysurvey/util/filters.py
# Compiled at: 2013-04-04 17:23:56
"""
Created on Dec 14, 2012

@author: jonathanfriedman
"""
import operator, numpy as np

def _presence_fun(x):
    return len(np.where(x > 0)[0])


namedComperators = {'==': ('==', '=', 'eq', 'equal'), '!=': ('!=', '-=', 'neq'), 
   '>=': ('>=', 'geq', 'ge'), 
   '<=': ('<=', 'leq', 'le', 'seq', 'se'), 
   '>': ('>', 'greater', 'bigger'), 
   '<': ('<', 'smaller', 'littler'), 
   'in': ('in', 'contains')}
namedActors = {'sum': ('sum', ), 'avg': ('average', 'avg', 'mean'), 
   'med': ('median', 'med'), 
   'var': ('var', 'variance'), 
   'std': ('std', 'standard-deviation'), 
   'min': ('min', 'minimum'), 
   'max': ('max', 'maximum'), 
   'presence': ('present', 'presence')}

def parse_comperator(c):
    """
    Parse the given comperator.
    
    Parameters
    ----------
    actor : str/callable 
        A callable remains unchanged.
        A string that matches one of the named comperators returns 
        the appropriate comperator.
        Named comperators are listed in pysurvey.util.filters.namedComperators

    Returns
    -------
    A callable that take two inputs and returns a bool.
    """
    if hasattr(c, '__call__'):
        return c
    if isinstance(c, str):
        c = c.strip().lower()
        if c in namedComperators['==']:
            return operator.eq
        if c in namedComperators['!=']:
            return operator.ne
        if c in namedComperators['>=']:
            return operator.ge
        if c in namedComperators['<=']:
            return operator.le
        if c in namedComperators['>']:
            return operator.gt
        if c in namedComperators['<']:
            return operator.lt
        if c in namedComperators['in']:
            return operator.contains
        raise ValueError, 'Unsupported comperator "%s"' % c
    else:
        raise TypeError, 'Unsupported comperator type'


def parse_actor(actor):
    """
    Parse the given actor.
    
    Parameters
    ----------
    actor : str/callable 
        A callable remains unchanged.
        A string that matches one of the named actors returns the appropriate actor.
        Otherwise returns an actor that returns the Series entry labeled with given str.
        To have a named actor be interpreted as a regular string, prefix an underscore to it.
        For example: '_sum' returns an actor that searches for the 'sum' label, 
        rather than take the sum of the series.
        Named actors are listed in pysurvey.util.filters.namedActors
        
    Returns
    -------
    A callable that take a pandas Series and returns a 
    single output (typically not a container) 
    """
    if hasattr(actor, '__call__'):
        return actor
    if isinstance(actor, str):
        a = actor.strip().lower()
        if a in namedActors['sum']:
            return np.sum
        if a in namedActors['avg']:
            return np.mean
        if a in namedActors['med']:
            return np.median
        if a in namedActors['var']:
            return np.var
        if a in namedActors['std']:
            return np.std
        if a in namedActors['min']:
            return np.min
        if a in namedActors['max']:
            return np.max
        if a in namedActors['presence']:
            return _presence_fun
        if actor.startswith('_'):
            return lambda x: x[actor[1:]]
        return lambda x: x[actor]
    else:
        raise TypeError, 'Unsupported actor type'


class Filter(object):

    def __init__(self, f, nan_val=None):
        """
        An object used for filtering rows/columns of a DataFrame.
        It has a __call__ method that takes a Series and returns a bool
        indicating whether the Series passes the filtering criteria. 
        
        Parameters
        ----------
        f : callable/container 
            Parameter containing information needed to construct 
            the __call__ method. 
            If f is a callable, it is called when the Filter is called.
            Otherwise, f needs to be consist of an actor, comperator, and value.
            The actor extracts the quantity of interest from a Series, 
            and the comperator compares it to the given value and returns a bool.
            See docstring of 'parse_actor' and 'parse_comperator' for more details.
        nan_val : bool 
            The value the filter returns when a NaN is encountered 
            by the actor/provided callable function.   
        """
        self.nan_val = nan_val
        if hasattr(f, '__call__'):
            self._actor_raw = None
            self._comperator_raw = None
            self._func_raw = f
            self._actor = None
            self._comperator = None
            self._value = None
        else:
            try:
                (actor, comperator, val) = f
            except:
                raise ValueError, 'Filter must be either a callable or a' + 'triplet of actor, comperator and value.'

            self._actor_raw = actor
            self._comperator_raw = comperator
            self._func_raw = None
            self._actor = parse_actor(actor)
            self._comperator = parse_comperator(comperator)
            self._value = val
        self.set_func()
        return

    def __call__(self, x):
        return self._func(x)

    def __repr__(self):
        if self._func_raw is None:
            return 'Filter(%r, %r, %r)' % (self._actor_raw, self._comperator_raw, self._value)
        else:
            import inspect
            return 'Filter function docstring is:\n%s' % inspect.getsource(self._func_raw)
            return

    def make_filter(self, f=None):
        if self._func_raw is None:
            actor = self._actor
            comperator = self._comperator
            val = self._value

            def filter_fun(x):
                if self.nan_val is not None:
                    try:
                        result = float(actor(x))
                        if np.isnan(result):
                            return self.nan_val
                    except ValueError:
                        pass

                if comperator is operator.contains:
                    return comperator(val, actor(x))
                else:
                    return comperator(actor(x), val)
                    return

        else:

            def filter_fun(x):
                func = self._func_raw
                if self.nan_val is not None:
                    try:
                        result = float(func(x))
                        if np.isnan(result):
                            return self.nan_val
                    except ValueError:
                        pass

                return func(x)

        return filter_fun

    def set_func(self, f=None):
        if f is not None:
            self._actor = None
            self._comperator = None
            self._value = None
            self._func_raw = f
        func = self.make_filter()
        self._func = func
        return


def parse_filters(criteria, nan_val=None):
    """
    Parse the given criteria to create Filter objects.
    
    Parameters
    ----------
    criteria : Filter/iterable 
        A Filter/valid input to Filter, or an iterable 
        containing multiple Filters/valid inputs to Filter.
        
    Returns
    -------
    filters: tuple
        Parsed Filter objects.
    """
    if isinstance(criteria, Filter):
        filters = (
         criteria,)
    else:
        try:
            filters = (
             Filter(criteria, nan_val),)
        except Exception:
            filters = tuple()
            for c in criteria:
                if isinstance(c, Filter):
                    filters += (c,)
                else:
                    filters += (Filter(c, nan_val),)

    return filters


if __name__ == '__main__':
    fil = Filter(('sum', '>', 3), nan_val=False)
    print fil([5, 3])
    print fil(np.nan)
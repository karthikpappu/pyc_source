# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/commandline/inspect_convenience.py
# Compiled at: 2009-06-12 11:49:41
"""These are convenience wrappers around the functions in "inspect"
They should probably be marked private before release."""
import inspect, types

def get_argnames(func):
    """returns the names of all arguments to func"""
    (argnames, _varargs, _varkw, _defaults) = getargspec(func)
    return argnames


def get_args_with_defaults(func):
    """returns the names of all defaulted arguments to func, 
    paired with their default values."""
    (argnames, _varargs, _varkw, defaults) = getargspec(func)
    num = no_of_compulsary_args(func)
    return zip(argnames[num:], defaults)


def get_compulsary_args(func):
    """returns the names of all arguments to func which *must* be provided."""
    (argnames, _varargs, _varkw, _defaults) = getargspec(func)
    num = no_of_compulsary_args(func)
    return argnames[:num]


def no_of_compulsary_args(func):
    """returns the number of arguments which *must* be provided."""
    (argnames, _varargs, _varkw, defaults) = getargspec(func)
    if defaults:
        num = len(argnames) - len(defaults)
    else:
        num = len(argnames)
    return num


def getargspec(func):
    """ a version of inspect.getargspec that isn't *horribly* broken """
    (argnames, varargs, varkw, defaults) = inspect.getargspec(func)
    if isinstance(func, types.MethodType) and func.im_self is not None:
        argnames = argnames[1:]
    if defaults is None:
        defaults = []
    return (
     argnames, varargs, varkw, defaults)


def get_usage(func, command_name):
    """Takes a function, inspects its signature, and turns it into a usage 
    message compatible with optparse."""
    (argnames, _varargs, _varkw, defaults) = getargspec(func)
    usage = [command_name]
    firstdefault = no_of_compulsary_args(func)
    for (i, argname) in enumerate(argnames):
        if i >= firstdefault:
            usage += [' [%(argname)s' % locals()]
        else:
            usage += [' ' + argname]

    usage += [']' * len(defaults)]
    usage += [' [Options]']
    return ('').join(usage)


def get_doc(func):
    """Just a wrapper around getdoc"""
    return inspect.getdoc(func)
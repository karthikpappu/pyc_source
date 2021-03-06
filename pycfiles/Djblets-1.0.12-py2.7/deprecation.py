# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/djblets/deprecation.py
# Compiled at: 2019-06-12 01:17:17
"""Internal support for handling deprecations in Djblets.

The version-specific objects in this module are not considered stable between
releases, and may be removed at any point. The base objects are considered
stable.
"""
from __future__ import unicode_literals
import warnings
from django.utils.functional import SimpleLazyObject

class BaseRemovedInDjbletsVersionWarning(DeprecationWarning):
    """Base class for a Djblets deprecation warning.

    All version-specific deprecation warnings inherit from this, allowing
    callers to check for Djblets deprecations without being tied to a specific
    version.
    """
    pass


class RemovedInDjblets20Warning(BaseRemovedInDjbletsVersionWarning):
    """Deprecations for features removed in Djblets 2.0.

    Note that this class will itself be removed in Djblets 2.0. If you need to
    check against Djblets deprecation warnings, please see
    :py:class:`BaseRemovedInDjbletsVersionWarning`. Alternatively, you can use
    the alias for this class, :py:data:`RemovedInNextDjbletsVersionWarning`.
    """
    pass


RemovedInNextDjbletsVersionWarning = RemovedInDjblets20Warning

def deprecated_arg_value(owner_name, value, old_arg_name, new_arg_name=None, warning_cls=DeprecationWarning):
    """Wrap a value in a lazy object to warn when used.

    Args:
        owner_name (unicode):
            The name of the owner of this argument.

        value (object):
            The argument value.

        old_arg_name (unicode):
            The name of the argument that was deprecated.

        new_arg_name (unicode, optional):
            The optional name of the argument to use in the deprecated
            argument's place, if one is available.

        warning_cls (type, optional):
            The class to use for the warning. This should be
            :py:exc:`DeprecationWarning`, :py:exc:`PendingDeprecationWarning`,
            or a subclass of one.

    Returns:
        django.utils.functional.SimpleLazyObject:
        The value wrapped in a lazy object. The first time it is accessed,
        a warning will be emitted.
    """

    def _warn_on_use():
        if new_arg_name:
            warnings.warn(b'The "%s" argument for "%s" has been deprecated and will be removed in a future version. Use "%s" instead.' % (
             old_arg_name, owner_name, new_arg_name), warning_cls)
        else:
            warnings.warn(b'The "%s" argument for "%s" has been deprecated and will be removed in a future version.' % (
             old_arg_name, owner_name), warning_cls)
        return value

    return SimpleLazyObject(_warn_on_use)
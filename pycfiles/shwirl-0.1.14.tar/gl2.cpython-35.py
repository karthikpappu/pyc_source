# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/gloo/gl/gl2.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 3132 bytes
""" GL ES 2.0 API implemented via desktop GL (i.e subset of normal OpenGL).
"""
import os, sys, ctypes.util
from . import _copy_gl_functions
from ._constants import *
from ...util import logger
_have_get_proc_address = False
_lib = os.getenv('VISPY_GL_LIB', '')
if _lib != '':
    if sys.platform.startswith('win'):
        _lib = ctypes.windll.LoadLibrary(_lib)
    else:
        _lib = ctypes.cdll.LoadLibrary(_lib)
else:
    if sys.platform.startswith('win'):
        _lib = ctypes.windll.opengl32
        try:
            wglGetProcAddress = _lib.wglGetProcAddress
            wglGetProcAddress.restype = ctypes.CFUNCTYPE(ctypes.POINTER(ctypes.c_int))
            wglGetProcAddress.argtypes = [ctypes.c_char_p]
            _have_get_proc_address = True
        except AttributeError:
            pass

    else:
        if sys.platform.startswith('darwin'):
            _fname = ctypes.util.find_library('OpenGL')
        else:
            _fname = ctypes.util.find_library('GL')
        if not _fname:
            logger.warning('Could not load OpenGL library.')
            _lib = None
        else:
            _lib = ctypes.cdll.LoadLibrary(_fname)

def _have_context():
    return _lib.glGetError() != 1282


def _get_gl_version(_lib):
    """Helper to get the GL version string"""
    try:
        return _lib.glGetString(7938).decode('utf-8')
    except Exception:
        return 'unknown'


def _get_gl_func(name, restype, argtypes):
    if _lib is None:
        raise RuntimeError('Could not load OpenGL library, gl cannot be used')
    try:
        func = getattr(_lib, name)
        func.restype = restype
        func.argtypes = argtypes
        return func
    except AttributeError:
        if sys.platform.startswith('win'):
            fargs = (
             restype,) + argtypes
            ftype = ctypes.WINFUNCTYPE(*fargs)
            if not _have_get_proc_address:
                raise RuntimeError('Function %s not available (OpenGL version is %s).' % (
                 name, _get_gl_version(_lib)))
            if not _have_context():
                raise RuntimeError('Using %s with no OpenGL context.' % name)
            address = wglGetProcAddress(name.encode('utf-8'))
            if address:
                pass
            return ctypes.cast(address, ftype)
        raise RuntimeError('Function %s not present in context (OpenGL version is %s).' % (
         name, _get_gl_version(_lib)))


from . import _gl2
_copy_gl_functions(_gl2, globals())
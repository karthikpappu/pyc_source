# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\g77.py
# Compiled at: 2016-07-07 03:21:35
"""engine.SCons.Tool.g77

Tool-specific initialization for g77.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/g77.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.Util
from SCons.Tool.FortranCommon import add_all_to_env, add_f77_to_env
compilers = [
 'g77', 'f77']

def generate(env):
    """Add Builders and construction variables for g77 to an Environment."""
    add_all_to_env(env)
    add_f77_to_env(env)
    fcomp = env.Detect(compilers) or 'g77'
    if env['PLATFORM'] in ('cygwin', 'win32'):
        env['SHFORTRANFLAGS'] = SCons.Util.CLVar('$FORTRANFLAGS')
        env['SHF77FLAGS'] = SCons.Util.CLVar('$F77FLAGS')
    else:
        env['SHFORTRANFLAGS'] = SCons.Util.CLVar('$FORTRANFLAGS -fPIC')
        env['SHF77FLAGS'] = SCons.Util.CLVar('$F77FLAGS -fPIC')
    env['FORTRAN'] = fcomp
    env['SHFORTRAN'] = '$FORTRAN'
    env['F77'] = fcomp
    env['SHF77'] = '$F77'
    env['INCFORTRANPREFIX'] = '-I'
    env['INCFORTRANSUFFIX'] = ''
    env['INCF77PREFIX'] = '-I'
    env['INCF77SUFFIX'] = ''


def exists(env):
    return env.Detect(compilers)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\ldc.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.ldc

Tool-specific initialization for the LDC compiler.
(http://www.dsource.org/projects/ldc)

Developed by Russel Winder (russel@winder.org.uk)
2012-05-09 onwards

Compiler variables:
    DC - The name of the D compiler to use.  Defaults to ldc2.
    DPATH - List of paths to search for import modules.
    DVERSIONS - List of version tags to enable when compiling.
    DDEBUG - List of debug tags to enable when compiling.

Linker related variables:
    LIBS - List of library files to link in.
    DLINK - Name of the linker to use.  Defaults to ldc2.
    DLINKFLAGS - List of linker flags.

Lib tool variables:
    DLIB - Name of the lib tool to use.  Defaults to lib.
    DLIBFLAGS - List of flags to pass to the lib tool.
    LIBS - Same as for the linker. (libraries to pull into the .lib)
"""
__revision__ = 'src/engine/SCons/Tool/ldc.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os, subprocess, SCons.Action, SCons.Builder, SCons.Defaults, SCons.Scanner.D, SCons.Tool, SCons.Tool.DCommon

def generate(env):
    static_obj, shared_obj = SCons.Tool.createObjBuilders(env)
    static_obj.add_action('.d', SCons.Defaults.DAction)
    shared_obj.add_action('.d', SCons.Defaults.ShDAction)
    static_obj.add_emitter('.d', SCons.Defaults.StaticObjectEmitter)
    shared_obj.add_emitter('.d', SCons.Defaults.SharedObjectEmitter)
    env['DC'] = env.Detect('ldc2')
    env['DCOM'] = '$DC $_DINCFLAGS $_DVERFLAGS $_DDEBUGFLAGS $_DFLAGS -c -of=$TARGET $SOURCES'
    env['_DINCFLAGS'] = '${_concat(DINCPREFIX, DPATH, DINCSUFFIX, __env__, RDirs, TARGET, SOURCE)}'
    env['_DVERFLAGS'] = '${_concat(DVERPREFIX, DVERSIONS, DVERSUFFIX, __env__)}'
    env['_DDEBUGFLAGS'] = '${_concat(DDEBUGPREFIX, DDEBUG, DDEBUGSUFFIX, __env__)}'
    env['_DFLAGS'] = '${_concat(DFLAGPREFIX, DFLAGS, DFLAGSUFFIX, __env__)}'
    env['SHDC'] = '$DC'
    env['SHDCOM'] = '$DC $_DINCFLAGS $_DVERFLAGS $_DDEBUGFLAGS $_DFLAGS -c -relocation-model=pic -of=$TARGET $SOURCES'
    env['DPATH'] = [
     '#/']
    env['DFLAGS'] = []
    env['DVERSIONS'] = []
    env['DDEBUG'] = []
    if env['DC']:
        SCons.Tool.DCommon.addDPATHToEnv(env, env['DC'])
    env['DINCPREFIX'] = '-I='
    env['DINCSUFFIX'] = ''
    env['DVERPREFIX'] = '-version='
    env['DVERSUFFIX'] = ''
    env['DDEBUGPREFIX'] = '-debug='
    env['DDEBUGSUFFIX'] = ''
    env['DFLAGPREFIX'] = '-'
    env['DFLAGSUFFIX'] = ''
    env['DFILESUFFIX'] = '.d'
    env['DLINK'] = '$DC'
    env['DLINKFLAGS'] = SCons.Util.CLVar('')
    env['DLINKCOM'] = '$DLINK -of=$TARGET $DLINKFLAGS $__DRPATH $SOURCES $_DLIBDIRFLAGS $_DLIBFLAGS'
    env['DSHLINK'] = '$DC'
    env['DSHLINKFLAGS'] = SCons.Util.CLVar('$DLINKFLAGS -shared -defaultlib=phobos2-ldc')
    if os.path.exists('/usr/lib64/libphobos-ldc.so') or os.path.exists('/usr/lib32/libphobos-ldc.so') or os.path.exists('/usr/lib/libphobos-ldc.so'):
        env['DSHLINKFLAGS'] = SCons.Util.CLVar('$DLINKFLAGS -shared -defaultlib=phobos-ldc')
    env['SHDLINKCOM'] = '$DLINK -of=$TARGET $DSHLINKFLAGS $__DSHLIBVERSIONFLAGS $__DRPATH $SOURCES $_DLIBDIRFLAGS $_DLIBFLAGS'
    env['DLIBLINKPREFIX'] = '' if env['PLATFORM'] == 'win32' else '-L-l'
    env['DLIBLINKSUFFIX'] = '.lib' if env['PLATFORM'] == 'win32' else ''
    env['_DLIBFLAGS'] = '${_stripixes(DLIBLINKPREFIX, LIBS, DLIBLINKSUFFIX, LIBPREFIXES, LIBSUFFIXES,  __env__)}'
    env['DLIBDIRPREFIX'] = '-L-L'
    env['DLIBDIRSUFFIX'] = ''
    env['_DLIBDIRFLAGS'] = '${_concat(DLIBDIRPREFIX, LIBPATH, DLIBDIRSUFFIX, __env__, RDirs, TARGET, SOURCE)}'
    env['DLIB'] = 'lib' if env['PLATFORM'] == 'win32' else 'ar cr'
    env['DLIBCOM'] = ('$DLIB $_DLIBFLAGS {0}$TARGET $SOURCES $_DLIBFLAGS').format('-c ' if env['PLATFORM'] == 'win32' else '')
    env['DLIBFLAGPREFIX'] = '-'
    env['DLIBFLAGSUFFIX'] = ''
    env['DRPATHPREFIX'] = '-L-rpath='
    env['DRPATHSUFFIX'] = ''
    env['_DRPATH'] = '${_concat(DRPATHPREFIX, RPATH, DRPATHSUFFIX, __env__)}'
    env['_DSHLIBVERSIONFLAGS'] = '$DSHLIBVERSIONFLAGS -L-soname=$_DSHLIBSONAME'
    env['_DSHLIBSONAME'] = '${DShLibSonameGenerator(__env__,TARGET)}'
    env['DShLibSonameGenerator'] = SCons.Tool.ShLibSonameGenerator
    env['DSHLIBVERSION'] = '$SHLIBVERSION'
    env['DSHLIBVERSIONFLAGS'] = []
    SCons.Tool.createStaticLibBuilder(env)


def exists(env):
    return env.Detect('ldc2')
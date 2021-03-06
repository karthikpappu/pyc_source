# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpMayaLib/core/mayapymanager.py
# Compiled at: 2020-01-16 21:52:40
# Size of source mod 2**32: 9834 bytes
"""
Exposes the MayaPyManager class, which is used to run instances of MayaPy with explict control over paths and environment variables. A Manager can run scripts, modules, or command strings in a separate MayaPy environment; results and errors are captured and returned.
Typical uses might be:
- running unit tests
- running a copy of Maya.standalone as a headless RPC server with StandaloneRPC https://github.com/theodox/standaloneRPC
- spawning multipe copies of maya to batch process files in parallel on a multi-core machine
- do any of the above on multiple maya versions concurrently
Basic usage is simply to create a MayaPyManager and then call run_script, run_module or run_command:
    example = MayaPyManager( '/path/to/Maya2014/bin/mayapy.exe', None)
    output, errors = example.run_command("print 'hello world'")
    print output
    > hello world
To control the PYTHONPATH of the created instance, pass the paths you want as a string array to the MayaPyManager. These paths will override the default system paths inside the interpreter.
    example = MayaPyManager( '/path/to/Maya2014/bin/mayapy.exe', None, 'path/to/modules', 'another/path/to/modules', 'etc/etc')
You can also control the environment variables in the interpreter by providing a dictionary:
    custom_env = os.environ.copy()
    custom_env['MAYA_DEBUG'] = 'False'
    custom_env['P4_CLIENT'] = 'test_client'
    example = MayaPyManager( '/path/to/Maya2014/bin/mayapy.exe', custom_env)
PYTHONHOME and PYTHONPATH will be set automatically, so don't bother changing them yourself.
Copyright (c) 2014 Steve Theodore
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import os, subprocess

class MayaPyManager(object):
    __doc__ = "\n    For running a maya python interpreter* under controlled conditions:\n\n        - Override default paths\n        - Overrides environment variables\n        - Disable userSetup.py\n    * Technically this _should_ work for any Python installation, although non-maya\n      versions may not be able to find their standard libraries if these are\n      installed in non-standard locations.\n      See https://docs.python.org/2/tutorial/interpreter.html for more details on interpeter flags\n      Here are the supported flags\n        -B     : don't write .py[co] files on import; also PYTHONDONTWRITEBYTECODE=x\n        -d     : debug output from parser; also PYTHONDEBUG=x\n        -E     : ignore PYTHON* environment variables (such as PYTHONPATH)\n        -O     : optimize generated bytecode slightly; also PYTHONOPTIMIZE=x\n        -OO    : remove doc-strings in addition to the -O optimizations\n        -Q arg : division options: -Qold (default), -Qwarn, -Qwarnall, -Qnew\n        -s     : don't add user site directory to sys.path; also PYTHONNOUSERSITE\n        -S     : don't imply 'import site' on initialization\n        -t     : issue warnings about inconsistent tab usage (-tt: issue errors)\n        -v     : verbose (trace import statements); also PYTHONVERBOSE=x\n                    can be supplied multiple times to increase verbosity\n        -W arg : warning control; arg is action:message:category:module:lineno\n    "
    DEFAULT_FLAGS = []

    def __init__(self, interpreter, environ, *paths, **flags):
        """
        Create a MayaPyManager for ths supplied interpreter and paths
        Arguments:

            -   intepreter is a disk path to a maya python interpreter
            -   environ is a dictionary of environment variables.
                If no dictionary is provided, intepreter will use os.environ.
            -   paths is an array of strings. It will completely replace
                existing PYTHONPATH variables
        Any flag set to True will be used by the intepreter, eg
            MayaPyManager('path/to/mayapy.exe', None, 'path', v=True)
        will produce a command line like:
            path/to/mayapy.exe -v <script.py>
        when run.
        """
        self.interpreter = interpreter
        assert os.path.isfile(interpreter) and os.path.exists(interpreter), "'%s' is not a valid interpreter path" % interpreter
        self.paths = paths
        self.flags = flags
        self.environ = environ

    def run_script(self, pyFile, *args):
        """
        Run the supplied script file in the interpreter.  Returns a tuple (results, errors) which contain,
        respectively, the output and error printouts produced by the script. Note that if errors is not
        None, the script did not complete successfully
        Arguments  will be passed to the script (NOT to the python interpreter). Thus

            someMayaPyMgr.run_script('test/script.py', "hello", "world")

        will be produce a command line like:

           c:/path/to/maya2014/mayapy.exe  test/script.py  hello world
        If the script expects flag -type argument, its up to the user to provide them in the right form:
          someMayaPyMgr.run_script('test/script.py', "-g", "greeting")

        will be produce a command line like:

           c:/path/to/maya2014/mayapy.exe  test/script.py  -g greeting
        """
        rt_env = self._runtime_environment(self.paths)
        arg_string = ''
        if len(args):
            arg_string = ' '.join(map(str, *args))
        flagstring = self._flag_string()
        cmdstring = '"%s" %s "%s" %s' % (self.interpreter, flagstring, pyFile, arg_string)
        runner = subprocess.Popen(cmdstring, env=rt_env, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        return runner.communicate()

    def run_module(self, module):
        """
        Run the supplied moudle file in the interpreter ('running' here is 'importing').
        Returns a tuple (results, errors) which contain, respectively, the output and
        error printouts produced by the module. Note that if errors is not None, the
        module did not import correctly

        The module must in the PYTHONPATH used by the intepreter.
        """
        rt_env = self._runtime_environment(self.paths)
        flagstring = self._flag_string()
        cmdstring = '"%s" %s -m %s' % (self.interpreter, flagstring, module)
        runner = subprocess.Popen(cmdstring, env=rt_env, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        return runner.communicate()

    def run_command(self, cmd):
        """
        Run the supplied command string in the intepreter.
        Returns a tuple (results, errors) which contain, respectively, the output and
        error printouts produced by the command string. Note that if errors is not None,
        the commands did not execute correctly.
        """
        rt_env = self._runtime_environment(self.paths)
        flagstring = self._flag_string()
        cmdstring = '"%s" %s -c "%s"' % (self.interpreter, flagstring, cmd)
        runner = subprocess.Popen(cmdstring, env=rt_env, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        return runner.communicate()

    def _flag_string(self):
        """
        generate correctly formatted flag strings
        """
        flagged = lambda x, y: '-' + x
        flaggedOpt = lambda x, y: '-' + x + ' ' + str(y)
        default_flags = [flagged(f, v) for f, v in self.flags.items() if v if f not in ('W',
                                                                                        'Q')] or ['']
        special_flags = [flaggedOpt(f, v) for f, v in self.flags.items() if v if f in ('W',
                                                                                       'Q')] or ['']
        return ' '.join(default_flags + special_flags)

    def _runtime_environment(self, *new_paths):
        """
        Returns a new environment dictionary for this intepreter, with only the supplied paths
        (and the required maya paths).  Dictionary is independent of machine level settings;
        non maya/python related values are preserved.
        """
        runtime_env = os.environ.copy()
        if self.environ:
            runtime_env = self.environ.copy()
        new_paths = list(self.paths)
        quoted = lambda x: '%s' % os.path.normpath(x)
        runtime_env['MAYA_LOCATION'] = os.path.dirname(self.interpreter)
        runtime_env['PYTHONHOME'] = os.path.dirname(self.interpreter)
        runtime_env['PYTHONPATH'] = ';'.join(map(quoted, new_paths))
        runtime_env['PATH'] = ''
        return runtime_env
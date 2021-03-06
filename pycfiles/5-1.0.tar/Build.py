# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Lib\DistExt\Build.py
# Compiled at: 2006-08-24 15:42:34
import sys, os
from distutils import util, ccompiler
from distutils.command import build
import Util

class Build(build.build):
    __module__ = __name__
    command_name = 'build'
    description = 'build everything needed to install'
    user_options = [
     (
      'build-base=', 'b', 'base directory for build library'), ('build-lib=', None, 'build directory for all distributions'), ('build-scripts=', None, 'build directory for scripts'), ('build-temp=', 't', 'temporary build directory'), ('build-docs=', None, 'build directory for documents'), ('build-l10n=', None, 'build directory for binary message catalogs'), ('compiler=', 'c', 'specify the compiler type'), ('ldflags=', 'l', 'specify additional linker options'), ('debug', 'g', 'compile with debugging information'), ('force', 'f', 'forcibly build everything (ignore file timestamps)'), ('with-docs', None, 'ignored; maintained for compatability'), ('without-docs', None, 'ignored; maintained for compatability')]
    boolean_options = [
     'debug', 'force', 'with-docs', 'without-docs']
    negative_opt = {'without-docs': 'with-docs'}
    help_options = [
     (
      'help-compiler', None, 'list available compilers', ccompiler.show_compilers)]

    def initialize_options(self):
        self.build_base = 'build'
        self.build_lib = None
        self.build_temp = None
        self.build_scripts = None
        self.build_docs = None
        self.build_l10n = None
        self.compiler = None
        self.ldflags = None
        self.debug = None
        self.force = False
        self.with_docs = True
        self.plat_name = None
        return
        return

    def finalize_options(self):
        self.set_undefined_options('config', (
         'compiler', 'compiler'), (
         'debug', 'debug'), (
         'plat_name', 'plat_name'))
        plat_build = '%s.' + self.plat_name + '-' + sys.version[:3]
        plat_build = os.path.join(self.build_base, plat_build)
        if self.debug:
            plat_build += '-debug'
        if self.build_lib is None:
            self.build_lib = plat_build % 'lib'
        if self.build_temp is None:
            self.build_temp = plat_build % 'temp'
        if self.build_scripts is None:
            self.build_scripts = plat_build % 'scripts'
        if self.build_docs is None:
            self.build_docs = os.path.join(self.build_base, 'docs')
        if self.build_l10n is None:
            self.build_l10n = os.path.join(self.build_base, 'locale')
        return
        return

    def run(self):
        self.run_command('config')
        return build.build.run(self)

    def get_source_files(self):
        """
        Called by 'sdist' command.
        """
        files = []
        for (cmd_name, predicate) in self.sub_commands:
            cmd = self.get_finalized_command(cmd_name)
            files.extend(cmd.get_source_files())

        return files

    def has_docs(self):
        return self.distribution.has_docs()

    def has_l10n(self):
        return self.distribution.has_l10n()

    sub_commands = build.build.sub_commands + [('build_docs', has_docs), ('build_l10n', has_l10n)]
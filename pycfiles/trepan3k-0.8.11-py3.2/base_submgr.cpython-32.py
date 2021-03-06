# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trepan/processor/command/base_submgr.py
# Compiled at: 2015-05-27 09:44:41
import inspect, os, re, string, sys, importlib
from trepan.processor.command import base_cmd as Mbase_cmd
from trepan.processor import subcmd as Msubcmd
from trepan.lib import complete as Mcomplete

def abbrev_stringify(name, min_abbrev):
    return '(%s)%s' % (name[:min_abbrev], name[min_abbrev:])


def capitalize(s):
    if s:
        return s[0].upper() + s[1:]
    else:
        return s


class SubcommandMgr(Mbase_cmd.DebuggerCommand):
    category = 'status'
    min_args = 0
    max_args = None
    name = '???'
    need_stack = False

    def __init__(self, proc, name=None):
        """Initialize show subcommands. Note: instance variable name
        has to be setcmds ('set' + 'cmds') for subcommand completion
        to work."""
        Mbase_cmd.DebuggerCommand.__init__(self, proc)
        if name is None:
            name = self.__module__.split('.')[(-1)]
        self.__class__.name = name
        self.cmds = Msubcmd.Subcmd(name, self)
        self.name = name
        self._load_debugger_subcommands(name)
        self.proc = proc
        return

    def _load_debugger_subcommands(self, name):
        """ Create an instance of each of the debugger
        subcommands. Commands are found by importing files in the
        directory 'name' + 'sub'. Some files are excluded via an array set
        in __init__.  For each of the remaining files, we import them
        and scan for class names inside those files and for each class
        name, we will create an instance of that class. The set of
        DebuggerCommand class instances form set of possible debugger
        commands."""
        cmd_instances = []
        class_prefix = capitalize(name)
        module_dir = 'trepan.processor.command.%s_subcmd' % name
        mod = __import__(module_dir, None, None, ['*'])
        eval_cmd_template = 'command_mod.%s(self)'
        for module_name in mod.__modules__:
            import_name = module_dir + '.' + module_name
            try:
                command_mod = importlib.import_module(import_name)
            except ImportError:
                print('Error importing name %s module %s: %s' % (
                 import_name, module_name, sys.exc_info()[0]))
                continue

            classnames = [classname for classname, classvalue in inspect.getmembers(command_mod, inspect.isclass) if 'DebuggerCommand' != classname and classname.startswith(class_prefix)]
            for classname in classnames:
                eval_cmd = eval_cmd_template % classname
                try:
                    instance = eval(eval_cmd)
                    self.cmds.add(instance)
                except:
                    print("Error eval'ing class %s" % classname)

        return cmd_instances

    def help(self, args):
        """Give help for a command which has subcommands. This can be
        called in several ways:
            help cmd
            help cmd subcmd
            help cmd commands

        Our shtick is to give help for the overall command only if
        subcommand or 'commands' is not given. If a subcommand is given and
        found, then specific help for that is given. If 'commands' is given
        we will list the all the subcommands.
        """
        if len(args) <= 2:
            doc = self.__doc__ or self.run.__doc__
            if doc:
                self.rst_msg(doc.rstrip('\n'))
            else:
                self.proc.intf[(-1)].errmsg('Sorry - author mess up. ' + 'No help registered for command' + self.name)
            return
        subcmd_name = args[2]
        if '*' == subcmd_name:
            self.section("List of subcommands for command '%s':" % self.name)
            self.msg(self.columnize_commands(self.cmds.list()))
            return
        cmd = self.cmds.lookup(subcmd_name)
        if cmd:
            doc = cmd.__doc__ or cmd.run.__doc__
            if doc:
                self.proc.rst_msg(doc.rstrip('\n'))
            else:
                self.proc.intf[(-1)].errmsg('Sorry - author mess up. No help registered for subcommand %s of command %s' % (
                 subcmd_name, self.name))
        else:
            cmds = [c for c in self.cmds.list() if re.match('^' + subcmd_name, c)]
            if cmds == []:
                self.errmsg('No %s subcommands found matching /^%s/. Try "help".' % (
                 self.name, subcmd_name))
            else:
                self.section('Subcommand(s) of "%s" matching /^%s/:' % (
                 self.name, subcmd_name))
                self.msg_nocr(self.columnize_commands(cmds))

    def complete(self, prefix):
        return Mcomplete.complete_token(self.subcmds.subcmds.keys(), prefix)

    def complete_token_with_next(self, prefix):
        result = Mcomplete.complete_token_with_next(self.cmds.subcmds, prefix)
        return result

    def run(self, args):
        """Ooops -- the debugger author didn't redefine this run docstring."""
        if len(args) < 2:
            self.section('List of %s commands (with minimum abbreviation in parenthesis):' % self.name)
            for subcmd_name in self.cmds.list():
                subcmd = self.cmds.subcmds[subcmd_name]
                self.summary_help(subcmd_name, subcmd)

            return False
        else:
            subcmd_prefix = args[1]
            subcmd = self.cmds.lookup(subcmd_prefix)
            if subcmd:
                nargs = len(args) - 2
                if nargs < subcmd.min_args:
                    self.errmsg(("Subcommand '%s %s' needs at least %d argument(s); " + 'got %d.') % (
                     self.name, subcmd.name, subcmd.min_args, nargs))
                    return False
                if subcmd.max_args is not None and nargs > subcmd.max_args:
                    self.errmsg(("Subcommand '%s %s' takes at most %d argument(s); " + 'got %d.') % (
                     self.name, subcmd.name, subcmd.max_args, nargs))
                    return False
                return subcmd.run(args[2:])
            else:
                return self.undefined_subcmd(self.name, subcmd_prefix)
            return

    def summary_help(self, subcmd_name, subcmd):
        self.msg_nocr('  %-12s -- ' % abbrev_stringify(subcmd_name, subcmd.min_abbrev))
        self.rst_msg(subcmd.short_help.rstrip('\n'))

    def undefined_subcmd(self, cmd, subcmd):
        """Error message when subcommand asked for but doesn't exist"""
        self.proc.intf[(-1)].errmsg(('Undefined "%s" subcommand: "%s". ' + 'Try "help %s *".') % (cmd, subcmd, cmd))


if __name__ == '__main__':
    pass
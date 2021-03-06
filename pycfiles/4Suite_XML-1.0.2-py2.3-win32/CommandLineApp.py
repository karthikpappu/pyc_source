# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Lib\CommandLine\CommandLineApp.py
# Compiled at: 2006-12-03 00:43:03
"""
Base class for a command-line application, which is a type of Command

Copyright 2003 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import sys, os
from Ft import GetConfigVars
from Ft.Lib.CommandLine import Options, Command, CommandLineUtil, CONSOLE_WIDTH

class CommandLineApp(Command.Command):
    __module__ = __name__
    project_name = None
    project_version = None
    project_url = None
    global_options = [
     Options.Option('h', 'help', 'show detailed help message'),
     Options.Option('V', 'version', 'display version information and exit')]
    name = None
    summary = None
    description = None
    example = None
    options = None
    arguments = None
    commands = None

    def __init__(self):
        self.script_name = None
        self.script_args = None
        self.stream = sys.stdout
        if __debug__:
            for attr in ('name', 'summary', 'description'):
                value = getattr(self, attr)
                if not isinstance(value, str):
                    tp_name = value is None and 'None' or type(value).__name__
                    raise TypeError('%r must be a string, not %s' % (name, tp_name))

        if self.options:
            global_options = self.global_options[:]
            global_options.extend(self.options)
        else:
            global_options = self.global_options
        if self.commands:
            options = self.global_options[:]
            options.append(Options.Option(None, 'show-commands', 'show system command tree'))
        else:
            options = global_options
        filename = sys.modules[self.__class__.__module__].__file__
        Command.Command.__init__(self, self.name, self.summary, self.example, self.description, None, options, self.arguments, self.commands, filename)
        if self.commands:
            commands = self.flatten_command_tree(0)
            for (level, cmd, fullName) in commands[1:]:
                cmd.options[0:0] = global_options

        return
        return

    def main(cls, argv=None):
        if argv is None:
            argv = sys.argv
        script_name = argv[0]
        script_args = argv[1:]
        return cls().run_commands(script_name, script_args)
        return

    main = classmethod(main)

    def run_commands(self, script_name=None, script_args=None):
        """
        Parse the command line and attempt to run the command.
        Typically overridden in the subclasses.
        """
        if not script_name:
            self.script_name = sys.argv[0]
        else:
            self.script_name = script_name
        self.script_name = os.path.basename(self.script_name or '')
        if not script_args:
            self.script_args = sys.argv[1:]
        else:
            self.script_args = script_args
        parsed = self.parse_command_line()
        if parsed:
            (cmd, options, args) = parsed
            try:
                status = cmd.run(options, args)
            except SystemExit, e:
                status = e.code
                if not isinstance(status, int):
                    print >> sys.stderr, str(e)
                    status = 1
            except KeyboardInterrupt:
                print >> sys.stderr, 'interrupted'
                status = 130
            except ImportError, e:
                print >> sys.stderr, str(e)
                status = 1

        else:
            status = 0
        return status

    def parse_command_line(self):
        """
        Parse the command line.
        """
        try:
            parsed = self._parse_command_opts(self.script_args)
        except CommandLineUtil.ArgumentError, err:
            if len(err.args) > 1:
                cmd = err.args[0]
                errmsg = err.args[1]
            else:
                errmsg = err.args[0]
            if errmsg:
                command_path = self.script_name
                for cmd in self._build_command_path(cmd):
                    command_path += ' ' + cmd.name

                raise SystemExit("%s: %s\nTry '%s --help' for more information." % (command_path, errmsg, command_path))
            else:
                help = self.gen_usage(cmd)
                raise SystemExit(help)

        return parsed

    def validate_options(self, options):
        if 'version' in options:
            print >> self.stream, self._get_version()
            return False
        if self.subCommands and 'show-commands' in options:
            print >> self.stream, self.gen_command_tree()
            return False
        return Command.Command.validate_options(self, options)

    def _get_version(self, name=None):
        if name is None:
            name = self.name
        version_string = name
        if self.project_name:
            version_string += ', from ' + self.project_name
            if self.project_version:
                version_string += ' ' + self.project_version
        if self.project_url:
            version_string += '; see %s' % self.project_url
        return version_string
        return

    def gen_usage(self, command=None):
        """
        Generate usage info. This includes description, command line,
        options, and subcommands or arguments.
        """
        command = command or self
        command_string = self.script_name
        for cmd in self._build_command_path(command):
            command_string += ' ' + cmd.name

        lines = [self._get_version(command_string)]
        description = CommandLineUtil.wrap_text(command.verbose_description, CONSOLE_WIDTH - 4)
        lines.extend([ '  %s' % line for line in description ])
        lines.append('\nUsage:')
        lines.extend(command._gen_usage('  %s ' % command_string))
        lines.append('')
        return ('\n').join(lines)

    def gen_command_tree(self):
        """
        Generate the command tree (a show all commands look)
        """
        commands = self.flatten_command_tree(0)
        max_cmd = 0
        for (level, cmd, fullName) in commands:
            if len(cmd.name) + level * 2 > max_cmd:
                max_cmd = len(cmd.name) + level * 2

        col_width = max_cmd + 2
        text_width = CONSOLE_WIDTH - col_width
        big_indent = ' ' * col_width
        lines = []
        last_level = 0
        first_level = 1
        for (level, cmd, fullName) in commands:
            if last_level > level or level == 0:
                lines.append('')
            last_level = level
            indent = '  ' * level
            padding = max_cmd - level * 2
            text = CommandLineUtil.wrap_text(cmd.description, text_width)
            lines.append('%s%-*s  %s' % (indent, padding, cmd.name, text[0]))
            for line in text[1:]:
                lines.append(big_indent + line)

            if first_level:
                lines.append('')
                lines.append('Available Commands:')
                lines.append('')
                first_level = 0

        lines.append('\nTo see help on a specific command:\n')
        lines.append('  %s command [subcommand]... --help\n' % self.script_name)
        return ('\n').join(lines)

    def get_help_doc_info(self):
        return map(lambda x: (x[2], x[1]), self.flatten_command_tree(0))

    def _build_command_path(self, command):
        self.build_parent_relationship()
        path = []
        cur = command
        while cur != self:
            path.append(cur)
            cur = cur.parent

        path.reverse()
        self.break_parent_relationship()
        return path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise SystemExit('%s: output filename required' % self.name)
    answer = raw_input('Are you sure (yes/no)? ')
    if answer == 'yes':
        open(sys.argv[1], 'w').write(GenHtml())
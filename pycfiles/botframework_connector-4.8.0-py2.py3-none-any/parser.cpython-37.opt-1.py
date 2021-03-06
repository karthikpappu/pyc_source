# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /botfly/parser.py
# Compiled at: 2019-12-01 19:22:12
# Size of source mod 2**32: 7562 bytes
__doc__ = 'Command parser module. Default is a simple, POSIX-like command parsing.\n'
__all__ = [
 'CommandParser']
import sys, os
from prompt_toolkit.completion import Completer, Completion
from . import exceptions
from . import controller
from .fsm import FSM, ANY

class CommandCompleter(Completer):

    def __init__(self, words):
        self.words = words

    def get_completions(self, document, complete_event):
        word_before_cursor = document.text_before_cursor
        for word in self.words:
            if word.startswith(word_before_cursor):
                yield Completion(word, (-len(word_before_cursor)), display_meta='command')


class CommandParser:
    """CommandParser"""
    VARCHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_?'
    _SPECIAL = {'r':'\r',  'n':'\n',  't':'\t',  'b':'\x08'}

    def __init__(self, controller=None, historyfile=None):
        if historyfile:
            self._historyfile = os.path.expanduser(os.path.expandvars(str(historyfile)))
        else:
            self._historyfile = None
        if self._historyfile:
            pass
        self.initialize()
        self.reset(controller)

    def close(self):
        self.reset()

    def reset(self, newcontroller=None):
        self._controllers = []
        self._controller = None
        self.arg_list = []
        self._buf = ''
        if newcontroller:
            self.push_controller(newcontroller)

    def push_controller(self, newcontroller):
        lvl = int(newcontroller.environ.setdefault('SHLVL', 0))
        newcontroller.environ['SHLVL'] = lvl + 1
        self._controllers.append(newcontroller)
        self._controller = newcontroller
        cmdlist = newcontroller.get_command_names()
        newcontroller.add_completion_scope('commands', CommandCompleter(cmdlist))
        newcontroller.add_completion_scope('help', CommandCompleter(cmdlist))

    def pop_controller(self, returnval=None):
        cont = self._controllers.pop()
        cont.finalize()
        if self._controllers:
            self._controller = self._controllers[(-1)]
            if returnval is not None:
                self._controller.handle_subcommand_exit(returnval)
        else:
            raise exceptions.CommandQuit('last command object quit.')

    def interact(self):
        try:
            while True:
                ui = self._controller._ui
                try:
                    line = ui.user_input(completer=(self._controller.get_completion_scope('commands')))
                    if not line:
                        continue
                    while self.feed(line + '\n'):
                        line = ui.more_user_input()

                except EOFError:
                    self._controller._ui.write('\n')
                    self.pop_controller()

        except (exceptions.CommandQuit, exceptions.CommandExit):
            pass

    def feed(self, text):
        text = self._buf + text
        i = 0
        for c in text:
            i += 1
            try:
                self._fsm.process(c)
                while self._fsm.stack:
                    self._fsm.process(self._fsm.pop())

            except EOFError:
                self.pop_controller()
            except exceptions.CommandQuit:
                val = sys.exc_info()[1]
                self.pop_controller(val.value)
            except exceptions.NewCommand as cmdex:
                try:
                    self.push_controller(controller.CommandController(cmdex.value))
                finally:
                    cmdex = None
                    del cmdex

        if self._fsm.current_state:
            self._buf = text[i:]
        return self._fsm.current_state

    def initialize(self):
        f = FSM(0)
        f.arg = ''
        f.add_default_transition(self._error, 0)
        f.add_transition(ANY, 0, self._addtext, 0)
        f.add_transitions(' \t', 0, self._wordbreak, 0)
        f.add_transitions(';\n', 0, self._doit, 0)
        f.add_transition('\\', 0, None, 1)
        f.add_transition('\\', 3, None, 6)
        f.add_transition(ANY, 1, self._slashescape, 0)
        f.add_transition(ANY, 6, self._slashescape, 3)
        f.add_transition('$', 0, self._startvar, 7)
        f.add_transition('{', 7, self._vartext, 9)
        f.add_transitions(self.VARCHARS, 7, self._vartext, 7)
        f.add_transition(ANY, 7, self._endvar, 0)
        f.add_transition('}', 9, self._endvar, 0)
        f.add_transition(ANY, 9, self._vartext, 9)
        f.add_transition('$', 3, self._startvar, 8)
        f.add_transition('{', 8, self._vartext, 10)
        f.add_transitions(self.VARCHARS, 8, self._vartext, 8)
        f.add_transition(ANY, 8, self._endvar, 3)
        f.add_transition('}', 10, self._endvar, 3)
        f.add_transition(ANY, 10, self._vartext, 10)
        f.add_transition("'", 0, None, 2)
        f.add_transition("'", 2, self._singlequote, 0)
        f.add_transition(ANY, 2, self._addtext, 2)
        f.add_transition('"', 0, None, 3)
        f.add_transition('"', 3, self._doublequote, 0)
        f.add_transition(ANY, 3, self._addtext, 3)
        f.add_transition("'", 3, None, 5)
        f.add_transition("'", 5, self._singlequote, 3)
        f.add_transition(ANY, 5, self._addtext, 5)
        self._fsm = f

    def _startvar(self, c, fsm):
        fsm.varname = c

    def _vartext(self, c, fsm):
        fsm.varname += c

    def _endvar(self, c, fsm):
        if c == '}':
            fsm.varname += c
        else:
            fsm.push(c)
        try:
            val = self._controller.environ.get(fsm.varname, '')
        except:
            ex, val, tb = sys.exc_info()
            self._controller._ui.error('Could not expand variable {!r}: {} ({})'.format(fsm.varname, ex, val))
        else:
            if val is not None:
                fsm.arg += str(val)

    def _error(self, input_symbol, fsm):
        self._controller._ui.error('Syntax error: {}\n{!r}'.format(input_symbol, fsm.stack))
        fsm.reset()

    def _addtext(self, c, fsm):
        fsm.arg += c

    def _wordbreak(self, c, fsm):
        if fsm.arg:
            self.arg_list.append(fsm.arg)
            fsm.arg = ''

    def _slashescape(self, c, fsm):
        fsm.arg += CommandParser._SPECIAL.get(c, c)

    def _singlequote(self, c, fsm):
        self.arg_list.append(fsm.arg)
        fsm.arg = ''

    def _doublequote(self, c, fsm):
        self.arg_list.append(fsm.arg)
        fsm.arg = ''

    def _doit(self, c, fsm):
        if fsm.arg:
            self.arg_list.append(fsm.arg)
            fsm.arg = ''
        args = self.arg_list
        self.arg_list = []
        self._controller.call(args)
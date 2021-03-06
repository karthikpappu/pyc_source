# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ptysh_main.py
# Compiled at: 2016-08-03 23:00:14
import readline
from ptysh_base import Parser
from ptysh_base import BasicCommand
from ptysh_base import Autocompleter
from ptysh_util import Signal
from ptysh_util import IoControl

def auto_completer(in_text, in_state):
    options = [ i for i in Autocompleter().get_cmd_list() if i.startswith(in_text) ]
    if in_state < len(options):
        return options[in_state]
    else:
        return


def main():
    Signal().set_signal()
    readline.parse_and_bind('tab: complete')
    readline.set_completer(auto_completer)
    io = IoControl()
    io.print_hello_message()
    BasicCommand()
    while True:
        io.set_prompt()
        Parser().parse_command_line(io.get_input_command())


if __name__ == '__main__':
    main()
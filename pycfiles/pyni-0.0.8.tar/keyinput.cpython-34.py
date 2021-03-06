# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/keyinput.py
# Compiled at: 2015-07-09 21:30:20
# Size of source mod 2**32: 1405 bytes


def tokenize_keypresses(input_str):
    keypresses = []
    key_mode = False
    current_sequence = KeySequence()
    current_key = ''
    for i, char in enumerate(input_str):
        if char == '{':
            if key_mode:
                if input_str[(i - 1)] != '{':
                    raise ValueError("invalid keypress string '{}'".format(input_str))
                else:
                    keypresses.append('{')
            key_mode = not key_mode
        elif char == '}':
            if key_mode:
                if current_key:
                    current_sequence.keys.append(current_key)
                    keypresses.append(current_sequence)
                    current_sequence = KeySequence()
                    current_key = ''
            else:
                if i + 1 == len(input_str) or input_str[(i + 1)] != '}':
                    raise ValueError("invalid keypress string '{}'".format(input_str))
                keypresses.append('}')
            key_mode = not key_mode
        elif key_mode:
            if char == '+':
                if current_key:
                    current_sequence.keys.append(current_key)
                    current_key = ''
                else:
                    raise ValueError("invalid keypress string '{}'".format(input_str))
            else:
                current_key += char
        else:
            keypresses.append(char)

    if key_mode:
        raise ValueError("invalid keypress string '{}'".format(input_str))
    return keypresses


class KeySequence:

    def __init__(self, key_name=None):
        if key_name is None:
            self.keys = []
        else:
            self.keys = [
             key_name]

    def __str__(self):
        return '<KeySequence: {}>'.format('+'.join(self.keys))

    def __repr__(self):
        return str(self)
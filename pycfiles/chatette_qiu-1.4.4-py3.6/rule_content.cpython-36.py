# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\units\word\rule_content.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2510 bytes
from chatette_qiu.units import Example, RuleContent, may_change_leading_case
from chatette_qiu.parsing.parser_utils import add_escapement_back_in_word

class WordRuleContent(RuleContent):
    __doc__ = '\n    Represents a word inside a rule\n    Accepted modifiers:\n        - leading-space: bool\n    '

    def __init__(self, name, leading_space=False, variation_name=None, arg_value=None, casegen=False, randgen=None, percentage_gen=None, parser=None):
        if variation_name is not None:
            raise SyntaxError("Words cannot have variations, yet '" + name + "' does (unescaped '#'?)")
        else:
            if arg_value is not None:
                raise SyntaxError("Words cannot have an argument, yet '" + name + "' does (unescaped ':'?)")
            else:
                if casegen:
                    raise SyntaxError("Words cannot generate different cases, yet '" + name + "' does (unescaped '&'?)")
                if randgen is not None or percentage_gen is not None:
                    raise SyntaxError("Words cannot have a random generation modifier, yet '" + name + "' does (unescaped '?'?)")
            if parser is not None:
                raise RuntimeError('Internal error: tried to create a word ' + 'with a pointer to the parser')
        super(WordRuleContent, self).__init__(name, leading_space=leading_space, variation_name=None,
          arg_value=None,
          casegen=False,
          randgen=None,
          percentage_gen=None,
          parser=None)
        self.word = name

    def can_have_casegen(self):
        return may_change_leading_case(self.word)

    def get_max_nb_generated_examples(self):
        return 1

    def generate_random(self, arg_value=None):
        if self.leading_space:
            return Example(' ' + self.word)
        else:
            return Example(self.word)

    def generate_all(self):
        if self.leading_space:
            return [Example(' ' + self.word)]
        else:
            return [
             Example(self.word)]

    def as_string(self):
        """
        Returns the representation of the rule
        as it would be written in a template file.
        """
        if self.leading_space:
            return ' ' + add_escapement_back_in_word(self.name)
        else:
            return add_escapement_back_in_word(self.name)
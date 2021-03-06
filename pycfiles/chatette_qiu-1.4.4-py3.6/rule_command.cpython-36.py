# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\cli\interactive_commands\rule_command.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2148 bytes
"""
Module `chatette_qiu.cli.interactive_commands.rule_command`.
Contains the strategy class that represents the interactive mode command
`rule` which generates as many examples as asked that the provided rule
can generate.
"""
from chatette_qiu.cli.interactive_commands.command_strategy import CommandStrategy
from chatette_qiu.units.alias.definition import AliasDefinition
from chatette_qiu.units import ENTITY_MARKER

class RuleCommand(CommandStrategy):

    def execute(self, facade):
        """
        Implements the command `rule` which generates a certain number of
        examples according to a provided rule.
        """
        if len(self.command_tokens) < 2:
            self.print_wrapper.error_log('Missing some arguments\nUsage: ' + 'rule "<rule>" [<number-of-examples]')
            return
        else:
            rule_str = CommandStrategy.remove_quotes(self.command_tokens[1])
            nb_examples = None
            if len(self.command_tokens) >= 3:
                try:
                    nb_examples = int(self.command_tokens[2])
                except ValueError:
                    self.print_wrapper.error_log('The number of examples asked (' + self.command_tokens[2] + ') is ' + 'a valid integer.')

            rule_tokens = facade.parser.tokenizer.tokenize(rule_str)
            rule = facade.parser.tokens_to_sub_rules(rule_tokens)
            definition = AliasDefinition('INTERNAL', None, [rule])
            try:
                examples = definition.generate_nb_examples(nb_examples)
                self.print_wrapper.write('Generated examples:')
                for ex in examples:
                    self.print_wrapper.write(ex.text.replace(ENTITY_MARKER, ''))

            except KeyError as e:
                self.print_wrapper.error_log('Upon generation: ' + str(e))

    def execute_on_unit(self, facade, unit_type, unit_name, variation_name=None):
        raise NotImplementedError()

    def finish_execution(self, facade):
        raise NotImplementedError()
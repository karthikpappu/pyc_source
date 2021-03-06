# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nicfit/shell/completion.py
# Compiled at: 2019-12-01 16:28:10
# Size of source mod 2**32: 4052 bytes
import uuid, shlex
from pprint import pformat
from prompt_toolkit.completion import Completion
from prompt_toolkit.contrib.regular_languages.compiler import compile
import prompt_toolkit.completion as BaseWordCompleter
from prompt_toolkit.contrib.regular_languages.completion import GrammarCompleter
from ..logger import getLogger
log = getLogger(__name__)

def _updateCompleterDict(completers, cdict, regex=None):
    """Merges ``cdict`` into ``completers``. In the event that a key
        in cdict already exists in the completers dict a ValueError is raised
        iff ``regex`` false'y. If a regex str is provided it and the duplicate
        key are updated to be unique, and the updated regex is returned.
        """
    for key in cdict:
        if key in completers:
            if not regex:
                raise ValueError(f"Duplicate completion key: {key}")
        if key in completers:
            uniq = '_'.join([key, str(uuid.uuid4()).replace('-', '')])
            regex = regex.replace(f"P<{key}>", f"P<{uniq}>")
            completers[uniq] = cdict[key]
        else:
            completers[key] = cdict[key]
    else:
        return regex


def makeCompleter(commands: list, word_completers: dict=None):
    grammars = []
    cmd_words = []
    cmd_completers = dict(word_completers) if word_completers else {}
    for cmd in set([c for c in commands if hasattr(c, 'grammar')]):
        cmd_grammar = cmd.grammar(cmd_completers)
        if cmd_grammar:
            cmd_words += [cmd.name()] + cmd.aliases()
            grammars.append(cmd_grammar)
        grammars = '|\n'.join(grammars)
        log.debug(f"Completer grammar:\n{grammars}")
        _updateCompleterDict(cmd_completers, {'HELP_OPTS':WordCompleter(['-h', '--help']), 
         'cmd':WordCompleter(cmd_words)})
        log.debug(f"Completer dict:\n{pformat(cmd_completers)}")
        return GrammarCompleter(compile(grammars), cmd_completers)


class WordCompleter(BaseWordCompleter):

    def __init__(self, words, ignore_case=False, meta_dict=None, WORD=False, sentence=True, match_middle=True, quote_if=None):
        self._words_callable = words if callable(words) else None
        if self._words_callable:
            words = self._words_callable()
        self.quote_if = quote_if
        super().__init__(words, ignore_case, meta_dict, WORD, sentence, match_middle)

    def quote(self, s):
        for q in self.quote_if or []:
            if q in s:
                s = shlex.quote(s)
            return s

    def get_completions(self, document, complete_event):
        if self.sentence:
            word_before_cursor = document.text_before_cursor
        else:
            word_before_cursor = document.get_word_before_cursor(WORD=(self.WORD))
        if self.ignore_case:
            word_before_cursor = word_before_cursor.lower()

        def word_matches(word):
            if self.ignore_case:
                word = word.lower()
            if self.match_middle:
                return word_before_cursor in word
            return word.startswith(word_before_cursor)

        words = self._words_callable() if self._words_callable else self.words
        for a in words:
            if word_matches(a):
                display_meta = self.meta_dict.get(a, '')
                log.debug(f"MATCH: {a}, {-len(word_before_cursor)}, meta: {display_meta}")
                (yield Completion((self.quote(a)), (-len(word_before_cursor)), display_meta=display_meta))
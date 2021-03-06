# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\parsing\tokenizer.py
# Compiled at: 2019-03-27 03:03:24
# Size of source mod 2**32: 12447 bytes
__doc__ = '\nModule `chatette_qiu.parsing.tokenizer`\nContains the tokenizer used by the parser.\n'
import os, chatette_qiu.parsing.parser_utils as pu
from chatette_qiu.parsing.line_count_file_wrapper import LineCountFileWrapper

class Tokenizer(object):

    def __init__(self, master_filename):
        self.master_file_paths = [
         master_filename]
        self.master_file_dir = os.path.dirname(master_filename)
        self.current_file = LineCountFileWrapper(master_filename)
        self._opened_files = []
        self._last_read_line = None

    def redefine_master_file(self, master_filename):
        """
        Change the master file and open it.
        If other files are still open, raise an exception.
        """
        if len(self._opened_files) > 0:
            raise ValueError('Tried to change master file during parsing of ' + 'other files')
        self.master_file_paths.append(master_filename)
        self.master_file_dir = os.path.dirname(master_filename)
        self.current_file = LineCountFileWrapper(master_filename)

    def open_file(self, filename):
        """
        Stores the current file for future use and opens `filename`.
        `filename` is given relatively to the master file.
        """
        filepath = os.path.join(os.path.dirname(self.current_file.name), filename)
        opened_filepaths = [f.name for f in self._opened_files]
        if filepath in opened_filepaths:
            raise ValueError("Tried to parse file '" + filepath + "' several " + "times (last time when parsing '" + self.current_file.name + "'). There seems to be circular includes in " + 'template files.')
        if self.current_file is not None:
            self._opened_files.append(self.current_file)
        self.current_file = LineCountFileWrapper(filepath)

    def close_files(self):
        for f in self._opened_files:
            if not f.closed:
                f.close()

        if self.current_file is not None:
            if not self.current_file.closed:
                self.current_file.close()

    def close_current_file(self):
        if self.current_file is not None:
            self.current_file.close()
        else:
            if len(self._opened_files) > 0:
                self.current_file = self._opened_files.pop()
            else:
                self.current_file = None

    def get_file_information(self):
        return (self.current_file.name, self.current_file.line_nb)

    def fail(self, exception):
        """Closes all files before raising an exception."""
        self.close_files()
        raise exception

    def syntax_error(self, message, line=None, line_index=0, word_to_find=None):
        """Makes an exception to be raised after closing all files."""
        if line is None:
            line = self._last_read_line
        if word_to_find is not None:
            line_index = line.find(word_to_find)
        exception = SyntaxError(message, (self.current_file.name,
         self.current_file.line_nb,
         line_index, line))
        self.fail(exception)

    def read_line(self):
        """
        Reads a line of `self.current_file` and returns it without the trailing
        new line (`
`).
        If the file was entirely read, closes it and continues to read the
        file that was previously being read (returning its next line).
        Returns `None` if there is no file left to read.
        """
        line = self.current_file.readline()
        while line == '':
            self.close_current_file()
            if self.current_file is None:
                return
            line = self.current_file.readline()

        line = line.rstrip()
        self._last_read_line = line
        return line

    def next_tokenized_line(self):
        """
        Yields the next relevant line of the current file as a list of tokens.
        An irrelevant line is an empty or comment line.
        """
        while True:
            line_str = pu.strip_comments(self.read_line())
            if line_str is None:
                break
            if line_str == '':
                pass
            else:
                yield self.tokenize(line_str)

    def tokenize(self, text):
        """
        Returns a tokenized version of the string `text`,
        i.e. a list of strings that make up words or special characters.
        The string `~[alias?] word. [&group]` would be tokenized into
        `["~", "[", "alias", "?", "]", " ", "word.", "[", "&", "group", "]"]`.
        @pre: `text` is not `None` or ''.
        """
        tokens = []
        current_token = ''

        def store_current_token():
            if current_token != '':
                tokens.append(current_token)
            return ''

        indentation = Tokenizer._get_indentation(text)
        if indentation is not None:
            tokens.append(indentation)
            text = text.lstrip()
        if indentation is None:
            if text[0] == pu.INCLUDE_FILE_SYM:
                return [
                 pu.INCLUDE_FILE_SYM, text[1:]]
        nb_closing_brackets_expected = 0
        expecting_percent_gen = False
        after_unit_declaration = False
        inside_annotation = False
        inside_choice = False
        next_char_escaped = False
        i = 0
        for i, c in enumerate(text):
            if next_char_escaped:
                current_token += c
                next_char_escaped = False
            elif c == pu.ESCAPE_SYM:
                current_token += c
                next_char_escaped = True
            elif c == pu.ALIAS_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif c == pu.SLOT_SYM:
                current_token = store_current_token()
                tokens.append(c)
            elif c == pu.INTENT_SYM:
                current_token = store_current_token()
                tokens.append(c)
            else:
                if c == pu.UNIT_OPEN_SYM:
                    current_token = store_current_token()
                    tokens.append(c)
                    nb_closing_brackets_expected += 1
                else:
                    if c == pu.UNIT_CLOSE_SYM:
                        if nb_closing_brackets_expected < 1:
                            self.syntax_error('Inconsistent use of unit brackets ' + "(too many closing unit symbols '" + pu.UNIT_CLOSE_SYM + "').", text, i)
                        current_token = store_current_token()
                        tokens.append(c)
                        nb_closing_brackets_expected -= 1
                        if indentation is None and nb_closing_brackets_expected == 0:
                            after_unit_declaration = True
                    else:
                        if c == pu.CHOICE_OPEN_SYM:
                            if inside_choice:
                                self.syntax_error('Nested choices are not supported. ' + "Did you mean to escape it ('" + pu.ESCAPE_SYM + pu.CHOICE_OPEN_SYM + "' instead of '" + pu.CHOICE_OPEN_SYM + "'?", text, i)
                            current_token = store_current_token()
                            tokens.append(c)
                            inside_choice = True
                        else:
                            if c == pu.CHOICE_CLOSE_SYM:
                                if not inside_choice:
                                    self.syntax_error('Cannot close a choice before ' + 'opening it. Did you mean to escape ' + "it ('" + pu.ESCAPE_SYM + pu.CHOICE_CLOSE_SYM + "' instead of '" + pu.CHOICE_CLOSE_SYM + "'?", text, i)
                                current_token = store_current_token()
                                tokens.append(c)
                                inside_choice = False
                            elif inside_choice:
                                if c == pu.CHOICE_SEP:
                                    current_token = store_current_token()
                                    tokens.append(c)
                            else:
                                if nb_closing_brackets_expected > 0:
                                    if c == pu.VARIATION_SYM:
                                        current_token = store_current_token()
                                        tokens.append(c)
                                else:
                                    if nb_closing_brackets_expected > 0:
                                        if c == pu.RAND_GEN_SYM:
                                            current_token = store_current_token()
                                            tokens.append(c)
                                            expecting_percent_gen = True
                                    else:
                                        if nb_closing_brackets_expected > 0:
                                            if expecting_percent_gen:
                                                if c == pu.PERCENT_GEN_SYM:
                                                    current_token = store_current_token()
                                                    tokens.append(c)
                                                    expecting_percent_gen = False
                                        if nb_closing_brackets_expected > 0:
                                            if c == pu.CASE_GEN_SYM:
                                                current_token = store_current_token()
                                                tokens.append(c)
                                        if nb_closing_brackets_expected > 0:
                                            if c == pu.ARG_SYM:
                                                current_token = store_current_token()
                                                tokens.append(c)
                                        if inside_choice:
                                            if c == pu.RAND_GEN_SYM:
                                                current_token = store_current_token()
                                                tokens.append(c)
                                        if inside_choice and c == pu.CASE_GEN_SYM:
                                            current_token = store_current_token()
                                            tokens.append(c)
                                    if nb_closing_brackets_expected == 0 and c == pu.ALT_SLOT_VALUE_NAME_SYM:
                                        current_token = store_current_token()
                                        tokens.append(c)
                                if after_unit_declaration and c == pu.ANNOTATION_OPEN_SYM:
                                    current_token = store_current_token()
                                    tokens.append(c)
                                    inside_annotation = True
                                    after_unit_declaration = False
                if inside_annotation and c == pu.ANNOTATION_CLOSE_SYM:
                    current_token = store_current_token()
                    tokens.append(c)
                    inside_annotation = False
                elif inside_annotation and c == pu.ANNOTATION_ASSIGNMENT_SYM:
                    current_token = store_current_token()
                    tokens.append(c)
                elif inside_annotation and c == pu.ANNOTATION_SEP:
                    current_token = store_current_token()
                    tokens.append(c)
                elif c.isspace():
                    if not current_token.isspace():
                        store_current_token()
                        current_token = c
                else:
                    if current_token.isspace():
                        if not c.isspace():
                            current_token = store_current_token()
                        current_token += c
                        if after_unit_declaration:
                            after_unit_declaration = False

        store_current_token()
        if nb_closing_brackets_expected > 0:
            self.syntax_error('Line ends with open unit(s).', text, i)
        if inside_annotation:
            self.syntax_error('Line ends with an open annotation.', text, i)
        if inside_choice:
            self.syntax_error('Line ends with open choice(s).', text, i)
        if next_char_escaped:
            self.syntax_error("Line ends with unexpected escapement '" + pu.ESCAPE_SYM + "'.", text, i)
        return tokens

    @staticmethod
    def _get_indentation(text):
        """
        Returns a string that is made
        of all the spaces at the beginning of `text`.
        """
        i = 0
        length = len(text)
        indentation = ''
        while i < length and text[i].isspace():
            indentation += text[i]
            i += 1

        if indentation != '':
            return indentation
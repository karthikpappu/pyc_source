# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vagrant/.virtualenvs/temp3/lib/python3.4/site-packages/colordiffs/diff.py
# Compiled at: 2015-06-21 18:59:35
# Size of source mod 2**32: 3803 bytes
import re
from .formats import green_bg, red_bg, discreet
__all__ = [
 'Diff']

def parse_diff_output(text):
    """Make a Diff out of each diff section"""
    return map(Diff, split_diffs(text))


def split_diffs(text):
    """Split up a diff output, which can potentially contain
    multiple diffs, into a list of Diff objects
    """
    arr = []
    for t in text:
        if t.startswith('diff') and len(arr) != 0:
            yield arr
            arr = [t]
        else:
            arr.append(t)

    yield arr


class Diff:

    def __init__(self, diff):
        self.diff = diff
        self.commits = []
        self.chunks = []
        self.parse_diff()

    def parse_diff(self):
        self.header = self.diff[0].strip()
        index = self.diff[1].strip()
        if index.startswith('index'):
            index_line = 1
            skip = False
        else:
            if index.startswith('new'):
                index_line = 2
                skip = True
            else:
                skip = False
                self.file_mode = self.diff[1].strip()
                index_line = 2
            self.index = self.diff[index_line].strip()
            self.commits = self.parse_commits()
            self.file_a, self.file_b = self.parse_filenames()
            if skip:
                self.line_a = None
                self.line_b = None
                self.line_spec = None
                self.dcs = []
            else:
                self.line_a = self.diff[(index_line + 1)].strip()
                self.line_b = self.diff[(index_line + 2)].strip()
                self.spec = self.diff[index_line + 3:]
                self.dcs = self.parse_chunks()

    def parse_commits(self):
        splits = re.split('\\.\\.| ', self.index)
        if len(splits) == 3:
            _, old, new = splits
        else:
            _, old, new, _ = splits
        return [
         old, new]

    def parse_filenames(self):
        _, _, file1, file2 = self.header.split(' ')
        return (file1[2:].strip(), file2[2:].strip())

    def parse_chunks(self):
        return map(DiffChunk, self.iter_chunks())

    def iter_chunks(self):
        part = []
        for no, line in enumerate(self.spec):
            if line.startswith('@@') and len(part) != 0:
                yield part
                part = [line]
            else:
                part.append(line)

        yield part


class DiffChunk:
    __doc__ = 'A Diff is tied to a file, and each file can have multiple\n    little diffs corresponding to changes in different\n    parts of that file.\n    Each of this portion is called a DiffChunk\n    '

    def __init__(self, spec):
        self.spec = spec
        self.parse_spec()

    def parse_spec(self):
        """
        parses a diff line that looks like this:

            @@ -1,29 +0,0 @@
        """
        self.diff_line = self.spec[0]
        self.output_instructions = self.spec[1:]
        splits = self.diff_line.split()
        self.a_hunk = self.parse_hunk(splits[1])
        self.b_hunk = self.parse_hunk(splits[2])

    def parse_hunk(self, spec):
        start, more = spec.split(',')
        return DiffHunk(start[1:], more)


class DiffHunk:
    __doc__ = 'A DiffChunk is made up of 2 DiffHunks,\n    one for the old content and one for the new contents.\n    '

    def __init__(self, start_line, num_lines):
        self.start_line = int(start_line)
        self.curr_offset = -1
        self.num_lines = int(num_lines)

    def get_current_line(self, colorized):
        if self.curr_offset >= self.num_lines:
            raise Exception()
        self.curr_offset += 1
        return colorized[(self.start_line + self.curr_offset - 1)]
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /src/mortoray.com/master/src/shelljob/python3/shelljob/fs.py
# Compiled at: 2014-02-12 00:08:19
# Size of source mod 2**32: 3834 bytes
"""
        A collection of filesystem related commands.
"""
import os, re, tempfile

def find(path, include_dirs=True, include_files=True, name_regex=None, not_name_regex=None, whole_name_regex=None, not_whole_name_regex=None, exclude_root=False, relative=False, limit_depth=None):
    """
                Creates an iterator of files matching a variety of conditions.
                
                @param path: which path to iterate
                @param include_dirs: include directories in output
                @param include_files: include files in output
                @param name_regex: optional regex string compared against basename of file
                @param not_name_regex: if specificed only produces names not matching this regex
                @param whole_name_regex: like name_regex but applies to whole path, not just basename
                @param not_whole_name_regex: like not_name_regex but applies to whole path
                @param exclude_root: do not include the intput 'path' itself in the output
                @param limit_depth: do not list items deeper than this level from root
                @param relative: filenames are relative to "path" as opposed to appended to path
                @return: a generator for the matched files
        """

    def maybe_regex(arg):
        if arg != None:
            return re.compile(arg)

    c_name_regex = maybe_regex(name_regex)
    c_not_name_regex = maybe_regex(not_name_regex)
    c_whole_name_regex = maybe_regex(whole_name_regex)
    c_not_whole_name_regex = maybe_regex(not_whole_name_regex)

    def check_name(name, whole_name):
        if c_name_regex != None:
            if not c_name_regex.match(name):
                return False
            else:
                if c_not_name_regex != None:
                    if c_not_name_regex.match(name):
                        return False
                if c_whole_name_regex != None:
                    if not c_whole_name_regex.match(whole_name):
                        return False
        else:
            if c_not_whole_name_regex != None:
                if c_not_whole_name_regex.match(whole_name):
                    return False
        return True

    def result(whole, rel):
        if relative:
            return rel
        else:
            return whole

    def filter_func():
        queue = [
         (
          0, path, '')]
        while len(queue) != 0:
            depth, root, rel_path = queue[0]
            queue = queue[1:]
            if root == path and exclude_root:
                pass
            else:
                if include_dirs:
                    if check_name(os.path.basename(root), root):
                        yield result(root, rel_path)
                if limit_depth != None:
                    if depth > limit_depth:
                        continue
                for item in os.listdir(root):
                    whole = os.path.join(root, item)
                    rel = os.path.join(rel_path, item)
                    if os.path.isdir(whole):
                        queue.append((depth + 1, whole, rel))
                    else:
                        if include_files and check_name(item, whole):
                            yield result(whole, rel)

    return filter_func()


class NamedTempFile:
    __doc__ = '\n\t\tCreates a temporary file for a \'with\' block. The file is deleted when the block exits.\n\t\tThis creates the file to ensure it exists/block a race, but does not write anything to\n\t\tit, nor does it keep it open. It is intended for times when you need a named file\n\t\tfor subprocesses.\n\t\t\n\t\tExample::\n\t\t\n\t\t\twith fs.NamedTempFile() as nm:\n\t\t\t\tproc.call( "curl http://mortoray.com/ -o {}".format( nm ) )\n\t\t\t\thtml = open(nm).read()\n\t\t\t\tprint( len(html) )\n\t\t\n\t'

    def __init__(self, suffix=None, prefix=None, dir=None):
        """
                        @param suffix: optional suffix for generated filename (a dot '.' is not automatically added, 
                                specifiy it if desired)
                        @param prefix: optional prefix for generated filename
                        @param dir: in which directory, if None then use a system default
                """
        self.args = {'text': False}
        if suffix != None:
            self.args['suffix'] = suffix
        if prefix != None:
            self.args['prefix'] = prefix
        if dir != None:
            self.args['dir'] = dir

    def __enter__(self):
        handle, name = (tempfile.mkstemp)(**self.args)
        os.close(handle)
        self.name = name
        return name

    def __exit__(self, type, value, traceback):
        os.remove(self.name)
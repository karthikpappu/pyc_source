# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setupmeta/content.py
# Compiled at: 2020-05-06 14:56:50
"""
Functionality related to interacting with project and distutils content
"""
import glob, os, re, setupmeta
RE_README_TOKEN = re.compile('(.?)\\.\\. \\[\\[([a-z]+) (.+)\\]\\](.)?')

def load_contents(relative_path, limit=0):
    """Return contents of file with 'relative_path'

    :param str relative_path: Relative path to file
    :param int limit: Max number of lines to load
    :return str|None: Contents, if any
    """
    lines = setupmeta.readlines(relative_path, limit=limit)
    if lines is not None:
        return ('').join(lines).strip()
    else:
        return


def load_readme(relative_path, limit=0):
    """ Loader for README files """
    lines = setupmeta.readlines(relative_path, limit=limit)
    if lines is not None:
        content = []
        for line in lines:
            m = RE_README_TOKEN.search(line)
            if not m:
                content.append(line)
                continue
            pre, post = m.group(1), m.group(4)
            pre = pre and pre.strip()
            post = post and post.strip()
            if pre or post:
                content.append(line)
                continue
            action = m.group(2)
            param = m.group(3)
            if action == 'end' and param == 'long_description':
                break
            if action == 'include':
                included = load_readme(param, limit=limit)
                if included:
                    content.append(included)

        return ('').join(content).strip()
    else:
        return


def extract_list(content, comment='#'):
    """ List of non-comment, non-empty strings from 'content'

    :param str|None content: Text content
    :param str|None comment: Optional comment marker
    :return list(str)|None: Contents, if any
    """
    if content is None:
        return
    else:
        result = []
        for line in content.strip().split('\n'):
            if comment and comment in line:
                i = line.index(comment)
                line = line[:i]
            line = line.strip()
            if line:
                result.append(line)

        return result


def load_list(relative_path, comment='#', limit=0):
    """ List of non-comment, non-empty strings from file

    :param str relative_path: Relative path to file
    :param str|None comment: Optional comment marker
    :param int limit: Max number of lines to load
    :return list(str)|None: Contents, if any
    """
    return extract_list(load_contents(relative_path, limit=limit), comment=comment)


def resolved_paths(relative_paths):
    """
    :param list(str) relative_paths: Ex: "README.rst", "README*"
    :return str|None: Contents of the first non-empty file found
    """
    candidates = []
    for path in relative_paths:
        if '*' in path:
            full_path = setupmeta.project_path(path)
            for expanded in sorted(glob.glob(full_path)):
                relative_path = os.path.basename(expanded)
                if relative_path not in candidates:
                    candidates.append(relative_path)

            continue
        if path not in candidates:
            candidates.append(path)

    return candidates


def find_contents(relative_paths, loader=None, limit=0):
    """ Return contents of first file found in 'relative_paths', globs OK

    :param list(str) relative_paths: Ex: "README.rst", "README*"
    :param callable|None loader: Optional custom loader function
    :param int limit: Max number of lines to load
    :return str|None, str|None: Contents and path where they came from, if any
    """
    if loader is None:
        loader = load_contents
    for relative_path in resolved_paths(relative_paths):
        contents = loader(relative_path, limit=limit)
        if contents:
            return (contents, relative_path)

    return (None, None)
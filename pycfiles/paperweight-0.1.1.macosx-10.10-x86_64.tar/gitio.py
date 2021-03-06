# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jsick/.virtualenvs/paperweight/lib/python2.7/site-packages/paperweight/gitio.py
# Compiled at: 2015-01-12 15:25:35
"""
Utilities for reading content in git repositories.
"""
import git, os
__all__ = [
 'read_git_blob', 'absolute_git_root_dir']

def read_git_blob(commit_ref, path, repo_dir='.'):
    """Get text from a git blob.

    Parameters
    ----------
    commit_ref : str
        Any SHA or git tag that can resolve into a commit in the
        git repository.
    path : str
        Path to the document in the git repository, relative to the root
        of the repository.
    repo_dir : str
        Path from current working directory to the root of the git repository.

    Returns
    -------
    text : unicode
        The document text.
    """
    repo = git.Repo(repo_dir)
    tree = repo.tree(commit_ref)
    dirname, fname = os.path.split(path)
    text = None
    if dirname == '':
        text = _read_blob(tree, fname)
    else:
        components = path.split(os.sep)
        text = _read_blob_in_tree(tree, components)
    return text


def _read_blob_in_tree(tree, components):
    """Recursively open trees to ultimately read a blob"""
    if len(components) == 1:
        return _read_blob(tree, components[0])
    dirname = components.pop(0)
    for t in tree.trees:
        if t.name == dirname:
            return _read_blob_in_tree(t, components)


def _read_blob(tree, filename):
    for blb in tree.blobs:
        if blb.name == filename:
            txt = unicode(blb.data_stream.read(), 'utf-8')
            return txt

    return


def absolute_git_root_dir(fpath=''):
    """Absolute path to the git root directory containing a given file or
    directory.
    """
    if len(fpath) == 0:
        dirname_str = os.getcwd()
    else:
        dirname_str = os.path.dirname(fpath)
    dirname_str = os.path.abspath(dirname_str)
    dirnames = dirname_str.split(os.sep)
    n = len(dirnames)
    for i in xrange(n):
        basedir = '/' + os.path.join(*dirnames[0:n - i])
        gitdir = os.path.join(basedir, '.git')
        if os.path.exists(gitdir):
            return basedir
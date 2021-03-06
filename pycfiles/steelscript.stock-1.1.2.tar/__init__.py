# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mgarabedian/steelscript/github/steelscript-stock/gitpy_versioning/__init__.py
# Compiled at: 2015-09-26 09:20:45
"""
This module contains code for interacting with git repositories. It is
used to determine an appropriate version number from either the local
git repository tags or from a version file.
"""
from __future__ import unicode_literals, print_function, division
import os, inspect, re
from subprocess import Popen, PIPE
from collections import namedtuple
ALPHA_NUM_PERIOD_UNDER_HYPHEN = b'[\\w._-]+$'
ALPHA_PERIOD_PLUS_UNDER_HYPHEN = b'[A-Za-z.+_-]+'
FINAL = b'\\d+(?:\\.\\d+)*'
PRE = b'(a|b|r?c)\\d+'
POST = b'\\.post\\d+'
DEV = b'\\.dev\\d+'
PEP440 = (b'{0}(?:{1})?(?:{2})?(?:{3})?\\s*$').format(FINAL, PRE, POST, DEV)
PEP8 = b'[a-z_]+'

class InvalidString(Exception):
    """Invalid strings"""

    def __init__(self, error):
        self.error = error


class InvalidTag(InvalidString):
    """Exception class for invalid tags"""

    def __str__(self):
        return (b'Invalid tag: {0}').format(self.error)


class InvalidBranch(InvalidString):
    """Exception class for invalid tags"""

    def __str__(self):
        return (b'Invalid branch {0}').format(self.error)


class InvalidCommand(InvalidString):
    """Exception class for invalid git command"""

    def __str__(self):
        return (b'Invalid command {0}, \n Exception {1}').format((b' ').join(self.error[0]), self.error[1])


def git(cmd, dir=None, input=False):
    """Return a git command results. raise an EnvironmentError if not a git repo.

    :param cmd: a list of strings with 'git' in front form a git command
    :param dir: dir to change to before run the git command
    :param input: flag indicating whether the git command has man-input params.
                  If yes, stderr would mean the param is invalid
    """
    cwd = None
    try:
        if dir is not None:
            cwd = os.getcwd()
            os.chdir(dir)
        process = Popen([b'git'] + cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
    finally:
        if cwd is not None:
            os.chdir(cwd)

    if stderr:
        if not input:
            raise EnvironmentError(stderr)
        else:
            raise InvalidCommand(([b'git'] + cmd, stderr))
    else:
        return stdout.strip()
    return


def call_git_describe(abbrev=None):
    """Return 'git describe' output.

    :param abbrev: Integer to use as the --abbrev value for git describe
    """
    cmd = [
     b'describe']
    if abbrev is not None:
        cmd.append((b'--abbrev={0}').format(abbrev))
    return git(cmd)


def get_branch():
    """Return the current branch's name."""
    input = git([b'branch'])
    line = [ ln for ln in input.split(b'\n') if ln.startswith(b'*') ][0]
    return line.split()[(-1)]


def get_parents(branch):
    """ Return the parent branch

    :param branch: name of the current branch
    """
    input = git([b'show-branch'])
    lines = [ ln for ln in input.split(b'\n') if b'*' in ln ]
    res = set([])
    for ln in lines:
        name = ln.split(b'[')[1].split(b']')[0]
        name = re.split(b'\\^|~', name)[0]
        if name != branch:
            res.add(name)

    return res


def valid_pep440(string):
    """return True if string is a valid pep440 version

    :param string: version string
    """
    if re.match(PEP440, string):
        return True
    return False


def valid_public_ver(tag, pkg_name=None):
    """Return True if tag is a valid public PEP440 version

    if tag is prefixed by a package name, then the package name
    must match

    :param tag: tag string
    :param pkg_name: package name if not None, need to prefix tag
    """
    if pkg_name is None:
        return valid_pep440(tag)
    else:
        return tag.startswith(pkg_name + b'-') and valid_pep440(tag[len(pkg_name) + 1:])
        return


def tag2cmt(tag):
    """Return the commit that the tag points to

    :param tag: the tag on the inquired commit, type:string
    """
    input = git([b'rev-list', (b'{0}').format(tag)], input=True)
    return input.split(b'\n')[0]


def get_commit():
    """Return the latest commit"""
    cmt = git([b'log', b'-n', b'1', b"--pretty=format:'%H'"])
    return cmt.replace(b"'", b'')


def tag2branches(tag):
    """Return the branches containing the given tag in their history

    except the current branch.

    :param tag: the tag name
    """
    lines = git([b'branch', b'--contains', (b'{0}').format(tag2cmt(tag))])
    return set([ ln.strip() for ln in lines.split(b'\n') if b'*' not in ln ])


def find_tag(pkg_name, nondev=False):
    """Return tag that can be used as a version using the following algorithm.

    the latest tag is not necessarily the one to use

    if the tag does not start with a pkg_name:
       if has not seen a tag with pkg_name,
            assume single-pkg repo, the tag is chosen
       else:
            assume multi-pkg repo, tag is wrong, error
    else:
       if matches pkg_name,
            the tag is chosen
       else:
            get next tag, go to the start
    if run out of commit history,
       error

    :param pkg_name: package name used to get a valid tag
    """
    lines = git([b'for-each-ref', b'--sort=taggerdate',
     b'--format', b"'%(refname) %(taggerdate)'", b'refs/tags'])
    lines = lines.split(b'\n')
    seen_tag_with_pkg = False
    for ind in range(len(lines) - 1, -1, -1):
        tag = lines[ind].replace(b"'", b'').split(b' ')[0][10:]
        if pkg_name is None:
            if re.match(PEP440, tag):
                if not nondev or b'.dev' not in tag:
                    return tag
        elif re.match(PEP8 + b'-\\d.*$', tag):
            seen_tag_with_pkg = True
            if tag.startswith(pkg_name + b'-') and re.match(PEP440, tag[len(pkg_name) + 1:]):
                if not nondev or b'.dev' not in tag:
                    return tag
        elif seen_tag_with_pkg:
            raise InvalidTag(tag)

    raise InvalidTag((b"could not find a valid tag with pkg_name '{0}'").format(pkg_name))
    return


def get_commits(tag):
    """Return the number of commits since the tag.

    :param tag: the tag name
    """
    return int(git([b'rev-list', b'--count', b'HEAD'])) - int(git([b'rev-list', b'--count', (b'{0}').format(tag)], input=True))


def git_info():
    """Return an git_info object, which contains attributes:
        branch: branch's name, type: string
        tag: most recent tag, type: string
        tagged_cmt: the commit that the most recent tag points to, type: string
        cmt: latest commit of the current branch, type:string
    """
    branch = get_branch()
    base_tag = call_git_describe(abbrev=0)
    GitInfo = namedtuple(b'GitInfo', b'branch tag tagged_cmt cmt')
    return GitInfo(branch=branch, tag=base_tag, tagged_cmt=tag2cmt(base_tag), cmt=get_commit())


def verify_repository(pkg_file):
    """Raise an error if this source file is not in tracked by git.

    :param pkg_file: pkig_file to be tested
    """
    dirname = os.path.dirname(pkg_file)
    basename = os.path.basename(pkg_file)
    git([b'ls-files', basename, b'--error-unmatch'], dir=dirname)


def valid_local_ver(version):
    """check if a version is valid.

    the version needs to consist of ASCII numbers, letters and periods
    :param version: version string to be validated
    """
    if re.match(ALPHA_NUM_PERIOD_UNDER_HYPHEN, version):
        return True
    return False


def increment_rightmost(version, number):
    """ increment the rightmost number of the version by the number

    :param version: the version string
    :param number: the number by which the rightmost number is incremented
    """
    num_str = re.split(ALPHA_PERIOD_PLUS_UNDER_HYPHEN, version)[(-1)]
    return version[:-len(num_str)] + str(int(num_str) + number)


def get_version(pkg_name=None, pkg_file=None, v_file=b'RELEASE-VERSION'):
    """Return PEP440 style version string.

    :param pkg_name: package name defaults to None for one-pkg repo
       if multi-pkg repo, package name refers to the pkg based on which
       release version will be generated

    :param pkg_file: Some filename in the package, used to test if this
       is a live git repostitory (defaults to caller's file)

    :param v_file: Fallback path name to a file where release_version is saved
    """
    if pkg_file is None:
        parent_frame = inspect.stack()[1]
        pkg_file = inspect.getabsfile(parent_frame[0])
    try:
        verify_repository(pkg_file)
        info = git_info()
        if valid_public_ver(info.tag, pkg_name) and info.cmt == info.tagged_cmt:
            version = info.tag
        else:
            tag = find_tag(pkg_name)
            if info.branch != b'master' and len(tag2branches(tag).intersection(get_parents(info.branch))) > 0:
                if valid_local_ver(info.branch):
                    non_dev_tag = find_tag(pkg_name, nondev=True)
                    commits = get_commits(non_dev_tag)
                    sha = info.cmt[:7]
                    version = (b'{0}+git.{1}.{2}.{3}').format(non_dev_tag, info.branch, commits, sha)
                else:
                    raise InvalidBranch((b"'{0}' is not a valid local version").format(info.branch))
            elif b'.dev' in tag:
                version = increment_rightmost(tag, get_commits(tag))
            else:
                version = (b'{0}.dev{1}').format(increment_rightmost(tag, 1), get_commits(tag))
        with open(v_file, b'w') as (f):
            f.write(version)
    except (EnvironmentError, InvalidString) as e:
        if type(e) in [InvalidTag, InvalidCommand, InvalidBranch]:
            print(e)
        else:
            print(b'Not a git repository')
        print((b"Reading the version from file '{0}'").format(v_file))
        if os.path.exists(v_file):
            with open(v_file, b'r') as (f):
                version = f.read().strip()
        else:
            version = b'unknown'

    return version
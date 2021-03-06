# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/vcs/bazaar.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 3957 bytes
from __future__ import absolute_import
import logging, os
import pip._vendor.six.moves.urllib as urllib_parse
from pip._internal.utils.misc import display_path, rmtree
from pip._internal.utils.subprocess import make_command
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.urls import path_to_url
from pip._internal.vcs.versioncontrol import VersionControl, vcs
if MYPY_CHECK_RUNNING:
    from typing import Optional, Tuple
    from pip._internal.utils.misc import HiddenText
    from pip._internal.vcs.versioncontrol import AuthInfo, RevOptions
logger = logging.getLogger(__name__)

class Bazaar(VersionControl):
    name = 'bzr'
    dirname = '.bzr'
    repo_name = 'branch'
    schemes = ('bzr', 'bzr+http', 'bzr+https', 'bzr+ssh', 'bzr+sftp', 'bzr+ftp', 'bzr+lp')

    def __init__(self, *args, **kwargs):
        (super(Bazaar, self).__init__)(*args, **kwargs)
        if getattr(urllib_parse, 'uses_fragment', None):
            urllib_parse.uses_fragment.extend(['lp'])

    @staticmethod
    def get_base_rev_args(rev):
        return ['-r', rev]

    def export(self, location, url):
        """
        Export the Bazaar repository at the url to the destination location
        """
        if os.path.exists(location):
            rmtree(location)
        url, rev_options = self.get_url_rev_options(url)
        self.run_command((make_command('export', location, url, rev_options.to_args())),
          show_stdout=False)

    def fetch_new(self, dest, url, rev_options):
        rev_display = rev_options.to_display()
        logger.info('Checking out %s%s to %s', url, rev_display, display_path(dest))
        cmd_args = make_command('branch', '-q', rev_options.to_args(), url, dest)
        self.run_command(cmd_args)

    def switch(self, dest, url, rev_options):
        self.run_command((make_command('switch', url)), cwd=dest)

    def update(self, dest, url, rev_options):
        cmd_args = make_command('pull', '-q', rev_options.to_args())
        self.run_command(cmd_args, cwd=dest)

    @classmethod
    def get_url_rev_and_auth(cls, url):
        url, rev, user_pass = super(Bazaar, cls).get_url_rev_and_auth(url)
        if url.startswith('ssh://'):
            url = 'bzr+' + url
        return (
         url, rev, user_pass)

    @classmethod
    def get_remote_url(cls, location):
        urls = cls.run_command(['info'], show_stdout=False, cwd=location)
        for line in urls.splitlines():
            line = line.strip()
            for x in ('checkout of branch: ', 'parent branch: '):
                if line.startswith(x):
                    repo = line.split(x)[1]
                    if cls._is_local_repository(repo):
                        return path_to_url(repo)
                    return repo

    @classmethod
    def get_revision(cls, location):
        revision = cls.run_command([
         'revno'],
          show_stdout=False, cwd=location)
        return revision.splitlines()[(-1)]

    @classmethod
    def is_commit_id_equal(cls, dest, name):
        """Always assume the versions don't match"""
        return False


vcs.register(Bazaar)
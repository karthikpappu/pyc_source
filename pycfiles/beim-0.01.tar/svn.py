# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/linjiao/dv/beim/beim/package/repoutils/svn.py
# Compiled at: 2013-12-08 21:45:16
from beim.svnrepoutils import checkoutCmd, updateCmd, repourl
default_repo_server = 'svn://danse.us'

def getPackageRepository(repo, branch, server=None, revision=None, name=None):
    """getPackageRepository(repo, branch, server,...) -> Package.Repository instance

repo: name of repository for the package
branch: branch in the repository for the package
server: server of the repository
revision: revision of the repository
name: name of the package. default to be the same as repo

Eg.:
 
 >>> getPackageRepository(
         "luban", "trunk", 
         server = "svn://danse.us", name = "luban")

"""
    if server is None:
        server = default_repo_server
    from ..Package import Repository
    r = Repository()
    r.checkout_command = checkoutCmd(server, repo, branch, revision=revision, name=name)
    r.update_command = updateCmd(revision=revision)
    r.url = repourl(repo, branch, server=server)
    r.name = repo
    r.pkgname = name or repo
    r.branch = branch
    r.server = server
    r.revision = revision
    r.type = 'svn'
    return r


def getRevision(pkgrepo):
    from beim.svnrepoutils import get_revision
    reponame = pkgrepo.name
    branch = pkgrepo.branch
    server = pkgrepo.server
    return get_revision(('/').join([reponame, branch]), server=server)


__id__ = '$Id$'
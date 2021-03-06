# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/svn/context.py
# Compiled at: 2008-05-07 15:44:29
"""
SubversionContext 
=================
  
Subversion Contexts represent a node hierarchy within a subversion repository and can
be pickled.
   
  >> from ore.svn import SubversionContext
  >> ctx = SubversionContext('tests/myrepo') 
   
you can also limit operations it to a particular path within a repository.
which will bind the context to a particular subtree.

  >> ctx = SubversionContext('test/myrepo', '/myproject')   

to access the svn nodes from the context, we access the root of
the node tree on the context.

  >> node = ctx.root
  >> node.svn_path
  '/myproject'
 
$Id: context.py 2205 2008-05-07 19:44:27Z hazmat $
"""
import os, time
from svn import fs, repos
from zope.interface import implements
from interfaces import ISubversionContext, InvalidRepositoryPath, RootPathViolation
from resource import tls, ResourceContext
from log import SVNLogFactory, log
from utils import svn_path_id, svn_path_join, make_aprtime
from directory import SubversionDirectory
from file import SubversionFile
from manager import SubversionTransaction

class SubversionContext(object):
    """
    a window into a subversion repository.
    """
    implements(ISubversionContext)

    def __init__(self, repository_path='', svn_path='/'):
        self.repository_path = repository_path
        self.svn_path = svn_path

    def getTransaction(self):
        """
        returns the a subversion transaction object for manipulation by the user, which
        allows for setting transaction/revision properties, and transaction control.
        """
        ctx = self.getResourceContext()
        return SubversionTransaction(ctx)

    transaction = property(getTransaction, doc=getTransaction.__doc__)

    def getSVNContext(self):
        return self

    def getSVNRootObject(self):
        """
        get the root object that the svn context/window is anchored to
        """
        n = time.time()
        v = self.getSVNObject(self.svn_path)
        return v

    root = property(getSVNRootObject, doc=getSVNRootObject.__doc__)

    def __getitem__(self, name):
        return self.root[name]

    def editContext(self, repository_path, svn_path):
        """
        edit the settings for the subversion context.
        """
        if not os.path.exists(repository_path):
            raise InvalidRepositoryPath(repository_path)
        ctx = self.getResourceContext()
        if ctx.txnroot is not None:
            raise SyntaxError("can't edit while in an svn transaction")
        self.clear()
        self.repository_path = repository_path
        self.svn_path = svn_path
        resource_context = self.getResourceContext(register=False)
        return

    def setAccess(self, name=None):
        """
        setup the name we should access the repository as, this is primarily
        for locking purposes, txn properties are set separately via the transaction
        properties. if name is none, then reuse a previously set access name.
        """
        res_ctx = self.getResourceContext()
        res_ctx.setAccess(name)

    def setRevision(self, revision=None):
        """
        change the revision root of the fs being inspected
        
        # setrevision is used as a callback from traversal, so it performs
        # a sanity check ones state, as a newly created svn context does not
        # have adequate state to be access a repository.
        """
        if not self.repository_path:
            return
        ctx = self.getResourceContext()
        ctx.setRevision(revision)

    def getRevision(self):
        """
        return the revision currently being introspected.
        """
        resource_context = self.getResourceContext()
        return resource_context.revision

    revision = property(getRevision, doc=getRevision.__doc__)

    def getRevisionInfo(self):
        """
        return a plethora of info about when and what was committed in this
        revision.
        """
        resource_ctx = self.getResourceContext()
        revision = resource_ctx.revision
        info = SVNLogFactory(resource_ctx.fsptr, revision, resource_ctx.pool)
        info.paths = fs.paths_changed(resource_ctx.fsroot, resource_ctx.pool)
        return info

    revision_info = property(getRevisionInfo, doc=getRevisionInfo.__doc__)

    def getRevisionByDate(self, rev_date):
        """
        return the youngest/highest revision as of this date.
        """
        ctx = self.getResourceContext()
        rev_date = make_aprtime(rev_date, ctx.pool)
        return repos.dated_revision(ctx.repository, rev_date, ctx.pool)

    def initialize(self, revision=None):
        """ *internal api*
        initialize the browser, with a new pool, revison root, and repository
        pointer. optional revision arg can specify the revision root.
        """
        if revision is not None:
            raise SyntaxError('initialize no longer takes a revision')
        context = self.getResourceContext()
        return context

    def getResourceContext(self, create=True, register=True):
        """ *internal api*
        get access to the resource context that holds our libsvn data structures.
        """
        context = tls.getFor(self)
        if context is not None:
            if register:
                context.register()
            return context
        elif not create:
            return
        context = ResourceContext(self.repository_path, self.svn_path)
        tls.setFor(self, context)
        if register:
            context.register()
        return context

    def clear(self):
        """ *internal api*
        reset any associated svn/apr resources, never call this unless its
        time to reinitialize
        """
        context = self.getResourceContext(create=False, register=False)
        if context is not None:
            context.finalize()
            tls.delFor(self)
        return

    def traverse(self, path):
        if not path.startswith(self.svn_path):
            raise RootPathViolation('%s not in %s' % (path, self.svn_path))
        parts = filter(None, path[len(self.svn_path):].split('/'))
        ob = self.getSVNRootObject()
        for p in parts:
            ob = ob[p]

        return ob

    def getSVNObject(self, path):
        """
        retrieve a subversion object for the given svn path.
        """
        log.debug('retrieving %s' % str(path))
        resource_context = self.getResourceContext()
        if not path.startswith(self.svn_path):
            raise RootPathViolation('%s not in %s' % (path, self.svn_path))
        if fs.is_dir(resource_context.root, path, resource_context.pool):
            if self.svn_path == path:
                return self.SVNRootFactory(path)
            return self.SVNDirectoryFactory(path)
        elif fs.is_file(resource_context.root, path, resource_context.pool):
            return self.SVNFileFactory(path)
        else:
            return
        return

    def getSVNContext(self):
        return self

    def SVNDirectoryFactory(self, svn_path):
        """ factory function, contruct an svn directory node from the given svn_path.
        """
        id = svn_path_id(svn_path)
        return SubversionDirectory(id, svn_path, self)

    def SVNFileFactory(self, svn_path):
        """ factory function, contruct an svn file node from the given svnpath
        """
        id = svn_path_id(svn_path)
        return SubversionFile(id, svn_path, self)

    SVNRootFactory = SVNDirectoryFactory
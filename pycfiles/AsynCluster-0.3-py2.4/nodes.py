# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asyncluster/master/nodes.py
# Compiled at: 2008-02-20 20:13:39
"""
The PB server for node-master TCP connections.
"""
from zope.interface import implements
from twisted.internet import defer, interfaces
from twisted.cred import credentials, checkers, portal, error
from twisted.python.failure import Failure
from twisted.spread import pb
from twisted_goodies.misc import AddressRestrictorMixin

class Perspective(pb.Avatar):
    """
    Each PB node and worker client receives a reference to its very own
    instance of me as its perspective upon making an authenticated TCP
    connection to the node master server.

    @ivar ID: A unique ID for this client, established during a mutually
      authenticated client-server connection.

    @ivar userID: The ID of any user having a session underway on the client if
      it is a node rather than a worker.

    @ivar nodeClient: A Boolean that is set C{True} if my client is a node
      client, as opposed to a child worker client.
    
    """
    __module__ = __name__

    def __init__(self, ctl):
        self.ctl = ctl

    def perspective_getSessionManager(self):
        """
        Remotely-accessible wrapper for
        L{control.Controller.getSessionManager}.
        """
        return self.ctl.getSessionManager()

    def _printableID(self):
        return '%s%04d' % ('WN'[self.nodeClient], self.ID)

    def attached(self, clientRoot):
        """
        Called by the node client L{Realm}, after a successful login, with a
        reference to the I{clientRoot} object supplied to it as the
        incomprehensibly named 'mind'.

        Performs a reverse login to the client to satisfy it that I am running
        on a trustworthy server and the arbitrary Python code it receives from
        this server to execute for computing jobs will not do bad things to it.
        """

        def responded(acceptanceCode):
            if acceptanceCode == 'node':
                self.nodeClient = True
                d = self.ctl.attachNode(self, clientRoot)
            elif acceptanceCode == 'child':
                self.nodeClient = False
                d = self.ctl.attachWorker(clientRoot)
            else:
                return (
                 pb.IPerspective, self, lambda : None)
            clientRoot.notifyOnDisconnect(self.detached)
            return d.addCallback(doneAttaching)

        def doneAttaching(ID):
            self.ID = ID
            print '%s: Attached' % self._printableID()
            return (pb.IPerspective, self, self.detached)

        serverPassword = self.ctl.config['common']['server password']
        d = clientRoot.callRemote('reverseLogin', serverPassword)
        return d.addCallback(responded)

    def detached(self, *null):
        """
        Called when the client disconnects.
        """
        if hasattr(self, 'ID'):
            print '%s: Detached' % self._printableID()
            if self.nodeClient:
                d = self.ctl.detachNode(self.ID)
            else:
                d = self.ctl.detachWorker(self.ID)
            del self.ID
            return d


class PasswordChecker(object):
    """
    Checks hashed passwords based on the 'client' section of the config file.
    """
    __module__ = __name__
    implements(checkers.ICredentialsChecker)
    credentialInterfaces = (
     credentials.IUsernameHashedPassword,)

    def __init__(self, clientSection):
        self.clientSection = clientSection

    def requestAvatarId(self, credentials):

        def possiblyMatched(matched, user):
            if matched:
                return user
            return Failure(error.UnauthorizedLogin())

        user = credentials.username
        if user != self.clientSection['user']:
            d = defer.succeed(False)
        else:
            password = self.clientSection.get('password', None)
            if password is None:
                d = defer.succeed(False)
            else:
                d = defer.maybeDeferred(credentials.checkPassword, password)
        d.addCallback(possiblyMatched, user)
        return d


class Realm(object):
    """
    Construct me with to a reference to the L{control.Controller} object that
    controls everything.
    """
    __module__ = __name__
    implements(portal.IRealm)

    def __init__(self, ctl):
        self.ctl = ctl

    def requestAvatar(self, avatarID, mind, *interfaces):
        """
        Returns a deferred that fires with the required I{interface,
        perspective, logout} tuple after the perspective attempts a reverse
        login to the client.
        """
        if pb.IPerspective not in interfaces:
            raise NotImplementedError(self, interfaces)
        perspective = Perspective(self.ctl)
        return perspective.attached(mind)


class ServerFactory(AddressRestrictorMixin, pb.PBServerFactory):
    """
    I am a PB server factory for the NDM node-master TCP server, which only
    accepts connections from one or more IP address subnets, defined in the
    config file as a comma-separated list of base/bits strings, e.g.,
    192.168.1.0/24.

    Construct me with a reference to the L{control.Controller} object that
    controls everything. It must have a public attribute 'config' referencing a
    config object loaded with the NDM configuration file.
    """
    __module__ = __name__

    def __init__(self, ctl, checker=None):
        for subnetString in ctl.config['server']['subnets']:
            self.addSubnet(subnetString.strip())

        rootPortal = portal.Portal(Realm(ctl))
        if checker is None:
            checker = PasswordChecker(ctl.config['client'])
        rootPortal.registerChecker(checker)
        pb.PBServerFactory.__init__(self, rootPortal)
        return
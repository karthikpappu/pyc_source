# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/txlb/application/director.py
# Compiled at: 2008-07-05 02:21:36
"""
In honor of its predecessor PythonDirector by Anthony Baxter, this module has
been named 'director.' It contains all the code neccessary for seting up and
running the stand-alone load-balancing application txlb.tac, which provides the
same functionality as the original pydir.py and pydir++.py apps.
"""
from twisted.web import server
from twisted.cred import portal
from twisted.conch import manhole
from twisted.conch import manhole_ssh
from twisted.internet import ssl
from twisted.application import service
from twisted.application import internet
from txlb import name
from txlb import util
from txlb import model
from txlb import config
from txlb import manager
from txlb.admin import auth
from txlb.admin import pages
from txlb.manager import checkBadHosts
from txlb.application.service import LoadBalancedService

def configuredProxyManagerFactory(configuration):
    """
    A factory for generating a ProxyManager, complete with pre-created
    services, groups, and data from a configuration file. Most of the work here
    is mapping configuration to models. The collection of models is what is
    passed to the proxyManagerFactory.
    """
    services = []
    for (serviceName, serviceConf) in configuration.services.items():
        addresses = [ util.splitHostPort(x) for x in serviceConf.listen ]
        pservice = model.ProxyService(serviceName, addresses=addresses)
        for (groupName, groupConf) in serviceConf.groups.items():
            pgroup = model.ProxyGroup(groupName, groupConf.scheduler, groupConf.isEnabled)
            for (hostName, hostConf) in groupConf.hosts.items():
                (host, port) = util.splitHostPort(hostConf.ip)
                phost = model.ProxyHost(hostName, host, port, hostConf.weight)
                pgroup.addHost(phost)

            pservice.addGroup(pgroup)

        services.append(pservice)

    return manager.proxyManagerFactory(services)


def setupAdminWebUIServer(configuration, director):
    """
    Given the director, set up a potentially SSL-enabled admin web UI on the
    configured port.
    """
    if not configuration.admin.webEnable:
        return
    root = pages.AdminServer(configuration, director)
    site = server.Site(root)
    (host, port) = util.splitHostPort(configuration.admin.webListen)
    if configuration.admin.webSecure:
        util.setupServerCert()
        context = ssl.DefaultOpenSSLContextFactory(util.privKeyFile, util.certFile)
        admin = internet.SSLServer(port, site, context, interface=host)
    else:
        admin = internet.TCPServer(port, site, interface=host)
    admin.setName('adminWeb')
    return admin


def setupAdminSSHServer(configuration, director, services):
    """
    Set up a server that will enable an admin user to SSH into the
    load-balancers's running Python Interpreter.
    """
    if not configuration.admin.sshEnable:
        return
    (host, port) = util.splitHostPort(configuration.admin.sshListen)

    def getManhole(serverProtocol):
        startingNamespace = {'config': configuration, 'services': services}
        return manhole.Manhole(util.getNamespace(startingNamespace))

    realm = manhole_ssh.TerminalRealm()
    realm.chainedProtocolFactory.protocolFactory = getManhole
    p = portal.Portal(realm)
    p.registerChecker(auth.LBAdminAuthChecker(configuration.admin))
    factory = manhole_ssh.ConchFactory(p)
    admin = internet.TCPServer(port, factory, interface=host)
    admin.setName('adminSSH')
    return admin


def setupHostChecker(configuration, director):
    """
    This is the setup for the "bad host check" management task.
    """
    if not configuration.manager.hostCheckEnabled:
        return service.Service()
    checkInterval = configuration.manager.hostCheckInterval
    checker = internet.TimerService(checkInterval, manager.checkBadHosts, configuration, director)
    checker.setName('hostChecker')
    return checker


def setupConfigChecker(configFile, configuration, director):
    """
    This is the setup for the "config check" management task.
    """
    checkInterval = configuration.manager.configCheckInterval
    checker = internet.TimerService(checkInterval, manager.checkConfigChanges, configFile, configuration, director)
    checker.setName('configChecker')
    return checker


def setupControlSocket(configuration, director):
    """
    This is for the functionaity that Apple introduced in the patches from its
    Calendar Server project.
    """
    control = service.Service()
    socket = configuration.control.socket
    if socket != None:
        control = internet.UNIXServer(socket, manager.ControlFactory(director))
    control.setName('control')
    return control


def setup(configFile):
    """
    Given the configuration file, instantiate the proxy manager and setup the
    necessary services.
    """
    conf = config.Config(configFile)
    director = configuredProxyManagerFactory(conf)
    application = service.Application(name)
    services = LoadBalancedService(director)
    services.setServiceParent(application)
    services.proxiesFactory()
    control = setupControlSocket(conf, director)
    control.setServiceParent(services)
    checker = setupHostChecker(conf, director)
    checker.setServiceParent(services)
    configer = setupConfigChecker(configFile, conf, director)
    configer.setServiceParent(services)
    adminWeb = setupAdminWebUIServer(conf, director)
    adminWeb.setServiceParent(services)
    adminSSH = setupAdminSSHServer(conf, director, services)
    adminSSH.setServiceParent(services)
    return application
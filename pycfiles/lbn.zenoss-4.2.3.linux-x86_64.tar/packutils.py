# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/lbn/zenoss/packutils.py
# Compiled at: 2012-06-05 01:24:14
"""
This is a bunch of helper functions that support creating and deploying
ZenPack-like modules as pure Python
"""
import logging, pkg_resources, os, re
from Acquisition import aq_base
from zExceptions import BadRequest
from Products.ZenModel.RRDTemplate import RRDTemplate
from Products.ZenRelations.Exceptions import RelationshipExistsError
logger = logging.getLogger('lbn.zenoss.packutils')
Metatag = re.compile('^([A-Z].+): (.+)$')

def zentinel(context):
    """
    return the zentinel object from an initialize context (or None)
    """
    try:
        from Zope2 import bobo_application
    except ImportError:
        bobo_application = None

    if bobo_application is not None:
        app = bobo_application()
    else:
        app = context._ProductContext__app
    zport = getattr(app, 'zport', None)
    if zport:
        try:
            packmgr = zport.dmd.ZenPackManager
            return zport
        except:
            return

    return


def hasZenPack(zport, zenpackname):
    """
     check if the ZenPackManager has this ZenPack
     """
    mgr = zport.dmd.ZenPackManager
    return mgr.packs._getOb(zenpackname, None) is not None


def addZenPack(zport, pack):
    """
    uber function to handle all Product --> ZenPack registration,
    returns the pack in context
    """
    _registerPack(zport, pack, force=True)
    return zport.dmd.ZenPackManager.packs._getOb(pack.getId())


def addZenPackObjects(zenpack, objs):
    """
    add a bunch of objects to the ZenPack
    """
    expanded = []
    for obj in objs:
        expanded.append(obj)
        if isinstance(obj, RRDTemplate):
            for ds in obj.datasources.objectValues():
                expanded.append(ds)
                expanded.extend(ds.datapoints.objectValues())

            for gd in obj.graphDefs.objectValues():
                expanded.append(gd)
                expanded.extend(gd.graphPoints.objectValues())

    packables = zenpack.packables
    for obj in expanded:
        obj.buildRelations()
        try:
            packables.addRelation(obj)
        except RelationshipExistsError:
            continue
        except AttributeError, e:
            if str(e) in ('pack', ):
                continue
            logger.error('failed adding %s into %s: %s (%s)' % (obj, zenpack.getId(),
             e.__class__.__name__, str(e)), exc_info=True)
        except Exception, e:
            logger.error('failed adding %s into %s: %s (%s)' % (obj, zenpack.getId(),
             e.__class__.__name__, str(e)), exc_info=True)


def _registerPack(zport, zenpack, force=False):
    """
    register with ZenPackManager - necessary to become datasource-aware etc
    """
    mgr = zport.dmd.ZenPackManager
    modulename = zenpack.getId()
    if mgr.packs._getOb(modulename, None):
        logger.info('ZenPack already registered: %s' % modulename)
        if not force:
            return
    else:
        mgr.packs._setObject(modulename, zenpack)
    logger.info('Adding ZenPack %s to ZenPackManager' % modulename)
    mgr.packs._setObject(modulename, zenpack)
    pack = mgr.packs._getOb(modulename)
    pack.eggPack = True
    egg = pkg_resources.get_distribution(modulename)
    pkginfo = {}
    for line in egg._get_metadata('PKG-INFO'):
        match = Metatag.match(line)
        if match:
            (k, v) = match.groups()
            pkginfo[k] = v

    pack.manage_changeProperties(title=modulename, version=egg.version, author=pkginfo.get('Author', ''), organization=pkginfo.get('Author', ''), url=pkginfo.get('Home-page', ''), license=pkginfo.get('License', ''))
    module_dir = egg.project_name.split('.')
    path = os.path.join(egg.location, *module_dir)
    logger.info('Installing egg path %s' % path)
    pack.install(pack)
    return
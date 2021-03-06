# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/blog/database.py
# Compiled at: 2014-05-08 12:29:58
__docformat__ = 'restructuredtext'
import transaction
from z3c.language.negotiator.interfaces import INegotiatorManager
from zope.authentication.interfaces import IAuthentication
from zope.catalog.interfaces import ICatalog
from zope.component.interfaces import IComponentRegistry, ISite
from zope.i18n.interfaces import INegotiator
from zope.intid.interfaces import IIntIds
from zope.processlifetime import IDatabaseOpenedWithRoot
from ztfy.base.interfaces import IPathElements, IBaseContentType
from ztfy.blog.interfaces.category import ICategorizedContent
from ztfy.i18n.interfaces.content import II18nBaseContent
from ztfy.security.interfaces import ISecurityManager, ILocalRoleManager, ILocalRoleIndexer
from ztfy.utils.interfaces import INewSiteManagerEvent
from ztfy.utils.timezone.interfaces import IServerTimezone
from z3c.language.negotiator.app import Negotiator
from zc.catalog.catalogindex import SetIndex, ValueIndex
from zope.app.publication.zopepublication import ZopePublication
from zope.catalog.catalog import Catalog
from zope.component import adapter, queryUtility
from zope.intid import IntIds
from zope.location import locate
from zope.pluggableauth.authentication import PluggableAuthentication
from zope.pluggableauth.plugins.groupfolder import GroupFolder, GroupInformation
from zope.pluggableauth.plugins.principalfolder import PrincipalFolder
from zope.site import hooks
from ztfy.utils.catalog.index import TextIndexNG
from ztfy.utils.site import locateAndRegister
from ztfy.utils.timezone.utility import ServerTimezoneUtility

def updateDatabaseIfNeeded(context):
    """Check for missing utilities at application startup"""
    try:
        sm = context.getSiteManager()
    except:
        return

    default = sm['default']
    intids = queryUtility(IIntIds)
    if intids is None:
        intids = default.get('IntIds')
        if intids is None:
            intids = IntIds()
            locate(intids, default)
            IComponentRegistry(sm).registerUtility(intids, IIntIds, '')
            default['IntIds'] = intids
    auth = default.get('Authentication')
    if auth is None:
        auth = PluggableAuthentication()
        locateAndRegister(auth, default, 'Authentication', intids)
        auth.credentialsPlugins = ['No Challenge if Authenticated',
         'Session Credentials',
         'Zope Realm Basic-Auth']
        IComponentRegistry(sm).registerUtility(auth, IAuthentication)
    if 'users' not in auth:
        folder = PrincipalFolder('usr.')
        locateAndRegister(folder, auth, 'users', intids)
        auth.authenticatorPlugins += ('users', )
    groups = auth.get('groups', None)
    if groups is None:
        groups = GroupFolder('grp.')
        locateAndRegister(groups, auth, 'groups', intids)
        auth.authenticatorPlugins += ('groups', )
    roles_manager = ILocalRoleManager(context, None)
    if 'administrators' not in groups:
        group = GroupInformation('Administrators (group)', 'Group of site services and utilities managers')
        locateAndRegister(group, groups, 'administrators', intids)
        if roles_manager is None or 'zope.Manager' in roles_manager.__roles__:
            ISecurityManager(context).grantRole('zope.Manager', 'grp.administrators', False)
    if 'managers' not in groups:
        group = GroupInformation('Managers (group)', "Group of site managers, which handle site's structure")
        locateAndRegister(group, groups, 'managers', intids)
        if roles_manager is None or 'ztfy.BlogManager' in roles_manager.__roles__:
            ISecurityManager(context).grantRole('ztfy.BlogManager', 'grp.managers', False)
    if 'contributors' not in groups:
        group = GroupInformation('Contributors (group)', "Group of site contributors, which handle site's contents")
        locateAndRegister(group, groups, 'contributors', intids)
        if roles_manager is None or 'ztfy.BlogContributor' in roles_manager.__roles__:
            ISecurityManager(context).grantRole('ztfy.BlogContributor', 'grp.contributors', False)
    if 'operators' not in groups:
        group = GroupInformation('Operators (group)', 'Group of site operators, which can get access to management interface')
        group.principals = ['grp.managers', 'grp.administrators', 'grp.contributors']
        locateAndRegister(group, groups, 'operators', intids)
        if roles_manager is None or 'ztfy.BlogOperator' in roles_manager.__roles__:
            ISecurityManager(context).grantRole('ztfy.BlogOperator', 'grp.operators', False)
    tz = queryUtility(IServerTimezone)
    if tz is None:
        tz = default.get('Timezone')
        if tz is None:
            tz = ServerTimezoneUtility()
            locateAndRegister(tz, default, 'Timezone', intids)
            IComponentRegistry(sm).registerUtility(tz, IServerTimezone)
    i18n = queryUtility(INegotiatorManager)
    if i18n is None:
        i18n = default.get('I18n')
        if i18n is None:
            i18n = Negotiator()
            locateAndRegister(i18n, default, 'I18n', intids)
            i18n.serverLanguage = 'en'
            i18n.offeredLanguages = ['en']
            IComponentRegistry(sm).registerUtility(i18n, INegotiator)
            IComponentRegistry(sm).registerUtility(i18n, INegotiatorManager)
    catalog = default.get('Catalog')
    if catalog is None:
        catalog = Catalog()
        locateAndRegister(catalog, default, 'Catalog', intids)
        IComponentRegistry(sm).registerUtility(catalog, ICatalog, 'Catalog')
    if catalog is not None:
        if 'paths' not in catalog:
            index = SetIndex('paths', IPathElements, False)
            locateAndRegister(index, catalog, 'paths', intids)
        if 'categories' not in catalog:
            index = SetIndex('categories_ids', ICategorizedContent, False)
            locateAndRegister(index, catalog, 'categories', intids)
        if 'content_type' not in catalog:
            index = ValueIndex('content_type', IBaseContentType, False)
            locateAndRegister(index, catalog, 'content_type', intids)
        if 'title' not in catalog:
            index = TextIndexNG('title shortname description heading', II18nBaseContent, False, languages='fr en', storage='txng.storages.term_frequencies', dedicated_storage=False, use_stopwords=True, use_normalizer=True, ranking=True)
            locateAndRegister(index, catalog, 'title', intids)
    catalog = default.get('SecurityCatalog')
    if catalog is None:
        catalog = Catalog()
        locateAndRegister(catalog, default, 'SecurityCatalog', intids)
        IComponentRegistry(sm).registerUtility(catalog, ICatalog, 'SecurityCatalog')
    if catalog is not None:
        if 'ztfy.BlogManager' not in catalog:
            index = SetIndex('ztfy.BlogManager', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.BlogManager', intids)
        if 'ztfy.BlogContributor' not in catalog:
            index = SetIndex('ztfy.BlogContributor', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.BlogContributor', intids)
        if 'ztfy.BlogOperator' not in catalog:
            index = SetIndex('ztfy.BlogOperator', ILocalRoleIndexer, False)
            locateAndRegister(index, catalog, 'ztfy.BlogOperator', intids)
    return


@adapter(IDatabaseOpenedWithRoot)
def handleOpenedDatabase(event):
    db = event.database
    connection = db.open()
    root = connection.root()
    root_folder = root.get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            updateDatabaseIfNeeded(site)
            transaction.commit()

    return


@adapter(INewSiteManagerEvent)
def handleNewSiteManager(event):
    updateDatabaseIfNeeded(event.object)
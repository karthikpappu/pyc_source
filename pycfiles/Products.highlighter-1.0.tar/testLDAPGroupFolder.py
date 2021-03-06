# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/GroupUserFolder/tests/testLDAPGroupFolder.py
# Compiled at: 2008-05-20 04:51:55
__doc__ = '\n\n'
__version__ = '$Revision:  $'
__docformat__ = 'restructuredtext'
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from Testing import ZopeTestCase
from AccessControl.Permissions import access_contents_information, view, add_documents_images_and_files, change_images_and_files, view_management_screens
from AccessControl.SecurityManagement import newSecurityManager, noSecurityManager, getSecurityManager
from AccessControl import Unauthorized
from AccessControl.User import UnrestrictedUser
import urllib
app = ZopeTestCase.app()
ZopeTestCase.utils.setupSiteErrorLog(app)
ZopeTestCase.close(app)
(host, port) = ZopeTestCase.utils.startZServer(4)
base = 'http://%s:%d/%s' % (host, port, ZopeTestCase.folder_name)
from Products.GroupUserFolder.interfaces import IUserFolder
from Interface import Verify
ZopeTestCase.installProduct('GroupUserFolder')
ZopeTestCase.installProduct('LDAPUserFolder')
import GRUFTestCase, testGroupUserFolderAPI, testLDAPUserFolder
from Log import *
try:
    from LDAPconfig import defaults
except ImportError:
    Log(LOG_ERROR, "\n    To perform this test case, you must provide a 'LDAPconfig.py' file with the following structure:\n\ndefaults = { 'title'  : 'LDAP User Folder'\n           , 'server' : 'localhost:389'\n           , 'login_attr' : 'cn'\n           , 'uid_attr': 'cn'\n           , 'users_base' : 'ou=people,dc=dataflake,dc=org'\n           , 'users_scope' : 2\n           , 'roles' : 'Anonymous'\n           , 'groups_base' : 'ou=groups,dc=dataflake,dc=org'\n           , 'groups_scope' : 2\n           , 'binduid' : 'cn=Manager,dc=dataflake,dc=org'\n           , 'bindpwd' : 'mypass'\n           , 'binduid_usage' : 1\n           , 'rdn_attr' : 'cn'\n           , 'local_groups' : 1                 # Keep this true\n           , 'use_ssl' : 0\n           , 'encryption' : 'SHA'\n           , 'read_only' : 0\n           }\n\n    Of course, you've got to replace all values by some relevant ones for your project.\n    This test case won't complete without.\n\n    NEVER PUT THIS FILE INTO YOUR CVS ! Unless you want your password to be publicly known...\n    ")
    ldapuf = False
else:
    ldapuf = True
    dg = defaults.get

class TestLDAPUserFolderGroups(testLDAPUserFolder.TestLDAPUserFolderAPI):
    """
    Now we create groups into LDAP. Groups won't be locally stored anymore.
    Remember that according to LDAPUF, a LDAP group = a zope role.
    However, for GRUF, a zope group = a zope role.
    So, by transitivity, we must be able at some point to say that a zope group = a LDAP group ;)

    The only caveat with this system is that we have to declare the zope roles we'll use in LDAP.
    That's why we create a few additional groups in gruf_sources_setup().
    """
    __module__ = __name__

    def gruf_sources_setup(self):
        """
        Basic LDAP initialization inside gruf's user source
        """
        self.gruf.replaceUserSource('Users', 'manage_addProduct/LDAPUserFolder/manage_addLDAPUserFolder')
        self.gruf.replaceUserSource('Groups', 'manage_addProduct/GroupUserFolder/manage_addLDAPGroupFolder', title='MyLDAPGF', luf='Users')
        self.gruf.Users.acl_users.manage_edit(title=dg('title'), login_attr=dg('login_attr'), uid_attr=dg('uid_attr'), users_base=dg('users_base'), users_scope=dg('users_scope'), roles=dg('roles'), obj_classes='top,inetOrgPerson', groups_base=dg('groups_base'), groups_scope=dg('groups_scope'), binduid=dg('binduid'), bindpwd=dg('bindpwd'), binduid_usage=dg('binduid_usage'), rdn_attr=dg('rdn_attr'), local_groups=dg('local_groups'), encryption=dg('encryption'))
        self.delete_created_users()

    def delete_created_users(self):
        """ldap-specify deletion"""
        groups = [
         'g1', 'g2', 'g3', 'g4', 'ng1', 'ng2', 'ng3', 'ng4', 'ng5', 'created_group', 'test_prefix', 'extranet', 'intranet', 'compta', 'r1', 'r2', 'r3', 'r4']
        g_dn = []
        for group in groups:
            g_dn.append('cn=%s,%s' % (group, self.gruf.Users.acl_users.groups_base))

        self.gruf.Users.acl_users.manage_deleteGroups(g_dn)
        self.gruf.userFolderDelUsers(['manager', 'u1', 'u2', 'u3', 'u4', 'u5', 'u6', 'u7', 'u8', 'u9', 'u10', 'u11', 'created_user', 'group_test_prefix'])

    def security_context_setup_groups(self):
        """create groups. We splitted to allow LDAP tests to override this"""
        self.gruf.userFolderAddGroup('r1')
        self.gruf.userFolderAddGroup('r2')
        self.gruf.userFolderAddGroup('r3')
        self.gruf.userFolderAddGroup('r4')
        self.gruf.userFolderAddGroup('g1', ())
        self.gruf.userFolderAddGroup('g2', ('r1', ))
        self.gruf.userFolderAddGroup('g3', ('r2', ))
        self.gruf.userFolderAddGroup('g4', ('r2', 'r3'))
        self.gruf.userFolderAddGroup('ng1', (), ('g1', ))
        self.gruf.userFolderAddGroup('ng2', (), ('g2', 'g3'))
        self.gruf.userFolderAddGroup('ng3', (), ('g2', 'ng2'))
        self.gruf.userFolderAddGroup('ng4', ('r3', ), ('g2', 'ng2'))
        self.gruf.userFolderAddGroup('ng5', (), ('g2', 'ng4'))
        self.gruf.userFolderAddGroup('extranet', (), ())
        self.gruf.userFolderAddGroup('intranet', (), ('extranet', ))
        self.gruf.userFolderAddGroup('compta', (), ('intranet', 'extranet'))

    def testLDAPSourceMove(self):
        """Ensure that LDAPGroupFolder will still work correctly if we move
        a source. This caused core dumps or GRUF3Beta1.
        """
        self.failUnlessEqual(self.gruf.Users.acl_users.meta_type, 'LDAPUserFolder')
        self.gruf.addUserSource('manage_addProduct/OFSP/manage_addUserFolder')
        self.gruf.moveUserSourceUp('Users01')
        self.failUnlessEqual(self.gruf.Users.acl_users.meta_type, 'User Folder')
        self.gruf.getUsers()
        self.gruf.getUserNames()
        self.gruf.moveUserSourceUp('Users01')
        self.gruf.getUsers()
        self.gruf.getUserNames()

    def test01_LDAPUp(self):
        """Ensure LDAP is up and running
        """
        self.gruf.Users.acl_users.getUsers()

    def test02_groupHasRole(self):
        """Test if a group can have a role
        """
        self.failUnless('r1' in self.gruf.getGroup('g2').getRoles(), self.gruf.getGroup('g2').getRoles())

    def test_getGroupNames(self):
        pass

    def test_getGroupIds(self):
        pass

    def test_getUserNames(self):
        pass

    def test_getUserIds(self):
        pass

    def test_getGroups(self):
        pass

    def test_userFolderDelRoles(self):
        """
        We cannot create additional roles easily with LDAP...
        So we don't test this.
        """
        pass

    def test_getGroupNames(self):
        """Same as getUserNames() but without pure users.
        """
        un = self.gruf.getGroupNames()
        users = ['g1', 'g2', 'g3', 'g4', 'ng1', 'ng2', 'ng3', 'ng4', 'ng5', 'extranet', 'intranet', 'compta', 'r1', 'r2', 'r3', 'r4']
        un.sort()
        users.sort()
        for u in users:
            self.failUnless(u in un, "Invalid users list: '%s' is not in acl_users." % (u,))

        for u in un:
            self.failUnless(u in users, "Invalid users list: '%s' is in acl_users but shouldn't be there." % (u,))

    def test_getGroupIds(self):
        un = self.gruf.getGroupIds()
        users = ['group_g1', 'group_g2', 'group_g3', 'group_g4', 'group_ng1', 'group_ng2', 'group_ng3', 'group_ng4', 'group_ng5', 'group_extranet', 'group_intranet', 'group_compta', 'group_r1', 'group_r2', 'group_r3', 'group_r4']
        un.sort()
        users.sort()
        for u in users:
            self.failUnless(u in un, "Invalid users list: '%s' is not in acl_users." % (u,))

        for u in un:
            self.failUnless(u in users, "Invalid users list: '%s' is in acl_users but shouldn't be there." % (u,))

    def test_getGroups(self):
        """Overloaded because roles are groups"""
        objects = self.gruf.getGroups()
        un = map(lambda x: x.getId(), objects)
        users = ['group_g1', 'group_g2', 'group_g3', 'group_g4', 'group_ng1', 'group_ng2', 'group_ng3', 'group_ng4', 'group_ng5', 'group_extranet', 'group_intranet', 'group_compta', 'group_r1', 'group_r2', 'group_r3', 'group_r4']
        un.sort()
        users.sort()
        for u in users:
            self.failUnless(u in un, "Invalid users list: '%s' is not in acl_users." % (u,))

        for u in un:
            self.failUnless(u in users, "Invalid users list: '%s' is in acl_users but shouldn't be there." % (u,))

    def test_setRolesOnUsers(self):
        """Set a common set of roles for a bunch of user atoms.
        We changed this because LDAPUF add garbage roles :(
        See http://www.dataflake.org/tracker/issue_00376
        """
        self.gruf.setRolesOnUsers(['r1', 'r2', 'r3'], ['u1', 'u2'])
        for r in ('r1', 'r2', 'r3'):
            self.failUnless(r in self.gruf.getUser('u1').getRoles(), self.gruf.getUser('u1').getRoles())
            self.failUnless(r in self.gruf.getUser('u2').getRoles(), self.gruf.getUser('u2').getRoles())

    def test_userFolderEditUser(self):
        """Changed because of http://www.dataflake.org/tracker/issue_00376
        """
        self.gruf.userFolderEditUser(name='u1', password='secret2', roles=['r1'], groups=['g1'])
        self.compareRoles(None, 'u1', ['r1', 'g1'])
        return

    def test_getUsersOfRole(self):
        should_be = [
         'group_ng2', 'group_ng3', 'group_ng4', 'group_ng5', 'u9', 'u5', 'u4', 'u7', 'u6', 'u11', 'u10', 'group_g3', 'group_g4']
        should_be.sort()
        users = list(self.gruf.getUsersOfRole('r2'))
        users.sort()
        self.failUnless(users == should_be, (should_be, users))


if __name__ == '__main__':
    framework(descriptions=1, verbosity=1)
else:
    import unittest

    def test_suite():
        suite = unittest.TestSuite()
        if ldapuf:
            suite.addTest(unittest.makeSuite(TestLDAPUserFolderGroups))
        return suite
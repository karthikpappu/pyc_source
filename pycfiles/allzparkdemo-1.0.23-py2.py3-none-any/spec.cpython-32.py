# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/security/rbac/core/spec.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Dec 21, 2012\n\n@package: security - role based access control\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Ioan v. Pocol\n\nProvides specification for handling RBAC data.\n'
import abc

class IRbacService(metaclass=abc.ABCMeta):
    """
    Provides support for handling the RBAC data.
    """

    @abc.abstractmethod
    def rightsForRbacSQL(self, rbacId, sql=None):
        """
        Constructs the SQL alchemy query that fetches the RightModel assigned to the provided rbac id.
        The sql will provide the directly associated rights and the rights of the owned tree roles.
        
        @param rbacId: integer
            The rbac id.
        @param sql: sql
            The sql used for fetching the data if not provided it something like "session().query(RightModel)"
        @return: sql[RightModel]
            The sql alchemy that fetches the rights.
        """
        pass

    @abc.abstractmethod
    def rolesForRbacSQL(self, rbacId, sql=None):
        """
        Constructs the SQL alchemy query that fetches the RoleModel assigned to the provided rbac id.
        The sql will provide all the roles determined from the RBAC structure (directly assigned or inherited)
        
        @param rbacId: integer
            The rbac id.
        @param sql: sql
            The sql used for fetching the data if not provided it something like "session().query(RoleModel)"
        @return: sql[RoleModel]
            The sql alchemy that fetches the roles.
        """
        pass

    @abc.abstractmethod
    def rbacsForRightSQL(self, rightId, sql=None):
        """
        Constructs the SQL alchemy query that fetches the RbacMapped assigned to the provided right id.
        The sql will provide all the Rbac's determined from the RBAC structure (directly assigned or inherited)
        
        @param rightId: integer
            The right id.   
        @param sql: sql
            The sql used for fetching the data if not provided it something like "session().query(RbacMapped)"
        @return: sql[RbacMapped]
            The sql alchemy that fetches the Rbac's.
        """
        pass

    @abc.abstractmethod
    def rbacsForRoleSQL(self, roleId, sql=None):
        """
        Constructs the SQL alchemy query that fetches the RbacMapped assigned to the provided role id.
        The sql will provide all the Rbac's determined from the RBAC structure (directly assigned or inherited)
        
        @param roleId: integer
            The role id.   
        @param sql: sql
            The sql used for fetching the data if not provided it something like "session().query(RbacMapped)"
        @return: sql[RbacMapped]
            The sql alchemy that fetches the Rbac's.
        """
        pass

    @abc.abstractmethod
    def mergeRole(self, roleId):
        """
        Merges the role into the RBAC structure.
        
        @param roleId: integer
            The role id to be merged.
        """
        pass

    @abc.abstractmethod
    def assignRole(self, roleId, toRoleId):
        """
        Assign the provided role id to the "to" role id.
        
        @param roleId: integer
            The role id to be assigned.
        @param toRoleId: integer
            The role id to be assigned to.
        @return: boolean
            True if the assignment was a success, False otherwise.
        """
        pass

    @abc.abstractmethod
    def unassignRole(self, roleId, toRoleId):
        """
        Unassignes the provided role id from the "to" role id.
        
        @param roleId: integer
            The role id to be unassigned.
        @param toRoleId: integer
            The role id to be unassigned from.
        @return: boolean
            True if the unassign was successful, False otherwise.
        """
        pass

    @abc.abstractmethod
    def deleteRole(self, roleId):
        """
        Delete the role from the RBAC structure, attention the role should not have any child before deletion.
        
        @param roleId: integer
            The role id to be deleted.
        """
        pass


class IRbacSupport(metaclass=abc.ABCMeta):
    """
    Provides support for querying RBAC data.
    """

    @abc.abstractmethod
    def iterateTypeAndRightsNames(self, rbacId):
        """
        Iterates the RBAC right types and rights names for the provided rbac id.
        
        @param rbacId: integer
            The rbac id.
        @return: Iterable(tuple(string, Iterable(string)))
            Iterable that provides (right type name, Iterable(right name)).
        """
        pass
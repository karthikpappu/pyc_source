# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/organization.py
# Compiled at: 2020-05-07 16:37:14
# Size of source mod 2**32: 6957 bytes
from uuid import UUID
from typing import List, Union, Optional
from datalogue.errors import DtlError

class Organization:

    def __init__(self, org_id: UUID, name: str):
        self.id = org_id
        self.name = name

    def __eq__(self, other: 'Organization'):
        if isinstance(self, other.__class__):
            return self.id == other.id and self.name == other.name
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name!r})"


def _organization_from_payload(json: dict) -> Union[(DtlError, Organization)]:
    org_id = json.get('id')
    if org_id is None:
        return DtlError("Organization object should have an 'id' property")
    try:
        org_id = UUID(org_id)
    except ValueError:
        return DtlError("'id' field was not a proper uuid")
    else:
        name = json.get('name')
        if name is None:
            return DtlError("Organization object should have a 'name' property")
        else:
            return Organization(org_id, name)


class Group:

    def __init__(self, group_id: UUID, org_id: UUID, name: str):
        self.id = group_id
        self.name = name
        self.org_id = org_id

    def __eq__(self, other: 'Group'):
        if isinstance(self, other.__class__):
            return self.id == other.id and self.name == other.name and self.org_id == other.org_id
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, name: {self.name!r}, org_id: {self.org_id!r})"


def _group_from_payload(json: dict) -> Union[(DtlError, Group)]:
    group_id = json.get('id')
    if group_id is None:
        return DtlError("Group object should have an 'id' property")
    try:
        group_id = UUID(group_id)
    except ValueError:
        return DtlError("'id' field was not a proper uuid")
    else:
        name = json.get('name')
        if name is None:
            return DtlError("Group object should have a 'name' property")
        org_id = json.get('orgId')
        if org_id is None:
            return DtlError("Group object should have a 'org_id' property")
        try:
            org_id = UUID(org_id)
        except ValueError:
            return DtlError("'orgId' field was not a proper uuid")
        else:
            return Group(group_id, org_id, name)


class CreateUserRequest:
    __doc__ = '\n    Definition of request needed to create user\n    '

    def __init__(self, email: str, first_name: str, last_name: Optional[str]):
        """
        constructor of CreateUserRequest
        :param email: email of the user
        :param first_name: first name of the user
        :param last_name: last name of the user
        """
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    def as_payload(self):
        """
        Dictionary representation of the object
        :return:
        """
        return {'email':self.email, 
         'firstName':self.first_name, 
         'lastName':self.last_name}


class User:
    __doc__ = '\n    Definition of user\n    '

    def __init__(self, user_id: UUID, first_name: Optional[str], last_name: Optional[str], email: str, organization_ids: Union[(None, List[str])], group_ids: Union[(None, List[str])]):
        """
        User constructor
        :param user_id: UUID of the user
        :param first_name: user first name
        :param last_name: user last name
        :param email: user email
        :param organization_ids: ids of organizations which users belongs to
        :param group_ids: ids of groups which users belongs to
        """
        self.id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.organization_ids = organization_ids
        self.group_ids = group_ids

    def __eq__(self, other: 'User'):
        if isinstance(self, other.__class__):
            return self.id == other.id and self.first_name == other.first_name and self.last_name == other.last_name and self.email == other.email
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(id: {self.id}, first_name: {self.first_name!r}, last_name: {self.last_name!r}, email: {self.email!r}, organization_ids: {self.organization_ids!r}, group_ids: {self.group_ids!r})"


def _user_from_payload(json: dict) -> Union[(DtlError, User)]:
    user_id = json.get('user').get('id')
    if user_id is None:
        return DtlError("User object should have an 'id' property")
    try:
        user_id = UUID(user_id)
    except ValueError:
        return DtlError("'id' field was not a proper uuid")
    else:
        first_name = json.get('user').get('firstName')
        last_name = json.get('user').get('lastName')
        email = json.get('user').get('email')
        if email is None:
            return DtlError("User object should have a 'email' property")
        else:
            organization_ids = json.get('organizationsIds')
            group_ids = json.get('groupsIds')
            if group_ids is None:
                return DtlError("User object should have a 'groupsIds' property")
            return User(user_id, first_name, last_name, email, organization_ids, group_ids)


def _users_from_payload(json: dict) -> Union[(DtlError, User)]:
    user_id = json.get('id')
    if user_id is None:
        return DtlError("User object should have an 'id' property")
    try:
        user_id = UUID(user_id)
    except ValueError:
        return DtlError("'id' field was not a proper uuid")
    else:
        first_name = json.get('firstName')
        last_name = json.get('lastName')
        email = json.get('email')
        if email is None:
            return DtlError("User object should have a 'email' property")
        else:
            group_ids = json.get('groupIds')
            return User(user_id, first_name, last_name, email, None, group_ids)


class Domain:

    def __init__(self, org_id: UUID, domain: str):
        self.org_id = org_id
        self.domain = domain

    def __eq__(self, other: 'Domain'):
        if isinstance(self, other.__class__):
            return self.org_id == other.org_id and self.domain == other.domain
        else:
            return False

    def __repr__(self):
        return f"{self.__class__.__name__}(org_id: {self.org_id}, domain: {self.domain!r})"

    def __hash__(self):
        return hash(self.org_id) ^ hash(self.domain)


def _domain_from_payload(json: dict) -> Union[(DtlError, Domain)]:
    org_id = json.get('orgId')
    if org_id is None:
        return DtlError("Domain object should have an 'orgId' property")
    try:
        org_id = UUID(org_id)
    except ValueError:
        return DtlError("'id' field was not a proper uuid")
    else:
        domain = json.get('domain')
        if domain is None:
            return DtlError("Domain object should have a 'domain' property")
        else:
            return Domain(org_id, domain)
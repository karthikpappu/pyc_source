# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/var/pyenv/versions/hub/lib/python2.7/site-packages/membersuite_api_client/security/models.py
# Compiled at: 2018-06-12 19:49:54
from __future__ import absolute_import, division, print_function, unicode_literals
from future.utils import python_2_unicode_compatible
from ..exceptions import ExecuteMSQLError
from ..models import MemberSuiteObject
from ..memberships import services as membership_services
from ..organizations.models import Organization
from ..utils import convert_ms_object

def generate_username(membersuite_object):
    """Return a username suitable for storing in auth.User.username.

    Has to be <= 30 characters long.  (Until we drop support for
    Django 1.4, after which we can define a custom User model with
    a larger username field.)

    We want to incorporate the membersuite_id in the username.
    Those look like this:

        6faf90e4-0032-c842-a28a-0b3c8b856f80

    That's 36 characters, too long for username.  Making the
    assumption that those leading digits will always be there in
    every ID.  Since they're not needed to generate a unique
    value, they can go.

    After chomping the intro, we're at 27 characters, so we
    insert "ms" in the front.

    """
    username = b'ms' + membersuite_object.membersuite_id[len(b'6faf90e4'):]
    return username


@python_2_unicode_compatible
class PortalUser(MemberSuiteObject):

    def __init__(self, membersuite_object_data, session_id=None):
        """Create a PortalUser object from a the Zeep'ed XML representation of
        a Membersuite PortalUser.

        """
        super(PortalUser, self).__init__(membersuite_object_data=membersuite_object_data)
        self.email_address = self.fields[b'EmailAddress']
        self.first_name = self.fields[b'FirstName']
        self.last_name = self.fields[b'LastName']
        self.owner = self.fields[b'Owner']
        self.session_id = session_id

    def __str__(self):
        return (b'<PortalUser: ID: {id}, email_address: {email_address}, first_name: {first_name}, last_name: {last_name}, owner: {owner}, session_id: {session_id}>').format(id=self.membersuite_id, email_address=self.email_address, first_name=self.first_name, last_name=self.last_name, owner=self.owner, session_id=self.session_id)

    def get_individual(self, client):
        """Return the Individual that owns this PortalUser.

        """
        if not client.session_id:
            client.request_session()
        object_query = (b"SELECT OBJECT() FROM INDIVIDUAL WHERE ID = '{}'").format(self.owner)
        result = client.execute_object_query(object_query)
        msql_result = result[b'body'][b'ExecuteMSQLResult']
        if msql_result[b'Success']:
            membersuite_object_data = msql_result[b'ResultValue'][b'SingleObject']
        else:
            raise ExecuteMSQLError(result=result)
        return Individual(membersuite_object_data=membersuite_object_data, portal_user=self)


@python_2_unicode_compatible
class Individual(MemberSuiteObject):

    def __init__(self, membersuite_object_data, portal_user=None):
        """Create an Individual object from the Zeep'ed XML representation of
        a MemberSuite Individual.

        """
        super(Individual, self).__init__(membersuite_object_data=membersuite_object_data)
        self.email_address = self.fields[b'EmailAddress']
        self.first_name = self.fields[b'FirstName']
        self.last_name = self.fields[b'LastName']
        self.title = self.fields[b'Title']
        self.primary_organization_id = self.fields[b'PrimaryOrganization__rtg']
        self.portal_user = portal_user

    def __str__(self):
        return (b'<Individual: ID: {id}, email_address: {email_address}, first_name: {first_name}, last_name: {last_name}>').format(id=self.membersuite_id, email_address=self.email_address, first_name=self.first_name, last_name=self.last_name)

    @property
    def phone_number(self):
        numbers = self.fields[b'PhoneNumbers'][b'MemberSuiteObject']
        if len(numbers):
            for key_value_pair in numbers[0][b'Fields'][b'KeyValueOfstringanyType']:
                if key_value_pair[b'Key'] == b'PhoneNumber':
                    return key_value_pair[b'Value']

        return

    def is_member(self, client):
        """Is this Individual a member?

        Assumptions:

          - a "primary organization" in MemberSuite is the "current"
            Organization for an Individual

          - get_memberships_for_org() returns Memberships ordered such
            that the first one returned is the "current" one.

        """
        if not client.session_id:
            client.request_session()
        primary_organization = self.get_primary_organization(client=client)
        if primary_organization:
            print(primary_organization, primary_organization.membersuite_id)
            membership_service = membership_services.MembershipService(client=client)
            membership = membership_service.get_current_membership_for_org(account_num=primary_organization.id)
            if membership:
                print(membership, membership.id)
                return membership.receives_member_benefits
            print(b'no membership')
            return False
        else:
            return False

    def get_primary_organization(self, client):
        """Return the primary Organization for this Individual.

        """
        if self.primary_organization_id is None:
            return
        else:
            if not client.session_id:
                client.request_session()
            object_query = (b"SELECT OBJECT() FROM ORGANIZATION WHERE ID = '{}'").format(self.primary_organization_id)
            result = client.execute_object_query(object_query)
            msql_result = result[b'body'][b'ExecuteMSQLResult']
            if msql_result[b'Success']:
                membersuite_object_data = msql_result[b'ResultValue'][b'SingleObject']
            else:
                raise ExecuteMSQLError(result=result)
            organization = convert_ms_object(membersuite_object_data[b'Fields'][b'KeyValueOfstringanyType'])
            return Organization(org=organization)
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pybitbucket/repository.py
# Compiled at: 2016-12-28 18:40:02
# Size of source mod 2**32: 15251 bytes
from __future__ import unicode_literals
from uritemplate import expand
from voluptuous import Schema, Required, Optional, In
from pybitbucket.bitbucket import Bitbucket, BitbucketBase, Client, PayloadBuilder, RepositoryType, Enum
from pybitbucket.user import User

class RepositoryRole(Enum):
    OWNER = 'owner'
    ADMIN = 'admin'
    CONTRIBUTOR = 'contributor'
    MEMBER = 'member'


class RepositoryForkPolicy(Enum):
    ALLOW_FORKS = 'allow_forks'
    NO_PUBLIC_FORKS = 'no_public_forks'
    NO_FORKS = 'no_forks'


class RepositoryPayload(PayloadBuilder):
    """RepositoryPayload"""
    schema = Schema({Optional('scm'): In(RepositoryType), 
     Optional('name'): str, 
     Required('is_private'): bool, 
     Optional('description'): str, 
     Required('fork_policy'): In(RepositoryForkPolicy), 
     Optional('language'): str, 
     Optional('has_issues'): bool, 
     Optional('has_wiki'): bool})

    def __init__(self, payload=None, owner=None):
        super(RepositoryPayload, self).__init__(payload=payload)
        self._owner = owner

    @property
    def owner(self):
        return self._owner

    @property
    def name(self):
        return self._payload.get('name')

    def add_owner(self, owner):
        return RepositoryPayload(payload=(self._payload.copy()),
          owner=owner)

    def add_name(self, name):
        new = self._payload.copy()
        new['name'] = name
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_is_private(self, is_private):
        new = self._payload.copy()
        new['is_private'] = is_private
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_fork_policy(self, policy):
        new = self._payload.copy()
        new['fork_policy'] = policy
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_scm(self, scm):
        new = self._payload.copy()
        new['scm'] = scm
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_description(self, description):
        new = self._payload.copy()
        new['description'] = description
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_language(self, language):
        new = self._payload.copy()
        new['language'] = language
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_has_wiki(self, has_wiki):
        new = self._payload.copy()
        new['has_wiki'] = has_wiki
        return RepositoryPayload(payload=new,
          owner=(self._owner))

    def add_has_issues(self, has_isues):
        new = self._payload.copy()
        new['has_issues'] = has_isues
        return RepositoryPayload(payload=new,
          owner=(self._owner))


class RepositoryForkPayload(RepositoryPayload):
    schema = Schema({Required('name'): str, 
     Optional('scm'): In(RepositoryType), 
     Optional('is_private'): bool, 
     Optional('description'): str, 
     Optional('language'): str, 
     Optional('fork_policy'): In(RepositoryForkPolicy)})


class Repository(BitbucketBase):
    """Repository"""
    id_attribute = 'full_name'
    resource_type = 'repositories'
    templates = {'create':'{+bitbucket_url}' + '/2.0/repositories' + '{/owner,repository_name}', 
     'fork':'{+bitbucket_url}' + '/1.0/repositories' + '{/owner,repository_name}' + '/fork'}

    @staticmethod
    def is_type(data):
        return Repository.has_v2_self_url(data)

    def __init__(self, data, client=None):
        client = client or Client()
        super(Repository, self).__init__(data, client=client)
        if data.get('links', {}).get('clone'):
            self.clone = {clone_method['name']:clone_method['href'] for clone_method in data['links']['clone']}
        self.v1 = RepositoryV1(data, client)

    @classmethod
    def create(cls, payload, repository_name=None, owner=None, client=None):
        """Create a new repository.

        :param payload: the options for creating the new repository
        :type payload: RepositoryPayload
        :param repository_name: name of the repository,
            also known as repo_slug. Optional, if provided in the payload.
        :type repository_name: str
        :param owner: the owner of the repository.
            If not provided, assumes the current user.
        :type owner: str
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the new repository object.
        :rtype: Repository
        :raises: ValueError
        """
        client = client or Client()
        owner = owner or client.get_username()
        repository_name = repository_name or payload.name
        if not (owner and repository_name):
            raise ValueError('owner and repository_name are required')
        json = payload.validate().build()
        api_url = expand(cls.templates['create'], {'bitbucket_url':client.get_bitbucket_url(), 
         'owner':owner, 
         'repository_name':repository_name})
        return cls.post(api_url, json=json, client=client)

    @classmethod
    def fork(cls, payload, repository_name=None, owner=None, client=None):
        """Forks a repository.

        :param payload: the options for forking repository as a new one
        :type payload: RepositoryForkPayload
        :param repository_name: name of the repository,
            also known as repo_slug. Optional, if provided in the payload.
        :type repository_name: str
        :param owner: the owner of the repository.
            If not provided, assumes the current user.
        :type owner: str
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the new repository object.
        :rtype: Repository
        :raises: ValueError
        """
        client = client or Client()
        owner = owner or client.get_username()
        repository_name = repository_name or payload.name
        if not (owner and repository_name):
            raise ValueError('owner and repository_name are required')
        data = payload.validate().build()
        api_url = expand(cls.templates['fork'], {'bitbucket_url':client.get_bitbucket_url(), 
         'owner':owner, 
         'repository_name':repository_name})
        return cls.post(api_url, data=data, client=client)

    @staticmethod
    def find_repository_by_name_and_owner(repository_name, owner=None, client=None):
        """
        A convenience method for finding a specific repository.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a Repository object, instead of the
        generator.

        :param repository_name: name of the repository,
            also known as repo_slug.
        :type repository_name: str
        :param owner: the owner of the repository.
            If not provided, assumes the current user.
        :type owner: str
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the specific repository object.
        :rtype: Repository
        """
        client = client or Client()
        owner = owner or client.get_username()
        return next(Bitbucket(client=client).repositoryByOwnerAndRepositoryName(owner=owner,
          repository_name=repository_name))

    @staticmethod
    def find_repository_by_full_name(full_name, client=None):
        """
        A convenience method for finding a specific repository.
        In contrast to the pure hypermedia driven method on the Bitbucket
        class, this method returns a Repository object, instead of the
        generator.

        :param full_name: full name of the repository,
            with both owner and repo_slug separated by slash.
        :type full_name: str
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: the specific repository object.
        :rtype: Repository
        :raises: TypeError
        """
        client = client or Client()
        if '/' not in full_name:
            raise TypeError('Repository full name must be in the form: username/name')
        owner, repository_name = full_name.split('/')
        return Repository.find_repository_by_name_and_owner(owner=owner,
          repository_name=repository_name,
          client=client)

    @staticmethod
    def find_public_repositories(client=None):
        """
        A convenience method for finding public repositories.
        The method is a generator Repository objects.

        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: an iterator over all public repositories.
        :rtype: iterator
        """
        client = client or Client()
        return Bitbucket(client=client).repositoriesThatArePublic()

    @staticmethod
    def find_repositories_by_owner_and_role(owner=None, role=RepositoryRole.OWNER, client=None):
        """
        A convenience method for finding a user's repositories.
        The method is a generator Repository objects.
        When no owner is provided, it uses the currently authenticated user.

        :param owner: the owner of the repository.
            If not provided, assumes the current user.
        :type owner: str
        :param role: the role of the current user on the repositories.
            If not provided, assumes the relationship owner.
        :type role: RepositoryRole
        :param client: the configured connection to Bitbucket.
            If not provided, assumes an Anonymous connection.
        :type client: bitbucket.Client
        :returns: an iterator over all public repositories.
        :rtype: iterator
        """
        client = client or Client()
        owner = owner or client.get_username()
        RepositoryRole(role)
        return Bitbucket(client=client).repositoriesByOwnerAndRole(owner=owner,
          role=role)


class RepositoryAdapter(object):
    """RepositoryAdapter"""

    def __init__(self, data, client=None):
        self.client = client or Client()
        if data.get('full_name') is None:
            self.owner_name = data.get('owner')
            self.repository_name = data.get('name')
        else:
            self.owner_name, self.repository_name = data['full_name'].split('/')

    def self(self):
        return Repository.find_repository_by_name_and_owner((self.repository_name),
          owner=(self.owner_name),
          client=(self.client))

    def owner(self):
        return User.find_user_by_username((self.owner_name),
          client=(self.client))


class RepositoryV1(BitbucketBase):
    """RepositoryV1"""
    id_attribute = 'name'
    links_json = '\n{\n  "_links": {\n    "self": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}"\n    },\n    "repositories": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner}"\n    },\n    "changesets": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/changesets{?limit,start}"\n    },\n    "deploy_keys": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/deploy-keys"\n    },\n    "events": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/events"\n    },\n    "followers": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/followers"\n    },\n    "issues": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/issues"\n    },\n    "integration_links": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/links"\n    },\n    "services": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/services"\n    },\n    "src": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/src{/revision,path}"\n    },\n    "wiki": {\n      "href": "{+bitbucket_url}/1.0/repositories{/owner,repository_name}/wiki{/page}"\n    }\n  }\n}\n'

    @staticmethod
    def is_type(data):
        return data.get('resource_uri') is not None and data.get('scm') is not None and data.get('slug') is not None

    def __init__(self, data, client=None):
        client = client or Client()
        super(RepositoryV1, self).__init__(data, client)
        self.v2 = RepositoryAdapter(data, client)
        expanded_links = self.expand_link_urls(bitbucket_url=(client.get_bitbucket_url()),
          owner=(self.v2.owner_name),
          repository_name=(self.v2.repository_name))
        self.links = expanded_links.get('_links', {})
        self.add_remote_relationship_methods(expanded_links)


Client.bitbucket_types.add(Repository)
Client.bitbucket_types.add(RepositoryV1)
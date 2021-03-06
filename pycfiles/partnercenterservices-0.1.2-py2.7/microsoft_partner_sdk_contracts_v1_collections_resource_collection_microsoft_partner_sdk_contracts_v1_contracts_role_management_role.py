# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_collections_resource_collection_microsoft_partner_sdk_contracts_v1_contracts_role_management_role.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1CollectionsResourceCollectionMicrosoftPartnerSdkContractsV1ContractsRoleManagementRole(Model):
    """Contains a collection of resources with JSON properties to represent the
    output.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar total_count: Gets the total count.
    :vartype total_count: int
    :ivar items: Gets the collection items.
    :vartype items:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1ContractsRoleManagementRole]
    :param links: Gets or sets the links.
    :type links:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceLinks
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'total_count': {'readonly': True}, 'items': {'readonly': True}, 'attributes': {'readonly': True}}
    _attribute_map = {'total_count': {'key': 'totalCount', 'type': 'int'}, 'items': {'key': 'items', 'type': '[MicrosoftPartnerSdkContractsV1ContractsRoleManagementRole]'}, 'links': {'key': 'links', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceLinks'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, links=None):
        super(MicrosoftPartnerSdkContractsV1CollectionsResourceCollectionMicrosoftPartnerSdkContractsV1ContractsRoleManagementRole, self).__init__()
        self.total_count = None
        self.items = None
        self.links = links
        self.attributes = None
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_relationship_request_details.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1RelationshipRequestDetails(Model):
    """Represents a relationship request contents with a partner.

    :param partner_id: Gets or sets the partner identifier.
    :type partner_id: str
    :param contact_lines: Gets or sets the contact lines.
    :type contact_lines: list[str]
    :param address_lines: Gets or sets the address lines.
    :type address_lines: list[str]
    """
    _attribute_map = {'partner_id': {'key': 'partnerId', 'type': 'str'}, 'contact_lines': {'key': 'contactLines', 'type': '[str]'}, 'address_lines': {'key': 'addressLines', 'type': '[str]'}}

    def __init__(self, partner_id=None, contact_lines=None, address_lines=None):
        super(MicrosoftPartnerSdkContractsV1RelationshipRequestDetails, self).__init__()
        self.partner_id = partner_id
        self.contact_lines = contact_lines
        self.address_lines = address_lines
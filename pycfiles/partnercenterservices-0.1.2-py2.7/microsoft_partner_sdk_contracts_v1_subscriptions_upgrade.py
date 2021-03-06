# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_subscriptions_upgrade.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1SubscriptionsUpgrade(Model):
    """Describes the behavior of an individual subscription upgrade resource.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param target_offer: Gets or sets the offer of the target subscription.
    :type target_offer:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1Offer
    :param upgrade_type: Gets or sets the type of upgrade. Possible values
     include: 'none', 'upgrade_only', 'upgrade_with_license_transfer'
    :type upgrade_type: str or
     ~microsoft.store.partnercenterservices.models.enum
    :param is_eligible: Gets or sets a value that indicates whether the
     upgrade can be performed.
    :type is_eligible: bool
    :param quantity: Gets or sets the quantity of the new offer to be
     purchased.  Defaults to the source subscription quantity.
    :type quantity: int
    :param upgrade_errors: The reasons the upgrade cannot be performed, if
     applicable.
    :type upgrade_errors:
     list[~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError]
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'target_offer': {'key': 'targetOffer', 'type': 'MicrosoftPartnerSdkContractsV1Offer'}, 'upgrade_type': {'key': 'upgradeType', 'type': 'str'}, 'is_eligible': {'key': 'isEligible', 'type': 'bool'}, 'quantity': {'key': 'quantity', 'type': 'int'}, 'upgrade_errors': {'key': 'upgradeErrors', 'type': '[MicrosoftPartnerSdkContractsV1SubscriptionsUpgradeError]'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, target_offer=None, upgrade_type=None, is_eligible=None, quantity=None, upgrade_errors=None):
        super(MicrosoftPartnerSdkContractsV1SubscriptionsUpgrade, self).__init__()
        self.target_offer = target_offer
        self.upgrade_type = upgrade_type
        self.is_eligible = is_eligible
        self.quantity = quantity
        self.upgrade_errors = upgrade_errors
        self.attributes = None
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_contracts_v1_partner_offer.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkContractsV1PartnerOffer(Model):
    """Represents a product availability to a partner.

    :param id: The unique identifier of the product availability.
    :type id: str
    :param name: The name.
    :type name: str
    :param description: The description.
    :type description: str
    :param product_id: The product Id.
    :type product_id: str
    :param sku_id: The SKU Id.
    :type sku_id: str
    :param currency_code: The currency code.
    :type currency_code: str
    :param currency_symbol: The currency symbol.
    :type currency_symbol: str
    :param list_price: The list price.
    :type list_price: float
    :param locale: The locale.
    :type locale: str
    :param country: The country.
    :type country: str
    """
    _attribute_map = {'id': {'key': 'id', 'type': 'str'}, 'name': {'key': 'name', 'type': 'str'}, 'description': {'key': 'description', 'type': 'str'}, 'product_id': {'key': 'productId', 'type': 'str'}, 'sku_id': {'key': 'skuId', 'type': 'str'}, 'currency_code': {'key': 'currencyCode', 'type': 'str'}, 'currency_symbol': {'key': 'currencySymbol', 'type': 'str'}, 'list_price': {'key': 'listPrice', 'type': 'float'}, 'locale': {'key': 'locale', 'type': 'str'}, 'country': {'key': 'country', 'type': 'str'}}

    def __init__(self, id=None, name=None, description=None, product_id=None, sku_id=None, currency_code=None, currency_symbol=None, list_price=None, locale=None, country=None):
        super(MicrosoftPartnerSdkContractsV1PartnerOffer, self).__init__()
        self.id = id
        self.name = name
        self.description = description
        self.product_id = product_id
        self.sku_id = sku_id
        self.currency_code = currency_code
        self.currency_symbol = currency_symbol
        self.list_price = list_price
        self.locale = locale
        self.country = country
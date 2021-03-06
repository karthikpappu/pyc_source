# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/microsoft/store/partnercenterservices/models/microsoft_partner_sdk_internal_contracts_analytics_customer_licenses.py
# Compiled at: 2019-02-19 17:42:21
from msrest.serialization import Model

class MicrosoftPartnerSdkInternalContractsAnalyticsCustomerLicenses(Model):
    """Business object model that represents a flat list of Licenses insights for
    a partner across all customers.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :param processed_timestamp: last Processed date for data
    :type processed_timestamp: datetime
    :param customer_name: Customer Name
    :type customer_name: str
    :param customer_id: Customer Tenant Id
    :type customer_id: str
    :param customer_country_code: Country Code
    :type customer_country_code: str
    :param channel_name: Channel Name
    :type channel_name: str
    :param service_name: Service Name
    :type service_name: str
    :param product_name: Product Name
    :type product_name: str
    :param workload_name: Workload Name
    :type workload_name: str
    :param total_sold_seats: Total Sold Seats
    :type total_sold_seats: long
    :param total_deployed_seats: Total Deployed Seats
    :type total_deployed_seats: long
    :param total_seats: Total Seats
    :type total_seats: long
    :param total_active_seats: Total Active Seats
    :type total_active_seats: long
    :param service_code: Service code of the given service (O365, CRM)
    :type service_code: str
    :ivar attributes: Gets the attributes.
    :vartype attributes:
     ~microsoft.store.partnercenterservices.models.MicrosoftPartnerSdkContractsV1CommonResourceAttributes
    """
    _validation = {'attributes': {'readonly': True}}
    _attribute_map = {'processed_timestamp': {'key': 'processedTimestamp', 'type': 'iso-8601'}, 'customer_name': {'key': 'customerName', 'type': 'str'}, 'customer_id': {'key': 'customerId', 'type': 'str'}, 'customer_country_code': {'key': 'customerCountryCode', 'type': 'str'}, 'channel_name': {'key': 'channelName', 'type': 'str'}, 'service_name': {'key': 'serviceName', 'type': 'str'}, 'product_name': {'key': 'productName', 'type': 'str'}, 'workload_name': {'key': 'workloadName', 'type': 'str'}, 'total_sold_seats': {'key': 'totalSoldSeats', 'type': 'long'}, 'total_deployed_seats': {'key': 'totalDeployedSeats', 'type': 'long'}, 'total_seats': {'key': 'totalSeats', 'type': 'long'}, 'total_active_seats': {'key': 'totalActiveSeats', 'type': 'long'}, 'service_code': {'key': 'serviceCode', 'type': 'str'}, 'attributes': {'key': 'attributes', 'type': 'MicrosoftPartnerSdkContractsV1CommonResourceAttributes'}}

    def __init__(self, processed_timestamp=None, customer_name=None, customer_id=None, customer_country_code=None, channel_name=None, service_name=None, product_name=None, workload_name=None, total_sold_seats=None, total_deployed_seats=None, total_seats=None, total_active_seats=None, service_code=None):
        super(MicrosoftPartnerSdkInternalContractsAnalyticsCustomerLicenses, self).__init__()
        self.processed_timestamp = processed_timestamp
        self.customer_name = customer_name
        self.customer_id = customer_id
        self.customer_country_code = customer_country_code
        self.channel_name = channel_name
        self.service_name = service_name
        self.product_name = product_name
        self.workload_name = workload_name
        self.total_sold_seats = total_sold_seats
        self.total_deployed_seats = total_deployed_seats
        self.total_seats = total_seats
        self.total_active_seats = total_active_seats
        self.service_code = service_code
        self.attributes = None
        return
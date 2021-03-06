# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/splunk_toolbox/__init__.py
# Compiled at: 2019-05-23 15:23:28
import requests, logging, json, time
name = 'splunk_toolbox'
logging.basicConfig(filename='betterSplunkITSI.log', filemode='w', level=logging.DEBUG, format='%(asctime)s.%(msecs)03d %(levelname)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S')
debug = 0

class splunkInstance:

    def __init__(self, host='127.0.0.1', mgmtPort='8089', authUser='admin', authPass='changeme', paramSsl='1', apiVersion='vLatest', debug=False, logging=0):
        """
        SplunkInstance:
        This class should represent a single splunk server connection
        Much of the data set here is to make a ubiquitous URI when connecting
        ------
        TODO: Name is a place holder. object represents literally a single splunk instance so using literal for now.
        ------
        Variables:
                -host: The splunk servers IP address or DNS alias. Defaults to localhost
                -mgmtPort: The management port of the splunk instance over which to sen
                -authUser: Username presented at time of REST connection to the server to authenticate our request, in conjunction with pass.
                -authPass: Password presented at time of REST connection to the server, to authenticate our request, in conjunction with user.
        """
        try:
            self.ssl = self.__interpret_ssl(ssl_input=paramSsl)
            self.host = host
            self.mgmtPort = int(mgmtPort)
            self.authUser = str(authUser)
            self.authPass = str(authPass)
            self.portColon = self.__interpret_colon(inputMgmtPort=mgmtPort)
            self.apiVersion = apiVersion
            self.baseUrl = self.__set_base_URL()
            self.debug = debug
        except Exception as E1:
            print 'Error Code E1 encountered while in splunkInstance __init__\n'
            logging.error('Error E1 in splunkInstance__init__ Please check configuration parameters')
            raise ValueError(E1)

    def __set_base_URL(self):
        """
        Private method-
        Just a simple test to see if we can assemble a basic request to a URI using the params provided by the end user
        """
        try:
            if self.mgmtPort == 80 or self.mgmtPort == 443:
                mgmtPort = ''
            else:
                mgmtPort = str(self.mgmtPort)
            currentURL = self.ssl + '://' + self.host + ':' + self.portColon + mgmtPort
            return currentURL
        except Exception as E2:
            print 'Error Code E2 encountered while in splunkInstance __set_base_URL\n'
            raise ValueError(E2)

    def __interpret_ssl(self, ssl_input):
        """
        Private method that reads the configuration input from the user to determine what the ssl state should be set to.
        Point of this function is to abstract away this logic away from the base object, for readability
        ------
        Params:
                -ssl: Checks user argument then sets the splunk instances internal state to http or https accordingly
        ------
        Returns:
        The expected return value of this function will either be a string http or https
        """
        if ssl_input == '1' or ssl_input == 'yes' or ssl_input == True or ssl_input == 'YES' or ssl_input == 'True' or ssl_input == 'T':
            sslReturn = 'https'
            return sslReturn
        if ssl_input == 0:
            sslReturn = 'http'
            sreturn(sslReturn)

    def __interpret_colon(self, inputMgmtPort):
        """
        Private method that reads the input management port from the user to determine,
        whether or not we need to indicate the port in 
        ------
        Params:
                -inputMgmtPort: the management port input from user level
        """
        if inputMgmtPort == None or inputMgmtPort == '80' or inputMgmtPort == 80 or inputMgmtPort == '443' or self.ssl == 'https':
            portColon = ''
            return portColon
        else:
            portColon = ':'
            return portColon
            return

    def __is_json(self, data=None):
        """
        Private method that checks if the data provided as a parameter is a JSON or not
        """
        if data != None:
            data = str(data)
            if json.loads(data):
                return True
            return False
        else:
            return False
        return

    def basic_post(self, payload=None, endpointPath=None, serviceId=None):
        """
        Public function
        Sends non garbage posts, free of charge
        TODO: clean this up. Was made hastily while watching an ITSI load process.
        TODO: url check end to see if ends in slash, if not, inject slashes
        """
        payload = str(payload)
        isValidJson = self.__is_json(payload)
        if self.debug == True:
            print 'JSON is valid status: ' + str(isValidJson)
        if isValidJson == True:
            if self.debug == True:
                print 'Debug Block 248E hit: hey its valid JSON'
            tempUrl = self.baseUrl + str(endpointPath) + str(serviceId) + '/?is_partial_data=1'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            currentRequest = requests.post(auth=(self.authUser, self.authPass), url=tempUrl, json=payload, headers=headers, verify=False)
            print currentRequest.status_code
        else:
            print 'invalid Json submitted'

    def post_update_to_notable_event_group(self, payload=None, endpointPath=None, itsi_group_id=None):
        """
        Public function
        Sends non garbage posts, free of charge
        TODO: clean this up. Was made hastily while watching an ITSI load process.
        TODO: url check end to see if ends in slash, if not, inject slashes
        """
        payload = str(payload)
        isValidJson = self.__is_json(payload)
        if self.debug == True:
            print 'JSON is valid status: ' + str(isValidJson)
        if isValidJson == True:
            if self.debug == True:
                print 'Debug Block 2499A hit: hey its valid JSON'
            tempUrl = self.baseUrl + '/servicesNS/nobody/SA-ITOA/event_management_interface/notable_event_group/' + str(itsi_group_id) + '/?is_partial_data=1'
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            currentRequest = requests.post(auth=(self.authUser, self.authPass), url=tempUrl, json=payload, headers=headers, verify=False)
            try:
                statusCode = currentRequest.status_code
                print statusCode
                if str(statusCode) == '200':
                    print 'Posted OK'
                if str(statusCode) == '500':
                    print 'Failed to find that ITSI_Group_ID in the KV store'
                if str(statusCode) == '401':
                    print 'Authentication Error - Change your username and or password'
            except Exception as responseStatusCode:
                print 'There was no HTTP response code  or the response code was botched'
                print responseStatusCode

            try:
                print currentRequest.text
            except Exception as responseTextError:
                print 'There was no Response text or it was botched, see reason:\n'
                print responseTextError

        else:
            print 'invalid Json submitted'

    def retrieve_indexes(self, **kwargs):
        """
        Retrieves indexes from Splunk via REST
        If no indexes are requested, then all will be retrieved from that host
        If no attributes of that index are specified, all attributes will be retrieved
        # https://splunk.openmobo.com:8089/servicesNS/nobody/introspection_generator_addon/admin/indexes
        Parameters:
        ------
         - index: string, when set, requests details of a specific index rather than all indexes.
         - attribute:string, when set, returns values/details of a specific index
         
         Return Values:
         ------
          - 0 if 
          - a dictionary if there are multiple key/value pairs for a given attribute, or if no attribute is selected, a dictionary of dictionaries.
        """
        is_valid_json = 0
        index = None
        attributes = []
        if isset(kwargs):
            for key, value in kwargs:
                key = str(key)
                value = str(value)
                if key == 'index':
                    index = value
                if key == 'attribute':
                    attributes.append(value)

        return

    def __debug_message(self, msg):
        """
        REPLs a message out to stdo stream if debug is enabled
        """
        if debug == 1:
            print str(msg)
            logging.debug(str(msg))

    def retrieve_correlation_search_count(self, recordSearches=0):
        """
        Retrieves correlation_searches from Splunk ITSI
        WIP
        TODO: API currently broken in ITSI, think of alternative way to list these out...

        Parameters:
         - recordSearches: integer, 0/1, default 0. If true, writes search results out to file
        """
        try:
            self.__debug_message(msg='starting correlation search count')
            endpointPath = '/servicesNS/nobody/SA-ITOA/event_management_interface/correlation_search/?'
            tempUrl = self.baseUrl + str(endpointPath) + '/\\?limit\\=1'
            currentRequest = requests.get(auth=(self.authUser, self.authPass), url=tempUrl, verify=False)
            if recordSearches == 1:
                recordSearchesFile = open('recordedSearches.xml', 'w')
                recordSearchesFile.write(str(currentRequest.text))
                recordSearchesFile.close()
            self.__debug_message(msg='Got past current_requests')
            self.__debug_message('Status Code = ' + str(currentRequest.status_code))
            self.__debug_message('Status_Text = ' + str(currentRequest.text))
        except Exception as Error01:
            systemMessage = str(Error01)
            errorTitle = 'Error01'
            errorDesc = ''
            ErrorMsg = 'ErrorTitle="%s" ErrorMessage="%s" System_Message="%s' % (errorTitle, errorDesc, systemMessage)
            logging.error(ErrorMsg)
            raise Exception(ErrorMsg)

    def retrieve_configured_saved_searches(self, recordSearches=0):
        """
        Retrieves saved searches from search head
        """
        try:
            self.__debug_message('Starting retrieval of saved splunk searches')
            endpointPath = '/services/saved/searches'
            tempUrl = self.baseUrl + str(endpointPath)
            currentRequest = requests.get(auth=(self.authUser, self.authPass), url=tempUrl, verify=False)
            if recordSearches == 1:
                timestr = time.strftime('%Y%m%d-%H%M%S')
                recordSearchesFile = open(timestr + '__recordedCorrelationSearches.xml', 'w')
                recordSearchesFile.write(str(currentRequest.text))
                recordSearchesFile.close()
            else:
                print currentRequest.text
        except Exception as retrieveSavedSearchError01:
            errorTitle = 'retrieveSavedSearchError01'
            errorDesc = 'error when trying to grab a core splunk saved search detail'
            systemMessage = str(retrieveSavedSearchError01)
            ErrorMsg = 'ErrorTitle="%s" ErrorMessage="%s" System_Message="%s' % (errorTitle, errorDesc, systemMessage)
            logging.error(ErrorMsg)
            raise Exception(ErrorMsg)

    def retrieve_search_jobs(self, recordSearches=0):
        """
        Retrieves correlation_searches from Splunk ITSI

        Parameters:
         - recordSearches: integer, 0/1, default 0. If true, writes search results out to file
        """
        try:
            self.__debug_message(msg='starting search jobs record')
            endpointPath = '/services/search/jobs'
            tempUrl = self.baseUrl + str(endpointPath)
            currentRequest = requests.get(auth=(self.authUser, self.authPass), url=tempUrl, verify=False)
            if recordSearches == 1:
                timestr = time.strftime('%Y%m%d-%H%M%S')
                recordSearchesFile = open(timestr + '__recordedSearches.xml', 'w')
                recordSearchesFile.write(str(currentRequest.text))
                recordSearchesFile.close()
            self.__debug_message(msg='Got past current_requests')
            self.__debug_message('Status Code = ' + str(currentRequest.status_code))
            self.__debug_message('Status_Text = ' + str(currentRequest.text))
        except Exception as Error02:
            systemMessage = str(Error02)
            errorTitle = 'Error01'
            errorDesc = ''
            ErrorMsg = 'ErrorTitle="%s" ErrorMessage="%s" System_Message="%s' % (errorTitle, errorDesc, systemMessage)
            logging.error(ErrorMsg)
            raise Exception(ErrorMsg)
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/botnee/taxonomy/metamap_wrapper.py
# Compiled at: 2012-06-19 11:32:18
import urllib, urllib2, xml.dom.minidom, signal, logging
from botnee import debug
import botnee_config
CONCEPT_FIELDS = ('cui', 'displayName', 'preferredName', 'sources', 'semanticTypes',
                  'matchedText')

class TimeoutException(Exception):
    pass


class MetamapWrapper(object):
    """
    Wrapper class for the RESTful metamamap server instance
    """

    def __init__(self):
        self.url = botnee_config.METAMAP_SERVER
        self.timeout = botnee_config.METAMAP_TIMEOUT
        self.logger = logging.getLogger(__name__)

    def query_by_text(self, text, verbose=False):
        """
        Queries the metamap instance using the supplied text string
        Uses signal module to create a timeout
        """

        def timeout_handler(signum, frame):
            raise TimeoutException()

        if self.timeout > 0:
            signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(self.timeout)
        with debug.Timer(None, None, verbose, self.logger):
            atext = text.encode('ascii', 'ignore')
            values = {'text': atext}
            data = urllib.urlencode(values)
            try:
                req = urllib2.Request(self.url, data)
                try:
                    response = urllib2.urlopen(req)
                except urllib2.HTTPError, e:
                    print e.__repr__()
                    return []

                the_page = response.read()
                self.xml_result = xml.dom.minidom.parseString(the_page)
                return self.process_result(self.xml_result)
            except TimeoutException:
                debug.print_verbose('Timed out', verbose, self.logger)
                return []

        return

    def process_result(self, xml_result):
        """
        Takes the xml result and constructs a list of dictionary objects
        """
        tags = []
        for option in xml_result.getElementsByTagName('option'):
            tags.append({})
            for label in ['score', 'start', 'length']:
                tags[(-1)][label] = option.getElementsByTagName(label)[0].childNodes[0].data

            concept = option.getElementsByTagName('concept')[0]
            tags[(-1)]['concept'] = {}
            for concept_field in CONCEPT_FIELDS:
                nodes = concept.getElementsByTagName(concept_field)
                if len(nodes) == 1:
                    tags[(-1)]['concept'][concept_field] = nodes[0].childNodes[0].data
                else:
                    tags[(-1)]['concept'][concept_field] = [ node.childNodes[0].data for node in nodes ]

        return tags
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/vocabularysearchparams.py
# Compiled at: 2016-01-05 13:51:01
from lxml import etree
from healthvaultlib.exceptions.healthserviceexception import HealthServiceException

class VocabularySearchParams:
    allowed_modes = [
     'Prefix', 'Contains', 'FullText']

    def __init__(self, search_string):
        self.search_string = search_string
        self.max_results = None
        self.search_mode = None
        return

    def write_xml(self):
        params = etree.Element('text-search-parameters')
        search_string = etree.Element('search-string')
        search_string.text = self.search_string
        if self.search_mode is not None:
            if self.search_mode not in self.allowed_modes:
                raise HealthServiceException('Invalid Xml')
            search_string.attrib['search-mode'] = self.search_mode
        params.append(search_string)
        if self.max_results is not None:
            max_results = etree.Element('max-results')
            max_results.text = str(self.max_results)
            params.append(max_results)
        return params
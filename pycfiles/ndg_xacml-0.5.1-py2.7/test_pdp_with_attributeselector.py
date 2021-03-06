# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/test/context/test_pdp_with_attributeselector.py
# Compiled at: 2012-06-19 10:10:36
"""Tests for AttributeSelector in policies with resource content XML in the
requests
"""
__author__ = 'R B Wilkinson'
__date__ = '06/01/12'
__copyright__ = '(C) 2012 Science and Technology Facilities Council'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: test_pdp_with_attributeselector.py 8078 2012-06-19 14:10:35Z pjkersha $'
from ndg.xacml import Config, importElementTree
ElementTree = importElementTree()
import logging, unittest
from ndg.xacml.core.context.resource import Resource as XacmlResource
from ndg.xacml.core.context import XacmlContextBase
from ndg.xacml.parsers.etree import QName
from ndg.xacml.parsers.etree.factory import ReaderFactory
from ndg.xacml.core.context.pdp import PDP
from ndg.xacml.core.context.result import Decision
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR1_FILEPATH
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR2_FILEPATH
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR3_FILEPATH
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR4_FILEPATH
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR5_FILEPATH
from ndg.xacml.test import XACML_ATTRIBUTESELECTOR6_FILEPATH
from ndg.xacml.test.context import XacmlContextBaseTestCase
from ndg.xacml.utils.etree import prettyPrint
from ndg.xacml.utils.xpath_selector import EtreeXPathSelector
from ndg.xacml.parsers.etree.context import RequestElementTree
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

class AttributeSelectorTestCase(XacmlContextBaseTestCase):
    """Tests use of AttributeSelector in policies with resource content XML in
    the requests.
    """
    NOT_APPLICABLE_RESOURCE_ID = 'https://localhost'
    PUBLIC_RESOURCE_ID = 'http://localhost/resource-only-restricted'
    RESOURCE_CONTENT_VERSION_100 = '<wps:GetCapabilities xmlns:ows="http://www.opengis.net/ows/1.1"\n                     xmlns:wps="http://www.opengis.net/wps/1.0.0"\n                     xmlns:xlink="http://www.w3.org/1999/xlink"\n                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n                     xsi:schemaLocation="http://www.opengis.net/wps/1.0.0/wpsGetCapabilities_request.xsd"\n                     language="en-CA" service="WPS">\n    <wps:AcceptVersions>\n        <ows:Version>1.0.0</ows:Version>\n    </wps:AcceptVersions>\n</wps:GetCapabilities>\n'
    RESOURCE_CONTENT_VERSION_200 = '<wps:GetCapabilities xmlns:ows="http://www.opengis.net/ows/1.1"\n                     xmlns:wps="http://www.opengis.net/wps/1.0.0"\n                     xmlns:xlink="http://www.w3.org/1999/xlink"\n                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n                     xsi:schemaLocation="http://www.opengis.net/wps/1.0.0/wpsGetCapabilities_request.xsd"\n                     language="en-CA" service="WPS">\n    <wps:AcceptVersions>\n        <ows:Version>2.0.0</ows:Version>\n    </wps:AcceptVersions>\n</wps:GetCapabilities>\n'
    RESOURCE_CONTENT_NO_VERSION = '<wps:GetCapabilities xmlns:ows="http://www.opengis.net/ows/1.1"\n                     xmlns:wps="http://www.opengis.net/wps/1.0.0"\n                     xmlns:xlink="http://www.w3.org/1999/xlink"\n                     xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n                     xsi:schemaLocation="http://www.opengis.net/wps/1.0.0/wpsGetCapabilities_request.xsd"\n                     language="en-CA" service="WPS">\n</wps:GetCapabilities>\n'
    RESOURCE_CONTENT_EXECUTE = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<wps:Execute service="WPS" version="1.0.0"\n             xmlns:wps="http://www.opengis.net/wps/1.0.0"\n             xmlns:ows="http://www.opengis.net/ows/1.1"\n             xmlns:xlink="http://www.w3.org/1999/xlink"\n             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n             xsi:schemaLocation="http://www.opengis.net/wps/1.0.0/wpsExecute_request.xsd">\n    <ows:Identifier>Buffer</ows:Identifier>\n    <wps:DataInputs>\n        <wps:Input>\n            <ows:Identifier>InputPolygon</ows:Identifier>\n            <ows:Title>Playground area</ows:Title>\n            <wps:Reference xlink:href="http://foo.bar/some_WFS_request.xml"/>\n        </wps:Input>\n        <wps:Input>\n            <ows:Identifier>BufferDistance</ows:Identifier>\n            <ows:Title>Distance which people will walk to get to a playground.</ows:Title>\n            <wps:Data>\n                <wps:LiteralData>400</wps:LiteralData>\n            </wps:Data>\n        </wps:Input>\n    </wps:DataInputs>\n    <wps:ResponseForm>\n        <wps:RawDataOutput>\n            <ows:Identifier>BufferedPolygon</ows:Identifier>\n        </wps:RawDataOutput>\n    </wps:ResponseForm>\n</wps:Execute>\n'

    @staticmethod
    def _make_element(tag, ns_prefix, ns_uri):
        if Config.use_lxml:
            elem = ElementTree.Element(tag, nsmap={ns_prefix: ns_uri})
        else:
            elem = ElementTree.Element(tag)
            ElementTree._namespace_map[ns_uri] = ns_prefix
        return elem

    def _make_resource_content_element(self, resourceContent):
        resourceContentSubElem = ElementTree.XML(resourceContent)
        tag = str(QName(XacmlContextBase.XACML_2_0_CONTEXT_NS, XacmlResource.RESOURCE_CONTENT_ELEMENT_LOCAL_NAME))
        resourceContentElem = self._make_element(tag, XacmlContextBase.XACML_2_0_CONTEXT_NS_PREFIX, XacmlContextBase.XACML_2_0_CONTEXT_NS)
        resourceContentElem.append(resourceContentSubElem)
        log.debug('\n%s', prettyPrint(resourceContentElem))
        return resourceContentElem

    def test01NotApplicable(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR1_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_VERSION_100)
        request = self._createRequestCtx(self.__class__.NOT_APPLICABLE_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.NOT_APPLICABLE, 'Expecting not applicable decision')

        return

    def test02Permit(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR1_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_VERSION_100)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting permit decision')

        return

    def test03Deny(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR1_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_VERSION_200)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting deny decision')

        return

    def test04Indeterminate(self):
        """This should result in an indeterminate decision because the policy
        includes an AttributeSelector with MustBePresent="true", whereas the
        request context path is not found in the request XML.
        """
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR1_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_NO_VERSION)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.INDETERMINATE, 'Expecting indeterminate decision')

        return

    def test05ExecutePermit(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR2_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting permit decision')

        return

    def test06ExecuteConditionPermit(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR3_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.PERMIT, 'Expecting permit decision')

        return

    def test07ExecuteConditionDeny(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR3_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, subjectId='https://nowhere.ac.uk/noone', resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            self.failIf(result.decision != Decision.DENY, 'Expecting deny decision')

        return

    def test08ExecuteLxmlPermit(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR4_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            if Config.use_lxml:
                self.failIf(result.decision != Decision.PERMIT, 'Expecting permit decision')
            else:
                log.debug('Using ElementTree: dependent on the version, this test may result in an indeterminate decision.  result.decision = %s' % result.decision)

        return

    def test09SelectAttributePermit(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR5_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            if Config.use_lxml:
                self.failIf(result.decision != Decision.PERMIT, 'Expecting permit decision')
            else:
                self.failIf(result.decision != Decision.INDETERMINATE, 'Expecting indeterminate decision')

        return

    def test10SelectAttributeDeny(self):
        self.pdp = PDP.fromPolicySource(XACML_ATTRIBUTESELECTOR6_FILEPATH, ReaderFactory)
        resourceContent = self._make_resource_content_element(self.__class__.RESOURCE_CONTENT_EXECUTE)
        request = self._createRequestCtx(self.__class__.PUBLIC_RESOURCE_ID, resourceContent=resourceContent)
        request.elem = RequestElementTree.toXML(request)
        request.attributeSelector = EtreeXPathSelector(request.elem)
        response = self.pdp.evaluate(request)
        self.failIf(response is None, 'Null response')
        for result in response.results:
            if Config.use_lxml:
                self.failIf(result.decision != Decision.DENY, 'Expecting deny decision')
            else:
                self.failIf(result.decision != Decision.INDETERMINATE, 'Expecting indeterminate decision')

        return


if __name__ == '__main__':
    unittest.main()
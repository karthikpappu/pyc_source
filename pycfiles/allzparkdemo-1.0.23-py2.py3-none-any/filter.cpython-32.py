# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/gateway/http/impl/processor/filter.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Feb 8, 2013\n\n@package: gateway service\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the gateway filter processor.\n'
from ally.container.ioc import injected
from ally.design.processor.assembly import Assembly
from ally.design.processor.attribute import requires, defines
from ally.design.processor.context import Context
from ally.design.processor.execution import Processing, Chain
from ally.design.processor.handler import HandlerBranchingProceed
from ally.design.processor.processor import Using
from ally.gateway.http.spec.gateway import IRepository
from ally.http.spec.codes import FORBIDDEN_ACCESS, BAD_GATEWAY, isSuccess
from ally.http.spec.server import HTTP, RequestHTTP, ResponseContentHTTP, ResponseHTTP, HTTP_GET
from ally.support.util_io import IInputStream
from babel.compat import BytesIO
from urllib.parse import urlparse, parse_qsl
import codecs, json, logging
log = logging.getLogger(__name__)

class Gateway(Context):
    """
    The gateway context.
    """
    filters = requires(list)


class Match(Context):
    """
    The match context.
    """
    gateway = requires(Context)
    groupsURI = requires(tuple)


class Request(Context):
    """
    The request context.
    """
    method = requires(str)
    headers = requires(dict)
    uri = requires(str)
    repository = requires(IRepository)
    match = requires(Context)


class Response(Context):
    """
    Context for response.
    """
    code = defines(str)
    status = defines(int)
    isSuccess = defines(bool)
    text = defines(str)


class RequestFilter(RequestHTTP):
    """
    The request filter context.
    """
    accTypes = defines(list)
    accCharSets = defines(list)


@injected
class GatewayFilterHandler(HandlerBranchingProceed):
    """
    Implementation for a handler that provides the gateway filter.
    """
    scheme = HTTP
    mimeTypeJson = 'json'
    encodingJson = 'utf-8'
    assembly = Assembly

    def __init__(self):
        assert isinstance(self.scheme, str), 'Invalid scheme %s' % self.scheme
        assert isinstance(self.mimeTypeJson, str), 'Invalid json mime type %s' % self.mimeTypeJson
        assert isinstance(self.encodingJson, str), 'Invalid json encoding %s' % self.encodingJson
        assert isinstance(self.assembly, Assembly), 'Invalid assembly %s' % self.assembly
        super().__init__(Using(self.assembly, request=RequestFilter).sources('requestCnt', 'response', 'responseCnt'))

    def process(self, processing, request: Request, response: Response, Gateway: Gateway, Match: Match, **keyargs):
        """
        @see: HandlerBranchingProceed.process
        """
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        assert isinstance(request, Request), 'Invalid request %s' % request
        assert isinstance(response, Response), 'Invalid response %s' % response
        if not request.match:
            return
        else:
            assert isinstance(request.repository, IRepository), 'Invalid request repository %s' % request.repository
            match = request.match
            assert isinstance(match, Match), 'Invalid response match %s' % match
            assert isinstance(match.gateway, Gateway), 'Invalid gateway %s' % match.gateway
            if match.gateway.filters:
                for filterURI in match.gateway.filters:
                    assert isinstance(filterURI, str), 'Invalid filter %s' % filterURI
                    try:
                        filterURI = filterURI.format(None, *match.groupsURI)
                    except IndexError:
                        response.code, response.status, response.isSuccess = BAD_GATEWAY
                        response.text = "Invalid filter URI '%s' for groups %s" % (filterURI, match.groupsURI)
                        return

                    isAllowed, status, text = self.obtainFilter(processing, filterURI)
                    if isAllowed is None:
                        log.info("Cannot fetch the filter from URI '%s', with response %s %s", request.uri, status, text)
                        response.code, response.status, response.isSuccess = BAD_GATEWAY
                        response.text = text
                        return
                    if not isAllowed:
                        response.code, response.status, response.isSuccess = FORBIDDEN_ACCESS
                        request.match = request.repository.find(request.method, request.headers, request.uri, FORBIDDEN_ACCESS.status)
                        return

            return

    def obtainFilter(self, processing, uri):
        """
        Checks the filter URI.

        @param processing: Processing
            The processing used for delivering the request.
        @param uri: string
            The URI to call, parameters are allowed.
        @return: tuple(boolean|None, integer, string)
            A tuple containing as the first True if the filter URI provided a True value, None if the filter cannot be fetched,
            on the second position the response status and on the last position the response text.
        """
        assert isinstance(processing, Processing), 'Invalid processing %s' % processing
        assert isinstance(uri, str), 'Invalid URI %s' % uri
        request = processing.ctx.request()
        assert isinstance(request, RequestFilter), 'Invalid request %s' % request
        url = urlparse(uri)
        request.scheme, request.method = self.scheme, HTTP_GET
        request.headers = {}
        request.uri = url.path.lstrip('/')
        request.parameters = parse_qsl(url.query, True, False)
        request.accTypes = [self.mimeTypeJson]
        request.accCharSets = [self.encodingJson]
        chain = Chain(processing)
        chain.process(request=request, requestCnt=processing.ctx.requestCnt(), response=processing.ctx.response(), responseCnt=processing.ctx.responseCnt()).doAll()
        response, responseCnt = chain.arg.response, chain.arg.responseCnt
        assert isinstance(response, ResponseHTTP), 'Invalid response %s' % response
        assert isinstance(responseCnt, ResponseContentHTTP), 'Invalid response content %s' % responseCnt
        if ResponseHTTP.text in response and response.text:
            text = response.text
        else:
            if ResponseHTTP.code in response and response.code:
                text = response.code
            else:
                text = None
        if ResponseContentHTTP.source not in responseCnt or responseCnt.source is None or not isSuccess(response.status):
            return (None, response.status, text)
        else:
            if isinstance(responseCnt.source, IInputStream):
                source = responseCnt.source
            else:
                source = BytesIO()
                for bytes in responseCnt.source:
                    source.write(bytes)

                source.seek(0)
            allowed = json.load(codecs.getreader(self.encodingJson)(source))
            return (
             allowed['HasAccess'] == 'True', response.status, text)
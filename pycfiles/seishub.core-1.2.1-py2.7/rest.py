# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\processor\resources\rest.py
# Compiled at: 2011-02-11 15:06:34
"""
REST based resources.
"""
from lxml import etree
from obspy.core import UTCDateTime
from seishub.core.exceptions import ForbiddenError, NotFoundError, SeisHubError, NotAllowedError, UnauthorizedError
from seishub.core.processor.interfaces import IRESTResource, IRESTProperty, IXMLIndex
from seishub.core.processor.processor import MAXIMAL_URL_LENGTH, PUT, GET, HEAD, POST
from seishub.core.processor.resources.resource import Resource, Folder, StaticFolder
from seishub.core.util.path import splitPath
from seishub.core.util.text import isInteger
from seishub.core.util.xml import addXMLDeclaration
from twisted.web import http
from zope.interface import implements

class RESTResource(Resource):
    """
    A REST resource node.
    """
    implements(IRESTResource)

    def __init__(self, res, **kwargs):
        Resource.__init__(self, **kwargs)
        self.category = 'resource'
        self.is_leaf = True
        self.folderish = False
        if isinstance(res, dict):
            self.package_id = res['package_id']
            self.resourcetype_id = res['resourcetype_id']
            self.name = res['resource_name']
            self.revision = res['revision']
            self.res = None
            self.meta = res
        else:
            self.package_id = res.package.package_id
            self.resourcetype_id = res.resourcetype.resourcetype_id
            self.name = res.name
            self.revision = res.document.revision
            self.res = res
            meta = self.res.document.meta
            self.meta = {'meta_size': meta.size, 
               'meta_uid': meta.uid, 
               'meta_datetime': meta.datetime}
        self.url = '/xml/%s/%s/%s' % (self.package_id, self.resourcetype_id,
         self.name)
        return

    def getMetadata(self):
        temp = int(UTCDateTime(self.meta['meta_datetime']).timestamp)
        return {'permissions': 33188, 
           'uid': self.meta['meta_uid'], 
           'size': self.meta['meta_size'], 
           'atime': temp, 
           'mtime': temp}

    def _format(self, request, data):
        """
        Handles output/format conversion of content.
        """
        formats = request.args.get('format', []) or request.args.get('output', [])
        for format in formats:
            reg = request.env.registry
            xslt = reg.stylesheets.get(package_id=self.package_id, resourcetype_id=self.resourcetype_id, type=format)
            if len(xslt):
                xslt = xslt[0]
                data = xslt.transform(data, request.env.xslt_params)
                if xslt.content_type:
                    request.setHeader('content-type', xslt.content_type + '; charset=UTF-8')
                continue
            cls = reg.formaters.get(package_id=self.package_id, resourcetype_id=self.resourcetype_id, format=format)
            if cls:
                return cls.format(request, data, self.name)
            msg = 'There is no output format "%s" for request %s.'
            request.env.log.debug(msg % (format, request.path))

        return data

    def _checkPermissions(self, request, permissions=755):
        uid = request.getUser()
        doc_uid = self.meta['meta_uid']
        if not doc_uid:
            return
        if uid == doc_uid:
            return
        user = request.env.auth.getUser(uid)
        if user.permissions < permissions:
            raise UnauthorizedError()

    def render_GET(self, request):
        """
        Process a resource query request.
        
        A query at the root of a resource type folder returns a list of all
        available XML resource objects of this resource type. Direct request on
        a XML resource results in the content of a XML document. Before 
        returning a XML document, we add a valid XML declaration header and 
        encode it as UTF-8 string.
        
        @see: 
        U{http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.1}
        for all possible error codes.
        """
        if request.env.auth.getUser('anonymous').permissions != 755:
            self._checkPermissions(request, 755)
        data = self.res.document.data
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        if not data.startswith('<xml'):
            data = addXMLDeclaration(data, 'utf-8')
        data = self._format(request, data)
        dt = UTCDateTime(self.res.document.meta.getDatetime())
        try:
            request.setLastModified(dt.timestamp)
        except:
            pass

        return data

    def render_PUT(self, request):
        """
        Processes a resource modification request.

        "The PUT method requests that the enclosed entity be stored under the 
        supplied Request-URI. If the Request-URI does not point to an existing 
        resource, and that URI is capable of being defined as a new resource by
        the requesting user agent, the server can create the resource with that
        URI. If a new resource is created, the origin server MUST inform the 
        user agent via the 201 (Created) response. 
        
        If the resource could not be created or modified with the Request-URI, 
        an appropriate error response SHOULD be given that reflects the nature 
        of the problem." 
        
        @see: U{http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.6}
        @see: U{http://thoughtpad.net/alan-dean/http-headers-status.gif}
        
        Modifying a document always needs a valid path to a resource or uses a
        user defined mapping.
        """
        self._checkPermissions(request, 777)
        if self.package_id == 'seishub':
            msg = 'SeisHub resources may not be modified directly.'
            raise ForbiddenError(msg)
        data = request.data
        data = self._format(request, data)
        uid = request.getUser()
        request.env.catalog.modifyResource(self.res, data, uid=uid)
        request.code = http.NO_CONTENT
        return ''

    def render_MOVE(self, request):
        """
        Processes a resource move/rename request.
        
        @see: 
        U{http://msdn.microsoft.com/en-us/library/aa142926(EXCHG.65).aspx}
        """
        self._checkPermissions(request, 777)
        if self.package_id == 'seishub':
            msg = 'SeisHub resources may not be moved directly.'
            raise ForbiddenError(msg)
        destination = request.received_headers.get('Destination', False)
        if not destination:
            msg = 'Expected a destination header.'
            raise SeisHubError(msg, code=http.BAD_REQUEST)
        if not destination.startswith(request.env.getRestUrl()):
            if destination.startswith('http'):
                msg = 'Destination URI is located on a different server.'
                raise SeisHubError(msg, code=http.BAD_GATEWAY)
            msg = 'Expected a complete destination path.'
            raise SeisHubError(msg, code=http.BAD_REQUEST)
        if len(destination) >= MAXIMAL_URL_LENGTH:
            msg = 'Destination URI is to long.'
            raise SeisHubError(msg, code=http.REQUEST_URI_TOO_LONG)
        destination = destination[len(request.env.getRestUrl()):]
        parts = splitPath(destination)
        if parts == request.prepath:
            msg = 'Source URI and destination URI must not be the same value.'
            raise ForbiddenError(msg)
        if len(parts) < 1 or parts[:-1] != request.prepath[:-1]:
            msg = 'Destination %s not allowed.' % destination
            raise ForbiddenError(msg)
        request.env.catalog.renameResource(self.res, parts[(-1)])
        request.code = http.CREATED
        url = request.env.getRestUrl() + destination
        request.headers['Location'] = str(url)
        return ''

    def render_DELETE(self, request):
        """
        Processes a resource deletion request.
        
        @see: U{http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.7}
        
        "The DELETE method requests that the server deletes the resource 
        identified by the given request URI. 
        
        A successful response SHOULD be 200 (OK) if the response includes an 
        entity describing the status, 202 (Accepted) if the action has not yet 
        been enacted, or 204 (No Content) if the action has been enacted but 
        the response does not include an entity."
        
        Deleting a document always needs a valid path to a resource or may use 
        a user defined mapping.
        """
        self._checkPermissions(request, 777)
        if self.package_id == 'seishub':
            msg = 'SeisHub resources may not be deleted directly.'
            raise ForbiddenError(msg)
        request.env.catalog.deleteResource(self.res)
        request.code = http.NO_CONTENT
        return ''


class XMLIndex(Resource):
    """
    A XML index node.
    """
    implements(IXMLIndex)

    def __init__(self, **kwargs):
        Resource.__init__(self, **kwargs)
        self.category = 'index'
        self.is_leaf = True
        self.folderish = False


class RESTProperty(Resource):
    """
    A REST property node.
    """
    implements(IRESTProperty)

    def __init__(self, package_id, resourcetype_id, name, revision=None, **kwargs):
        Resource.__init__(self, **kwargs)
        self.is_leaf = True
        self.folderish = False
        self.package_id = package_id
        self.resourcetype_id = resourcetype_id
        self.name = name
        self.revision = revision

    def render_GET(self, request):
        property = request.postpath[(-1)]
        if property == '.index':
            res = request.env.catalog.getResource(self.package_id, self.resourcetype_id, self.name, self.revision)
            index_dict = request.env.catalog.getIndexData(res)
            root = etree.Element('seishub')
            for label, values_dict in index_dict.iteritems():
                sub = etree.SubElement(root, label)
                for _pos, values in values_dict.iteritems():
                    for value in values:
                        if not value:
                            continue
                        if not isinstance(value, basestring):
                            value = unicode(value)
                        etree.SubElement(sub, 'value').text = value

            data = etree.tostring(root, pretty_print=True, encoding='utf-8')
            format_prefix = 'index'
        elif property == '.meta':
            res = request.env.catalog.getResource(self.package_id, self.resourcetype_id, self.name, self.revision)
            meta = res.document.meta
            root = etree.Element('seishub')
            etree.SubElement(root, 'package').text = self.package_id
            etree.SubElement(root, 'resourcetype').text = self.resourcetype_id
            etree.SubElement(root, 'name').text = self.name
            etree.SubElement(root, 'document_id').text = str(res.document._id)
            etree.SubElement(root, 'resource_id').text = str(res._id)
            etree.SubElement(root, 'revision').text = str(res.document.revision)
            etree.SubElement(root, 'uid').text = unicode(meta.uid)
            etree.SubElement(root, 'datetime').text = unicode(meta.datetime.isoformat())
            etree.SubElement(root, 'size').text = unicode(meta.size)
            etree.SubElement(root, 'hash').text = unicode(meta.hash)
            data = etree.tostring(root, pretty_print=True, encoding='utf-8')
            format_prefix = 'meta'
        else:
            raise NotFoundError('Property %s is not defined.' % property)
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        if not data.startswith('<xml'):
            data = addXMLDeclaration(data, 'utf-8')
        format = request.args.get('format', [None])[0] or request.args.get('output', [None])[0]
        if format:
            format = '%s.%s' % (format_prefix, format)
            reg = request.env.registry
            xslt = reg.stylesheets.get(package_id='seishub', resourcetype_id='stylesheet', type=format)
            if len(xslt):
                xslt = xslt[0]
                data = xslt.transform(data)
                if xslt.content_type:
                    request.setHeader('content-type', xslt.content_type + '; charset=UTF-8')
            else:
                msg = 'There is no stylesheet for requested format %s.'
                request.env.log.debug(msg % format)
        return data


class RESTResourceTypeFolder(Folder):
    """
    A REST resource type folder.
    """

    def __init__(self, package_id, resourcetype_id, **kwargs):
        Folder.__init__(self, **kwargs)
        self.category = 'resourcetype'
        self.is_leaf = True
        self.package_id = package_id
        self.resourcetype_id = resourcetype_id

    def render(self, request):
        rlen = len(request.postpath)
        if request.method in [GET, HEAD] and rlen == 0:
            return self.render_GET(request)
        if request.method == POST and rlen in (0, 1):
            return self.render_POST(request)
        if len(request.postpath) == 1:
            return self._processResource(request)
        if request.method == GET and rlen >= 2:
            if isInteger(request.postpath[1]):
                if rlen == 2:
                    return self._processRevision(request)
                if rlen == 3 and request.postpath[2].startswith('.'):
                    name = request.postpath.pop(0)
                    request.prepath.append(name)
                    revision = request.postpath.pop(0)
                    request.prepath.append(revision)
                    return RESTProperty(self.package_id, self.resourcetype_id, name, revision)
            elif request.postpath[1].startswith('.'):
                name = request.postpath.pop(0)
                request.prepath.append(name)
                return RESTProperty(self.package_id, self.resourcetype_id, name)
        allowed_methods = getattr(self, 'allowedMethods', ())
        msg = 'This operation is not allowed on this resource.'
        raise NotAllowedError(allowed_methods=allowed_methods, message=msg)

    def _processResource(self, request):
        try:
            res = request.env.catalog.getResource(self.package_id, self.resourcetype_id, request.postpath[0], revision=None)
        except NotFoundError:
            if request.method == PUT:
                return self.render_POST(request)
            raise
        except:
            raise

        name = request.postpath.pop(0)
        request.prepath.append(name)
        result = RESTResource(res)
        if request.method == GET:
            return result
        else:
            return result.render(request)
            return

    def _processRevision(self, request):
        name = request.postpath.pop(0)
        request.prepath.append(name)
        revision = request.postpath.pop(0)
        request.prepath.append(revision)
        res = request.env.catalog.getResource(self.package_id, self.resourcetype_id, name, revision=revision)
        return RESTResource(res)

    def render_POST(self, request):
        """
        Create a new XML resource for this resource type.
        
        "The POST method is used to request that the origin server accept the 
        entity enclosed in the request as a new subordinate of the resource 
        identified by the Request-URI in the Request-Line.
        
        The action performed by the POST method might not result in a resource
        that can be identified by a URI. In this case, either 200 (OK) or 204 
        (No Content) is the appropriate response status, depending on whether 
        or not the response includes an entity that describes the result. If a
        resource has been created on the origin server, the response SHOULD be
        201 (Created) and contain an entity which describes the status of the 
        request and refers to the new resource, and a Location header." 
        
        @see: U{http://www.w3.org/Protocols/rfc2616/rfc2616-sec9.html#sec9.5}
        """
        if self.package_id == 'seishub':
            msg = 'SeisHub resources may not be added directly.'
            raise ForbiddenError(msg)
        if len(request.postpath) == 1:
            name = request.postpath[0]
        else:
            name = None
        uid = request.getUser()
        data = request.data
        formats = request.args.get('format', []) or request.args.get('output', [])
        for format in formats:
            reg = request.env.registry
            xslt = reg.stylesheets.get(package_id=self.package_id, resourcetype_id=self.resourcetype_id, type=format)
            if len(xslt):
                xslt = xslt[0]
                data = xslt.transform(data)
                if xslt.content_type:
                    request.setHeader('content-type', xslt.content_type + '; charset=UTF-8')
            else:
                msg = 'There is no stylesheet for requested format %s.'
                request.env.log.debug(msg % format)

        res = request.env.catalog.addResource(self.package_id, self.resourcetype_id, data, uid=uid, name=name)
        request.code = http.CREATED
        url = '%s/%s/%s' % (request.env.getRestUrl(),
         ('/').join(request.prepath),
         str(res.name))
        request.headers['Location'] = str(url)
        return ''

    def render_GET(self, request):
        """
        Returns all resources and indexes of this resource type.
        """
        temp = {}
        xpath = '/%s/%s' % (self.package_id, self.resourcetype_id)
        res_dict = request.env.catalog.query(xpath)
        for id in res_dict['ordered']:
            temp[res_dict[id]['resource_name']] = RESTResource(res_dict[id])

        xmlindex_list = request.env.catalog.getIndexes(package_id=self.package_id, resourcetype_id=self.resourcetype_id)
        for id in xmlindex_list:
            temp[str(id)] = XMLIndex()

        return temp


class RESTPackageFolder(StaticFolder):
    """
    A REST package folder.
    """

    def __init__(self, package_id, **kwargs):
        Folder.__init__(self, **kwargs)
        self.category = 'package'
        self.package_id = package_id

    def getChild(self, id, request):
        """
        Returns a L{RESTResourceTypeFolder} object for a valid id.
        """
        if request.env.registry.isResourceTypeId(self.package_id, id):
            return RESTResourceTypeFolder(self.package_id, id)
        raise NotFoundError('XML resource type %s not found.' % id)

    def render_GET(self, request):
        """
        Returns a dictionary of all resource types of this package.
        """
        temp = {}
        for id in request.env.registry.getResourceTypeIds(self.package_id):
            temp[id] = RESTResourceTypeFolder(self.package_id, id)

        return temp


class RESTFolder(StaticFolder):
    """
    A REST root folder.
    """

    def __init__(self, **kwargs):
        Folder.__init__(self, **kwargs)
        self.category = 'xmlroot'

    def getChild(self, id, request):
        """
        Returns a L{XMLPackageFolder} object for a valid id.
        """
        if request.env.registry.isPackageId(id):
            return RESTPackageFolder(id)
        raise NotFoundError('XML package %s not found.' % id)

    def render_GET(self, request):
        """
        Returns a dictionary of all SeisHub packages.
        """
        temp = {}
        for id in request.env.registry.getPackageIds():
            temp[id] = RESTPackageFolder(id)

        return temp
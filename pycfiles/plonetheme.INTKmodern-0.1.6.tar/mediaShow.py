# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/AG/Projects/intk/Plone/intk/src/plonetheme.INTKmodern/plonetheme/intkModern/browser/mediaShow.py
# Compiled at: 2014-09-15 09:08:49
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
import json
from AccessControl import getSecurityManager
try:
    from collective.flowplayer.interfaces import IFlowPlayable
    FLOWPLAYER_EXISTS = True
except ImportError:
    FLOWPLAYER_EXISTS = False

class GetMediaShowItemView(BrowserView):
    """ Class that extracts relevant information for the slideshow
    """

    def getJSON(self):
        if hasattr(self.request, 'presentation'):
            presentation = self.request['presentation']
        else:
            presentation = 'false'
        presentationMode = False
        if presentation.find('true') != -1:
            presentationMode = True
        callback = hasattr(self.request, 'callback') and 'json' + self.request['callback'] or None
        media = self.getMediaURL()
        mediaType = self.getMediaType()
        if hasattr(self.context, 'title'):
            title = self.context.title
        elif hasattr(self.context, 'Title'):
            title = self.context.Title()
        else:
            title = ''
        if presentationMode and hasattr(self.context, 'aq_explicit') and hasattr(self.context.aq_explicit, 'getText'):
            description = self.context.getText()
        elif hasattr(self.context, 'Description'):
            description = self.context.Description()
        else:
            description = ''
        if description is None or description == '':
            if hasattr(self.context.__parent__, 'Description'):
                description = self.context.__parent__.Description()
            else:
                description = ''
        type = self.context.portal_type
        jsonStr = json.dumps({'title': title, 'description': description, 'type': type, 'media': {'url': media, 'type': mediaType}})
        if callback is not None:
            return callback + '(' + jsonStr + ')'
        else:
            return jsonStr
            return

    def sanitizeStringForJson(self, str):
        str = str.replace('\n', ' ').replace('"', '\\"').replace("'", "\\'")
        return str

    def getMediaURL(self):
        """ finds and returns relevant leading media for the context item
        """
        item = self.context
        if self.isVideo(item):
            return item.absolute_url()
        if item.portal_type == 'Image':
            return item.absolute_url() + '/image_crop'
        if item.portal_type == 'Link' and (item.remoteUrl.find('youtube.com') > -1 or item.remoteUrl.find('vimeo.com') > -1):
            return item.remoteUrl
        catalog = getToolByName(self.context, 'portal_catalog')
        plone_utils = getToolByName(self.context, 'plone_utils')
        path = ('/').join(item.getPhysicalPath())
        if plone_utils.isStructuralFolder(item):
            results = catalog.searchResults(path={'query': path, 'depth': 1}, type=['Image', 'File'], sort_on='getObjPositionInParent')
            if len(results) > 0:
                leadMedia = results[0]
                if leadMedia.portal_type == 'Image':
                    return leadMedia.getURL() + '/image_crop'
                return leadMedia.getURL()
            else:
                return ''
        else:
            return ''

    def getMediaType(self):
        """ Finds and returns the type of lead media
        """
        item = self.context
        try:
            if self.isVideo(item):
                return 'Video'
            else:
                if item.portal_type == 'Link' and item.remoteUrl.find('youtube.com') > -1:
                    return 'Youtube'
                if item.portal_type == 'Link' and item.remoteUrl.find('vimeo.com') > -1:
                    return 'Vimeo'
                return 'Image'

        except:
            if self.isVideo(item):
                return 'Video'
            else:
                if item.portal_type == 'Link' and item.getObject().remoteUrl.find('youtube.com') > -1:
                    return 'Youtube'
                if item.portal_type == 'Link' and item.getObject().remoteUrl.find('vimeo.com') > -1:
                    return 'Vimeo'
                return 'Image'

    def isVideo(self, item):
        if FLOWPLAYER_EXISTS:
            result = IFlowPlayable.providedBy(item)
        else:
            result = False
        return result
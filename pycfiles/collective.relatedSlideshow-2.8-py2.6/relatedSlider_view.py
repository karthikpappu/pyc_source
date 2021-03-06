# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/relatedSlideshow/browser/relatedSlider_view.py
# Compiled at: 2011-03-08 06:11:52
from Products.Five import BrowserView
from zope.interface import implements
from zope.viewlet.interfaces import IViewlet
from Products.CMFCore.utils import getToolByName
from Acquisition import aq_base, aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets import ViewletBase
from zope.component import getMultiAdapter
import time, string
from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.config import IMAGE_CAPTION_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from collective.flowplayer.interfaces import IFlowPlayable
from collective.flowplayer.interfaces import IAudio

class RelatedSliderView(BrowserView):
    """view for the Slider
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getManualSlideshowFolder(self):
        """Searches for a folder named slideshow in the related items and returns it, or else, returns None
        """
        return

    def getCollectionSlideshow(self):
        """Gathers all items on the collection for the slideshow
        """
        catalog = getToolByName(self, 'portal_catalog')
        catalogResults = []
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        query = self.context.buildQuery()
        if query != None:
            catalogResults = catalog.searchResults(query)
        else:
            catalogResults = []
        result = []
        result.append(self.context)
        for item in catalogResults:
            if portal_state.language() == item.Language:
                result.append(item.getObject())

        resultNoRepeated = self.uniq(result)
        resultNoRepeated.reverse()
        return resultNoRepeated

    def getManualSlideshow(self, manualContext):
        """generates the slideshow items by recursing into a folder named slideshow
        """
        return []

    def getMedia(self, item):
        """Get the media folder inside the item and return all it's contents
        """
        if hasattr(item, 'media'):
            return self.getRecursiveFolderishContents(item.media)
        else:
            return []

    def getWorkRelatedPeople(self, work):
        result = []
        if work.portal_type == 'Work':
            related = work.getRefs()
            backRelated = work.getBRefs()
            related.extend(backRelated)
            for item in related:
                if item.portal_type == 'Person' or item.portal_type == 'Organization':
                    result.append(item)

        resultNoRepeated = self.uniq(result)
        return resultNoRepeated

    def getSlideshow(self):
        """Generate the slideshow items properly selected and ordered, this is the function to ultimately call on the template
        """
        manualContext = self.getManualSlideshowFolder()
        if manualContext is None and self.context.portal_type != 'Topic':
            result = []
            last = []
            items = []
            media = []
            relatedPeople = []
            result.append(self.context)
            media = self.getMedia(self.context)
            for medium in media:
                result.append(medium.getObject())

            types = self.getOrderedTypes()
            for currentType in types:
                items = self.getRelatedItemsByType(currentType)
                if currentType == 'Person':
                    for person in relatedPeople:
                        result.append(person)

                    relatedPeople = []
                if self.getTypeName(currentType) != 'Folderish':
                    for item in items:
                        if currentType == 'File':
                            if self.isVideo(item):
                                result.append(item)
                            else:
                                last.append(item)
                        elif item.restrictedTraverse('@@plone').isStructuralFolder():
                            result.append(item)
                            media = self.getMedia(item)
                            for medium in media:
                                result.append(medium.getObject())

                            if currentType == 'Work':
                                relatedPeople.extend(self.getWorkRelatedPeople(item))
                        else:
                            result.append(item)

                else:
                    for item in items:
                        folderishItems = self.getFolderishContents(item)
                        for fItem in folderishItems:
                            result.append(fItem.getObject())

            resultNoRepeated = self.uniq(result)
            resultNoRepeated.reverse()
            return resultNoRepeated
        else:
            if manualContext is not None:
                return self.getManualSlideshow(manualContext)
            else:
                if self.context.portal_type == 'Topic':
                    return self.getCollectionSlideshow()
                return []
            return

    def getDocumentationStart(self):
        rf = self.getRelatedItemsByType('Folder')
        if len(rf) > 0:
            relatedfolder = rf[0]
            contents = self.getFolderishContents(relatedfolder)
            for item in contents:
                if hasattr(item, 'getObject'):
                    itemobj = item.getObject()
                else:
                    itemobj = item
                if itemobj.portal_type == 'Image' or self.isVideo(itemobj) or self.hasContentLeadImage(itemobj):
                    return item.UID

        return

    def currenttime(self):
        return time.time()

    def filterResults(self, results):
        """Takes away Items of diferent languages than the current
        """
        filtered = []
        portal_state = getMultiAdapter((self.context, self.request), name='plone_portal_state')
        for item in results:
            if portal_state.language() == item.Language:
                filtered.append(item)

        return filtered

    def trimDescription(self, desc, num):
        if len(desc) > num:
            res = desc[0:num]
            lastspace = res.rfind(' ')
            res = res[0:lastspace] + ' ...'
            return res
        else:
            return desc

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        try:
            return util.ulocalized_time(time, long_format, time_only, self.context, domain='plonelocales')
        except TypeError:
            return util.ulocalized_time(time, long_format, self.context, domain='plonelocales')

    def getFolderishContents(self, folder):
        catalog = getToolByName(self, 'portal_catalog')
        physicalPath = folder.getPhysicalPath()
        folderURL = ('/').join(physicalPath)
        if folder.portal_type == 'Folder':
            results = catalog.searchResults(path={'query': folderURL, 'depth': 1}, sort_on='getObjPositionInParent')
        elif folder.portal_type == 'Topic':
            if hasattr(folder, 'getObject'):
                query = folder.getObject().buildQuery()
            else:
                query = folder.buildQuery()
            if query != None:
                results = catalog.searchResults(query)
            else:
                results = []
        else:
            results = []
        return results

    def getRecursiveFolderishContents(self, folder):
        catalog = getToolByName(self, 'portal_catalog')
        physicalPath = folder.getPhysicalPath()
        folderURL = ('/').join(physicalPath)
        if folder.portal_type == 'Folder':
            results = catalog.searchResults(path={'query': folderURL}, sort_on='getObjPositionInParent')
        elif folder.portal_type == 'Topic':
            query = folder.getObject().buildQuery()
            if query != None:
                results = catalog.searchResults(query)
            else:
                results = []
        else:
            results = []
        return results

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def tag(self, obj, css_class='tileImage'):
        context = aq_inner(obj)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None:
            if field.get_size(context) != 0:
                scale = self.prefs.desc_scale_name
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def isVideo(self, item):
        result = IFlowPlayable.providedBy(item)
        return result

    def clearsReferences(self):
        return True

    def audio_only(self, item):
        result = IAudio.providedBy(item)
        return result

    def getValidTypes(self):
        properties_tool = getToolByName(self.context, 'portal_properties', None)
        if properties_tool is not None:
            references_properties = getattr(properties_tool, 'references_properties', None)
            if references_properties:
                if references_properties.hasProperty('apply_to'):
                    types = references_properties.apply_to
                    return types
        return []

    def isValidType(self, type):
        types = self.getValidTypes()
        if type in types:
            return True
        else:
            return False

    def isPublishable(self, item):
        if item.getPortalTypeName() == 'File' or item.getPortalTypeName() == 'Image':
            return False
        else:
            return True

    def getOneWayRelatedItems(self):
        result = []
        try:
            related = self.context.getRefs()
            workflow = getToolByName(self, 'portal_workflow')
            member = getToolByName(self, 'portal_membership')
            for item in related:
                if not self.isPublishable(item) or workflow.getInfoFor(item, 'review_state') == 'published' or not member.isAnonymousUser():
                    if item.id != self.context.id:
                        result.append(item)

            return self.uniq(result)
        except:
            return result

    def getTwoWayRelatedItems(self):
        result = []
        try:
            related = self.context.getRefs()
            backRelated = self.context.getBRefs()
            workflow = getToolByName(self, 'portal_workflow')
            member = getToolByName(self, 'portal_membership')
            for item in related:
                if not self.isPublishable(item) or workflow.getInfoFor(item, 'review_state') == 'published' or not member.isAnonymousUser():
                    if item.id != self.context.id:
                        result.append(item)

            for backItem in backRelated:
                if not self.isPublishable(backItem) or workflow.getInfoFor(backItem, 'review_state') == 'published' or not member.isAnonymousUser():
                    if backItem.id != self.context.id:
                        result.append(backItem)

            return self.uniq(result)
        except:
            return result

    def getRelatedItemsByType(self, type):
        related = self.context.getRefs()
        backRelated = self.context.getBRefs()
        result = []
        workflow = getToolByName(self, 'portal_workflow')
        member = getToolByName(self, 'portal_membership')
        for backItem in backRelated:
            if self.getTypeName(backItem.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(backItem) or workflow.getInfoFor(backItem, 'review_state') == 'published' or not member.isAnonymousUser()):
                if backItem.id != self.context.id:
                    result.append(backItem)

        for item in related:
            if self.getTypeName(item.getPortalTypeName()) == self.getTypeName(type) and (not self.isPublishable(item) or workflow.getInfoFor(item, 'review_state') == 'published' or not member.isAnonymousUser()):
                if item.id != self.context.id:
                    result.append(item)

        return self.uniq(result)

    def uniq(self, alist):
        set = {}
        return [ set.setdefault(e, e) for e in alist if e not in set ]

    def creator(self):
        return self.context.Creator()

    def author(self):
        return 0

    def authorname(self):
        author = self.author()
        return author and author['fullname'] or self.creator()

    def translateMonth(self, month):
        if self.request['LANGUAGE'][:2] == 'en':
            return month
        if self.request['LANGUAGE'][:2] == 'es':
            if month == 'Jan':
                return 'Ene'
            else:
                if month == 'Apr':
                    return 'Abr'
                if month == 'Aug':
                    return 'Ago'
                if month == 'Dec':
                    return 'Dic'
                return month
        else:
            return month

    def getTypeName(self, type):
        if self.request['LANGUAGE'][:2] == 'es':
            if type == 'Person':
                name = 'Personas'
            elif type == 'Event':
                name = 'Eventos'
            elif type == 'Organization':
                name = 'Personas'
            elif type == 'Work':
                name = 'Obras'
            elif type == 'All':
                name = 'Todo'
            elif type == 'Media':
                name = 'Media'
            elif type == 'News Item':
                name = 'Noticias'
            elif type == 'Folder':
                name = 'Folderish'
            elif type == 'Topic':
                name = 'Folderish'
            else:
                name = type + 's'
        elif type == 'Person':
            name = 'People'
        elif type == 'Event':
            name = 'Events'
        elif type == 'Organization':
            name = 'People'
        elif type == 'Work':
            name = 'Works'
        elif type == 'All':
            name = 'All'
        elif type == 'Media':
            name = 'Media'
        elif type == 'News Item':
            name = 'News'
        elif type == 'Folder':
            name = 'Folderish'
        elif type == 'Topic':
            name = 'Folderish'
        else:
            name = type + 's'
        return name

    def getFolderImages(self, folderItem):
        catalog = getToolByName(self, 'portal_catalog')
        physicalPath = folderItem.getPhysicalPath()
        folderURL = ('/').join(physicalPath)
        catResults = catalog.searchResults(path={'query': folderURL, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                                 'File'))
        results = []
        for item in catResults:
            if item.portal_type == 'Image' or item.portal_type == 'File' and IFlowPlayable.providedBy(item.getObject()):
                results.append(item)

        return results

    def purgeTypes(self, types):
        names = []
        purged = []
        for item in types:
            if self.getTypeName(item) not in names:
                names.append(self.getTypeName(item))
                purged.append(item)

        return purged

    def howManyOfType(self, itemArray, type):
        counter = 0
        for item in itemArray:
            if item.id != self.context.id:
                if self.getTypeName(item.portal_type) == self.getTypeName(type) and self.hasContentLeadImage(item):
                    counter = counter + 1

        return counter

    def getOrderedTypes(self):
        result = [
         'File', 'Work', 'Person', 'Organization', 'Folder', 'Topic', 'Event']
        putils = getToolByName(self, 'plone_utils')
        types = putils.getUserFriendlyTypes()
        for item in types:
            if item not in result:
                result.append(item)

        purgedResult = self.purgeTypes(result)
        return purgedResult

    def normalizeString(self, str):
        return self.context.plone_utils.normalizeString(str)

    def hasContentLeadImage(self, obj):
        field = obj.getField(IMAGE_FIELD_NAME)
        if field is not None:
            value = field.get(obj)
            return not not value
        else:
            return

    def hasContentLeadImageCaption(self, obj):
        field = obj.getField(IMAGE_CAPTION_FIELD_NAME)
        if field is not None:
            value = field.get(obj)
            return not not value
        else:
            return

    def getContentLeadImageCaption(self, obj):
        field = obj.getField(IMAGE_CAPTION_FIELD_NAME)
        if field is not None:
            value = field.get(obj)
            return value
        else:
            return
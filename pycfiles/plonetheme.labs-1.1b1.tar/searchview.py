# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/browser/searchview.py
# Compiled at: 2011-05-20 07:51:00
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone import utils
from collective.flowplayer.interfaces import IFlowPlayable
from Products.Archetypes.utils import shasattr

class SearchView(BrowserView):

    def isVideo(self, item):
        result = IFlowPlayable.providedBy(item)
        return result

    def audioOnly(self, item):
        result = IAudio.providedBy(item)
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

    def getSearchableTypes(self):
        ploneTypes = getToolByName(self, 'plone_utils').getUserFriendlyTypes()
        v2Types = ['All', 'Media']
        result = []
        for type in ploneTypes:
            result.append(type)

        for type in v2Types:
            result.append(type)

        if 'Image' in result:
            result.remove('Image')
        if 'File' in result:
            result.remove('File')
        clean = self.removeBlackListed(result)
        order = self.orderTypesList(clean)
        return order

    def removeBlackListed(self, list):
        blackList = [
         'Link', 'Document', 'Favorite', 'Folder', 'FormFolder', 'Large Plone Folder', 'Topic']
        for item in blackList:
            if item in list:
                list.remove(item)

        return list

    def orderTypesList(self, list):
        order = [
         'All', 'News Item', 'Event', 'Media', 'Organization', 'Person', 'Work']
        result = []
        for type in order:
            if type in list:
                result.append(type)

        for extra in list:
            if extra not in result:
                result.append(extra)

        return result

    def purgeType(self, type):
        purgedResult = []
        if type == 'All':
            purgedResult = getToolByName(self, 'plone_utils').getUserFriendlyTypes()
        elif type == 'Media':
            purgedResult = [
             'File', 'Image']
        else:
            purgedResult = [
             type]
        return purgedResult

    def getTypeName(self, type):
        if self.request['LANGUAGE'][:2] == 'es':
            if type == 'Person':
                name = 'Personas'
            elif type == 'Event':
                name = 'Eventos'
            elif type == 'Organization':
                name = 'Organizaciones'
            elif type == 'Work':
                name = 'Obras'
            elif type == 'All':
                name = 'Todo'
            elif type == 'Media':
                name = 'Media'
            elif type == 'News Item':
                name = 'Noticias'
            else:
                name = type + 's'
        elif type == 'Person':
            name = 'People'
        elif type == 'Event':
            name = 'Events'
        elif type == 'Organization':
            name = 'Organizations'
        elif type == 'Work':
            name = 'Works'
        elif type == 'All':
            name = 'All'
        elif type == 'Media':
            name = 'Media'
        elif type == 'News Item':
            name = 'News'
        else:
            name = type + 's'
        return name

    def createSearchURL(self, request, type):
        purgedType = self.purgeType(type)
        portal_url = getToolByName(self, 'portal_url')
        stext = request.form.get('SearchableText', '')
        searchURL = portal_url() + '/' + request['LANGUAGE'][:2] + '/search?SearchableText=' + stext
        for item in purgedType:
            searchURL += '&portal_type%3Alist=' + item

        return searchURL
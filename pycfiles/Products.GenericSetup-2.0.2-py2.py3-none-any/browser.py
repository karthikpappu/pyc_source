# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/galleriffic/browser.py
# Compiled at: 2011-08-29 07:26:20
from Products.Five import BrowserView
from Products.CMFPlone.utils import getToolByName
from zope.interface import Interface, alsoProvides
from zope import schema
from Products.Five.formlib import formbase
from zope.formlib import form
from Products.galleriffic import PLONE3, PLONE4
if PLONE3:
    from zope.app.annotation.interfaces import IAnnotations
if PLONE4:
    from zope.annotation.interfaces import IAnnotations
from Products.galleriffic.interfaces import IGallerifficView
from Products.ATContentTypes.interface.topic import IATTopic
from Products.galleriffic import AbstractGallerifficMessageFactory as _
default_values = {'delay': 2500, 'numThumbs': 10, 'enableTopPager': 'true', 'enableBottomPager': 'true', 'renderSSControls': 'true', 'renderNavControls': 'true', 'autoStart': 'false', 'enableLightBox': 'false', 'viewCaption': 'false'}

class IGallerificSetting(Interface):
    """ """
    __module__ = __name__
    delay = schema.Int(title=_('Delay'), required=False, default=2500)
    numThumbs = schema.Int(title=_('Number of thumbnails to show page'), required=False, default=10)
    enableTopPager = schema.Choice(title=_('Show top navigation'), values=['true', 'false'], default='true')
    enableBottomPager = schema.Choice(title=_('Show bottom navigation'), values=['true', 'false'], default='true')
    enableLightBox = schema.Choice(title=_('Open image in popup with lightbox'), values=['true', 'false'], default='false')
    viewCaption = schema.Choice(title=_('Show image caption'), values=['true', 'false'], default='false')
    renderSSControls = schema.Choice(title=_('Show Play and Pause links'), values=['true', 'false'], default='true')
    renderNavControls = schema.Choice(title=_('Show Next and Previous links'), values=['true', 'false'], default='true')
    autoStart = schema.Choice(title=_('Should be playing or paused when the page first loads'), values=['true', 'false'], default='false')


class setIGallerifficView(BrowserView):
    """ """
    __module__ = __name__

    def __call__(self):
        """ """
        type_tool = getToolByName(self.context, 'portal_types')
        type_ = self.context.Type()
        folder_view_methods = list(type_tool[type_].view_methods)
        if 'galleriffic_view' not in folder_view_methods:
            folder_view_methods.append('galleriffic_view')
            type_tool[type_].view_methods = tuple(folder_view_methods)
        alsoProvides(self.context, IGallerifficView)
        return self.request.response.redirect(self.context.absolute_url())


class gelleriffic_settings_form(formbase.PageForm):
    """ """
    __module__ = __name__
    form_fields = form.FormFields(IGallerificSetting)

    def __init__(self, context, request):
        """View initialization"""
        self.request = request
        self.context = context

    def setUpWidgets(self, ignore_request=False):
        """Manually set the widget values"""
        annotated_obj = IAnnotations(self.context)
        keys = IGallerificSetting.names()
        data = {}
        try:
            for key in keys:
                data[key] = annotated_obj[key]

            self.widgets = form.setUpWidgets(self.form_fields, self.prefix, self.context, self.request, data=data, ignore_request=ignore_request)
        except:
            self.widgets = form.setUpWidgets(self.form_fields, self.prefix, self.context, self.request, ignore_request=ignore_request)

    @form.action('save settings')
    def save(self, action, data):
        """ """
        annotated_obj = IAnnotations(self.context)
        for key in data.keys():
            annotated_obj[key] = data[key]

        self.request.response.redirect(self.context.absolute_url())


class galleriffic_view(BrowserView):
    """ """
    __module__ = __name__

    def __init__(self, context, request):
        """ """
        self.context = context
        self.request = request

    def getJSTranslation(self, key):
        js_vars2 = {}
        js_vars2['playLinkText'] = _('Play Slideshow')
        js_vars2['pauseLinkText'] = _('Pause Slideshow')
        js_vars2['prevLinkText'] = _('&lsaquo; Previous Photo')
        js_vars2['nextLinkText'] = _('Next Photo &rsaquo;')
        js_vars2['nextPageLinkText'] = _('Next &rsaquo;')
        js_vars2['prevPageLinkText'] = _('&lsaquo; Prev')
        js_vars2['showCaption'] = _('Show Caption')
        js_vars2['hideCaption'] = _('Hide Caption')
        return js_vars2[key]

    @property
    def settings(self):
        annotated_obj = IAnnotations(self.context)
        return annotated_obj

    def showCaption(self):
        if not self.settings.has_key('viewCaption'):
            return False
        return self.settings.get('viewCaption')

    def __getJS__(self):
        """ """
        annotated_obj = self.settings
        js_vars = {}
        keys = IGallerificSetting.names()
        for key in keys:
            if annotated_obj.has_key(key):
                js_vars[key] = annotated_obj[key]
            else:
                js_vars[key] = default_values[key]

        js = '<script type="text/javascript">'
        for var in js_vars.keys():
            js += '%s = %s;\n' % ('js_' + var, js_vars[var])

        js += "%s = '%s';\n" % ('js_absolute_url', self.context.absolute_url())
        js += '</script>'
        return js

    def getImages(self):
        """docstring for getImages"""
        if IATTopic.providedBy(self.context):
            images = self.context.queryCatalog()
        else:
            ct_tool = getToolByName(self.context, 'portal_catalog')
            images = ct_tool(Type='Image', path=('/').join(self.context.getPhysicalPath()), sort_on='getObjPositionInParent')
        return images
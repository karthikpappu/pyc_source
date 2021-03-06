# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/anz/dashboard/browser/widgetview.py
# Compiled at: 2010-09-26 21:53:54
import cjson
from Products.Five import BrowserView
from zope.interface import implements
from Acquisition import aq_parent, aq_inner, aq_base
from zope.i18n import translate
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.ActionInformation import ActionInfo
from Products.CMFPlone.PloneBaseTool import getExprContext
from anz.dashboard.interfaces import IWidgetView
from anz.dashboard import MSG_FACTORY as _

class WidgetView(BrowserView):
    """  """
    __module__ = __name__
    implements(IWidgetView)

    def __init__(self, context, request):
        super(WidgetView, self).__init__(context, request)
        self.ec = getExprContext(context, object=None)
        return

    def getWidgets(self, check_visibility=True, check_permissions=True, check_condition=True, retJson=True):
        """ Return a sequence of registered widgets' information.
        
        @param check_visibility
        if True, return only actions whose "visible" flag is set.
        
        @param check_permissions
        if True, return only actions for whose permissions the current user is
        authorized.
        
        @param check_condition
        if True, return only actions whose condition expression evaluates True.
        
        @param retJson
        format return value to json format or not
        
        @return
        a dict with widgets' information, format like:
        {
            'success': True,
            'msg': 'Get widgets success.',
            'widgets': [{
                'id': '',
                'title': '',
                'desc': '',
                'icon': ''
                },
                ...
                ]
        }
        """
        context = self.context
        request = self.request
        ret = {}
        ret['widgets'] = []
        try:
            action_infos = self._getActions(check_visibility=check_visibility, check_permissions=check_permissions, check_condition=check_condition)
            for ai in action_infos:
                item = {}
                item['id'] = ai['id']
                item['title'] = translate(ai['title'], context=request)
                item['desc'] = translate(ai['description'], context=request)
                item['icon'] = ai['icon']
                ret['widgets'].append(item)

            ret['success'] = True
            ret['msg'] = translate(_('Get widgets success.'), context=request)
        except Exception, e:
            ret['success'] = False
            ret['msg'] = str(e)

        return retJson and cjson.encode(ret) or ret

    def getWidget(self, id, check_visibility=True, check_permissions=True, check_condition=True, retJson=True):
        """ Return the specific widget's information.
                
                @param id
                id of the wanted widget
                
                @param check_visibility
        if True, return only action whose "visible" flag is set.
                
                @param check_permissions
        if True, return only action for whose permissions the current user is
                authorized.
                
                @param check_condition
        if True, return only action whose condition expression evaluates True.
        
        @param retJson
                format return value to json format or not
                
                @return
                a dict with the following format:
                {
                    'success': True,
                        'msg': 'Get widget success.',
                    'id': '',
                        'title': '',
                        'desc': '',
                        'icon': ''
                }
                
                """
        context = self.context
        request = self.request
        ret = {}
        widgets = self.getWidgets(check_visibility=check_visibility, check_permissions=check_permissions, check_condition=check_condition, retJson=False)['widgets']
        for w in widgets:
            if w['id'] == id:
                ret['success'] = True
                ret['msg'] = translate(_('Get widget success.'), context=request)
                ret.update(w)
                break
        else:
            ret['success'] = False
            ret['msg'] = translate(_('No widget with id "${id}" found.'), mapping={'id': id}, context=request)

        return retJson and cjson.encode(ret) or ret

    def _getActions(self, check_visibility=True, check_permissions=True, check_condition=True):
        ret = []
        pa = getToolByName(self.context, 'portal_actions')
        category = getattr(aq_inner(pa), 'dashboard_widgets', None)
        if category is not None:
            for action in category.listActions():
                ai = ActionInfo(action, self.ec)
                if check_visibility and not ai['visible']:
                    continue
                if check_permissions and not ai['allowed']:
                    continue
                if check_condition and not ai['available']:
                    continue
                ret.append(ai)

        return ret
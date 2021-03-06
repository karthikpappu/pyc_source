# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_viewlet/viewlet.py
# Compiled at: 2020-02-18 20:07:12
# Size of source mod 2**32: 8983 bytes
"""PyAMS_viewlet.viewlet module

This module provides base content providers and viewlets classes, as well as a decorators
which can be used instead of ZCML declarations to register content providers and viewlets.
"""
import logging, venusian
from pyramid.exceptions import ConfigurationError
from pyramid.interfaces import IRequest, IView
from zope.contentprovider.interfaces import IContentProvider
from zope.interface import Interface, implementer
from pyams_template.template import get_view_template
from pyams_viewlet.interfaces import IViewlet, IViewletManager
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (viewlet)')

@implementer(IContentProvider)
class EmptyContentProvider:
    __doc__ = 'Empty content provider base class'
    permission = None

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        if self.permission and not self.request.has_permission(self.permission, context=self.context):
            return ''
        self.update()
        return self.render()

    def update(self):
        """See `IContentProvider` interface"""
        pass

    def render(self):
        """See `IContentProvider` interface"""
        return ''


class BaseContentProvider(EmptyContentProvider):
    __doc__ = 'Base template based content provider'
    resources = ()

    def update(self):
        for resource in self.resources:
            resource.need()

    render = get_view_template()


@implementer(IContentProvider)
class ViewContentProvider(BaseContentProvider):
    __doc__ = 'Template based content provider'

    def __init__(self, context, request, view):
        super(ViewContentProvider, self).__init__(context, request)
        self.view = self.__parent__ = view


class contentprovider_config:
    __doc__ = "Class decorator used to declare a content provider\n\n    You can provide same arguments as in 'viewlet' ZCML directive:\n    @name = name of the viewlet; may be unique for a given viewlet manager\n    @view = the view class or interface for which viewlet is displayed\n    @for = the context class or interface for which viewlet is displayed\n    @permission = name of a permission required to display the viewlet\n    @layer = request interface required to display the viewlet\n    "
    venusian = venusian

    def __init__(self, **settings):
        if not settings.get('name'):
            raise ConfigurationError('You must provide a name for a content provider')
        if 'for_' in settings and settings.get('context') is None:
            settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, obj):
            cdict = {'__name__': settings.get('name'), 
             '__module__': obj.__module__}
            if 'permission' in settings:
                settings['permission'] = settings.get('permission')
            bases = (obj,)
            if not IContentProvider.implementedBy(obj):
                bases = bases + (ViewContentProvider,)
            new_class = type('<ViewContentProvider %s>' % settings.get('name'), bases, cdict)
            LOGGER.debug('Registering content provider {0} ({1})'.format(settings.get('name'), str(new_class)))
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            registry.registerAdapter(new_class, (
             settings.get('context', Interface),
             settings.get('layer', IRequest),
             settings.get('view', IView)), IContentProvider, settings.get('name'))

        info = self.venusian.attach(wrapped, callback, category='pyams_viewlet')
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped


@implementer(IViewlet)
class EmptyViewlet:
    __doc__ = 'Empty viewlet base class'
    permission = None

    def __init__(self, context, request, view, manager):
        self.context = context
        self.request = request
        self.__parent__ = view
        self.manager = manager

    def update(self):
        """See `IContentProvider` interface"""
        pass

    def render(self):
        """See `IContentProvider` interface"""
        return ''


class Viewlet(EmptyViewlet):
    __doc__ = 'Viewlet adapter class used in meta directive as a mixin class.'
    render = get_view_template()


class viewlet_config:
    __doc__ = "Class decorator used to declare a viewlet\n\n    You can provide same arguments as in 'viewlet' ZCML directive:\n    @name = name of the viewlet; may be unique for a given viewlet manager\n    @manager = manager class or interface holding the viewlet\n    @view = the view class or interface for which viewlet is displayed\n    @for = the context class or interface for which viewlet is displayed\n    @permission = name of a permission required to display the viewlet\n    @layer = request interface required to display the viewlet\n    @weight = weight of the viewlet when using a weight ordered viewlet manager\n    "
    venusian = venusian

    def __init__(self, **settings):
        if not settings.get('name'):
            raise ConfigurationError('You must provide a name for a viewlet')
        if 'for_' in settings and settings.get('context') is None:
            settings['context'] = settings['for_']
        self.__dict__.update(settings)

    def __call__(self, wrapped):
        settings = self.__dict__.copy()

        def callback(context, name, obj):
            cdict = {'__name__': settings.get('name'), 
             '__module__': obj.__module__}
            if 'permission' in settings:
                cdict['permission'] = settings.get('permission')
            if 'weight' in settings:
                cdict['weight'] = settings.get('weight')
            bases = (obj,)
            if not IViewlet.implementedBy(obj):
                bases = bases + (Viewlet,)
            new_class = type('<Viewlet %s>' % settings.get('name'), bases, cdict)
            LOGGER.debug('Registering viewlet {0} ({1})'.format(settings.get('name'), str(new_class)))
            registry = settings.get('registry')
            if registry is None:
                config = context.config.with_package(info.module)
                registry = config.registry
            registry.registerAdapter(new_class, (
             settings.get('context', Interface),
             settings.get('layer', IRequest),
             settings.get('view', IView),
             settings.get('manager', IViewletManager)), IViewlet, settings.get('name'))

        info = self.venusian.attach(wrapped, callback, category='pyams_viewlet')
        if info.scope == 'class' and settings.get('attr') is None:
            settings['attr'] = wrapped.__name__
        settings['_info'] = info.codeinfo
        return wrapped
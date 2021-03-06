# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/senex/__init__.py
# Compiled at: 2016-04-30 12:40:20
from pyramid.config import Configurator
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy import engine_from_config
from senex.security import groupfinder
from .models import DBSession, Base
from worker import start_worker

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    start_worker()
    authn_policy = AuthTktAuthenticationPolicy('blargon5', callback=groupfinder, hashalg='sha512', timeout=900)
    authz_policy = ACLAuthorizationPolicy()
    config = Configurator(settings=settings, root_factory='senex.models.RootFactory')
    config.set_authentication_policy(authn_policy)
    config.set_authorization_policy(authz_policy)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('view_main_page', '/')
    config.add_route('return_status', '/senexstatus')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('view_old', '/{oldname}')
    config.add_route('add_old', '/add/{oldname}')
    config.add_route('edit_old', '/{oldname}/edit')
    config.scan()
    return config.make_wsgi_app()
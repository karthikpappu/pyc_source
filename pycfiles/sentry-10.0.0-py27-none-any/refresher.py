# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/mediators/token_exchange/refresher.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry import analytics
from sentry.coreapi import APIUnauthorized
from sentry.mediators import Mediator, Param
from sentry.mediators.token_exchange.validator import Validator
from sentry.mediators.token_exchange.util import token_expiration
from sentry.models import ApiApplication, ApiToken, SentryApp
from sentry.utils.cache import memoize

class Refresher(Mediator):
    """
    Exchanges a Refresh Token for a new Access Token
    """
    install = Param('sentry.models.SentryAppInstallation')
    refresh_token = Param(six.string_types)
    client_id = Param(six.string_types)
    user = Param('sentry.models.User')

    def call(self):
        self._validate()
        self._delete_token()
        return self._create_new_token()

    def record_analytics(self):
        analytics.record('sentry_app.token_exchanged', sentry_app_installation_id=self.install.id, exchange_type='refresh')

    def _validate(self):
        Validator.run(install=self.install, client_id=self.client_id, user=self.user)
        self._validate_token_belongs_to_app()

    def _validate_token_belongs_to_app(self):
        if self.token.application != self.application:
            raise APIUnauthorized

    def _delete_token(self):
        self.token.delete()

    def _create_new_token(self):
        token = ApiToken.objects.create(user=self.user, application=self.application, scope_list=self.sentry_app.scope_list, expires_at=token_expiration())
        self.install.api_token = token
        self.install.save()
        return token

    @memoize
    def token(self):
        try:
            return ApiToken.objects.get(refresh_token=self.refresh_token)
        except ApiToken.DoesNotExist:
            raise APIUnauthorized

    @memoize
    def application(self):
        try:
            return ApiApplication.objects.get(client_id=self.client_id)
        except ApiApplication.DoesNotExist:
            raise APIUnauthorized

    @property
    def sentry_app(self):
        try:
            return self.application.sentry_app
        except SentryApp.DoesNotExist:
            raise APIUnauthorized
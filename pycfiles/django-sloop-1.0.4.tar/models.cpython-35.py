# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/django_sloop/models.py
# Compiled at: 2019-07-23 09:11:36
# Size of source mod 2**32: 6125 bytes
import json
from django.conf import settings
from django.contrib.gis.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.encoding import smart_text
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import truncatechars
from django_sloop.exceptions import DeviceIsNotActive
from .settings import DJANGO_SLOOP_SETTINGS
from . import tasks

class PushNotificationMixin(object):
    __doc__ = '\n    A Mixin that handles push notification sending through the User model.\n    '

    def get_badge_count(self):
        return 0

    def get_active_pushable_device(self):
        """
        Finds and returns the last active device with push token for this user, if available
        """
        try:
            device = self.devices.filter(deleted_at__isnull=True).order_by('-date_created').first()
        except ObjectDoesNotExist:
            return

        return device

    def send_push_notification_async(self, message, url=None, sound=None, extra=None, category=None, **kwargs):
        device = self.get_active_pushable_device()
        if not device:
            return False
        if settings.DEBUG:
            print('Push notification: %s / Receiver: %s' % (message, self))
        sound = sound or DJANGO_SLOOP_SETTINGS.get('DEFAULT_SOUND') or None
        tasks.send_push_notification.delay(device.id, message, url, self.get_badge_count(), sound, extra, category, **kwargs)

    def send_silent_push_notification_async(self, extra=None, content_available=True, **kwargs):
        """
        Sends a push notification to the user's last active device
        """
        if settings.DEBUG:
            print('Silent push notification to: %s' % self)
        device = self.get_active_pushable_device()
        if not device:
            return False
        tasks.send_silent_push_notification.delay(device.id, extra, self.get_badge_count(), content_available, **kwargs)


class AbstractSNSDevice(models.Model):
    PLATFORM_IOS = 'ios'
    PLATFORM_ANDROID = 'android'
    PLATFORM_CHOICES = (
     (
      PLATFORM_IOS, 'iOS'),
     (
      PLATFORM_ANDROID, 'Android'))
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='devices', on_delete=models.CASCADE)
    locale = models.CharField(max_length=255, default='en_US')
    push_token = models.CharField(max_length=255, null=True)
    platform = models.CharField(max_length=255, choices=PLATFORM_CHOICES)
    model = models.CharField(max_length=255, blank=True)
    sns_platform_endpoint_arn = models.CharField(_('SNS Platform Endpoint'), max_length=255, null=True, unique=True)
    deleted_at = models.DateTimeField(null=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Device')
        verbose_name_plural = _('Devices')
        unique_together = ('push_token', 'platform')
        ordering = ('-date_updated', )
        get_latest_by = 'date_updated'
        abstract = True

    def __str__(self):
        return smart_text(_('Push Token %(push_token)s for %(user)s') % {'user': str(self.user), 
         'push_token': self.push_token})

    def invalidate(self):
        self.deleted_at = timezone.now()
        self.save()

    def prepare_message(self, message):
        """
        Prepares message before sending.
        """
        return truncatechars(message, 255)

    def send_push_notification(self, message, url=None, badge_count=None, sound=None, extra=None, category=None, **kwargs):
        """
        Sends push message using device push token
        """
        from .handlers import SNSHandler
        if self.deleted_at:
            raise DeviceIsNotActive
        message = self.prepare_message(message)
        handler = SNSHandler(device=self)
        message_payload, response = handler.send_push_notification(message, url, badge_count, sound, extra, category, **kwargs)
        if DJANGO_SLOOP_SETTINGS['LOG_SENT_MESSAGES']:
            PushMessage.objects.create(device=self, body=message_payload, sns_message_id=response.get('MessageId') or None, sns_response=response)
        return response

    def send_silent_push_notification(self, extra=None, badge_count=None, content_available=None, **kwargs):
        """
        Sends silent push notification
        """
        from .handlers import SNSHandler
        if self.deleted_at:
            raise DeviceIsNotActive
        handler = SNSHandler(device=self)
        message_payload, response = handler.send_silent_push_notification(extra, badge_count, content_available, **kwargs)
        if DJANGO_SLOOP_SETTINGS['LOG_SENT_MESSAGES']:
            PushMessage.objects.create(device=self, body=message_payload, sns_message_id=response.get('MessageId') or None, sns_response=response)
        return response


class PushMessage(models.Model):
    device = models.ForeignKey(DJANGO_SLOOP_SETTINGS['DEVICE_MODEL'], related_name='push_messages', on_delete=models.CASCADE)
    body = models.TextField(null=False, blank=False)
    sns_message_id = models.CharField(max_length=255, unique=True, blank=True, null=True)
    sns_response = models.TextField(null=False, blank=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Push Message'
        verbose_name_plural = 'Push Messages'
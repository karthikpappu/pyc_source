# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/notifications/views.py
# Compiled at: 2019-02-21 19:34:58
# Size of source mod 2**32: 2546 bytes
"""views.py."""
from json import loads
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView, View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from . import default_settings as settings
from .signals import notify
from .models import Notification

class NotificationsView(ListView):
    __doc__ = 'View for notifications for clients/mechanics.'
    model = Notification
    context_object_name = 'notifications_list'
    paginate_by = settings.NOTIFICATIONS_PAGINATE_BY

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(recipient=(self.request.user))


class GenerateNotification(View):
    __doc__ = 'View to generate test notifications.'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return (super(GenerateNotification, self).dispatch)(request, *args, **kwargs)

    def add_access_control_headers(self, response):
        """Add headers for CORS."""
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Max-Age'] = '1000'
        response['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type'

    def post(self, request, *args, **kwargs):
        """Generate the notification."""
        data = loads(request.body)
        message = data['message']
        User = get_user_model()
        try:
            user = User.objects.get(username='demouser')
        except ObjectDoesNotExist:
            user = User.objects.create_user(username='demouser',
              email='example@gmail.com',
              password='mypassword')

        args = {'source':user, 
         'source_display_name':user.get_full_name(),  'recipient':user, 
         'category':'Quote',  'action':'Sent',  'obj':user.id, 
         'short_description':'You a message: {}'.format(message), 
         'url':'http://example.com', 
         'channels':('websocket', )}
        (notify.send)(sender=self.__class__, **args)
        response = JsonResponse({'message': 'Notification generated'})
        self.add_access_control_headers(response)
        return response
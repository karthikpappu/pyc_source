# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ali/ownCloud/Project/python/django-aparnik-framework-project/testandbuildprojectframework/aparnik/packages/shops/orders/tasks.py
# Compiled at: 2020-03-11 04:57:46
# Size of source mod 2**32: 1341 bytes
"""Celery tasks."""
from __future__ import absolute_import, unicode_literals
import time
from celery import shared_task
from aparnik.contrib.users.models import User
from aparnik.packages.shops.orders.api.serializers import OrderSummarySerializer
from aparnik.packages.shops.orders.models import *
from aparnik.contrib.messaging.utils import notify
from aparnik.utils.utils import get_request

@shared_task
def send_order_message(order_id, is_create):
    """Send chat message create notification and etc via a channel to celery."""
    time.sleep(0.2)
    order_obj = Order.objects.get(pk=order_id)
    serializer = OrderSummarySerializer(order_obj, many=False, read_only=True, context={'request': get_request()})
    users = User.objects.admins()
    for user in users:
        notify(uri=(order_obj.user.username),
          source=(order_obj.user),
          source_display_name=(order_obj.user.get_full_name()),
          recipient=user,
          action=('Create' if is_create else 'Modified'),
          obj=order_obj,
          short_description=('You have a {} order.'.format('new' if is_create else 'modified')),
          extra_data={'uri':order_obj.user.username, 
         'message':serializer.data},
          channels=[
         'push'],
          silent=True)
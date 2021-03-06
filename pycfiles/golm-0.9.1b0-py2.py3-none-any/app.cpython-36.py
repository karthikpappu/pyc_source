# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prihodad/Documents/projects/visitor/golm/golm/golm_webgui/app.py
# Compiled at: 2018-04-15 14:10:04
# Size of source mod 2**32: 297 bytes
from django.apps import AppConfig
from core.interfaces import all

class WebGui(AppConfig):
    name = 'golm_webgui'
    prefix = 'web'
    verbose_name = 'Chatbot web GUI'

    def ready(self):
        from .interface import WebGuiInterface
        all.register_chat_interface(WebGuiInterface)
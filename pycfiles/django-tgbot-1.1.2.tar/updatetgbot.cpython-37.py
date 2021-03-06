# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/alireza/Projects/Mac/DjangoTGBot/project/django_tgbot/management/commands/updatetgbot.py
# Compiled at: 2020-04-06 03:46:14
# Size of source mod 2**32: 1334 bytes
import os
from django.conf import settings
from django.core.management.base import BaseCommand
from django_tgbot.management import helpers

class Command(BaseCommand):
    help = 'Updates the token for an existing tgbot'

    def handle(self, *args, **options):
        bot_username = input('Enter the username of the bot (without @): ').lower()
        dst = os.path.join(settings.BASE_DIR, bot_username)
        if not os.path.isdir(dst):
            self.stdout.write(self.style.ERROR('No such bot found. Make sure you have created your bot with command `createtgbot`.'))
            return
        get_me_result, bot_token = helpers.prompt_token(self, prompt_message='Enter the new token for this bot: ')
        bot_name = str(get_me_result.get_first_name())
        received_username = str(get_me_result.get_username()).lower()
        if received_username != bot_username:
            self.stdout.write(self.style.ERROR('Given token does not belong to this bot.'))
            return
        with open(os.path.join(dst, '__init__.py'), 'w') as (f):
            f.write("# Do not remove these 2 lines:\nbot_token = '{}'\napp_name='{}'".format(bot_token, bot_username))
        self.stdout.write(self.style.SUCCESS('Successfully updated token for bot {}(@{}).'.format(bot_name, bot_username)))
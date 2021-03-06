# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/uittenbroek/Projects/buildout-nuffic/src/collective.newrelic/collective/newrelic/patches/cron4plone.py
# Compiled at: 2013-12-24 05:41:42
HAS_CRON4PLONE = False
import newrelic.agent
from collective.newrelic.utils import logger
try:
    from Products.cron4plone.browser.views.cron_tick import CronTick
    HAS_CRON4PLONE = True
except ImportError, e:
    pass

if HAS_CRON4PLONE:
    original_tick = CronTick.tick

    @newrelic.agent.background_task(name='crontick')
    def patched_tick(self, *args, **kwargs):
        original_tick(self, *args, **kwargs)


    CronTick.tick = patched_tick
    logger.info('Patched Products.cron4plone.browser.CronTick:tick to become a background task')
else:
    logger.info('Unable to patched Products.cron4plone, probably not used.')
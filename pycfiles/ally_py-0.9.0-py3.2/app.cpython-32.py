# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/container/app.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Jan 10, 2013

@package: ally plugin
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the IoC container plugin distribution support.
"""
from . import ioc
from .event import REPAIR, onDecorator, Trigger, ITrigger
from ally.support.util_sys import callerLocals
from itertools import chain
REPAIR = REPAIR
DEPLOY = Trigger('deploy')
SUPPORT = Trigger('support')
NORMAL = Trigger('normal')
DEVEL = Trigger('development')
POPULATE = Trigger('populate')
CHANGED = Trigger('changed', REPAIR)
PRIORITY_FINAL = ioc.PRIORITY_FINAL
PRIORITY_LAST = ioc.PRIORITY_LAST
PRIORITY_NORMAL = ioc.PRIORITY_NORMAL
PRIORITY_FIRST = ioc.PRIORITY_FIRST
PRIORITY_TOP = ioc.PRIORITY_TOP

def deploy(*triggers, priority=PRIORITY_NORMAL):
    """
    Decorator for deploy setup functions. The deploy function will be called every time the  application is started.
    This should manly be used to gather data.
    
    @param triggers: arguments[ITrigger]
        Triggers to be considered for the deploy call, this will actually condition the deploy call to the provided triggers.
    @param priority: one of priority markers
        The priority to associate with the event.
    """
    if not triggers:
        return onDecorator((DEPLOY,), priority, callerLocals())
    if len(triggers) == 1 and not isinstance(triggers[0], ITrigger):
        return onDecorator((DEPLOY,), priority, callerLocals())(triggers[0])
    return onDecorator(triggers, priority, callerLocals())


def populate(*triggers, priority=PRIORITY_NORMAL):
    """
    Decorator for populate setup functions. The populate function will be called until a True or None value is returned.
    This should manly be used in order to populate default data.
    If the function returns False it means it needs to be called again for the same event, if True or None is returned
    it means the function executed successfully.
    
    @param triggers: arguments[ITrigger]
        Additional triggers to be considered for the populate, this events will trigger the populate for other situations
        rather just the application first start.
    @param priority: one of priority markers
        The priority to associate with the event.
    """
    if not triggers:
        return onDecorator((POPULATE,), priority, callerLocals())
    if len(triggers) == 1 and not isinstance(triggers[0], ITrigger):
        return onDecorator((POPULATE,), priority, callerLocals())(triggers[0])
    return onDecorator(chain(triggers, (POPULATE,)), priority, callerLocals())
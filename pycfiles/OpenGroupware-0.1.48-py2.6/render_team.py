# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/core/vcard/render_team.py
# Compiled at: 2012-10-12 07:02:39
import vobject

def render_team(team, ctx, **params):
    card = vobject.vCard()
    card.add('n')
    card.n.value = vobject.vcard.Name(family='OpenGroupware', given=team.name)
    card.add('fn').value = team.name
    card.add('uid').value = 'coils://Team/%d' % team.object_id
    return str(card.serialize())
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/reviews/evolutions/extra_data.py
# Compiled at: 2020-02-11 04:03:56
from django_evolution.mutations import AddField
from djblets.db.fields import JSONField
MUTATIONS = [
 AddField('ReviewRequest', 'extra_data', JSONField, null=True),
 AddField('Group', 'extra_data', JSONField, null=True),
 AddField('Review', 'extra_data', JSONField, null=True),
 AddField('ReviewRequestDraft', 'extra_data', JSONField, null=True)]
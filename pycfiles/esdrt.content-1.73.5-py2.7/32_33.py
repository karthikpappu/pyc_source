# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/upgrades/32_33.py
# Compiled at: 2019-05-21 05:08:43
from zope.globalrequest import getRequest
from Products.CMFCore.utils import getToolByName
PROFILE_ID = 'profile-esdrt.content:default'

def upgrade(context, logger=None):
    if logger is None:
        from logging import getLogger
        logger = getLogger('esdrt.content.upgrades.32_33')
    install_workflow(context, logger)
    reindex_myview_index(context, logger)
    logger.info('Upgrade steps executed')
    return


def reindex_myview_index(context, logger):
    logger.info('Reindexing indexes')
    catalog = getToolByName(context, 'portal_catalog')
    catalog.reindexIndex(name='observation_question_status', REQUEST=getRequest())


def install_workflow(context, logger):
    setup = getToolByName(context, 'portal_setup')
    wtool = getToolByName(context, 'portal_workflow')
    wtool.manage_delObjects([
     'esd-answer-workflow',
     'esd-comment-workflow',
     'esd-conclusion-workflow',
     'esd-conclusion-phase2-workflow',
     'esd-file-workflow',
     'esd-question-review-workflow',
     'esd-reviewtool-folder-workflow',
     'esd-review-workflow'])
    setup.runImportStepFromProfile(PROFILE_ID, 'rolemap')
    setup.runImportStepFromProfile(PROFILE_ID, 'workflow')
    setup.runImportStepFromProfile(PROFILE_ID, 'sharing')
    logger.info('Reinstalled Workflows, Roles and Permissions ')
    wtool.updateRoleMappings()
    logger.info('Security settings updated')
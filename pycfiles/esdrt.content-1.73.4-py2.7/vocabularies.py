# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/vocabularies.py
# Compiled at: 2020-04-08 10:59:15
import itertools
from five import grok
from plone import api
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
import esdrt.content.constants as C

def mk_term(key, value):
    return SimpleVocabulary.createTerm(key, key, value)


class MSVocabulary(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('eea_member_states')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(MSVocabulary, name='esdrt.content.eea_member_states')

class GHGSourceCategory(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('ghg_source_category')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(GHGSourceCategory, name='esdrt.content.ghg_source_category')

class GHGSourceSectors(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('ghg_source_sectors')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(GHGSourceSectors, name='esdrt.content.ghg_source_sectors')

class Gas(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('gas')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(Gas, name='esdrt.content.gas')

class Fuel(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('fuel')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(Fuel, name='esdrt.content.fuel')

class Highlight(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('highlight')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(Highlight, name='esdrt.content.highlight')

class Parameter(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('parameter')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(Parameter, name='esdrt.content.parameter')

class StatusFlag(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('status_flag')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(StatusFlag, name='esdrt.content.status_flag')
from .crf_code_matching import crf_codes

class CRFCode(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = []
        crfcodes = crf_codes()
        for key, value in crfcodes.items():
            terms.append(SimpleVocabulary.createTerm(key, key, value['title']))

        return SimpleVocabulary(terms)


grok.global_utility(CRFCode, name='esdrt.content.crf_code')

class Conclusions(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('conclusion_reasons')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(Conclusions, name='esdrt.content.conclusionreasons')

class ConclusionsPhase2(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        pvoc = api.portal.get_tool('portal_vocabularies')
        voc = pvoc.getVocabularyByName('conclusion_phase2_reasons')
        terms = []
        if voc is not None:
            for key, value in voc.getVocabularyLines():
                terms.append(SimpleVocabulary.createTerm(key, key, value))

        return SimpleVocabulary(terms)


grok.global_utility(ConclusionsPhase2, name='esdrt.content.conclusionphase2reasons')

class Roles(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
        terms = list(itertools.starmap(mk_term, [
         ('Manager', 'Manager'),
         (
          C.ROLE_SE, 'Sector Expert'),
         (
          C.ROLE_RE, 'Review Expert'),
         (
          C.ROLE_QE, 'Quality Expert'),
         (
          C.ROLE_LR, 'Lead Reviewer'),
         (
          C.ROLE_RP1, 'Reviewer Phase 1'),
         (
          C.ROLE_RP2, 'Reviewer Phase 2'),
         (
          C.ROLE_MSA, 'MS Authority'),
         (
          C.ROLE_MSE, 'MS Expert')]))
        return SimpleVocabulary(terms)


grok.global_utility(Roles, name='esdrt.content.roles')
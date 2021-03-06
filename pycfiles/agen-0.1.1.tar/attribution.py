# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ageliaco/rd/content/attribution.py
# Compiled at: 2011-10-12 13:31:11
from five import grok
from zope import schema
from plone.namedfile import field as namedfile
from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.directives import form, dexterity
from plone.app.textfield import RichText
from plone.app.z3cform.wysiwyg import WysiwygFieldWidget
from zope.lifecycleevent.interfaces import IObjectModifiedEvent
from zope.interface import Interface, Attribute
from zope.component.factory import Factory
from zope.schema.fieldproperty import FieldProperty
from ageliaco.rd import _
import datetime
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
from zope.lifecycleevent.interfaces import IObjectCreatedEvent
from Products.CMFCore.utils import getToolByName
from plone.formwidget.autocomplete import AutocompleteMultiFieldWidget
from zope.interface import invariant, Invalid
from z3c.form.object import registerFactoryAdapter
from copy import deepcopy

class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """
    grok.implements(IContextSourceBinder)

    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        try:
            parent = context.aq_inner.aq_parent
            group = parent.contributor
        except:
            print context.aq_inner, context.aq_inner.parent

        terms = []
        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    member_mail = user.getProperty('email') or ''
                    ecole = user.getProperty('ecole') or ''
                    if ecole:
                        member_name = member_name + ' (' + ecole + ')'
                    terms.append(SimpleVocabulary.createTerm(member_id, str(member_id), member_name))

        return SimpleVocabulary(terms)


class IAttribution(form.Schema):
    """
    Attribution horaire
    """
    title = schema.TextLine(title='Titre', required=True)
    contributor = schema.TextLine(title='Contributeur', required=False)
    school = schema.TextLine(title='Ecole', required=False)
    sector = schema.TextLine(title='Centre de concertation', required=False)
    hour = schema.Float(title='Heure(s) totale demandée (R&D + école)', min=0.0, required=False)
    dexterity.read_permission(hourRD='cmf.ReviewPortalContent')
    dexterity.write_permission(hourRD='cmf.ReviewPortalContent')
    hourRD = schema.Float(title='Heure(s) totale proposée par R&D (R&D + école)', min=0.0, required=False)
    dexterity.write_permission(hourFinal='cmf.ReviewPortalContent')
    hourFinal = schema.Float(title='Heure(s) totale allouée au final(R&D + école)', min=0.0, required=False)


class Attribution(object):
    grok.implements(IAttribution)
    contributor = FieldProperty(IAttribution['contributor'])
    hour = FieldProperty(IAttribution['hour'])
    hourRD = FieldProperty(IAttribution['hourRD'])
    hourFinal = FieldProperty(IAttribution['hourFinal'])

    def __init__(self):
        pass

    def set(self, contributor, school, hour=0.0, hourRD=0.0, hourFinal=0.0):
        self.school = school
        self.contributor = contributor
        if school in schools.keys():
            self.sector = schools[school][1]
        else:
            self.sector = 'non disponible'
        self.hour = hour
        self.hourRD = hourRD
        self.hourFinal = hourFinal

    def __repr__(self):
        return '<%s %r>' % (self.__class__.__name__, self.id)


schools = {'ECGGR': ['EC Bougeries', 'CEC'], 'CEBOU': [
           'Nicolas-Bouvier', 'CEC'], 
   'CECHA': [
           'André-Chavanne', 'CEC'], 
   'CEGOU': [
           'Emilie-Gourd', 'CEC'], 
   'ECASE': [
           'Madame-de-Stael', 'CEC'], 
   'ECSTI': [
           'EC Aimée-Stitelmann', 'CEC'], 
   'CALV': [
          'Calvin', 'COLLEGES'], 
   'CAND': [
          'Candolle', 'COLLEGES'], 
   'CLAP': [
          'Claparède', 'COLLEGES'], 
   'COPAD': [
           'Alice-Rivaz', 'COLLEGES'], 
   'ROUS': [
          'Rousseau', 'COLLEGES'], 
   'SAUS': [
          'Saussure', 'COLLEGES'], 
   'SISM': [
          'Sismondi', 'COLLEGES'], 
   'VOLT': [
          'Voltaire', 'COLLEGES'], 
   'ECBGR': [
           'ECG RHONE', 'ECG'], 
   'DUNAN': [
           'Henry-Dunand', 'ECG'], 
   'MAILL': [
           'Ella-Maillart', 'ECG'], 
   'ECGJP': [
           'Jean-Piaget', 'ECG'], 
   'CFPC': [
          'CFPC', 'ECOLES PROFESSIONNELLES'], 
   'CFPS': [
          'CFPS', 'ECOLES PROFESSIONNELLES'], 
   'CFPT': [
          'CFPT', 'ECOLES PROFESSIONNELLES'], 
   'CFPSH': [
           'CFPSHR-EGEI', 'ECOLES PROFESSIONNELLES'], 
   'BOUV': [
          'CFPCOM-Bouvier', 'ECOLES PROFESSIONNELLES'], 
   'CFPNE': [
           'CFPNE', 'ECOLES PROFESSIONNELLES'], 
   'CFPAA': [
           'CFPAA', 'ECOLES PROFESSIONNELLES'], 
   'SCAI': [
          'SCAI', 'INSERTION'], 
   'COUDR': [
           'CO Coudriers', 'CYCLES']}
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/controlpanel/socialnetworks.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import _
from brasil.gov.portal.config import REDES
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope import schema
from zope.component import adapter
from zope.formlib.form import FormFields
from zope.formlib.objectwidget import ObjectWidget
from zope.formlib.sequencewidget import ListSequenceWidget
from zope.formlib.widget import CustomWidgetFactory
from zope.interface import implementer
from zope.interface import Interface
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
networks = SimpleVocabulary([ SimpleTerm(value=rede['id'], title=_(rede['title'])) for rede in REDES
                            ])

class ISocialNetworksPair(Interface):
    site = schema.Choice(title=_('Site'), description=_(_('help_social_network'), default='Escolha a rede a ser cadastrada'), required=True, vocabulary=networks)
    info = schema.TextLine(title='Identificador')


@implementer(ISocialNetworksPair)
class SocialNetworksPair:

    def __init__(self, site='', info=''):
        self.site = site
        self.info = info


class ISocialNetworksSchema(Interface):
    accounts_info = schema.List(title=_('Social Network'), default=[], value_type=schema.Object(ISocialNetworksPair, title='Rede'), required=False)


sn_widget = CustomWidgetFactory(ObjectWidget, SocialNetworksPair)
accounts_widget = CustomWidgetFactory(ListSequenceWidget, subwidget=sn_widget)

@implementer(ISocialNetworksSchema)
@adapter(IPloneSiteRoot)
class SocialNetworksPanelAdapter(SchemaAdapterBase):
    """ Adapter para a raiz do site Plone suportar o schema
        de configuracao da barra de identidade
        Esta classe implementa uma maneira da raiz do site armazenar
        as configuracoes que serao geridas pelo painel de controle
    """

    def __init__(self, context):
        super(SocialNetworksPanelAdapter, self).__init__(context)
        self.pp = getToolByName(context, 'portal_properties')
        self.context = getattr(self.pp, 'brasil_gov', None)
        return

    @apply
    def accounts_info():

        def get(self):
            accounts = []
            configs = self.context
            if configs:
                data = configs.getProperty('social_networks', [])
                for item in data:
                    k, v = item.split('|')
                    accounts.append(SocialNetworksPair(k, v))

                return accounts

        def set(self, value):
            accounts = []
            configs = self.context
            if configs:
                for ta in value:
                    if not ta.site:
                        continue
                    accounts.append('%s|%s' % (ta.site, ta.info))

                configs.manage_changeProperties(social_networks=accounts)

        return property(get, set)


class SocialNetworksControlPanel(ControlPanelForm):
    """ Implementacao do painel de controle da Barra de Identidade """
    form_fields = FormFields(ISocialNetworksSchema)
    form_fields['accounts_info'].custom_widget = accounts_widget
    label = _('.gov.br: Social Network')
    description = _('Identity Bar behavior Configuration')
    form_name = _('Visual and functional Configuration')
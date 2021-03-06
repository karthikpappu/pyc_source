# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/core/BaseObjectMaker.py
# Compiled at: 2019-12-11 16:37:48
"""The base card and related objects creation helper"""
from sqlobject import SQLObjectNotFound
from .BaseTables import CardType, Expansion, Rarity, RarityPair, PhysicalCard, Ruling, Keyword, Artist, Printing, PrintingProperty, LookupHints
from .BaseAdapters import ICardType, IExpansion, IRarity, IRarityPair, IPhysicalCard, IRuling, IKeyword, IArtist, IPrinting, IPrintingProperty, ILookupHint
from .BaseAbbreviations import CardTypes, Expansions, Rarities

class BaseObjectMaker(object):
    """Creates all kinds of program Objects from simple strings.

       All the methods will return either a copy of an existing object
       or a new object.
       """

    def _make_object(self, cObjClass, fAdapter, cAbbreviation, sObj, bShortname=False, bFullname=False):
        try:
            return fAdapter(sObj)
        except SQLObjectNotFound:
            sObj = cAbbreviation.canonical(sObj)
            dKw = {'name': sObj}
            if bShortname:
                dKw['shortname'] = cAbbreviation.shortname(sObj)
            if bFullname:
                dKw['fullname'] = cAbbreviation.fullname(sObj)
            return cObjClass(**dKw)

    def make_card_type(self, sType):
        return self._make_object(CardType, ICardType, CardTypes, sType)

    def make_expansion(self, sExpansion):
        return self._make_object(Expansion, IExpansion, Expansions, sExpansion, bShortname=True)

    def make_rarity(self, sRarity):
        return self._make_object(Rarity, IRarity, Rarities, sRarity, bShortname=True)

    def make_abstract_card(self, sCard):
        raise NotImplementedError

    def make_physical_card(self, oCard, oPrinting):
        try:
            return IPhysicalCard((oCard, oPrinting))
        except SQLObjectNotFound:
            return PhysicalCard(abstractCard=oCard, printing=oPrinting)

    def make_default_printing(self, oExp):
        return self.make_printing(oExp, None)

    def make_printing(self, oExp, sPrinting):
        try:
            return IPrinting((oExp, sPrinting))
        except SQLObjectNotFound:
            return Printing(name=sPrinting, expansion=oExp)

    def make_lookup_hint(self, sLookupDomain, sKey, sValue):
        try:
            return ILookupHint((sLookupDomain, sKey))
        except SQLObjectNotFound:
            return LookupHints(domain=sLookupDomain, lookup=sKey, value=sValue)

    def make_rarity_pair(self, sExp, sRarity):
        try:
            return IRarityPair((sExp, sRarity))
        except SQLObjectNotFound:
            oExp = self.make_expansion(sExp)
            oRarity = self.make_rarity(sRarity)
            return RarityPair(expansion=oExp, rarity=oRarity)

    def make_ruling(self, sText, sCode):
        try:
            return IRuling((sText, sCode))
        except SQLObjectNotFound:
            return Ruling(text=sText, code=sCode)

    def make_keyword(self, sKeyword):
        try:
            return IKeyword(sKeyword)
        except SQLObjectNotFound:
            return Keyword(keyword=sKeyword)

    def make_artist(self, sArtist):
        try:
            return IArtist(sArtist)
        except SQLObjectNotFound:
            return Artist(canonicalName=sArtist.lower(), name=sArtist)

    def make_printing_property(self, sValue):
        try:
            return IPrintingProperty(sValue)
        except SQLObjectNotFound:
            return PrintingProperty(value=sValue, canonicalValue=sValue.lower())
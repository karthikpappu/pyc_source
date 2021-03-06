# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1_modules/rfc5917.py
# Compiled at: 2020-01-09 12:20:13
from pyasn1.type import char
from pyasn1.type import constraint
from pyasn1.type import namedtype
from pyasn1.type import univ
from pyasn1_modules import rfc5280

class DirectoryString(univ.Choice):
    __module__ = __name__
    componentType = namedtype.NamedTypes(namedtype.NamedType('utf8String', char.UTF8String().subtype(subtypeSpec=constraint.ValueSizeConstraint(1, 64))))


id_clearanceSponsor = univ.ObjectIdentifier((2, 16, 840, 1, 101, 2, 1, 5, 68))
ub_clearance_sponsor = univ.Integer(64)
at_clearanceSponsor = rfc5280.Attribute()
at_clearanceSponsor['type'] = id_clearanceSponsor
at_clearanceSponsor['values'][0] = DirectoryString()
_certificateAttributesMapUpdate = {id_clearanceSponsor: DirectoryString()}
rfc5280.certificateAttributesMap.update(_certificateAttributesMapUpdate)
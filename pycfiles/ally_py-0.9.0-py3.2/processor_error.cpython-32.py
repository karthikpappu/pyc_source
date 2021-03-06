# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/processor_error.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Feb 7, 2013

@package: ally core http
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the processors used in presenting REST errors.
"""
from ..ally_core.processor import renderer
from ..ally_http.processor import contentLengthEncode, allowEncode, methodOverride, headerDecodeRequest, headerEncodeResponse, contentTypeResponseEncode
from .processor import allow_method_override, internalDevelError, uri, explainError, acceptDecode
from ally.container import ioc
from ally.core.http.impl.processor.error_populator import ErrorPopulator
from ally.design.processor.assembly import Assembly
from ally.design.processor.handler import Handler
from ally.http.spec.codes import METHOD_NOT_AVAILABLE

@ioc.entity
def statusToCode():
    return {METHOD_NOT_AVAILABLE.status: METHOD_NOT_AVAILABLE}


@ioc.entity
def errorPopulator() -> Handler:
    b = ErrorPopulator()
    b.statusToCode = statusToCode()
    return b


@ioc.entity
def assemblyErrorDelivery() -> Assembly:
    """
    The assembly containing the handlers that will be used in delivery for the error responses.
    """
    return Assembly('Error delivery')


@ioc.before(assemblyErrorDelivery)
def updateAssemblyErrorDelivery():
    assemblyErrorDelivery().add(internalDevelError(), headerDecodeRequest(), uri(), acceptDecode(), renderer(), errorPopulator(), explainError(), headerEncodeResponse(), contentTypeResponseEncode(), contentLengthEncode(), allowEncode())
    if allow_method_override():
        assemblyErrorDelivery().add(methodOverride(), before=acceptDecode())
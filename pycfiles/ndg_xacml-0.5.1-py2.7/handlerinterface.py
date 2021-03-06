# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ndg/xacml/core/context/handlerinterface.py
# Compiled at: 2012-06-19 10:10:35
"""NDG Security Context handler interface definition

NERC DataGrid
"""
__author__ = 'P J Kershaw'
__date__ = '24/02/10'
__copyright__ = '(C) 2010 Science and Technology Facilities Council'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__license__ = 'BSD - see LICENSE file in top-level directory'
__contact__ = 'Philip.Kershaw@stfc.ac.uk'
__revision__ = '$Id: handlerinterface.py 8078 2012-06-19 14:10:35Z pjkersha $'
from abc import ABCMeta, abstractmethod

class CtxHandlerInterface(object):
    """Context Handler interface."""
    __metaclass__ = ABCMeta
    __slots__ = ()

    @abstractmethod
    def handlePEPRequest(self, pepRequest):
        """Handle request from Policy Enforcement Point
        
        @param pepRequest: request from PEP, derived class determines its type
        e.g. SAML AuthzDecisionQuery
        @type pepRequest: type
        @return: PEP response - derived class determines type
        @rtype: None
        """
        raise NotImplementedError()

    def pipQuery(self, request, designator):
        """Query a Policy Information Point to retrieve the attribute values
        corresponding to the specified input designator.  Optionally, update the
        requestCtx.  This could be a subject, environment or resource.  Matching
        attributes values are returned
        
        @param request: request context
        @type request: ndg.xacml.core.context.request.Request
        @param designator: designator requiring additional subject attribute 
        information
        @type designator: ndg.xacml.core.expression.Expression derived type
        @return: list of attribute values for subject corresponding to given
        policy designator
        @rtype: list
        """
        return []
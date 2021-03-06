# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/constants.py
# Compiled at: 2019-02-15 13:51:23
""" LDAP Role mapping constants.
"""
LDAP_BASE = 'extranet-necd-review'
LDAP_BASE_PROJECTION = 'extranet-necd-projection'
LDAP_BASE_DN = '{base_dn}'
LDAP_SECRETARIAT = LDAP_BASE_DN + '-secretariat'
LDAP_TERT = LDAP_BASE_DN + '-tert'
LDAP_LEADREVIEW = LDAP_TERT + '-leadreview'
LDAP_SECTOREXP = LDAP_TERT + '-sectorexp'
LDAP_COUNTRIES = LDAP_BASE_DN + '-countries'
LDAP_MSA = LDAP_COUNTRIES + '-msa'
LDAP_MSEXPERT = LDAP_COUNTRIES + '-msexpert'
ROLE_SE = 'SectorExpert'
ROLE_CP = 'CounterPart'
ROLE_LR = 'LeadReviewer'
ROLE_MSA = 'MSAuthority'
ROLE_MSE = 'MSExpert'
P_OBS_REDRAFT_REASON_VIEW = 'emrt.necd.content: View Observation Redraft Reason'
__all__ = ('LDAP_BASE', 'LDAP_BASE_DN', 'LDAP_BASE_PROJECTION', 'LDAP_SECRETARIAT',
           'LDAP_TERT', 'LDAP_LEADREVIEW', 'LDAP_SECTOREXP', 'LDAP_COUNTRIES', 'LDAP_MSA',
           'LDAP_MSEXPERT', 'ROLE_SE', 'ROLE_CP', 'ROLE_LR', 'ROLE_MSA', 'ROLE_MSE')
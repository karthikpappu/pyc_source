# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/url/crawl/blocklist_utils.py
# Compiled at: 2019-11-16 18:33:01
# Size of source mod 2**32: 3021 bytes
from urllib import parse as urlparse
import url.crawl_utils.openWPM.domain_utils as du

def get_option_dict(request):
    """Build an options dict for BlockListParser

    Parameters
    ----------
    request : sqlite3.Row
        A single HTTP request record pulled from OpenWPM's http_requests table
    public_suffix_list : PublicSuffixList
        An instance of PublicSuffixList()

           BINARY_OPTIONS = [
        "script",
        "image",
        "stylesheet",
        "object",
        "xmlhttprequest",
        "object-subrequest",
        "subdocument",
        "document",
        "elemhide",
        "other",
        "background",
        "xbl",
        "ping",
        "dtd",
        "media",
        "third-party",
        "match-case",
        "collapse",
        "donottrack",
    ]

    Returns
    -------
    dict
        An "options" dictionary for use with BlockListParser
        refs: [1] https://github.com/MoonchildProductions/UXP/blob/master/dom/base/nsIContentPolicyBase.idl
              [2] https://adblockplus.org/en/filters#options
              [3] 
           
    """
    OPTIONS = {'other':{'enabled':False, 
      'content_policy_type':1}, 
     'script':{'enabled':False, 
      'content_policy_type':2}, 
     'image':{'enabled':False, 
      'content_policy_type':3}, 
     'stylesheet':{'enabled':False, 
      'content_policy_type':4}, 
     'object':{'enabled':False, 
      'content_policy_type':5}, 
     'document':{'enabled':False, 
      'content_policy_type':6}, 
     'subdocument':{'enabled':False, 
      'content_policy_type':7}, 
     'xbl':{'enabled':False, 
      'content_policy_type':9}, 
     'ping':{'enabled':False, 
      'content_policy_type':10}, 
     'xmlhttprequest':{'enabled':False, 
      'content_policy_type':11}, 
     'object-subrequest':{'enabled':False, 
      'content_policy_type':12}, 
     'dtd':{'enabled':False, 
      'content_policy_type':13}, 
     'media':{'enabled':False, 
      'content_policy_type':15}, 
     'elemhide':{'enabled': False}, 
     'background':{'enabled': False}, 
     'third-party':{'enabled': False}, 
     'match-case':{'enabled': False}, 
     'collapse':{'enabled': False}, 
     'donottrack':{'enabled': False}}
    options = {}
    try:
        for name in OPTIONS:
            if OPTIONS[name]['enabled']:
                if name == 'third-party':
                    options['third-party'] = du.get_ps_plus_1(request['url']) != du.get_ps_plus_1(request['top_level_url'])
                elif 'content_policy_type' in OPTIONS[name]:
                    options[name] = request['content_policy_type'] == OPTIONS[name]['content_policy_type']

    except Exception as e:
        try:
            print('exception {}'.format(e))
        finally:
            e = None
            del e

    return options
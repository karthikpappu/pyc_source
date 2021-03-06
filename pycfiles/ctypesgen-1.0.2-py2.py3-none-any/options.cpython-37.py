# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/options.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 1279 bytes
"""
All of the components of ctypegencore require an argument called "options".
In command-line usage, this would be an optparser.Values object. However, if
ctypesgen is used as a standard Python module, constructing this object
would be a pain. So this module exists to provide a "default" options object
for convenience.
"""
import optparse, copy
default_values = {'other_headers':[],  'modules':[],  'include_search_paths':[],  'compile_libdirs':[],  'runtime_libdirs':[],  'cpp':'gcc -E', 
 'cpp_defines':[],  'cpp_undefines':[],  'save_preprocessed_headers':None, 
 'all_headers':False, 
 'builtin_symbols':False, 
 'include_symbols':[],  'exclude_symbols':[],  'show_all_errors':False, 
 'show_long_errors':False, 
 'show_macro_warnings':True, 
 'header_template':None, 
 'inserted_files':[],  'other_known_names':[],  'include_macros':True, 
 'include_undefs':True, 
 'libraries':[],  'strip_build_path':None, 
 'output_language':'py', 
 'no_stddef_types':False, 
 'no_gnu_types':False, 
 'no_python_types':False, 
 'debug_level':0, 
 'strip_prefixes':[]}

def get_default_options():
    return optparse.Values(copy.deepcopy(default_values))
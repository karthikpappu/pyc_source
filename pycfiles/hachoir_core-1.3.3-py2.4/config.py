# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/hachoir_core/config.py
# Compiled at: 2009-09-07 17:44:28
"""
Configuration of Hachoir
"""
import os
max_string_length = 40
max_byte_length = 14
max_bit_length = 256
unicode_stdout = True
debug = False
verbose = False
quiet = False
if os.name == 'nt':
    use_i18n = False
else:
    use_i18n = True
autofix = True
check_padding_pattern = True
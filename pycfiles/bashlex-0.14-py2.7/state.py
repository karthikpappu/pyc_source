# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/bashlex/state.py
# Compiled at: 2019-03-01 15:42:24
from bashlex import flags, utils
parserstate = lambda : utils.typedset(flags.parser)
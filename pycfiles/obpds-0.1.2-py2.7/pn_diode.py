# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/obpds/examples/pn_diode.py
# Compiled at: 2015-11-15 13:26:57
import logging
logging.basicConfig()
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from obpds import *
p = Layer(1 * um, GaAs, 1e+17 / cm3)
n = Layer(1 * um, GaAs, -1e+17 / cm3)
d = TwoTerminalDevice(layers=[p, n], Fp='left', Fn='right')
d.show_zero_current(V=0.5)
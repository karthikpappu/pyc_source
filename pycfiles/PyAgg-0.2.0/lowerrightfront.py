# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyage_forams/conf/distributed3d/lowerrightfront.py
# Compiled at: 2014-11-03 18:14:25
from functools import partial
from pyage_forams.solutions.agent.remote_aggegate import create_remote_agent
from pyage_forams.conf.distributed3d.common import *
agents = partial(create_remote_agent, 'lowerrightfront')
neighbours = lambda : {'left': 'lowerleftfront', 'upper': 'upperrightfront', 'back': 'lowerrightback'}
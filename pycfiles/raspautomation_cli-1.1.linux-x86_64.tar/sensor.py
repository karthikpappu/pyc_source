# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/sensor.py
# Compiled at: 2016-05-27 19:16:12
from raspautomation_cli.device import Device

class Sensor(Device):
    api_endpoint = 'sensor'
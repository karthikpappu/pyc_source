# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/test/test_hardware_modules/test_scope.py
# Compiled at: 2017-08-29 09:44:06
import logging
logger = logging.getLogger(name=__name__)
import time, numpy as np
from pyrpl.async_utils import sleep as async_sleep
from qtpy import QtCore, QtWidgets
from pyrpl.test.test_base import TestPyrpl
from pyrpl import APP
from pyrpl.curvedb import CurveDB

class TestScope(TestPyrpl):
    """
    Be carreful to stop the scope at the end of each test!!!
    """

    def test_scope_stopped_at_startup(self):
        """
        This was so hard to detect, I am making a unit test
        """
        assert self.r.scope.running_state == 'stopped'

    def data_changing(self):
        async_sleep(0.1)
        APP.processEvents()
        if self.r.scope.data_avg is not None:
            data = self.r.scope.data_avg[0]
        else:
            data = None
        async_sleep(0.75)
        for i in range(1000):
            APP.processEvents()

        async_sleep(0.1)
        if self.r.scope.data_avg is not None:
            res = self.r.scope.data_avg[0]
        else:
            res = None
        if data is None:
            return res is not None
        else:
            return (data != res)[(~np.isnan(data))].any()

    def test_scope_rolling_mode_and_running_state_update(self):
        """
        makes sure scope rolling_mode and running states are correctly
        setup when something is changed
        """
        self.r.asg1.frequency = 0
        self.r.asg1.trigger_source = 'immediately'
        self.r.scope.setup_attributes = dict(duration=0.5, trigger_source='asg1', trigger_delay=0.0, rolling_mode=True, running_state='running_continuous', input1='in1', ch1_active=True, ch2_active=True)
        self.r.scope.continuous()
        assert self.data_changing()
        self.r.scope.save_state('running_roll')
        self.r.scope.duration = 0.001
        assert not self.data_changing()
        async_sleep(0.5)
        self.r.scope.duration = 0.5
        assert self.data_changing()
        self.r.scope.rolling_mode = False
        self.r.scope.duration = 0.2
        self.r.scope.save_state('running_triggered')
        assert not self.data_changing()
        self.r.asg1.frequency = 100000.0
        assert self.data_changing()
        self.r.scope.stop()
        self.r.scope.save_state('stop')
        assert not self.data_changing()
        self.r.scope.load_state('running_roll')
        assert self.data_changing()
        async_sleep(1)
        assert self.data_changing()
        self.r.scope.stop()
        self.r.scope.load_state('running_triggered')
        assert self.data_changing()
        self.r.scope.load_state('stop')
        assert not self.data_changing()
        self.r.scope.stop()

    def test_setup_rolling_mode(self):
        """
        recalling a state with rolling mode should work.
        """
        self.r.scope.setup_attributes = dict(duration=0.5, trigger_delay=0.0, input1='in1', ch1_active=True, ch2_active=True, rolling_mode=True, running_state='running_continuous')
        assert self.data_changing()
        async_sleep(1)
        assert self.data_changing()
        self.r.scope.stop()

    def test_scope_slave_free(self):
        """
        Make sure the scope returns to rolling mode after being freed
        """
        self.pyrpl.rp.scope.setup(duration=0.5, trigger_delay=0.0, trigger_source='immediately', input1='in1', ch1_active=True, ch2_active=True, rolling_mode=True, running_state='running_continuous')
        with self.pyrpl.scopes.pop('myapplication') as (sco):
            sco.setup(duration=0.5, trigger_delay=0.0, trigger_source='immediately', input1='in1', ch1_active=True, ch2_active=True, rolling_mode=False, running_state='stopped')
            assert not self.data_changing()
            curve = sco.curve()
        assert self.data_changing()
        async_sleep(1)
        assert self.data_changing()
        self.pyrpl.rp.scope.stop()

    def test_no_write_in_config(self):
        """
        Make sure the scope isn't continuously writing to config file,
        even in running mode.
        """
        self.pyrpl.rp.scope.stop()
        async_sleep(1.0)
        old = self.pyrpl.c._save_counter
        async_sleep(1.0)
        new = self.pyrpl.c._save_counter
        assert old == new, (old, new, 'scope is not the reason')
        for rolling_mode in (True, False):
            self.pyrpl.rp.scope.setup(duration=0.005, trigger_delay=0.0, input1='in1', ch1_active=True, ch2_active=True, rolling_mode=True, trace_average=1, running_state='running_continuous')
            old = self.pyrpl.c._save_counter
            async_sleep(1.0)
            APP.processEvents()
            new = self.pyrpl.c._save_counter
            self.pyrpl.rp.scope.stop()
            assert old == new, (old, new, 'scope is the problem', rolling_mode)

    def test_save_curve_old(self):
        self.r.scope.setup(duration=0.01, trigger_source='immediately', trigger_delay=0.0, rolling_mode=True, input1='in1', ch1_active=True, ch2_active=True)
        self.r.scope.single()
        time.sleep(0.1)
        APP.processEvents()
        curve1, curve2 = self.r.scope.save_curve()
        attr = self.r.scope.setup_attributes
        for curve in (curve1, curve2):
            intersect = set(curve.params.keys()) & set(attr)
            assert len(intersect) >= 5
            p1 = dict((k, curve.params[k]) for k in intersect)
            p2 = dict((k, attr[k]) for k in intersect)
            assert p1 == p2

        self.curves += [curve1, curve2]

    def test_save_curve(self):
        self.pyrpl.rp.scope.stop()
        self.pyrpl.rp.scope.setup(duration=0.005, trigger_delay=0.0, input1='in1', ch1_active=True, ch2_active=True, rolling_mode=True, trace_average=1, running_state='stopped')
        self.pyrpl.rp.scope.single()
        curves = self.pyrpl.rp.scope.save_curve()
        for i in range(2):
            for j in range(2):
                assert len(curves[i].data[j]) == self.pyrpl.rp.scope.data_length

        self.curves += curves
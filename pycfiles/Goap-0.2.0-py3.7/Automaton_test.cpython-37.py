# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/Automaton_test.py
# Compiled at: 2019-07-05 11:36:04
# Size of source mod 2**32: 3289 bytes
from os import path
import unittest, subprocess
from pprint import PrettyPrinter
from Goap.Action import Actions
from Goap.Sensor import Sensors
import Goap.Automaton as Automaton

class AutomatonTest(unittest.TestCase):

    @staticmethod
    def __reset_environment():
        if path.isdir('/tmp/goap_tmp'):
            subprocess.call(['rm', '-rf', '/tmp/goap_tmp'])

    def __print(self):
        self.print.pprint('Acknowledge world: {}, Action Plan: {}, Result: {}'.format(self.automaton.world_state, self.automaton.action_plan, self.automaton.actions_response))

    def setUp(self):
        self.print = PrettyPrinter(indent=4)
        self.goal = {'tmp_dir_state':'exist', 
         'tmp_dir_content':'token_found'}
        self.actions = Actions()
        self.sensors = Sensors()
        self.sensors.add(name='SenseTmpDirState',
          shell='if [ -d "/tmp/goap_tmp" ]; then echo -n "exist"; else echo -n "not_exist"; fi',
          binding='tmp_dir_state')
        self.sensors.add(name='SenseTmpDirContent',
          shell='[ -f /tmp/goap_tmp/.token ] && echo -n "token_found" || echo -n "token_not_found"',
          binding='tmp_dir_content')
        self.actions.add(name='CreateTmpDir',
          pre_conditions={'tmp_dir_state':'not_exist', 
         'tmp_dir_content':'token_not_found'},
          effects={'tmp_dir_state':'exist', 
         'tmp_dir_content':'token_not_found'},
          shell='mkdir -p /tmp/goap_tmp')
        self.actions.add(name='CreateToken',
          pre_conditions={'tmp_dir_state':'exist', 
         'tmp_dir_content':'token_not_found'},
          effects={'tmp_dir_state':'exist', 
         'tmp_dir_content':'token_found'},
          shell='touch /tmp/goap_tmp/.token')
        world_state_matrix = {'tmp_dir_state':'Unknown', 
         'tmp_dir_content':'Unknown'}
        self.automaton = Automaton(name='directory_watcher',
          actions=(self.actions),
          sensors=(self.sensors),
          world_state=world_state_matrix)

    def test_sensing(self):
        self._AutomatonTest__reset_environment()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        assert self.automaton.world_state == {'tmp_dir_state':'not_exist',  'tmp_dir_content':'token_not_found'}

    def test_planning(self):
        create_tmp_dir = self.actions.get('CreateTmpDir')
        create_token = self.actions.get('CreateToken')
        self._AutomatonTest__reset_environment()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        self.automaton.plan()
        action_plan = [action[2]['object'] for action in self.automaton.action_plan]
        assert action_plan == [create_tmp_dir, create_token]

    def test_acting(self):
        self._AutomatonTest__reset_environment()
        self.automaton.input_goal(self.goal)
        self.automaton.sense()
        self.automaton.plan()
        self.automaton.act()
        if not (path.isdir('/tmp/goap_tmp') and path.isfile('/tmp/goap_tmp/.token')):
            raise AssertionError
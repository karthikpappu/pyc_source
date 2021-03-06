# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/sample/maze/maze_performance_watcher.py
# Compiled at: 2016-10-26 09:22:48
from kyoka.callback.base_performance_watcher import BasePerformanceWatcher
from sample.maze.maze_helper import MazeHelper

class MazePerformanceWatcher(BasePerformanceWatcher):

    def define_performance_test_interval(self):
        return 1

    def run_performance_test(self, domain, value_function):
        step_to_goal = MazeHelper.measure_performance(domain, value_function)
        policy = MazeHelper.visualize_policy(domain, value_function)
        return (step_to_goal, policy)

    def define_log_message(self, iteration_count, domain, value_function, test_result):
        step_to_goal, _ = test_result
        return 'Step = %d (nb_iteration=%d)' % (step_to_goal, iteration_count)

    def tearDown(self, domain, value_function):
        msg_prefix = 'Policy which agent learned is like this.\n'
        self.log(msg_prefix + MazeHelper.visualize_policy(domain, value_function))
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mfi/mytools/muteria/muteria/drivers/testgeneration/custom_dev_testcase.py
# Compiled at: 2019-09-19 05:11:43
# Size of source mod 2**32: 4580 bytes
from __future__ import print_function
import os, sys, glob, shutil, logging, muteria.common.matrices as common_matrices, muteria.common.mix as common_mix
from muteria.drivers.testgeneration.base_testcasetool import BaseTestcaseTool
from muteria.drivers.testgeneration.testcases_info import TestcasesInfoObject
ERROR_HANDLER = common_mix.ErrorHandler

class CustomTestcases(BaseTestcaseTool):
    CUSTOM_TEST_TOOLNAME = 'custom_devtests'

    @classmethod
    def installed(cls, custom_binary_dir=None):
        """ Check that the tool is installed
            :return: bool reprenting whether the tool is installed or not 
                    (executable accessible on the path)
                    - True: the tool is installed and works
                    - False: the tool is not installed or do not work
        """
        return True

    def get_testcase_info_object(self):
        tc_info_obj = TestcasesInfoObject()
        dtl = self.code_builds_factory.repository_manager.get_dev_tests_list()
        ERROR_HANDLER.assert_true(dtl is not None, 'invalid dev_test_list', __file__)
        for tc in dtl:
            tc_info_obj.add_test(tc)

        return tc_info_obj

    def execute_testcase(self, testcase, exe_path_map, env_vars, timeout=None):
        return self._in_repo_execute_testcase(testcase=testcase, exe_path_map=exe_path_map, env_vars=env_vars, timeout=timeout)

    def runtests(self, testcases, exe_path_map, env_vars, stop_on_failure=False, per_test_timeout=None, parallel_count=1):
        """ Override runtests
        """
        return self._in_repo_runtests(testcases=testcases, exe_path_map=exe_path_map, env_vars=env_vars, stop_on_failure=stop_on_failure, per_test_timeout=per_test_timeout, parallel_count=parallel_count)

    def _prepare_executable(self, exe_path_map, env_vars):
        """ Make sure we have the right executable ready (if needed)
        """
        pass

    def _restore_default_executable(self, exe_path_map, env_vars):
        """ Restore back the default executable (if needed).
            Useful for test execution that require the executable
            at a specific location.
        """
        pass

    def _execute_a_test(self, testcase, exe_path_map, env_vars, callback_object=None, timeout=None):
        """ Execute a test given that the executables have been set 
            properly
        """
        if timeout is None:
            timeout = self.config.ONE_TEST_EXECUTION_TIMEOUT
        rep_mgr = self.code_builds_factory.repository_manager
        pre, verdict, post = rep_mgr.run_dev_test(dev_test_name=testcase, exe_path_map=exe_path_map, env_vars=env_vars, timeout=timeout, callback_object=callback_object)
        ERROR_HANDLER.assert_true(pre == common_mix.GlobalConstants.COMMAND_SUCCESS, 'before command failed', __file__)
        ERROR_HANDLER.assert_true(post != common_mix.GlobalConstants.COMMAND_FAILURE, 'after command failed', __file__)
        return verdict

    def _do_generate_tests(self, exe_path_map, outputdir, code_builds_factory, max_time=None):
        pass
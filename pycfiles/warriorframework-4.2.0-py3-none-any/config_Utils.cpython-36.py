# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/Framework/Utils/config_Utils.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 2455 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from warrior.WarriorCore.Classes import war_print_class
from warrior.Framework.Utils.print_Utils import print_info, print_error
console_logfile = None
junit_resultfile = None
resultfile = None
datafile = None
logsdir = None
filename = None
data_repository = None
logfile = None
par_data_repository = {}
redirect_print = war_print_class.RedirectPrint(console_logfile)
tc_path = None

def debug_file(console_filepath):
    """
    Set debug file
    """
    global console_logfile
    try:
        console_logfile = open(console_filepath, 'a')
        redirect_print.get_file(console_logfile)
    except Exception as e:
        print_error('unexpected error {}'.format(e))
        console_logfile = None


def junit_file(junit_filepath):
    """
    Set junitfile
    """
    global junit_resultfile
    junit_resultfile = junit_filepath


def set_resultfile(filepath):
    """
    Set resultfile
    """
    global resultfile
    resultfile = filepath


def set_datafile(filepath):
    """
    Set datafile
    """
    global datafile
    datafile = filepath


def set_logsdir(filepath):
    """
    Set logsdir
    """
    global logsdir
    logsdir = filepath


def set_logfile(filepath):
    """
    Set logfile
    """
    global logfile
    logfile = filepath


def set_filename(name):
    """
    Set filename
    """
    global filename
    filename = name


def set_datarepository(repository):
    """
    Set datarepository
    """
    global data_repository
    data_repository = repository


def set_data_repository_for_parallel(repository):
    """
    Set data repository for parallel
    """
    global par_data_repository
    par_data_repository.update(repository)
    print_info(par_data_repository)


def set_testcase_path(testcase_file_path):
    """
    Set testcase path
    """
    global tc_path
    tc_path = testcase_file_path
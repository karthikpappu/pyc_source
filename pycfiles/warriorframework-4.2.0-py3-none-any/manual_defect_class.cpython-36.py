# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/Classes/manual_defect_class.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 4440 bytes
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
import json, os
from warrior.Framework.Utils import file_Utils
from warrior.Framework.Utils.print_Utils import print_error, print_info
from warrior.WarriorCore import defects_driver

class ManualDefectClass(object):
    __doc__ = 'parse files and upload issues to jira'

    def __init__(self, path_type, jiraproj=None):
        """Constructor
        """
        self.path_type = path_type
        self.jiraproj = jiraproj

    @staticmethod
    def check_defect_file(path):
        """Gets the list of defect json files for the testcase execution """
        abs_cur_dir = os.path.abspath(os.curdir)
        value = None
        if path.endswith('.json'):
            defect_file = file_Utils.getAbsPath(path, abs_cur_dir)
            if file_Utils.fileExists(defect_file):
                print_info('Defect file location is :{0}'.format(defect_file))
                value = defect_file
            else:
                print_error('File Does not exist in provided location: {0} relative to cwd'.format(path))
        return value

    @staticmethod
    def defects_json_parser(filepath):
        """check if the json file has all the information needed"""
        data_repository = {}
        full_list = json.load(open(filepath))
        for dictionary in full_list:
            key = list(dictionary.keys())[0]
            item = list(dictionary.values())[0]
            if key == 'testcase_filepath' or key == 'defectsdir' or key == 'logsdir' or key == 'resultfile':
                data_repository['wt_' + key] = item

        if len(data_repository) < 4:
            print_error('not a valid json file')
            return
        else:
            return data_repository

    def manual_defects(self, paths):
        """parse file list and create jira issue for each failures"""
        print_info('manual-create defects')
        if self.path_type == 'dir':
            defects_json_list = []
            i = 0
            abs_cur_dir = os.path.abspath(os.curdir)
            for path in paths:
                i += 1
                print_info('Directory {0}: {1}'.format(i, path))
                defect_dir = file_Utils.getAbsPath(path, abs_cur_dir)
                if file_Utils.dirExists(defect_dir):
                    for j_file in os.listdir(path):
                        j_file = os.path.join(path, j_file)
                        if j_file is not None:
                            check_file = self.check_defect_file(j_file)
                            if check_file is not None:
                                defects_json_list.append(check_file)

                else:
                    print_error('Directory does not exist in provided path {0} relative to cwd'.format(path))
                print_info('\n')

        else:
            defects_json_list = []
            i = 0
            for path in paths:
                i += 1
                print_info('File {0}: {1}'.format(i, path))
                check_file = self.check_defect_file(path)
                if check_file is not None:
                    defects_json_list.append(check_file)
                print_info('\n')

        if len(defects_json_list) == 0:
            print_info('No defect json files found')
            exit(0)
        elif len(defects_json_list) > 0:
            for j_file in defects_json_list:
                data_repository = self.defects_json_parser(j_file)
                if data_repository is not None:
                    data_repository['jiraproj'] = self.jiraproj
                    defect_obj = defects_driver.DefectsDriver(data_repository)
                    if defect_obj.connect_warrior_jira() is True:
                        defect_obj.create_jira_issues([j_file])
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/cloud-harness/gbdx_cloud_harness/services/task_service.py
# Compiled at: 2016-10-31 16:11:18
import json
from gbdx_auth import gbdx_auth

class TaskRegistryError(Exception):
    pass


class TaskService(object):

    def __init__(self, auth=None):
        self.session = auth if auth is not None else gbdx_auth.get_session()
        self.task_url = 'https://geobigdata.io/workflows/v1/tasks'
        return

    def register_task(self, task_def):
        """
        Register a task for a python dict
        :param task_def: dict defining gbdx task
        """
        r = self.session.post(self.task_url, data=task_def, headers={'Content-Type': 'application/json', 'Accept': 'application/json'})
        task_dict = json.loads(task_def)
        if r.status_code == 200:
            return (r.status_code, 'Task %s registered' % task_dict['name'])
        else:
            return (
             r.status_code, 'Task %s was not registered: %s' % (task_dict['name'], r.text))

    def delete_task(self, task_name):
        """
        Delete a task from the platforms regoistry
        :param task_name: name of the task to delete
        """
        response = self.session.delete('%s/%s' % (self.task_url, task_name))
        if response.status_code == 200:
            return (response.status_code, 'Task %s deleted' % task_name)
        else:
            if response.status_code == 400:
                return (response.status_code, None)
            else:
                return (
                 response.status_code, 'Task %s was not deleted: %s' % (task_name, response.text))

            return
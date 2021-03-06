# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/russell/client/project.py
# Compiled at: 2018-12-27 05:19:41
import json, sys
from russell.manager.auth_config import AuthConfigManager
from russell.client.base import RussellHttpClient
from russell.cli.utils import get_files_in_directory
from russell.log import logger as russell_logger
from russell.client.auth import AuthClient

class ProjectClient(RussellHttpClient):
    """
    Client to interact with projects api
    """

    def __init__(self):
        self.url = '/projects/'
        self.project_api_url = '/{user_name}/project/{project_name}'
        super(ProjectClient, self).__init__()

    def clone(self, project_url_or_id, compression='zip', uncompress=True, delete_after_uncompress=True):
        """
        Download and optionally untar the tar file from the given url
        """
        try:
            project_info = self.get_project_info_by_id(project_url_or_id)
            if not project_info or not isinstance(project_info, dict):
                sys.exit('Project id is illegal or not found')
            else:
                project_permission = int(project_info['permission'])
                access_token = AuthConfigManager.get_access_token()
                if project_permission >= 1 and AuthClient().get_user(access_token.token).uid != project_info.get('owner_id'):
                    russell_logger.info('Project permission denied')
                    return False
                project_name = project_info['name']
                russell_logger.debug(project_name)
                url = self.url + 'clone/' + project_url_or_id
                self.download_compressed(url, compression=compression, uncompress=uncompress, delete_after_uncompress=delete_after_uncompress, dir=project_name)
                return project_info
        except Exception as e:
            russell_logger.error(('Clone ERROR! {}').format(e))
            return False

    def async_request_clone(self, url, api_version=1):
        if api_version == 2:
            task_resp = self.request('GET', url=url, api_version=2)
            if isinstance(task_resp, dict):
                task_id = task_resp.get('task_id')
            else:
                russell_logger.error('Clone task invalid response')
                return
            while True:
                status_resp = self.request('GET', url=url, params={'task_id': task_id}, api_version=2)
                if isinstance(status_resp, dict):
                    state = status_resp.get('state')
                    if state == 'STARTED':
                        yield status_resp.get('status')
                    elif state == 'FAILURE':
                        yield False
                    elif state == 'SUCCESS':
                        yield dict(task_id=task_id)
                else:
                    russell_logger.error('Clone task invalid response')
                    return

    def create(self, user_name, project_name):
        response = None
        try:
            response = self.request(method='PUT', url=self.project_api_url.format(user_name=user_name, project_name=project_name))
        except Exception as e:
            russell_logger.error('Create remote project failed')
            russell_logger.debug(repr(e))

        return response

    def delete(self, id):
        return True

    def get_project_name(self, id):
        project = self.request('GET', url='/anonymous/project/anonymous', params={'id': id})
        if isinstance(project, dict):
            return project.get('name')

    def get_project_info_by_name(self, user_name, project_name):
        project = self.request('GET', url=self.project_api_url.format(user_name=user_name, project_name=project_name))
        return project

    def get_project_info_by_id(self, id):
        project = self.request('GET', url='/anonymous/project/anonymous', params={'id': id})
        return project
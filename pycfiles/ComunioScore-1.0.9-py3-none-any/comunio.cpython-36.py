# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ComunioScore/comunio.py
# Compiled at: 2020-04-27 15:29:14
# Size of source mod 2**32: 10236 bytes
import json, logging, requests

class Comunio:
    """Comunio"""

    def __init__(self):
        self.logger = logging.getLogger('ComunioScore')
        self.logger.info('Create class Comunio')
        self.username = ''
        self.userid = ''
        self.leader = False
        self.user_budget = ''
        self.user_teamvalue = ''
        self.communityid = ''
        self.communityname = ''
        self.userids = list()
        self.placement_and_userids = []
        self.last_matchday = ''
        self.session = requests.Session()
        self.auth_token = None
        self.auth_token_expires = ''
        self.auth_info = None
        self.origin = 'http://www.comunio.de'
        self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/60.0.3112.78 Chrome/60.0.3112.78 Safari/537.36'
        self.accept_encoding = 'gzip, deflate, br'
        self.connection = 'keep-alive'
        self.headers_login = {'Origin':self.origin, 
         'Accept-Encoding':self.accept_encoding, 
         'Accept-Language':'de-DE,en-EN;q=0.9', 
         'User-Agent':self.user_agent, 
         'Content-Type':'application/x-www-form-urlencoded', 
         'Accept':'application/json, text/plain, */*', 
         'Referer':'http://www.comunio.de/home', 
         'Connection':self.connection}
        self.standard_header = {'Origin':self.origin, 
         'Accept-Encoding':self.accept_encoding, 
         'Accept-Language':'de-DE,en-EN;q=0.9', 
         'Accept':'application/json, text/plain, */*', 
         'User-Agent':self.user_agent, 
         'Connection':self.connection}

    def __del__(self):
        """ destructor

        """
        self.session.close()
        self.session.cookies.clear()

    def login(self, username, password):
        """ comunio login with username and password

        :param username: username of account
        :param password: password of account
        :return: bool, if login was successful
        """
        self.logger.info('Login to Comunio with username {}'.format(username))
        login_form = [
         (
          'username', username),
         (
          'password', password)]
        try:
            request_login = self.session.post('https://api.comunio.de/login', headers=(self.headers_login), data=login_form)
        except requests.exceptions.RequestException as e:
            self.logger.error('Comunio login error: {}'.format(e))
            return False

        if request_login.status_code == 400:
            error_data = json.loads(request_login.text)
            self.logger.error(error_data)
            return False
        if not request_login.status_code // 100 == 2:
            error_data = json.loads(request_login.text)
            self.logger.error(error_data)
            return False
        else:
            json_data = json.loads(request_login.text)
            self.auth_token = str(json_data['access_token'])
            self.auth_token_expires = str(json_data['expires_in'])
            self.auth_info = json_data
            if self._Comunio__set_user_and_community_info() != 200:
                self.logger.error('Failed to set user and community attributes')
                raise AttributeError('Failed to set user and community attributes')
            return True

    def __set_user_and_community_info(self):
        """ sets user and community specific attributes

        :return: response code from request
        """
        self.standard_header['Authorization'] = 'Bearer ' + self.auth_token
        self.standard_header['Referer'] = 'http://www.comunio.de/dashboard'
        request_info = requests.get('https://api.comunio.de/', headers=(self.standard_header))
        json_data = json.loads(request_info.text)
        self.username = json_data['user']['name']
        self.userid = json_data['user']['id']
        self.leader = json_data['user']['isLeader']
        self.user_budget = json_data['user']['budget']
        self.user_teamvalue = json_data['user']['teamValue']
        self.communityname = json_data['community']['name']
        self.communityid = json_data['community']['id']
        return request_info.status_code

    def get_auth_info(self):
        """ get the auth infos from login process

        :return: auth_info as json dict
        """
        return self.auth_info

    def get_all_user_ids(self):
        """ get all user ids in community

        :return: list containing all user ids with name as dict()
        """
        self.logger.info('Get all user ids from comunio')
        self.standard_header['Authorization'] = 'Bearer ' + self.auth_token
        params_standings = (('period', 'season'), )
        request_standing = requests.get(('https://api.comunio.de/communities/' + self.communityid + '/standings'), headers=(self.standard_header),
          params=params_standings)
        json_data = json.loads(request_standing.text)
        tempid = ''
        userids = list()
        for id in json_data.get('items'):
            tempid = id

        for id in json_data['items'][tempid]['players']:
            player_dict = dict()
            player_dict['id'] = id['id']
            player_dict['name'] = id['name']
            userids.append(player_dict)

        return userids

    def get_player_standings(self):
        """ get the player standings

        :return: list with dicts of player standings
        """
        self.logger.info('Get all player standings from comunio')
        self.standard_header['Authorization'] = 'Bearer ' + self.auth_token
        self.standard_header['Referer'] = 'http://www.comunio.de/standings/total'
        params_standings = (('period', 'season'), )
        request_standing = requests.get(('https://api.comunio.de/communities/' + self.communityid + '/standings'), headers=(self.standard_header),
          params=params_standings)
        json_data = json.loads(request_standing.text)
        tempid = ''
        for id in json_data.get('items'):
            tempid = id

        return json_data['items'][tempid]['players']

    def set_auth_token(self, auth_token):
        """ sets the auth token

        """
        self.auth_token = auth_token

    def get_auth_token(self):
        """ get auth token

        :return: auth_token as string
        """
        return self.auth_token

    def get_auth_expire_time(self):
        """ get auth token expire time

        :return: string, auth token expire time
        """
        return self.auth_token_expires

    def get_user_id(self):
        """ get user id from logged in user

        :return: userid as string
        """
        return self.userid

    def get_community_id(self):
        """ get community id from logged in user

        :return: communityid as string
        """
        return self.communityid

    def get_community_name(self):
        """ get community name from logged in user

        :return: community name as string
        """
        return self.communityname

    def get_wealth(self, userid):
        """ get wealth from given userid

        :param userid: int number

        :return: wealth as int number
        """
        self.logger.info('Get comunio wealth data from userid {}'.format(userid))
        self.standard_header['Authorization'] = 'Bearer ' + self.auth_token
        request_info = requests.get(('https://api.comunio.de/users/' + str(userid) + '/squad-latest'), headers=(self.standard_header))
        json_data = json.loads(request_info.text)
        wealth = json_data['matchday']['budget']
        if wealth is None:
            return wealth
        else:
            return int(json_data['matchday']['budget'])

    def get_squad(self, userid):
        """ get squad from given userid

        :param userid: int number
        :return: list, containing the squad as dict
        """
        self.logger.info('Get comunio squad data from userid {}'.format(userid))
        self.standard_header['Authorization'] = 'Bearer ' + self.auth_token
        squad_request = requests.get(('https://api.comunio.de/users/' + str(userid) + '/squad'), headers=(self.standard_header))
        json_data = squad_request.json()
        return json_data['items']

    def get_comunio_user_data(self):
        """ get comunio user data -> id, name, squad

        :return: dict with id, name, squad in list
        """
        users = self.get_all_user_ids()
        comunio_user_data = list()
        for user in users:
            user_data = user
            squad = self.get_squad(user['id'])
            squad_list = list()
            for player in squad:
                player_dict = dict()
                player_dict['name'] = player['name']
                player_dict['club'] = player['club']['name']
                player_dict['position'] = player['position']
                player_dict['linedup'] = player['linedup']
                squad_list.append(player_dict)

            user_data.update({'squad': squad_list})
            comunio_user_data.append(user_data)

        return comunio_user_data


if __name__ == '__main__':
    comunio = Comunio()
    if comunio.login(username='', password=''):
        print(comunio.get_auth_token())
        print(comunio.get_squad(userid=13065521))
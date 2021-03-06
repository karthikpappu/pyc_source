# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\procode\login_init\startInit.py
# Compiled at: 2019-09-04 23:26:49
# Size of source mod 2**32: 7120 bytes
"""
author:hexiaoxia
date:2019/09/03
启动POS时一些内存数据获取及设置
"""
from poslocalmodel.pos_sys.pos_global_obj import PosGlobalObj
from poslocalmodel.pos_sys.possystem import PosSystem
from procode.tools.servertime import ServerTime, updatetime
from procode.tools.gethardware import GethardWare
import os, json, time, datetime, threading

class StartInit(object):
    runpath = None

    def __init__(self, runpath):
        self.runpath = runpath

    def setBaseInfo(self):
        apiurl = ''
        datarootpath = ''
        runrootpath = ''
        foldername = ''
        version = ''
        environment = 'development'
        jsonfilepath = ''
        cpu = ''
        code = 0
        cpu = GethardWare().get_cpuidOrSerialNumber()
        self.read_possystem_file()
        if os.path.exists(self.runpath + os.sep + 'install_success.log'):
            environment = 'produce'
            apiurl, datarootpath, foldername, version, jsonfilepath, code = self.read_posconfig_file(self.runpath)
        else:
            datarootpath = self.runpath
            apiurl = PosSystem.serviceapi_url
        PosGlobalObj.RootPath = self.runpath
        PosGlobalObj.DataRootPath = datarootpath
        PosGlobalObj.Host = apiurl.split('//')[1] if len(apiurl.split('//')) >= 2 else ''
        PosGlobalObj.JsonFilePath = jsonfilepath
        PosGlobalObj.EnvironMent = environment
        PosGlobalObj.FolderName = foldername
        PosGlobalObj.PosVersion = version
        PosGlobalObj.Cpuserialnumber = cpu

    def read_posconfig_file(self, runpath):
        """
        读取posconfig.json文件
        :param runpath:
        :return:
        """
        apiurl = ''
        datarootpath = ''
        foldername = ''
        version = ''
        jsonfilepath = ''
        jsonfilepath_list = runpath.split(os.sep)[:-1]
        jsonfilepath = str(os.sep).join(jsonfilepath_list)
        code = 0
        try:
            try:
                with open(jsonfilepath + os.sep + 'posconfig.json', 'r') as (f):
                    temp = json.loads(f.read())
                    version = temp['version']
                    apiurl = temp['serviceurl']
                    runrootpath = temp['foldername']
                    foldername = runrootpath
                    runrootpath_list = runrootpath.split('\\')[:-1]
                    datarootpath = str('\\').join(runrootpath_list)
                    self.runpath = runrootpath + os.sep + 'app'
                    f.close()
                if os.path.isdir(jsonfilepath + os.sep + 'app' + os.sep + 'externalfile') and os.path.exists(jsonfilepath + os.sep + 'app' + os.sep + 'externalfile' + os.sep + 'update.json'):
                    with open(jsonfilepath + os.sep + 'app' + os.sep + 'externalfile' + os.sep + 'update.json', 'r') as (f):
                        temp1 = json.loads(f.read())
                        if temp1:
                            apiurl = temp1['serviceurl']
                        f.close()
                    with open(jsonfilepath + os.sep + 'posconfig.json', 'r') as (f):
                        temp2 = json.loads(f.read())
                        f.close()
                    if temp2:
                        temp2['serviceurl'] = apiurl
                        json_str = json.dumps(temp2, indent=4)
                        try:
                            with open(jsonfilepath + os.sep + 'posconfig.json', 'w') as (f1):
                                f1.write(json_str)
                            with open(jsonfilepath + os.sep + 'app' + os.sep + 'externalfile' + os.sep + 'update.json', 'w') as (f2):
                                f2.write('')
                            os.remove(jsonfilepath + os.sep + 'app' + os.sep + 'externalfile' + os.sep + 'update.json')
                        except Exception as e:
                            print(e.__str__())

            except Exception as e:
                code = -1

        finally:
            return (
             apiurl, datarootpath, foldername, version, jsonfilepath, code)

    def read_possystem_file(self):
        """
        读取系统级配置文件possystem.json
        :return:
        """
        temp = {}
        code = 0
        try:
            try:
                with open(self.runpath + os.sep + 'possystem.json', 'r') as (f):
                    temp = json.loads(f.read())
                    f.close()
                if temp:
                    PosSystem.setAllAttr(temp)
                else:
                    code = -1
            except Exception as e:
                code = -1

        finally:
            return code

    @classmethod
    def checkHealth(cls):
        """
        启动pos时检测服务端接口网络是否通畅
        :return:
        """
        from poslocalbll.src.login_init import OnLineClass
        args = args = {'params': {}, 'apiname': cls.checkHealth.__name__}
        res = OnLineClass.checkHealth(**args)
        if res == None or res == '':
            PosGlobalObj.Serverapi = -1
            return -1
        if res.status_code != 200:
            PosGlobalObj.Serverapi = -1
            return -1
        if res.json:
            cls.startLocalClock(res)
            if res.json.get('code') == 0:
                PosGlobalObj.Serverapi = 0
                return int(res.elapsed.total_seconds() * 1000)
        PosGlobalObj.Serverapi = -1
        return -1

    @classmethod
    def startLocalClock(cls, res):
        """
        创建本地时钟，网络通畅那么使用的是服务端时间
        :param res:
        :return:
        """
        try:
            set_cookie_list = str(res._headers._store.get('set-cookie')[1]).split(';')
            current_server_time = int(str(set_cookie_list[0]).split('|')[(-1)])
            current_server_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(current_server_time))
            ServerTime.server_time = datetime.datetime.strptime(current_server_time, '%Y-%m-%d %H:%M:%S')
            if not ServerTime.is_request_system_flug:
                ServerTime.is_request_system_flug = True
                threading.Thread(target=updatetime, name='servertime').start()
        except Exception as e:
            pass


class_dict = {key:var for key, var in locals().items() if isinstance(var, type) if isinstance(var, type)}
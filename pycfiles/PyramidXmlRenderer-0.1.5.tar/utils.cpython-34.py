# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Python34\lib\site-packages\pyramid_ueditor\pyramid_ueditor\utils.py
# Compiled at: 2015-06-05 02:42:47
# Size of source mod 2**32: 8370 bytes
__all__ = []
__author__ = 'lfblogs (email:13701242710@163.com)'
__version__ = '1.0.1'
import os, re, base64, random, urllib, datetime
from werkzeug.utils import secure_filename

class Uploader:
    stateError = {'ERROR_CREATE_DIR': '存储目录无权限,创建失败', 
     'ERROR_DIR_WRITE_NOT_ENABLE': '存储目录无写入权限', 
     'ERROR_DEAD_LINK': '链接不可用', 
     'ERROR_FILE_SAVE': '文件保存时出错', 
     'ERROR_FILE_NOT_FOUND': '未找到上传文件', 
     'ERROR_HTTP_CONTENTTYPE': '链接类型不正确', 
     'ERROR_HTTP_LINK': '链接无效,只允许HTTP链接', 
     'ERROR_SIZE_EXCEED': '文件大小超出限制', 
     'ERROR_TEMP_FILE': '临时文件错误', 
     'ERROR_TEMP_FILE_NOT_FOUNT': '未找到临时文件', 
     'ERROR_TYPE_NOT_ALLOWED': '文件类型不允许', 
     'ERROR_UNKNOWN': '未知错误', 
     'ERROR_WRITE_CONTENT': '写入文件内容错误'}
    stateMap = [
     'SUCCESS',
     '文件大小超出 upload_max_filesize 限制',
     '文件大小超出 MAX_FILE_SIZE 限制',
     '文件未被完整上传',
     '没有文件被上传',
     '上传文件为空']

    def __init__(self, file_obj, settings, static_root, _type=None):
        """
        :param file_obj: Image URL, FileStorage or Base64Encode
        :param settings: Config
        :param static_root: File save content
        :param _type: upload type,base64,remote
        """
        self.file_obj = file_obj
        self.settings = settings
        self.static_root = static_root
        self._type = _type
        if _type == 'remote':
            self.saveRemote()
        else:
            if _type == 'base64':
                self.upBase64()
            else:
                self.upFile()

    def saveRemote(self):
        _file = urllib.urlopen(self.file_obj)
        self.oriName = self.settings['oriName']
        self.FileSize = 0
        self.FileType = self.getFileExt()
        self.FullName = self.getFullName()
        self.FilePath = self.getFilePath()
        if not self.checkSize():
            self.statInfo = self.getStateError('ERROR_SIZE_EXCEED')
            return
        dirname = os.path.dirname(self.FilePath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.getStateError('ERROR_CREATE_DIR')
                return

        if not os.access(dirname, os.W_OK):
            self.statInfo = self.getStateError('ERROR_DIR_WRITE_NOT_ENABLE')
        try:
            with open(self.FilePath, 'wb') as (fp):
                fp.write(_file.read())
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.getStateError('ERROR_FILE_SAVE')
            return

    def upBase64(self):
        image = base64.b64decode(self.file_obj)
        self.oriName = self.settings['oriName']
        self.FileSize = len(image)
        self.FileType = self.getFileExt()
        self.FullName = self.getFullName()
        self.FilePath = self.getFilePath()
        if not self.checkSize():
            self.stateInfo = self.getStateError('ERROR_SIZE_EXCEED')
            return
        dirname = os.path.dirname(self.FilePath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.getStateError('ERROR_CREATE_DIR')
                return

        if not os.access(dirname, os.W_OK):
            self.stateInfo = self.getStateError('ERROR_DIR_WRITE_NOT_ENABLE')
            return
        try:
            with open(self.FilePath, 'wb') as (fp):
                fp.write(image)
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.getStateError('ERROR_FILE_SAVE')
            return

    def upFile(self):
        self.oriName = self.file_obj.filename
        self.FileSize = len(self.file_obj.value)
        self.FileType = self.getFileExt()
        self.FullName = self.getFullName()
        self.FilePath = self.getFilePath()
        if not self.checkSize():
            self.stateInfo = self.getStateError('ERROR_SIZE_EXCEED')
            return
        if not self.checkType():
            self.stateInfo = self.getStateError('ERROR_TYPE_NOT_ALLOWED')
            return
        dirname = os.path.dirname(self.FilePath)
        if not os.path.exists(dirname):
            try:
                os.makedirs(dirname)
            except:
                self.stateInfo = self.getStateError('ERROR_CREATE_DIR')
                return

        if not os.access(dirname, os.W_OK):
            self.stateInfo = self.getStateError('ERROR_DIR_WRITE_NOT_ENABLE')
            return
        try:
            with open(self.FilePath, 'wb') as (fp):
                fp.write(self.file_obj.value)
            self.stateInfo = self.stateMap[0]
        except:
            self.stateInfo = self.getStateError('ERROR_FILE_SAVE')
            return

    def getStateError(self, error):
        return self.stateError.get(error, 'ERROR_UNKNOWN')

    def checkSize(self):
        return self.FileSize <= self.settings['maxSize']

    def checkType(self):
        return self.FileType.lower() in self.settings['allowFiles']

    def getFilePath(self):
        rootPath = self.static_root
        filePath = ''
        for path in self.FullName.split('/'):
            filePath = os.path.join(filePath, path)

        return os.path.join(rootPath, filePath)

    def getFileExt(self):
        return '.%s' % self.oriName.split('.')[(-1)].lower()

    def getFullName(self):
        now = datetime.datetime.now()
        _time = now.strftime('%H%M%S')
        _format = self.settings['pathFormat']
        _format = _format.replace('{yyyy}', str(now.year))
        _format = _format.replace('{mm}', str(now.month))
        _format = _format.replace('{dd}', str(now.day))
        _format = _format.replace('{hh}', str(now.hour))
        _format = _format.replace('{ii}', str(now.minute))
        _format = _format.replace('{ss}', str(now.second))
        _format = _format.replace('{ss}', str(now.second))
        _format = _format.replace('{time}', _time)
        _format = _format.replace('{filename}', secure_filename(self.oriName))
        rand_re = '\\{rand\\:(\\d*)\\}'
        _pattern = re.compile(rand_re, flags=re.I)
        _match = _pattern.search(_format)
        if _match is not None:
            n = int(_match.groups()[0])
            _format = _pattern.sub(str(random.randrange(10 ** (n - 1), 10 ** n)), _format)
        _ext = self.getFileExt()
        return '%s%s' % (_format, _ext)

    def getFileInfo(self):
        filename = self.FullName
        return {'state': self.stateInfo, 
         'url': filename, 
         'title': self.oriName, 
         'original': self.oriName, 
         'type': self.FileType, 
         'size': self.FileSize}
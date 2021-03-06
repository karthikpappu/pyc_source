# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/backend_file.py
# Compiled at: 2015-06-01 10:45:56
import os, glob
from mimetypes import MimeTypes
from django.conf import settings as conf
from utils import *

class File(object):
    path = ''
    mime_type = ''

    def __init__(self, path):
        self.path = path
        try:
            mime = MimeTypes()
            m = str(mime.guess_type(self.path)[0])
        except:
            m = ''

        self.mime_type = m


def name():
    return 'file'


def set_dirs(source):
    source = source
    photo_target = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
    video_target = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'videos')
    if os.path.exists(photo_target) is False:
        mkdir_p(photo_target)
    if os.path.exists(video_target) is False:
        mkdir_p(video_target)
    return (
     source, photo_target, video_target)


def get_contents(srcdir):
    types = (
     os.path.join(srcdir, '*'),)
    bucket = []
    for files in types:
        bucket.extend(glob.glob(files))

    file2 = []
    for file in bucket:
        file2.append(File(file))

    return (
     False, file2)


def filepath(file):
    return file.path


def is_image(file):
    if file.mime_type == 'image/jpeg':
        return True
    return False


def is_video(file):
    if file.mime_type == 'video/mp4' or file.mime_type == 'video/3gpp' or file.mime_type == 'video/quicktime' or file.mime_type == 'video/x-msvideo':
        return True
    return False


def download(client, file, nombre_imagen, srcdir, destdir):
    f = open(file.path, 'r')
    img = os.path.join(destdir, nombre_imagen)
    out = open(img, 'wb')
    out.write(f.read())
    out.close()
    return img
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/uploadr/uploadr.py
# Compiled at: 2010-10-15 17:52:04
import os.path, argparse, flickrapi
from configobj import ConfigObj
import os, random

class FileStorage:

    def storeSetNo(self, setNoFile, no):
        with open(setNoFile, 'w') as (f):
            f.write(str(no))

    def storeFileMapping(self, mappingFile, filename, photoid):
        with open(mappingFile, 'a') as (f):
            f.write(filename + '=' + str(photoid) + '\n')


class TestStorage:

    def storeSetNo(self, setNoFile, no):
        print 'storing set number ' + str(no)

    def storeFileMapping(self, mappingFile, filename, photoid):
        print 'storing ' + filename + ' map to ' + str(photoid)


class FlickrAPI:

    def __init__(self):
        self.api_key = '35c1f76f44831da16371329162eae7b4'
        self.api_secret = '70a10e2cd57e534f'
        self.flickr = flickrapi.FlickrAPI(self.api_key, self.api_secret)
        (token, frob) = self.flickr.get_token_part_one(perms='write')
        if not token:
            raw_input('Press ENTER after you authorized this program')
        self.flickr.get_token_part_two((token, frob))

    def createSet(self, name, pid):
        res = self.flickr.photosets_create(title=name, primary_photo_id=pid)
        return res.find('photoset').get('id')

    def uploadFile(self, filename):
        print 'upload ' + filename
        res = self.flickr.upload(filename, callback=self.progress, is_public=0)
        return res.findtext('photoid')

    def assignToSet(self, photoid, setid):
        self.flickr.photosets_addPhoto(photoset_id=setid, photo_id=photoid)

    def progress(self, progress, done):
        if done:
            print 'Done uploading'
        else:
            print 'At %s%%' % progress


class TestAPI:

    def createSet(self, name, pid):
        print 'createSet'
        return random.randint(0, 10000000)

    def uploadFile(self, filename):
        print 'upload ' + filename
        return random.randint(0, 10000000)

    def assignToSet(self, photoid, setid):
        print 'assign ' + str(photoid) + ' to ' + str(setid)


class Controller:

    def __init__(self, args):
        if args.simulate:
            self.api = TestAPI()
            self.storage = TestStorage()
        else:
            self.api = FlickrAPI()
            self.storage = FileStorage()

    def readSetNo(self, file):
        if os.path.exists(file):
            with open(file) as (f):
                return f.read()
        else:
            return
        return

    def readPhotoMapping(self, file):
        if os.path.exists(file):
            return ConfigObj(file)
        else:
            return {}

    def fileNameFilter(self, name):
        return name.rfind('jpg') > 0

    def handleDir(self, root, files):
        files = filter(self.fileNameFilter, files)
        if len(files) == 0:
            return
        else:
            print '*******PROCESSING DIRECTORY ' + root
            setFileName = os.path.join(root, '.flickr.set')
            setNo = self.readSetNo(setFileName)
            photosFile = os.path.join(root, '.flickr.photos')
            photoMapping = self.readPhotoMapping(photosFile)
            print photoMapping
            print setNo
            createSet = False
            if setNo == None:
                createSet = True
            else:
                print 'set already created with id ' + setNo
            for f in files:
                if f in photoMapping:
                    print 'photo ' + f + ' is already uploaded'
                else:
                    no = self.api.uploadFile(os.path.join(root, f))
                    self.storage.storeFileMapping(photosFile, f, no)
                    if createSet:
                        (d, f) = os.path.split(root)
                        setNo = self.api.createSet(f, no)
                        self.storage.storeSetNo(setFileName, setNo)
                        createSet = False
                    else:
                        self.api.assignToSet(no, setNo)

            return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload photos to flickr.')
    parser.add_argument('dir', metavar='dir', type=str, help='directory to upload')
    parser.add_argument('-s', dest='simulate', action='store_true', default=False, help="Don't do anything jut simulate and log to the output")
    args = parser.parse_args()
    c = Controller(args)
    for (root, dirs, files) in os.walk(args.dir):
        c.handleDir(root, files)
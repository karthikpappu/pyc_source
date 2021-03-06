# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/moxie/music.py
# Compiled at: 2008-12-19 04:33:52
import glob, os, os.path, mutagen, mutagen.easyid3, mutagen.id3

class TrackList(dict):
    """A dictionary with keys as MP3 files and values as TrackInfo instances."""
    HEADER = 'README'

    def __init__(self, directory):
        if not os.path.isdir(directory):
            raise IOError('%s not a directory' % directory)
        self.directory = directory
        try:
            header = [ line.strip() for line in file(os.path.join(directory, self.HEADER)).readlines()
                     ]
        except IOError:
            self.title = 'A Moxie Mixtape!'
            self.subtitle = 'Make a README'
        else:
            self.title = header[0]
            self.subtitle = ('\n').join(header[1:])

        for fn in glob.glob(os.path.join(directory, '*.mp3')):
            self[os.path.basename(fn)] = TrackInfo(fn)


class TrackInfo:
    """Metadata for audio files."""

    def __init__(self, filename):
        try:
            self._load(filename)
        except mutagen.id3.error:
            self.album = 'No Album'
            self.artist = 'No Artist'
            self.duration = '?:??'
            self.length = 0
            self.title = 'No Title'
            self.size = 0

    def _load(self, filename):
        short_tags = full_tags = mutagen.File(filename)
        if isinstance(full_tags, mutagen.mp3.MP3):
            short_tags = mutagen.easyid3.EasyID3(filename)
        self.album = short_tags.get('album', ['No Album'])[0]
        self.artist = short_tags.get('artist', ['No Artist'])[0]
        self.duration = '%u:%.2d' % (full_tags.info.length / 60, full_tags.info.length % 60)
        self.length = full_tags.info.length
        self.title = short_tags.get('title', ['No Title'])[0]
        self.size = os.stat(filename).st_size
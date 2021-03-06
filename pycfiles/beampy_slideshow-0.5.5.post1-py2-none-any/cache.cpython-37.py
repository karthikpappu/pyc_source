# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hugo/developpement/python/beampy_git/beampy/cache.py
# Compiled at: 2019-05-17 13:59:39
# Size of source mod 2**32: 9993 bytes
"""
Part of beampy project

Manage cache system for slides
"""
import os, sys
try:
    import cPickle as pkl
except:
    import pickle as pkl

import gzip, copy, hashlib, tempfile, glob, logging
_log = logging.getLogger(__name__)

class cache_slides:

    def __init__(self, cache_dir, document):
        """
            Create a cache_slides object to store cache in the given cache folder
        """
        self.folder = cache_dir
        self.version = document.__version__
        self.global_store = document._global_store
        self.data = {}
        self.data_file = 'data.pklz'
        if os.path.isdir(self.folder):
            if os.path.exists(self.folder + '/' + self.data_file):
                with gzip.open(self.folder + '/' + self.data_file, 'rb') as (f):
                    self.data = pkl.load(f)
        else:
            os.mkdir(self.folder)
        if 'version' not in self.data or self.data['version'] != self.version:
            print('Cache file from an other beampy version!')
            self.data = {}
            self.remove_files()
        else:
            if 'optimize' not in self.data or self.data['optimize'] != document._optimize_svg:
                print('Reset cache du to optimize')
                self.data = {}
                self.remove_files()
            else:
                if 'glyphs' in self.data:
                    document._global_store['glyphs'] = self.data['glyphs']
                self.data['version'] = self.version
                self.data['optimize'] = document._optimize_svg

    def remove_files(self):
        for f in glob.glob(self.folder + '/*.pklz'):
            os.remove(f)

    def clear(self):
        if os.path.isdir(self.folder):
            os.removedirs(self.folder)
        self.data = {}

    def add_to_cache(self, slide, bp_module):
        """
        Add the element of a given slide to the cache data

        slide: str of slide id, exemple: "slide_1"

        bp_module: neampy_module instance
        """
        if bp_module.type not in ('group', ):
            if bp_module.rendered:
                elemid = create_element_id(bp_module, use_args=False, add_slide=False, slide_position=False)
                if elemid is not None:
                    self.data[elemid] = {}
                    self.data[elemid]['width'] = bp_module.positionner.width.value
                    self.data[elemid]['height'] = bp_module.positionner.height.value
                    if bp_module.svgout is not None:
                        svgoutname = tempfile.mktemp(prefix='svgout_', dir='')
                        self.data[elemid]['svgout'] = svgoutname
                        self.write_file_cache(svgoutname, bp_module.svgout)
                    if bp_module.htmlout is not None:
                        htmloutname = tempfile.mktemp(prefix='htmlout_', dir='')
                        self.data[elemid]['htmlout'] = htmloutname
                        self.write_file_cache(htmloutname, bp_module.htmlout)
                    if bp_module.jsout is not None:
                        jsoutname = tempfile.mktemp(prefix='jsout_', dir='')
                        self.data[elemid]['jsout'] = jsoutname
                        self.write_file_cache(jsoutname, bp_module.jsout)
                    try:
                        self.data[elemid]['file_id'] = os.path.getmtime(bp_module.content)
                    except:
                        pass

    def add_file(self, filename, content):
        """
        Function to add to the cache a file with it's content. It used to
        store required javascript libraries for instance.
        """
        file_id = hash(filename)
        self.data[file_id] = {'filename': filename}
        self.write_file_cache(filename, content)

    def get_cached_file(self, filename):
        """
        Try to get a given filename from cache 
        """
        file_id = hash(filename)
        if file_id in self.data:
            output_content = self.read_file_cache(filename)
        else:
            print('File %s is not cached' % filename)
            output_content = ''
        return output_content

    def is_file_cached(self, filename):
        """
        Check if a file with a given filename is in cache directory
        """
        out = False
        file_id = hash(filename)
        if file_id in self.data:
            out = True
        return out

    def is_cached(self, slide, bp_module):
        """
            Function to check if the given element is in the cache or not
        """
        out = False
        if bp_module.name not in ('group', ):
            elemid = create_element_id(bp_module, use_args=False, add_slide=False, slide_position=False)
            if elemid is not None:
                if elemid in self.data:
                    cacheelem = self.data[elemid]
                    out = True
                    if 'file_id' in cacheelem:
                        try:
                            curtime = os.path.getmtime(bp_module.content)
                        except:
                            curtime = None

                        if curtime != cacheelem['file_id']:
                            out = False
                        else:
                            out = True
                    if out:
                        for key in ('svgout', 'jsout', 'htmlout'):
                            if key in cacheelem:
                                content = self.read_file_cache(cacheelem[key])
                                setattr(bp_module, key, content)

                        bp_module.update_size(cacheelem['width'], cacheelem['height'])
        return out

    def write_cache(self):
        """
            Export cache data to a pickle file
        """
        if 'glyphs' in self.global_store:
            self.data['glyphs'] = self.global_store['glyphs']
        with gzip.open(self.folder + '/' + self.data_file, 'wb') as (f):
            pkl.dump((self.data), f, protocol=2)

    def write_file_cache(self, filename, content):
        with gzip.open(self.folder + '/' + filename + '.pklz', 'wb') as (f):
            try:
                f.write(content.encode('utf-8'))
            except Exception as e:
                try:
                    f.write(content)
                finally:
                    e = None
                    del e

    def read_file_cache(self, filename):
        output = None
        with gzip.open(self.folder + '/' + filename + '.pklz', 'rb') as (f):
            try:
                output = f.read().decode('utf-8')
            except Exception as e:
                try:
                    output = f.read()
                finally:
                    e = None
                    del e

        return output


def create_element_id(bp_mod, use_args=True, use_render=True, use_content=True, add_slide=True, slide_position=True, use_size=False):
    import beampy.document as document
    ct_to_hash = ''
    _log.debug('Create id for %s on slide %s' % (str(bp_mod.name), bp_mod.slide_id))
    if add_slide:
        ct_to_hash += bp_mod.slide_id
    if use_args:
        if hasattr(bp_mod, 'args'):
            ct_to_hash += ''.join(['%s:%s' % (k, v) for k, v in bp_mod.args.items()])
    if use_render:
        if bp_mod.name is not None:
            ct_to_hash += bp_mod.name
    if use_content:
        if bp_mod.content is not None:
            ct_to_hash += str(bp_mod.content)
    if use_size:
        if 'height' in bp_mod.args:
            h = bp_mod.args['height']
        else:
            h = 'None'
        if 'width' in bp_mod.args:
            w = bp_mod.args['width']
        else:
            w = 'None'
        ct_to_hash += '(%s,%s)' % (str(w), str(h))
    if slide_position:
        ct_to_hash += str(len(document._slides[bp_mod.slide_id].element_keys))
    if bp_mod.args_for_cache_id is not None:
        for key in bp_mod.args_for_cache_id:
            try:
                tmp = getattr(bp_mod, key)
                ct_to_hash += str(tmp)
            except:
                print('No parameters %s for cache id for %s' % (key, bp_mod.name))

    outid = None
    if ct_to_hash != '':
        try:
            outid = hashlib.md5(ct_to_hash.encode('utf-8')).hexdigest()
        except:
            outid = hashlib.md5(ct_to_hash).hexdigest()

        if outid in document._slides[bp_mod.slide_id].element_keys:
            print('Id for this element already exist!')
            sys.exit(0)
            outid = None
    return outid
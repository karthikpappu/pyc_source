# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/apps/command/base.py
# Compiled at: 2010-09-24 15:52:30
import fnmatch, json, logging, os, pkg_resources, re, shutil, tempfile, urllib2, urlparse, zipfile, sys, apps.project

class Command(object):
    help = 'Uninteresting command.'
    user_options = []
    option_defaults = {}
    pre_commands = []
    post_commands = []
    btapp_excludes = [
     'libs']

    def __init__(self, vanguard):
        reload(sys)
        sys.setdefaultencoding('utf-8')
        self.vanguard = vanguard
        self.options = self.vanguard.command_options.get(self.__class__.__name__, {})
        for (k, v) in self.option_defaults.iteritems():
            if not self.options.get(k, None):
                self.options[k] = v

        self.project = apps.project.Project(self.options.get('name', '.'))
        self.added = []
        return

    def file_list(self):
        if not os.path.exists(os.path.join(self.project.path, '.ignore')):
            shutil.copy(pkg_resources.resource_filename('apps.data', '.ignore'), os.path.join(self.project.path, '.ignore'))
        ignore = [ os.path.join(self.project.path, x) for x in open(os.path.join(self.project.path, '.ignore')).read().split('\n')
                 ]

        def _filter(fname):
            for pat in ignore:
                if fnmatch.fnmatch(fname, pat):
                    return False

            return True

        file_list = []
        for (p, dirs, files) in os.walk(self.project.path):
            for f in filter(_filter, [ os.path.join(p, x) for x in files ]):
                file_list.append(f)

        return file_list

    def run(self):
        logging.error('This command has not been implemented yet.')

    def update_libs(self, name, url):
        if name not in [ x['name'] for x in self.project.metadata.get('bt:libs', [])
                       ]:
            self.project.metadata['bt:libs'].append({'name': name, 'url': url})
        if not os.path.exists('package.json') or self.project.metadata != json.load(open('package.json')):
            self.write_metadata()

    def write_metadata(self, refresh=True):
        logging.info('\tupdating project metadata')
        if refresh and (not os.path.exists('package.json') or self.project.metadata != json.load(open('package.json'))):
            json.dump(self.project.metadata, open(os.path.join(self.project.path, 'package.json'), 'wb'), indent=4)
        if self.project.metadata.get('bt:package', False):
            return
        keys = [
         'name', 'version'] + filter(lambda x: x[:3] == 'bt:' and x[3:] not in self.btapp_excludes, self.project.metadata.keys())
        try:
            os.makedirs(os.path.join(self.project.path, 'build'))
        except OSError:
            pass

        btapp = open(os.path.join(self.project.path, 'build', 'btapp'), 'wb')
        for i in keys:
            btapp.write('%s:%s\n' % (i.split(':')[(-1)],
             self.project.metadata[i]))

        btapp.close()

    def update_deps(self):
        logging.info('\tupdating project dependencies')
        pkg_dir = os.path.join(self.project.path, 'packages')
        try:
            shutil.rmtree(pkg_dir)
        except OSError:
            pass

        os.makedirs(pkg_dir)
        for pkg in self.project.metadata.get('bt:libs', []):
            self.add(pkg['name'], pkg['url'])

    def add(self, name, url, update=True):
        if name in self.added:
            return
        self.added.append(name)
        handlers = {'.js': self._add_javascript, '.pkg': self._add_pkg}
        url_handlers = {'file': self._get_file}
        fobj = tempfile.NamedTemporaryFile('wb', delete=False)
        fname = fobj.name
        try:
            logging.info('\tfetching %s ...' % (url,))
            protocol = url.split('://', 1)[0]
            handler = url_handlers.get(protocol, self._get_url)
            fobj.write(handler(url))
            fobj.close()
        except urllib2.HTTPError:
            print 'The file at <%s> is missing.' % (url,)
            sys.exit(1)
        except urllib2.URLError, e:
            logging.error(e.reason)
            sys.exit(1)

        ext = os.path.splitext(urlparse.urlsplit(url).path)[(-1)]
        if not handlers.has_key(ext):
            logging.error('ERROR: Unsupported file type: %s' % (ext,))
            sys.exit(1)
        name = handlers[ext](fname, os.path.split(urlparse.urlsplit(url).path)[(-1)])
        os.remove(fname)
        if update:
            self.update_libs(name, url)

    def _get_file(self, url):
        url = url.split('://', 1)[1]
        return open(os.path.realpath(url), 'rb').read()

    def _get_url(self, url):
        return urllib2.urlopen(url).read()

    def _add_javascript(self, source, fname):
        shutil.copy(source, os.path.join(self.project.path, 'packages', fname))
        return os.path.splitext(fname)[0]

    def _add_pkg(self, source, fname):
        pkg = zipfile.ZipFile(source)
        pkg_manifest = json.loads(pkg.read('package.json'))
        pkg_root = os.path.join(self.project.path, 'packages', pkg_manifest['name'])
        tmpdir = tempfile.mkdtemp(dir=os.path.join(self.project.path, 'packages'))
        for finfo in pkg.infolist():
            if re.match('lib/.+', finfo.filename):
                pkg.extract(finfo.filename, tmpdir)

        shutil.rmtree(pkg_root, True)
        shutil.copytree(os.path.join(tmpdir, 'lib'), pkg_root)
        shutil.rmtree(tmpdir)
        pkg.extract('package.json', pkg_root)
        logging.info('\tfetching %s dependencies ...' % (pkg_manifest['name'],))
        for pkg in pkg_manifest.get('bt:libs', []):
            self.add(pkg['name'], pkg['url'], False)

        return pkg_manifest['name']
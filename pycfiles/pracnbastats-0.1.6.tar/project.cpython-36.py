# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /data/code/pracmln/python3/pracmln/utils/project.py
# Compiled at: 2019-02-27 05:10:32
# Size of source mod 2**32: 16482 bytes
import copy
from zipfile import ZipFile, ZIP_DEFLATED
import os, sys
from dnutils import ifnone, logs
import json, collections
from pracmln.utils import locs
logger = logs.getlogger(__name__)

class MLNProject(object):
    """MLNProject"""

    def __init__(self, name=None):
        self._name = name if (name is not None and '.pracmln' in name) else ('{}.pracmln'.format(name or 'unknown'))
        self._mlns = {}
        self.learnconf = PRACMLNConfig()
        self.queryconf = PRACMLNConfig()
        self._emlns = {}
        self._dbs = {}
        self._results = {}
        self._dirty = True
        self.dirty_listeners = []

    @property
    def dirty(self):
        return self._dirty or self.learnconf.dirty or self.queryconf.dirty

    @dirty.setter
    def dirty(self, d):
        self._dirty = d
        for l in self.dirty_listeners:
            l(d)

    def addlistener(self, listener):
        self.dirty_listeners.append(listener)

    @property
    def mlns(self):
        return self._mlns

    @mlns.setter
    def mlns(self, mlns):
        self._mlns = mlns
        self.dirty = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name if (name is not None and '.pracmln' in name) else ('{}.pracmln'.format(name or 'unknown'))
        self.dirty = True

    @property
    def dbs(self):
        return self._dbs

    @dbs.setter
    def dbs(self, dbs):
        self._dbs = dbs
        self.dirty = True

    @property
    def emlns(self):
        return self._emlns

    @emlns.setter
    def emlns(self, emlns):
        self._emlns = emlns
        self.dirty = True

    @property
    def results(self):
        return self._results

    @results.setter
    def results(self, results):
        self._results = results
        self.dirty = True

    def add_mln(self, name, content=''):
        self._mlns[name] = content
        self.dirty = True

    def add_db(self, name, content=''):
        self._dbs[name] = content
        self.dirty = True

    def add_emln(self, name, content=''):
        self._emlns[name] = content
        self.dirty = True

    def add_result(self, name, content=''):
        self._results[name] = content
        self.dirty = True

    def rm_mln(self, name):
        del self._mlns[name]
        self.dirty = True

    def rm_db(self, name):
        del self._dbs[name]
        self.dirty = True

    def rm_emln(self, name):
        del self._emlns[name]
        self.dirty = True

    def rm_result(self, name):
        del self._results[name]
        self.dirty = True

    def copy(self):
        proj_ = copy.deepcopy(self)
        return proj_

    def loadmln(self, config, mln=None):
        if config == 'query':
            config = self.queryconf
        else:
            if config == 'learn':
                config = self.learnconf
        from pracmln.mln.base import parse_mln
        path = self.path if hasattr(self, 'path') else None
        return parse_mln((self.mlns[ifnone(mln, config['mln'])]), projectpath=path, logic=(config['logic']), grammar=(config['grammar']))

    def loaddb(self, mln, config, db=None):
        if db is None:
            if config not in ('query', 'learn'):
                raise Exception('Need a database name or config.')
        if config == 'query':
            config = self.queryconf
        else:
            if config == 'learn':
                config = self.learnconf
        from pracmln.mln.database import parse_db
        path = self.path if hasattr(self, 'path') else None
        return parse_db(mln, (self.dbs[ifnone(db, config['db'])]), ignore_unknown_preds=(config['ignore_unknown_preds']), projectpath=path)

    def save(self, dirpath='.'):
        filename = self.name
        self.path = dirpath
        with open(os.path.join(dirpath, filename), 'wb') as (zf):
            self.tostream(zf)
        self.dirty = False

    @staticmethod
    def open(filepath):
        fullpath = os.path.expanduser(os.path.expandvars(filepath))
        name = os.path.basename(fullpath)
        proj = MLNProject(name)
        proj.path = os.path.dirname(fullpath)
        with ZipFile(fullpath, 'r') as (zf):
            for member in zf.namelist():
                if member == 'learn.conf':
                    tmpconf = eval(zf.open(member).read().decode('utf-8'))
                    proj.learnconf = PRACMLNConfig()
                    proj.learnconf.update(tmpconf)
                elif member == 'query.conf':
                    tmpconf = eval(zf.open(member).read().decode('utf-8'))
                    proj.queryconf = PRACMLNConfig()
                    proj.queryconf.update(tmpconf)
                else:
                    path, f = os.path.split(member)
                    if path == 'mlns':
                        proj._mlns[f] = zf.open(member).read().decode('utf-8')
                    else:
                        if path == 'emlns':
                            proj._emlns[f] = zf.open(member).read().decode('utf-8')
                        else:
                            if path == 'dbs':
                                proj._dbs[f] = zf.open(member).read().decode('utf-8')
                            else:
                                if path == 'results':
                                    proj._results[f] = zf.open(member).read().decode('utf-8')

        return proj

    @staticmethod
    def read(filename, stream, path=None):
        proj = MLNProject(filename)
        proj.path = path
        with ZipFile(stream, 'r') as (zf):
            for member in zf.namelist():
                if member == 'learn.conf':
                    tmpconf = eval(zf.open(member).read().decode('utf-8'))
                    proj.learnconf = PRACMLNConfig()
                    proj.learnconf.update(tmpconf)
                elif member == 'query.conf':
                    tmpconf = eval(zf.open(member).read().decode('utf-8'))
                    proj.queryconf = PRACMLNConfig()
                    proj.queryconf.update(tmpconf)
                else:
                    path, f = os.path.split(member)
                    if path == 'mlns':
                        proj._mlns[f] = zf.open(member).read().decode('utf-8')
                    else:
                        if path == 'emlns':
                            proj._emlns[f] = zf.open(member).read().decode('utf-8')
                        else:
                            if path == 'dbs':
                                proj._dbs[f] = zf.open(member).read().decode('utf-8')
                            else:
                                if path == 'results':
                                    proj._results[f] = zf.open(member).read().decode('utf-8')

        return proj

    def tostream(self, stream):
        with ZipFile(stream, 'w', ZIP_DEFLATED) as (zf):
            zf.writestr('learn.conf', self.learnconf.dumps())
            zf.writestr('query.conf', self.queryconf.dumps())
            for name, mln in self.mlns.items():
                zf.writestr(os.path.join('mlns', name), mln)

            for name, emln in self.emlns.items():
                zf.writestr(os.path.join('emlns', name), emln)

            for name, db in self.dbs.items():
                zf.writestr(os.path.join('dbs', name), db)

            for name, result in self.results.items():
                zf.writestr(os.path.join('results', name), result)

    def write(self, stream=sys.stdout):
        stream.write('MLN Project: %s\n' % self.name)
        if self.learnconf is not None:
            stream.write('learn.conf\n')
        if self.queryconf is not None:
            stream.write('query.conf\n')
        stream.write('mlns/\n')
        for name in self.mlns:
            stream.write('  ./%s\n' % name)

        stream.write('dbs/\n')
        for name in self.dbs:
            stream.write('  ./%s\n' % name)

        stream.write('emlns/\n')
        for name in self.emlns:
            stream.write('  ./%s\n' % name)

        stream.write('results/\n')
        for name in self.results:
            stream.write('  ./%s\n' % name)


def convert(data):
    """
    convert everything to ASCII
    """
    if isinstance(data, str):
        return str(data)
    else:
        if isinstance(data, collections.Mapping):
            return dict(list(map(convert, iter(data.items()))))
        if isinstance(data, collections.Iterable):
            return type(data)(list(map(convert, data)))
        return data


class PRACMLNConfig(object):

    def __init__(self, filepath=None):
        self.config_file = mlnpath(filepath) if filepath is not None else None
        self.config = {}
        self._dirty = False
        if self.config_file is None or not self.config_file.exists:
            self.config = {}
        else:
            if self.config_file.project is not None:
                self.config = convert(dict(self.config_file.content.config))
            else:
                self.config = convert(json.loads(self.config_file.content))
            logger.debug('loaded %s config' % self.config_file.compose())

    @property
    def dirty(self):
        return self._dirty

    def get(self, k, d=None):
        return self.config.get(k, d)

    def update(self, d):
        self.config.update(d)
        self._dirty = True

    def __getitem__(self, s):
        if type(s) is slice:
            prim = s.start
            sec = s.stop
            if self.config.get(prim) is not None:
                return self.config.get(prim).get(sec)
            else:
                return
        else:
            return self.config.get(s)

    def __setitem__(self, s, v):
        if type(s) is slice:
            prim = s.start
            sec = s.stop
            p = self.config.get(prim)
            if p is None:
                p = {}
                self.config[prim] = p
            p[sec] = v
        else:
            self.config[s] = v
        self._dirty = True

    def dump(self):
        if self.config_file is None:
            raise Exception('no filename specified')
        else:
            if self.config_file.project is not None:
                project = mlnpath(self.config_file.projectloc).content
                if self.config_file.file == 'query.conf':
                    project.queryconf.config = self.config
                else:
                    if self.config_file.file == 'learn.conf':
                        project.queryconf.file = self.config
                    else:
                        Exception('Invalid config file name: %s' % self.config_file.file)
                project.save(project.resolve_path())
            else:
                with open(os.path.join(self.config_file.resolve_path(), self.config_file.file), 'w+') as (cf):
                    cf.write(json.dumps(self.config))
        self._dirty = False

    def dumps(self):
        self._dirty = False
        return json.dumps((self.config), indent=4)


class mlnpath(object):
    """mlnpath"""

    def __init__(self, path):
        self.path, file = os.path.split(path)
        self._abspath = self.path.startswith('/')
        if ':' in file or file.endswith('.pracmln'):
            res = file.split(':')
            if len(res) == 2:
                self.project, self.file = res
            elif len(res) == 1:
                self.project, self.file = res[0], None
        else:
            self.project = None
            self.file = file

    def compose(self):
        p = (os.path.join)(*self.path)
        if self.project is not None:
            p += ('/' if p else '') + self.project
            if self.file is not None:
                p += ':' + str(self.file)
        else:
            p += ifnone(self.file, '', lambda x: '/' + str(x))
        return p

    def resolve_path(self):
        p = self.path
        for f in (os.path.expanduser, os.path.expandvars, os.path.normpath):
            p = f(p)

        return p

    @property
    def file(self):
        """
        Returns the name of the file specified by this ``mlnpath``.
        """
        return self._file

    @file.setter
    def file(self, f):
        self._file = f

    @property
    def project(self):
        """
        Returns the project name specified.
        """
        return self._project

    @project.setter
    def project(self, p):
        self._project = p

    @property
    def content(self):
        """
        Returns the content of the file specified by this ``mlnpath``.
        """
        path = self.resolve_path()
        if self.project is not None:
            proj = MLNProject.open(os.path.join(self.resolve_path(), self.project))
            if self.file is None:
                return proj
            fileext = self.file.split('.')[(-1)]
            if fileext == 'mln':
                mln = proj.mlns.get(self.file)
                if mln is None:
                    raise Exception('Project %s does not contain and MLN named %s' % (self.project, self.file))
                return mln
            if fileext == 'db':
                db = proj.dbs.get(self.file)
                if db is None:
                    raise Exception('Project %s does not contain a database named %s' % (self.project, self.file))
                return db
            if fileext == 'conf':
                conf = {'query.conf':proj.queryconf, 
                 'learn.conf':proj.learnconf}.get(self.file)
                if conf is None:
                    raise Exception('Project %s does not contain a config file named %s' % (self.project, self.file))
                return conf
        else:
            with open(os.path.join(path, self.file)) as (f):
                return f.read()

    @property
    def projectloc(self):
        """
        Returns the location of the project file, if any is specified.
        """
        if self.project is None:
            raise Exception('No project specified in the path.')
        return os.path.join(self.resolve_path(), self.project)

    @property
    def exists(self):
        """
        Checks if the file exists.
        """
        return os.path.exists(os.path.join(self.resolve_path(), ifnone(self.project, self.file)))

    @property
    def isabs(self):
        return self._abspath

    def __str__(self):
        return self.compose()

    def __repr__(self):
        return 'mlnpath(%s)' % str(self)


if __name__ == '__main__':
    proj = MLNProject.open(os.path.join(locs.examples, 'smokers', 'smokers.pracmln'))
    proj.write()
    print(proj.queryconf.config)
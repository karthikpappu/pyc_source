# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/grun/__init__.py
# Compiled at: 2009-10-05 16:43:15
"""
GRUN %s : "express your scripts". By manatlan.com under MIT terms.

method to forms:    @grun or grun(method)(*a,**k) -> what method returns
notifications:      grun( "x"           )
messagebox info:    grun( "x!"          )
messagebox error:   grun( "x!!"         )
prompt dialog:      grun( "x?"          )         -> bool or None
icon app:           grun( (f1,f2, ... ) )
windowed app:       grun( [f1,f2, ... ] )
popup app:          grun( popup=(f1,. ) )
quick form:         grun( form=[...]    )(*a,**k) -> [(k,v), ... ]
progress window:    grun( generator     )
config backend:     grun(               )         -> cfg (dict)
 - config save:     cfg.save()
 - config delete:   cfg.delete()                  -> bool

more info:
http://www.manatlan.com/page/grun
gtk icon stock:
http://www.pygtk.org/docs/pygtk/gtk-stock-items.html
gtk pango markup :
http://www.pygtk.org/pygtk2reference/pango-markup-language.html
"""
__version__ = '0.14'
import types, os, time, pickle, string

def beautifuler(s):
    s = ('').join([ i in string.uppercase and ' %s' % i or i for i in list(s) ])
    s = (' ').join([ word.capitalize() for word in s.replace('_', ' ').split(' ') ])
    return s.strip(' ')


try:
    from __main__ import NAME
except:
    try:
        from __main__ import __file__ as mainfile
        NAME = beautifuler(os.path.basename(mainfile).replace('.py', ''))
    except:
        NAME = 'Grun'

from gui import GuiInit, MessageBox, QuestionBox, ProgressBox, NotifyBox, IconApp, PopApp, GrunApp, ExoArg, Clipboard
try:
    from __main__ import ICON
except Exception, m:
    ICON = None

GuiInit(ICON)

def mapInArray(l, cb):
    """map callback replacement 'cb' for each item of array 'l' (list or tuple)
    """
    if type(l) == tuple:
        isTuple = True
        l = list(l)
    else:
        isTuple = False
    for (idx, i) in enumerate(l):
        if type(i) in (list, tuple):
            l[idx] = mapInArray(l[idx], cb)
        else:
            l[idx] = cb(i)

    if isTuple:
        return tuple(l)
    else:
        return l


def zipfullLeft(a, b, elt=None):
    a = list(a)
    b = list(b)
    d = len(a) - len(b)
    if d == 0:
        return zip(a, b)
    else:
        if d > 0:
            b += [elt] * d
        else:
            a += [elt] * -d
        return zip(a, b)


def zipfullRight(a, b, elt=None):
    a = list(a)
    b = list(b)
    d = len(a) - len(b)
    if d == 0:
        return zip(a, b)
    else:
        if d > 0:
            b = [
             elt] * d + b
        else:
            a = [
             elt] * -d + a
        return zip(a, b)


class Config(dict):

    def __init__(self, name=None):
        name = name or NAME
        confName = name + '.conf'
        if os.path.isfile(confName):
            filename = confName
        else:
            try:
                from xdg.BaseDirectory import xdg_config_home as home
                filename = os.path.join(home, confName)
            except:
                try:
                    home = os.environ['HOME']
                    filename = os.path.join(home, '.' + confName)
                except:
                    try:
                        home = os.environ['APPDATA']
                        filename = os.path.join(home, confName)
                    except:
                        home = '.'
                        filename = os.path.join(home, confName)

            try:
                fid = open(filename, 'rb')
                d = pickle.load(fid)
                fid.close()
            except:
                d = {}

            self._file = filename
            dict.__init__(self, d)

    def __getitem__(self, key):
        return dict.get(self, key, None)

    def save(self):
        fid = open(self._file, 'wb')
        pickle.dump(self, fid)
        fid.close()

    def delete(self):
        if self.exists:
            os.unlink(self._file)
            return True
        else:
            return False

    @property
    def exists(self):
        return os.path.isfile(self._file)


class ExoBase(object):

    def __init__(self):
        pass

    def _mkinfosdoc(self, doc):
        self._infos = {}
        self._docs = []
        for i in doc.split('\n'):
            if ':' in i:
                infos = i.split(':')
                self._infos[infos[0].strip()] = infos[(-1)].strip()
            elif i.strip():
                self._docs.append(i.strip())

    def _mkargs(self, arg_defval, callargs, callkargs):
        self._args = []
        ladv = [ (a, d, None) for (a, d) in arg_defval ]
        if callargs:
            nladv = []
            for (idx, elt) in enumerate(ladv):
                (a, d, v) = elt
                if idx < len(callargs):
                    v = callargs[idx]
                nladv.append((a, d, v))

            ladv = nladv
        if callkargs:
            nladv = []
            for (a, d, v) in ladv:
                if a in callkargs:
                    v = callkargs[a]
                nladv.append((a, d, v))

            ladv = nladv
        self._args = [ ExoArg(self, a, d, v) for (a, d, v) in ladv ]
        self.labelmax = self._args and max([ len(i.affname) for i in self._args ])
        return

    @property
    def doc(self):
        return ('\n').join(self._docs)

    @property
    def infos(self):
        return self._infos

    @property
    def prototype(self):
        return '%s(%s)' % (self.name, (', ').join([ i.realname for i in self.args ]))

    @property
    def args(self):
        return self._args

    @property
    def name(self):
        return self._name


class ExoFct(ExoBase):

    def __init__(self, fn, callargs=(), callkargs={}, name=None, doc=None):
        ExoBase.__init__(self)
        self._fn = fn
        l = list(self._fn.func_code.co_varnames[:self._fn.func_code.co_argcount])
        if 'self' in l:
            l.remove('self')
        self._instance = None
        if callargs:
            if 'class' in str(type(callargs[0])):
                self._instance = callargs[0]
                callargs = callargs[1:]
        dv = self._fn.func_defaults and self._fn.func_defaults[:] or []
        lad = zipfullRight(l, dv)
        self._mkinfosdoc(doc or self._fn.__doc__ or '')
        self._mkargs(lad, callargs, callkargs)
        self._name = name or self._fn.__name__
        return

    def call(self, *a, **k):
        if self._instance is not None:
            return self._fn(self._instance, *a, **k)
        else:
            return self._fn(*a, **k)
            return


class ExoForm(ExoBase):

    def __init__(self, args, defvals=[], callargs=(), callkargs={}, name=None, doc=None):
        ExoBase.__init__(self)
        self._name = name or 'form'
        self._mkinfosdoc(doc or '')
        lad = zipfullLeft(args, defvals)
        self._mkargs(lad, callargs, callkargs)

    def call(self, *a, **k):
        args = [ i.realname for i in self.args ]
        vals = [ i.value for i in self.args ]
        self._mkargs(zip(args, vals), a, k)
        return [ (i.realname, i.value) for i in self.args ]


class GrunCmd(object):

    def __init__(self):
        self._c = Clipboard()

    def __call__(self, x=None, name=None, doc=None, form=None, popup=None):
        if x is None:
            if popup:
                assert not doc
                assert type(popup) in (tuple, list)

                def transInExoFct(obj):
                    if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType):
                        return ExoFct(obj)
                    else:
                        return obj

                ef = mapInArray(popup, transInExoFct)
                return PopApp(ef, name or NAME)
            else:
                if form == None:
                    assert doc is None
                    return Config(name)
                if form:
                    if isinstance(form, basestring):
                        f = [ i.strip() for i in form.replace(',', ' ').split(' ') if i.strip() ]
                    else:
                        f = list(form)
                else:
                    f = []
                if f:
                    if type(f[0]) not in (list, tuple):
                        f = zipfullLeft(f, [])
                args = [ a for (a, v) in f ]
                defvals = [ v for (a, v) in f ]

                def _f(*a, **k):
                    d = GrunApp([ExoForm(args, defvals, a, k, name=name, doc=doc)])
                    return d.run(name)

                return _f
        else:
            if type(x) == list:
                ef = [ ExoFct(obj) for obj in x if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType) ]
                d = GrunApp(ef)
                d.run(NAME, doc=doc)
                return
                assert type(x) == types.GeneratorType and not doc
                name = name and (' - ').join([NAME, name]) or NAME
                w = ProgressBox(x, name)
                w.run()
            elif type(x) == tuple:
                ef = [ ExoFct(obj) for obj in x if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType) ]
                ico = IconApp(ef, NAME, ICON)
                ico.run()
            elif isinstance(x, basestring):
                assert not doc
                name = name and (' - ').join([NAME, name]) or NAME
                if x == 'help':
                    print __doc__ % __version__
                elif x == 'help!':
                    MessageBox('<tt>%s</tt>' % (__doc__ % __version__), 'Grun help')
                else:
                    if x.strip().endswith('?'):
                        return QuestionBox(x, name or NAME)
                    if x.strip().endswith('!!'):
                        MessageBox(x.strip('! \n\r'), name or NAME, error=True)
                    elif x.strip().endswith('!'):
                        MessageBox(x.strip('! \n\r'), name or NAME)
                    else:
                        NotifyBox(x.strip(), name or NAME)
            else:
                if isinstance(x, types.FunctionType) or isinstance(x, types.MethodType):

                    def _f(*a, **k):
                        d = GrunApp([ExoFct(x, a, k, name=name, doc=doc)])
                        return d.run(NAME)

                    return _f
                else:
                    return
            return

    def popup(self, l, name=None):
        return self(popup=l, name=name)

    def form(self, l, name=None, doc=None):
        return self(form=l, name=name, doc=None)

    def _get(self):
        return self._c.get()

    def _set(self, v):
        self._c.set(v)

    def _del(self, v):
        self._c.clr()

    clipboard = property(_get, _set, _del, 'manage clipboard')


grun = GrunCmd()
if __name__ == '__main__':
    assert NAME == 'Init'
    assert beautifuler('hello_from paris') == 'Hello From Paris'
    assert beautifuler('renameImage') == 'Rename Image'
    assert beautifuler('loveINA') == 'Love I N A'
    a = list('abc')
    b = list('12')
    assert zipfullRight(a, b) == [('a', None), ('b', '1'), ('c', '2')]
    assert zipfullRight(b, a) == [(None, 'a'), ('1', 'b'), ('2', 'c')]
    assert zipfullLeft(a, b) == [('a', '1'), ('b', '2'), ('c', None)]
    assert zipfullLeft(b, a) == [('1', 'a'), ('2', 'b'), (None, 'c')]

    def test(a=12):
        pass


    f = ExoFct(test)
    assert [ i.value for i in f.args ] == [12]
    f = ExoFct(test, (13, ))
    assert [ i.value for i in f.args ] == [13]

    def test(a, b, c=3):
        pass


    f = ExoFct(test)
    assert [ i.value for i in f.args ] == [None, None, 3]

    def test(a=1, b=2, c=3):
        pass


    f = ExoFct(test)
    assert [ i.value for i in f.args ] == [1, 2, 3]
    f = ExoFct(test, ('a', 'b'))
    assert [ i.value for i in f.args ] == ['a', 'b', 3]
    f = ExoFct(test, ('a', ), {'c': 'c'})
    assert [ i.value for i in f.args ] == ['a', 2, 'c']

    def test(a, b, c=3):
        pass


    f = ExoFct(test, (), {'b': 'b'})
    assert [ i.value for i in f.args ] == [None, 'b', 3]
    f = ExoFct(test, 'a', {'c': 'c'})
    assert [ i.value for i in f.args ] == ['a', None, 'c']
    assert f.call(1, 2) == None
    f = ExoForm(['a', 'b'], [], [], {})
    assert [ i.value for i in f.args ] == [None, None]
    f = ExoForm(['a', 'b'], [1], [], {})
    assert [ i.value for i in f.args ] == [1, None]
    f = ExoForm(['a', 'b'], [], [1], {})
    assert [ i.value for i in f.args ] == [1, None]
    f = ExoForm(['a', 'b'], [1], [2], {})
    assert [ i.value for i in f.args ] == [2, None]
    f = ExoForm(['a', 'b'], [], [1], {'a': 2})
    assert [ i.value for i in f.args ] == [2, None]
    f = ExoForm(['a', 'b'], [], [1], {'a': 2, 'b': 3})
    assert [ i.value for i in f.args ] == [2, 3]
    assert dict(f.call()) == {'a': 2, 'b': 3}
    assert dict(f.call(1, 2)) == {'a': 1, 'b': 2}
    assert dict(f.call(b=4)) == {'a': 1, 'b': 4}

    def test(a, int_b=4):
        """hihi
        a: un texte
        int_b : un chiffre
        """
        return a


    f = ExoFct(test)
    assert f.name == 'test'
    assert f.doc == 'hihi'
    assert f.infos == {'a': 'un texte', 'int_b': 'un chiffre'}
    assert f.call('3', 2) == test('3', 2)
    assert [ i.realname for i in f.args ] == ['a', 'int_b']
    assert [ i.name for i in f.args ] == ['a', 'b']
    assert [ i.value for i in f.args ] == [None, 4]
    assert f.prototype == 'test(a, int_b)'
    f = ExoForm(['a', 'int_b'], [], {}, name='jojo', doc='dodo\na:un texte')
    assert f.name == 'jojo'
    assert f.doc == 'dodo'
    assert f.infos == {'a': 'un texte'}
    assert [ i.realname for i in f.args ] == ['a', 'int_b']
    assert [ i.name for i in f.args ] == ['a', 'b']
    assert [ i.value for i in f.args ] == [None, None]
    assert f.prototype == 'jojo(a, int_b)'
    assert dict(f.call()) == {'a': None, 'int_b': None}
    assert dict(f.call(1, 2)) == {'a': 1, 'int_b': 2}
    assert f.call(1, 2) == [('a', 1), ('int_b', 2)]
    l = list(list('abc') + [list('abc') + [tuple(list('abc'))] + ['b']])
    assert mapInArray(l, lambda item: item == 'b' and ' ' or item) == [
     'a', ' ', 'c', ['a', ' ', 'c', ('a', ' ', 'c'), ' ']]
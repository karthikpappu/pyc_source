# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../py010parser/ply/lex.py
# Compiled at: 2019-04-24 09:45:01
# Size of source mod 2**32: 40739 bytes
__version__ = '3.4'
__tabversion__ = '3.2'
import re, sys, types, copy, os
try:
    StringTypes = (
     types.StringType, types.UnicodeType)
except AttributeError:
    StringTypes = (
     str, bytes)

if sys.version_info[0] < 3:

    def func_code(f):
        return f.func_code


else:

    def func_code(f):
        return f.__code__


_is_identifier = re.compile('^[a-zA-Z0-9_]+$')

class LexError(Exception):

    def __init__(self, message, s):
        self.args = (
         message,)
        self.text = s


class LexToken(object):

    def __str__(self):
        return 'LexToken(%s,%r,%d,%d)' % (self.type, self.value, self.lineno, self.lexpos)

    def __repr__(self):
        return str(self)


class PlyLogger(object):

    def __init__(self, f):
        self.f = f

    def critical(self, msg, *args, **kwargs):
        self.f.write(msg % args + '\n')

    def warning(self, msg, *args, **kwargs):
        self.f.write('WARNING: ' + msg % args + '\n')

    def error(self, msg, *args, **kwargs):
        self.f.write('ERROR: ' + msg % args + '\n')

    info = critical
    debug = critical


class NullLogger(object):

    def __getattribute__(self, name):
        return self

    def __call__(self, *args, **kwargs):
        return self


class Lexer:

    def __init__(self):
        self.lexre = None
        self.lexretext = None
        self.lexstatere = {}
        self.lexstateretext = {}
        self.lexstaterenames = {}
        self.lexstate = 'INITIAL'
        self.lexstatestack = []
        self.lexstateinfo = None
        self.lexstateignore = {}
        self.lexstateerrorf = {}
        self.lexreflags = 0
        self.lexdata = None
        self.lexpos = 0
        self.lexlen = 0
        self.lexerrorf = None
        self.lextokens = None
        self.lexignore = ''
        self.lexliterals = ''
        self.lexmodule = None
        self.lineno = 1
        self.lexoptimize = 0

    def clone(self, object=None):
        c = copy.copy(self)
        if object:
            newtab = {}
            for key, ritem in self.lexstatere.items():
                newre = []
                for cre, findex in ritem:
                    newfindex = []
                    for f in findex:
                        if not f or not f[0]:
                            newfindex.append(f)
                        else:
                            newfindex.append((getattr(object, f[0].__name__), f[1]))

                newre.append((cre, newfindex))
                newtab[key] = newre

            c.lexstatere = newtab
            c.lexstateerrorf = {}
            for key, ef in self.lexstateerrorf.items():
                c.lexstateerrorf[key] = getattr(object, ef.__name__)

            c.lexmodule = object
        return c

    def writetab(self, tabfile, outputdir=''):
        if isinstance(tabfile, types.ModuleType):
            return
        basetabfilename = tabfile.split('.')[(-1)]
        filename = os.path.join(outputdir, basetabfilename) + '.py'
        tf = open(filename, 'w')
        tf.write("# %s.py. This file automatically created by PLY (version %s). Don't edit!\n" % (tabfile, __version__))
        tf.write('_tabversion   = %s\n' % repr(__version__))
        tf.write('_lextokens    = %s\n' % repr(self.lextokens))
        tf.write('_lexreflags   = %s\n' % repr(self.lexreflags))
        tf.write('_lexliterals  = %s\n' % repr(self.lexliterals))
        tf.write('_lexstateinfo = %s\n' % repr(self.lexstateinfo))
        tabre = {}
        initial = self.lexstatere['INITIAL']
        initialfuncs = []
        for part in initial:
            for f in part[1]:
                if f and f[0]:
                    initialfuncs.append(f)

        for key, lre in self.lexstatere.items():
            titem = []
            for i in range(len(lre)):
                titem.append((self.lexstateretext[key][i], _funcs_to_names(lre[i][1], self.lexstaterenames[key][i])))

            tabre[key] = titem

        tf.write('_lexstatere   = %s\n' % repr(tabre))
        tf.write('_lexstateignore = %s\n' % repr(self.lexstateignore))
        taberr = {}
        for key, ef in self.lexstateerrorf.items():
            if ef:
                taberr[key] = ef.__name__
            else:
                taberr[key] = None

        tf.write('_lexstateerrorf = %s\n' % repr(taberr))
        tf.close()

    def readtab(self, tabfile, fdict):
        if isinstance(tabfile, types.ModuleType):
            lextab = tabfile
        else:
            if sys.version_info[0] < 3:
                exec('import %s as lextab' % tabfile)
            else:
                env = {}
                exec('import %s as lextab' % tabfile, env, env)
                lextab = env['lextab']
        if getattr(lextab, '_tabversion', '0.0') != __version__:
            raise ImportError('Inconsistent PLY version')
        self.lextokens = lextab._lextokens
        self.lexreflags = lextab._lexreflags
        self.lexliterals = lextab._lexliterals
        self.lexstateinfo = lextab._lexstateinfo
        self.lexstateignore = lextab._lexstateignore
        self.lexstatere = {}
        self.lexstateretext = {}
        for key, lre in lextab._lexstatere.items():
            titem = []
            txtitem = []
            for i in range(len(lre)):
                titem.append((re.compile(lre[i][0], lextab._lexreflags | re.VERBOSE), _names_to_funcs(lre[i][1], fdict)))
                txtitem.append(lre[i][0])

            self.lexstatere[key] = titem
            self.lexstateretext[key] = txtitem

        self.lexstateerrorf = {}
        for key, ef in lextab._lexstateerrorf.items():
            self.lexstateerrorf[key] = fdict[ef]

        self.begin('INITIAL')

    def input(self, s):
        c = s[:1]
        if not isinstance(c, StringTypes):
            raise ValueError('Expected a string')
        self.lexdata = s
        self.lexpos = 0
        self.lexlen = len(s)

    def begin(self, state):
        if state not in self.lexstatere:
            raise ValueError('Undefined state')
        self.lexre = self.lexstatere[state]
        self.lexretext = self.lexstateretext[state]
        self.lexignore = self.lexstateignore.get(state, '')
        self.lexerrorf = self.lexstateerrorf.get(state, None)
        self.lexstate = state

    def push_state(self, state):
        self.lexstatestack.append(self.lexstate)
        self.begin(state)

    def pop_state(self):
        self.begin(self.lexstatestack.pop())

    def current_state(self):
        return self.lexstate

    def skip(self, n):
        self.lexpos += n

    def token(self):
        lexpos = self.lexpos
        lexlen = self.lexlen
        lexignore = self.lexignore
        lexdata = self.lexdata
        while lexpos < lexlen:
            if lexdata[lexpos] in lexignore:
                lexpos += 1
            else:
                for lexre, lexindexfunc in self.lexre:
                    m = lexre.match(lexdata, lexpos)
                    if not m:
                        continue
                    tok = LexToken()
                    tok.value = m.group()
                    tok.lineno = self.lineno
                    tok.lexpos = lexpos
                    i = m.lastindex
                    func, tok.type = lexindexfunc[i]
                    if not func:
                        if tok.type:
                            self.lexpos = m.end()
                            return tok
                        lexpos = m.end()
                        break
                    lexpos = m.end()
                    tok.lexer = self
                    self.lexmatch = m
                    self.lexpos = lexpos
                    newtok = func(tok)
                    if not newtok:
                        lexpos = self.lexpos
                        lexignore = self.lexignore
                        break
                    if not self.lexoptimize:
                        if newtok.type not in self.lextokens:
                            raise LexError("%s:%d: Rule '%s' returned an unknown token type '%s'" % (
                             func_code(func).co_filename, func_code(func).co_firstlineno,
                             func.__name__, newtok.type), lexdata[lexpos:])
                    return newtok
                else:
                    if lexdata[lexpos] in self.lexliterals:
                        tok = LexToken()
                        tok.value = lexdata[lexpos]
                        tok.lineno = self.lineno
                        tok.type = tok.value
                        tok.lexpos = lexpos
                        self.lexpos = lexpos + 1
                        return tok
                    if self.lexerrorf:
                        tok = LexToken()
                        tok.value = self.lexdata[lexpos:]
                        tok.lineno = self.lineno
                        tok.type = 'error'
                        tok.lexer = self
                        tok.lexpos = lexpos
                        self.lexpos = lexpos
                        newtok = self.lexerrorf(tok)
                        if lexpos == self.lexpos:
                            raise LexError("Scanning error. Illegal character '%s'" % lexdata[lexpos], lexdata[lexpos:])
                        lexpos = self.lexpos
                        if not newtok:
                            continue
                        return newtok
                    self.lexpos = lexpos
                    raise LexError("Illegal character '%s' at index %d" % (lexdata[lexpos], lexpos), lexdata[lexpos:])

        self.lexpos = lexpos + 1
        if self.lexdata is None:
            raise RuntimeError('No input string given with input()')

    def __iter__(self):
        return self

    def next(self):
        t = self.token()
        if t is None:
            raise StopIteration
        return t

    __next__ = next


def get_caller_module_dict(levels):
    try:
        raise RuntimeError
    except RuntimeError:
        e, b, t = sys.exc_info()
        f = t.tb_frame
        while levels > 0:
            f = f.f_back
            levels -= 1

        ldict = f.f_globals.copy()
        if f.f_globals != f.f_locals:
            ldict.update(f.f_locals)
        return ldict


def _funcs_to_names(funclist, namelist):
    result = []
    for f, name in zip(funclist, namelist):
        if f and f[0]:
            result.append((name, f[1]))
        else:
            result.append(f)

    return result


def _names_to_funcs(namelist, fdict):
    result = []
    for n in namelist:
        if n and n[0]:
            result.append((fdict[n[0]], n[1]))
        else:
            result.append(n)

    return result


def _form_master_re(relist, reflags, ldict, toknames):
    if not relist:
        return []
    regex = '|'.join(relist)
    try:
        lexre = re.compile(regex, re.VERBOSE | reflags)
        lexindexfunc = [
         None] * (max(lexre.groupindex.values()) + 1)
        lexindexnames = lexindexfunc[:]
        for f, i in lexre.groupindex.items():
            handle = ldict.get(f, None)
            if type(handle) in (types.FunctionType, types.MethodType):
                lexindexfunc[i] = (
                 handle, toknames[f])
                lexindexnames[i] = f
            else:
                if handle is not None:
                    lexindexnames[i] = f
                    if f.find('ignore_') > 0:
                        lexindexfunc[i] = (None, None)
                    else:
                        lexindexfunc[i] = (
                         None, toknames[f])

        return (
         [
          (
           lexre, lexindexfunc)], [regex], [lexindexnames])
    except Exception:
        m = int(len(relist) / 2)
        if m == 0:
            m = 1
        llist, lre, lnames = _form_master_re(relist[:m], reflags, ldict, toknames)
        rlist, rre, rnames = _form_master_re(relist[m:], reflags, ldict, toknames)
        return (llist + rlist, lre + rre, lnames + rnames)


def _statetoken(s, names):
    nonstate = 1
    parts = s.split('_')
    for i in range(1, len(parts)):
        if parts[i] not in names:
            if parts[i] != 'ANY':
                break

    if i > 1:
        states = tuple(parts[1:i])
    else:
        states = ('INITIAL', )
    if 'ANY' in states:
        states = tuple(names)
    tokenname = '_'.join(parts[i:])
    return (states, tokenname)


class LexerReflect(object):

    def __init__(self, ldict, log=None, reflags=0):
        self.ldict = ldict
        self.error_func = None
        self.tokens = []
        self.reflags = reflags
        self.stateinfo = {'INITIAL': 'inclusive'}
        self.files = {}
        self.error = 0
        if log is None:
            self.log = PlyLogger(sys.stderr)
        else:
            self.log = log

    def get_all(self):
        self.get_tokens()
        self.get_literals()
        self.get_states()
        self.get_rules()

    def validate_all(self):
        self.validate_tokens()
        self.validate_literals()
        self.validate_rules()
        return self.error

    def get_tokens(self):
        tokens = self.ldict.get('tokens', None)
        if not tokens:
            self.log.error('No token list is defined')
            self.error = 1
            return
        if not isinstance(tokens, (list, tuple)):
            self.log.error('tokens must be a list or tuple')
            self.error = 1
            return
        if not tokens:
            self.log.error('tokens is empty')
            self.error = 1
            return
        self.tokens = tokens

    def validate_tokens(self):
        terminals = {}
        for n in self.tokens:
            if not _is_identifier.match(n):
                self.log.error("Bad token name '%s'", n)
                self.error = 1
            if n in terminals:
                self.log.warning("Token '%s' multiply defined", n)
            terminals[n] = 1

    def get_literals(self):
        self.literals = self.ldict.get('literals', '')

    def validate_literals(self):
        try:
            for c in self.literals:
                if not isinstance(c, StringTypes) or len(c) > 1:
                    self.log.error('Invalid literal %s. Must be a single character', repr(c))
                    self.error = 1
                    continue

        except TypeError:
            self.log.error('Invalid literals specification. literals must be a sequence of characters')
            self.error = 1

    def get_states(self):
        self.states = self.ldict.get('states', None)
        if self.states:
            if not isinstance(self.states, (tuple, list)):
                self.log.error('states must be defined as a tuple or list')
                self.error = 1
            else:
                for s in self.states:
                    if not isinstance(s, tuple) or len(s) != 2:
                        self.log.error("Invalid state specifier %s. Must be a tuple (statename,'exclusive|inclusive')", repr(s))
                        self.error = 1
                    else:
                        name, statetype = s
                        if not isinstance(name, StringTypes):
                            self.log.error('State name %s must be a string', repr(name))
                            self.error = 1
                        elif not (statetype == 'inclusive' or statetype == 'exclusive'):
                            self.log.error("State type for state %s must be 'inclusive' or 'exclusive'", name)
                            self.error = 1
                        elif name in self.stateinfo:
                            self.log.error("State '%s' already defined", name)
                            self.error = 1
                        else:
                            self.stateinfo[name] = statetype

    def get_rules(self):
        tsymbols = [f for f in self.ldict if f[:2] == 't_']
        self.toknames = {}
        self.funcsym = {}
        self.strsym = {}
        self.ignore = {}
        self.errorf = {}
        for s in self.stateinfo:
            self.funcsym[s] = []
            self.strsym[s] = []

        if len(tsymbols) == 0:
            self.log.error('No rules of the form t_rulename are defined')
            self.error = 1
            return
        for f in tsymbols:
            t = self.ldict[f]
            states, tokname = _statetoken(f, self.stateinfo)
            self.toknames[f] = tokname
            if hasattr(t, '__call__'):
                if tokname == 'error':
                    for s in states:
                        self.errorf[s] = t

                else:
                    if tokname == 'ignore':
                        line = func_code(t).co_firstlineno
                        file = func_code(t).co_filename
                        self.log.error("%s:%d: Rule '%s' must be defined as a string", file, line, t.__name__)
                        self.error = 1
                    else:
                        for s in states:
                            self.funcsym[s].append((f, t))

            elif isinstance(t, StringTypes):
                if tokname == 'ignore':
                    for s in states:
                        self.ignore[s] = t

                    if '\\' in t:
                        self.log.warning("%s contains a literal backslash '\\'", f)
                else:
                    if tokname == 'error':
                        self.log.error("Rule '%s' must be defined as a function", f)
                        self.error = 1
                    else:
                        for s in states:
                            self.strsym[s].append((f, t))

            else:
                self.log.error('%s not defined as a function or string', f)
                self.error = 1

        for f in self.funcsym.values():
            if sys.version_info[0] < 3:
                f.sort(lambda x, y: cmp(func_code(x[1]).co_firstlineno, func_code(y[1]).co_firstlineno))
            else:
                f.sort(key=(lambda x: func_code(x[1]).co_firstlineno))

        for s in self.strsym.values():
            if sys.version_info[0] < 3:
                s.sort(lambda x, y: (len(x[1]) < len(y[1])) - (len(x[1]) > len(y[1])))
            else:
                s.sort(key=(lambda x: len(x[1])), reverse=True)

    def validate_rules(self):
        for state in self.stateinfo:
            for fname, f in self.funcsym[state]:
                line = func_code(f).co_firstlineno
                file = func_code(f).co_filename
                self.files[file] = 1
                tokname = self.toknames[fname]
                if isinstance(f, types.MethodType):
                    reqargs = 2
                else:
                    reqargs = 1
                nargs = func_code(f).co_argcount
                if nargs > reqargs:
                    self.log.error("%s:%d: Rule '%s' has too many arguments", file, line, f.__name__)
                    self.error = 1
                elif nargs < reqargs:
                    self.log.error("%s:%d: Rule '%s' requires an argument", file, line, f.__name__)
                    self.error = 1
                elif not f.__doc__:
                    self.log.error("%s:%d: No regular expression defined for rule '%s'", file, line, f.__name__)
                    self.error = 1
                else:
                    try:
                        c = re.compile('(?P<%s>%s)' % (fname, f.__doc__), re.VERBOSE | self.reflags)
                        if c.match(''):
                            self.log.error("%s:%d: Regular expression for rule '%s' matches empty string", file, line, f.__name__)
                            self.error = 1
                    except re.error:
                        _etype, e, _etrace = sys.exc_info()
                        self.log.error("%s:%d: Invalid regular expression for rule '%s'. %s", file, line, f.__name__, e)
                        if '#' in f.__doc__:
                            self.log.error("%s:%d. Make sure '#' in rule '%s' is escaped with '\\#'", file, line, f.__name__)
                        self.error = 1

            for name, r in self.strsym[state]:
                tokname = self.toknames[name]
                if tokname == 'error':
                    self.log.error("Rule '%s' must be defined as a function", name)
                    self.error = 1
                else:
                    if tokname not in self.tokens:
                        if tokname.find('ignore_') < 0:
                            self.log.error("Rule '%s' defined for an unspecified token %s", name, tokname)
                            self.error = 1
                            continue
                    try:
                        c = re.compile('(?P<%s>%s)' % (name, r), re.VERBOSE | self.reflags)
                        if c.match(''):
                            self.log.error("Regular expression for rule '%s' matches empty string", name)
                            self.error = 1
                    except re.error:
                        _etype, e, _etrace = sys.exc_info()
                        self.log.error("Invalid regular expression for rule '%s'. %s", name, e)
                        if '#' in r:
                            self.log.error("Make sure '#' in rule '%s' is escaped with '\\#'", name)
                        self.error = 1

            if not self.funcsym[state]:
                if not self.strsym[state]:
                    self.log.error("No rules defined for state '%s'", state)
                    self.error = 1
            efunc = self.errorf.get(state, None)
            if efunc:
                f = efunc
                line = func_code(f).co_firstlineno
                file = func_code(f).co_filename
                self.files[file] = 1
                if isinstance(f, types.MethodType):
                    reqargs = 2
                else:
                    reqargs = 1
                nargs = func_code(f).co_argcount
                if nargs > reqargs:
                    self.log.error("%s:%d: Rule '%s' has too many arguments", file, line, f.__name__)
                    self.error = 1
                if nargs < reqargs:
                    self.log.error("%s:%d: Rule '%s' requires an argument", file, line, f.__name__)
                    self.error = 1

        for f in self.files:
            self.validate_file(f)

    def validate_file(self, filename):
        import os.path
        base, ext = os.path.splitext(filename)
        if ext != '.py':
            return
        try:
            f = open(filename)
            lines = f.readlines()
            f.close()
        except IOError:
            return
        else:
            fre = re.compile('\\s*def\\s+(t_[a-zA-Z_0-9]*)\\(')
            sre = re.compile('\\s*(t_[a-zA-Z_0-9]*)\\s*=')
            counthash = {}
            linen = 1
            for l in lines:
                m = fre.match(l)
                if not m:
                    m = sre.match(l)
                if m:
                    name = m.group(1)
                    prev = counthash.get(name)
                    if not prev:
                        counthash[name] = linen
                    else:
                        self.log.error('%s:%d: Rule %s redefined. Previously defined on line %d', filename, linen, name, prev)
                        self.error = 1
                linen += 1


def lex(module=None, object=None, debug=0, optimize=0, lextab='lextab', reflags=0, nowarn=0, outputdir='', debuglog=None, errorlog=None):
    global input
    global lexer
    global token
    ldict = None
    stateinfo = {'INITIAL': 'inclusive'}
    lexobj = Lexer()
    lexobj.lexoptimize = optimize
    if errorlog is None:
        errorlog = PlyLogger(sys.stderr)
    if debug:
        if debuglog is None:
            debuglog = PlyLogger(sys.stderr)
    if object:
        module = object
    else:
        if module:
            _items = [(k, getattr(module, k)) for k in dir(module)]
            ldict = dict(_items)
        else:
            ldict = get_caller_module_dict(2)
        linfo = LexerReflect(ldict, log=errorlog, reflags=reflags)
        linfo.get_all()
        if not optimize:
            if linfo.validate_all():
                raise SyntaxError("Can't build lexer")
        if optimize:
            if lextab:
                try:
                    lexobj.readtab(lextab, ldict)
                    token = lexobj.token
                    input = lexobj.input
                    lexer = lexobj
                    return lexobj
                except ImportError:
                    pass

        if debug:
            debuglog.info('lex: tokens   = %r', linfo.tokens)
            debuglog.info('lex: literals = %r', linfo.literals)
            debuglog.info('lex: states   = %r', linfo.stateinfo)
        lexobj.lextokens = {}
        for n in linfo.tokens:
            lexobj.lextokens[n] = 1

        if isinstance(linfo.literals, (list, tuple)):
            lexobj.lexliterals = type(linfo.literals[0])().join(linfo.literals)
        else:
            lexobj.lexliterals = linfo.literals
    stateinfo = linfo.stateinfo
    regexs = {}
    for state in stateinfo:
        regex_list = []
        for fname, f in linfo.funcsym[state]:
            line = func_code(f).co_firstlineno
            file = func_code(f).co_filename
            regex_list.append('(?P<%s>%s)' % (fname, f.__doc__))
            if debug:
                debuglog.info("lex: Adding rule %s -> '%s' (state '%s')", fname, f.__doc__, state)

        for name, r in linfo.strsym[state]:
            regex_list.append('(?P<%s>%s)' % (name, r))
            if debug:
                debuglog.info("lex: Adding rule %s -> '%s' (state '%s')", name, r, state)

        regexs[state] = regex_list

    if debug:
        debuglog.info('lex: ==== MASTER REGEXS FOLLOW ====')
    for state in regexs:
        lexre, re_text, re_names = _form_master_re(regexs[state], reflags, ldict, linfo.toknames)
        lexobj.lexstatere[state] = lexre
        lexobj.lexstateretext[state] = re_text
        lexobj.lexstaterenames[state] = re_names
        if debug:
            for i in range(len(re_text)):
                debuglog.info("lex: state '%s' : regex[%d] = '%s'", state, i, re_text[i])

    for state, stype in stateinfo.items():
        if state != 'INITIAL' and stype == 'inclusive':
            lexobj.lexstatere[state].extend(lexobj.lexstatere['INITIAL'])
            lexobj.lexstateretext[state].extend(lexobj.lexstateretext['INITIAL'])
            lexobj.lexstaterenames[state].extend(lexobj.lexstaterenames['INITIAL'])

    lexobj.lexstateinfo = stateinfo
    lexobj.lexre = lexobj.lexstatere['INITIAL']
    lexobj.lexretext = lexobj.lexstateretext['INITIAL']
    lexobj.lexreflags = reflags
    lexobj.lexstateignore = linfo.ignore
    lexobj.lexignore = lexobj.lexstateignore.get('INITIAL', '')
    lexobj.lexstateerrorf = linfo.errorf
    lexobj.lexerrorf = linfo.errorf.get('INITIAL', None)
    if not lexobj.lexerrorf:
        errorlog.warning('No t_error rule is defined')
    for s, stype in stateinfo.items():
        if stype == 'exclusive':
            if s not in linfo.errorf:
                errorlog.warning("No error rule is defined for exclusive state '%s'", s)
            if s not in linfo.ignore:
                if lexobj.lexignore:
                    errorlog.warning("No ignore rule is defined for exclusive state '%s'", s)
            elif stype == 'inclusive':
                if s not in linfo.errorf:
                    linfo.errorf[s] = linfo.errorf.get('INITIAL', None)
                if s not in linfo.ignore:
                    linfo.ignore[s] = linfo.ignore.get('INITIAL', '')

    token = lexobj.token
    input = lexobj.input
    lexer = lexobj
    if lextab:
        if optimize:
            lexobj.writetab(lextab, outputdir)
    return lexobj


def runmain(lexer=None, data=None):
    if not data:
        try:
            filename = sys.argv[1]
            f = open(filename)
            data = f.read()
            f.close()
        except IndexError:
            sys.stdout.write('Reading from standard input (type EOF to end):\n')
            data = sys.stdin.read()

    else:
        if lexer:
            _input = lexer.input
        else:
            _input = input
        _input(data)
        if lexer:
            _token = lexer.token
        else:
            _token = token
    while True:
        tok = _token()
        if not tok:
            break
        sys.stdout.write('(%s,%r,%d,%d)\n' % (tok.type, tok.value, tok.lineno, tok.lexpos))


def TOKEN(r):

    def set_doc(f):
        if hasattr(r, '__call__'):
            f.__doc__ = r.__doc__
        else:
            f.__doc__ = r
        return f

    return set_doc


Token = TOKEN
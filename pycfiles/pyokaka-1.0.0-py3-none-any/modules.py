# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dojo\modules.py
# Compiled at: 2013-06-08 13:13:23
__doc__ = ' Asynchronous Module Definition\n'
from pyojo.js.code import js_try, Code

class DojoAMD(Code):
    """ Base class for Require and Define.
    
        Is Code not Dojo because "new" method is not applicable.
    """

    def requires(self, *args):
        """ Require this AMD module too.
        """
        for module in args:
            self.require.append(module)

        return self

    def get_code_block(self, block):
        """ Ensure is a code block, or convert to it.
        """
        if type(block) == type(''):
            return Code(block)
        else:
            get_requires = getattr(block, 'get_requires', None)
            if get_requires is not None:
                for req in block.get_requires():
                    if req not in self.require:
                        self.require.append(req)

            return block

    def js_AMD_parameters(self):
        params = ''
        for item in self.require:
            if '!' in item:
                if 'domReady!' in item:
                    continue
                elif 'text!' in item:
                    params += 'data, '
                    continue
            name = item.rpartition('/')[2]
            if '-' in name:
                i = name.find('-')
                n = name[0:i] + name[(i + 1)].upper() + name[i + 2:]
                name = n
            params += name + ', '

        return params[:-2]

    def _check_requires(self):
        if 'dojo/domReady!' in self.require:
            self.require.remove('dojo/domReady!')
            self.require.append('dojo/domReady!')

    def get_js_from_block(self, code, catch=False):
        if code is None:
            return ''
        else:
            if catch:
                return js_try(code.code(), code) + '\n'
            else:
                return code.code() + '\n'

            return

    def js_AMD_function(self, catch=True):
        loc = ''
        for script in self.scripts:
            loc += self.get_js_from_block(script, catch)

        if 'dojo/ready' in self.require:
            loc = '\nready(function(){\n%s})' % loc
        return loc

    def vars(self):
        var = {}
        for script in self.scripts:
            if hasattr(script, 'var'):
                for v in script.var:
                    var[v] = script.__class__.__name__

        return var

    def add(self, block):
        """ Append js.Code blocks. 
        
            The code is appended, and the require set is updated.
        """
        if isinstance(block, (list, tuple)):
            for item in block:
                self.add(item)

            return
        block = self.get_code_block(block)
        self.scripts.append(block)


class Require(DojoAMD):
    """ Collects Dojo object's require list and generates code.
        
        code::
            
            require([], function() {});
            
        .. warning:: falta __str__
            

    contenido
    """

    def __init__(self, *args):
        """ Accepts a mixed list of strings, Code, Require. 
        """
        self.require = []
        self.scripts = []
        self.catch = False
        for block in args:
            self.add(block)

    def code(self, catch=None):
        if catch is not None:
            self.catch = catch
        self._check_requires()
        if self.require == []:
            return self.js_AMD_function(self.catch)
        else:
            return 'require(%s, function(%s) {%s});' % (repr(self.require),
             self.js_AMD_parameters(),
             self.js_AMD_function(self.catch))


class Define(DojoAMD):

    def __init__(self, *args, **kwargs):
        """ Accepts a mixed list of strings, Code, Require. 
        """
        self.require = []
        self.scripts = []
        self.functions = {}
        self.parameters = {}
        for block in args:
            self.add(block)

        for name, block in kwargs.iteritems():
            self.function(name, block)

    def function(self, name, block):
        if '(' in name:
            name, rest = name.split('(')
            para = rest.split(')')[0].replace(' ', '')
        else:
            para = ''
        block = self.get_code_block(block)
        self.functions[name] = block
        self.parameters[name] = para

    def code(self, catch=True):
        defs = ''
        for name, code in self.functions.iteritems():
            para = self.parameters[name]
            code.catch = catch
            defs += '\n%s: function (%s) {%s},' % (name, para, code.code())

        definitions = 'return {%s}' % defs[:-1]
        return 'define(%s,\nfunction(%s) {%s\n%s});' % (repr(self.require),
         self.js_AMD_parameters(),
         self.js_AMD_function(),
         definitions)


def call(module):
    """ Use Dojo AMD to load module
    """
    return "check(); require(['pyojo/%s'], function(mod){mod.run()});" % module


def recall(module, command=None):
    """ Use Dojo AMD to load module, forcing reload.
    
        TODO: Forget crazy tricks and use headers.
    """
    epoch = 'new Date().getTime()'
    if command is None:
        func = ' '
    else:
        func = ', function(mod){mod.%s()}' % command
    return "check(); require(['pyojo/%s/'+%s]%s);" % (module, epoch, func)
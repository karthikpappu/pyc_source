# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/parser/cdeclarations.py
# Compiled at: 2019-12-10 16:20:40
# Size of source mod 2**32: 7965 bytes
__doc__ = "\nThis file contains classes that represent C declarations. cparser produces\ndeclarations in this format, and ctypesparser reformats them into a format that\nis not C-specific. The other modules don't need to touch these.\n"
__docformat__ = 'restructuredtext'

class Declaration(object):

    def __init__(self):
        self.declarator = None
        self.type = Type()
        self.storage = None
        self.attrib = Attrib()

    def __repr__(self):
        d = {'declarator':self.declarator, 
         'type':self.type}
        if self.storage:
            d['storage'] = self.storage
        l = ['%s=%r' % (k, v) for k, v in d.items()]
        return 'Declaration(%s)' % ', '.join(l)


class Declarator(object):
    pointer = None

    def __init__(self):
        self.identifier = None
        self.initializer = None
        self.array = None
        self.parameters = None
        self.bitfield = None
        self.attrib = Attrib()

    pointer = property(lambda self: None)

    def __repr__(self):
        s = self.identifier or ''
        if self.bitfield:
            s += ':%d' % self.bitfield
        if self.array:
            s += repr(self.array)
        if self.initializer:
            s += ' = %r' % self.initializer
        if self.parameters is not None:
            s += '(' + ', '.join([repr(p) for p in self.parameters]) + ')'
        return s


class Pointer(Declarator):
    pointer = None

    def __init__(self):
        super(Pointer, self).__init__()
        self.qualifiers = []

    def __repr__(self):
        q = ''
        if self.qualifiers:
            q = '<%s>' % ' '.join(self.qualifiers)
        return 'POINTER%s(%r)' % (q, self.pointer) + super(Pointer, self).__repr__()


class Array(object):

    def __init__(self):
        self.size = None
        self.array = None

    def __repr__(self):
        if self.size:
            a = '[%r]' % self.size
        else:
            a = '[]'
        if self.array:
            return repr(self.array) + a
        else:
            return a


class Parameter(object):

    def __init__(self):
        self.type = Type()
        self.storage = None
        self.declarator = None
        self.attrib = Attrib()

    def __repr__(self):
        d = {'type': self.type}
        if self.declarator:
            d['declarator'] = self.declarator
        if self.storage:
            d['storage'] = self.storage
        l = ['%s=%r' % (k, v) for k, v in d.items()]
        return 'Parameter(%s)' % ', '.join(l)


class Type(object):

    def __init__(self):
        self.qualifiers = []
        self.specifiers = []

    def __repr__(self):
        return ' '.join(self.qualifiers + [str(s) for s in self.specifiers])


class StorageClassSpecifier(str):

    def __repr__(self):
        return 'StorageClassSpecifier({})'.format(str(self))


class TypeSpecifier(str):

    def __repr__(self):
        return 'TypeSpecifier({})'.format(str(self))


class StructTypeSpecifier(object):

    def __init__(self, is_union, attrib, tag, declarations):
        self.is_union = is_union
        self.attrib = attrib
        self.tag = tag
        self.declarations = declarations
        self.filename = None
        self.lineno = -1

    def __repr__(self):
        if self.is_union:
            s = 'union'
        else:
            s = 'struct'
        if self.attrib:
            attrs = list()
            for attr, val in self.attrib.items():
                if val and type(val) == str:
                    attrs.append('{}({})'.format(attr, val))
                else:
                    if val:
                        attrs.append(attr)

            s += ' __attribute__(({}))'.format(','.join(attrs))
        if self.tag:
            s += ' %s' % self.tag
        if self.declarations:
            s += ' {%s}' % '; '.join([repr(d) for d in self.declarations])
        return s


class EnumSpecifier(object):

    def __init__(self, tag, enumerators, src=None):
        self.tag = tag
        self.enumerators = enumerators
        self.filename = None
        self.lineno = -1

    def __repr__(self):
        s = 'enum'
        if self.tag:
            s += ' %s' % self.tag
        if self.enumerators:
            s += ' {%s}' % ', '.join([repr(e) for e in self.enumerators])
        return s


class Enumerator(object):

    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def __repr__(self):
        s = self.name
        if self.expression:
            s += ' = %r' % self.expression
        return s


class TypeQualifier(str):

    def __repr__(self):
        return 'TypeQualifier({})'.format(str(self))


class PragmaPack(object):
    DEFAULT = None

    def __init__(self):
        self.current = self.DEFAULT
        self.stack = list()

    def set_default(self):
        self.current = self.DEFAULT

    def push(self, id=None, value=None):
        item = (
         id, self.current)
        self.stack.append(item)
        if value is not None:
            self.current = value

    def pop(self, id=None):
        if not self.stack:
            if id:
                return (
                 '#pragma pack(pop, {id}) encountered without matching #pragma pack(push, {id})'.format(id=id),)
            return '#pragma pack(pop) encountered without matching #pragma pack(push)'
        else:
            item = None
            err = None
            if id is not None:
                i = len(self.stack) - 1
                while i >= 0 and self.stack[i][0] != id:
                    i -= 1

                if i >= 0:
                    item = self.stack[i]
                    self.stack = self.stack[:i]
                else:
                    err = '#pragma pack(pop, {id}) encountered without matching #pragma pack(push, {id}); popped last'.format(id=id)
            if item is None:
                item = self.stack.pop()
            self.current = item[1]
            return err


pragma_pack = PragmaPack()

class Attrib(dict):

    def __init__(self, *a, **kw):
        if pragma_pack.current:
            super(Attrib, self).__init__(packed=True, aligned=[pragma_pack.current])
            (super(Attrib, self).update)(*a, **kw)
        else:
            (super(Attrib, self).__init__)(*a, **kw)
        self._unalias()

    def __repr__(self):
        return 'Attrib({})'.format(dict(self))

    def update(self, *a, **kw):
        (super(Attrib, self).update)(*a, **kw)
        self._unalias()

    def _unalias(self):
        """
        Check for any attribute aliases and remove leading/trailing '__'

        According to https://gcc.gnu.org/onlinedocs/gcc/Attribute-Syntax.html,
        an attribute can also be preceeded/followed by a double underscore
        ('__').
        """
        self.pop(None, None)
        fixes = [attr for attr in self if attr.startswith('__') if attr.endswith('__')]
        for attr in fixes:
            self[attr[2:len(attr) - 2]] = self.pop(attr)


def apply_specifiers(specifiers, declaration):
    """Apply specifiers to the declaration (declaration may be
    a Parameter instead)."""
    for s in specifiers:
        if type(s) == StorageClassSpecifier:
            if declaration.storage:
                pass
            declaration.storage = s
        else:
            if type(s) in (TypeSpecifier, StructTypeSpecifier, EnumSpecifier):
                declaration.type.specifiers.append(s)
            else:
                if type(s) == TypeQualifier:
                    declaration.type.qualifiers.append(s)
                else:
                    if type(s) == Attrib:
                        declaration.attrib.update(s)
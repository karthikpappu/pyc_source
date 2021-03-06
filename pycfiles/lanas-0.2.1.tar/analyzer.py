# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: kanzen/kanzen/analyzer.py
# Compiled at: 2012-08-23 22:01:30
from __future__ import absolute_import
import re, ast, _ast
from kanzen import model
MAX_THRESHOLD = 3

def expand_attribute(attribute):
    parent_name = []
    while attribute.__class__ is ast.Attribute:
        parent_name.append(attribute.attr)
        attribute = attribute.value

    name = ('.').join(reversed(parent_name))
    attribute_id = ''
    if attribute.__class__ is ast.Name:
        attribute_id = attribute.id
    elif attribute.__class__ is ast.Call:
        if attribute.func.__class__ is ast.Attribute:
            attribute_id = '%s.%s()' % (
             expand_attribute(attribute.func.value),
             attribute.func.attr)
        else:
            attribute_id = '%s()' % attribute.func.id
    name = attribute_id if name == '' else '%s.%s' % (attribute_id, name)
    return name


class Analyzer(object):
    __mapping = {_ast.Tuple: '__builtin__.tuple', 
       _ast.List: '__builtin__.list', 
       _ast.ListComp: '__builtin__.list', 
       _ast.Str: '__builtin__.str', 
       _ast.Dict: '__builtin__.dict', 
       _ast.Num: '__builtin__.int', 
       '_ast.Float': '__builtin__.float', 
       '_ast.Bool': '__builtin__.bool', 
       _ast.Call: model.late_resolution, 
       _ast.Name: model.late_resolution, 
       _ast.Attribute: model.late_resolution}

    def __init__(self):
        self._fixed_line = -1
        self.content = None
        return

    def _get_valid_module(self, source, retry=0):
        """Try to parse the module and fix some errors if it has some."""
        astModule = None
        try:
            astModule = ast.parse(source)
        except SyntaxError as reason:
            line = reason.lineno - 1
            if line != self._fixed_line:
                self._fixed_line = line
                new_line = ''
                indent = re.match('^\\s+', str(reason.text))
                if indent is not None:
                    new_line = indent.group() + 'pass'
                split_source = source.splitlines()
                split_source[line] = new_line
                source = ('\n').join(split_source)
                if retry < MAX_THRESHOLD:
                    astModule = self._get_valid_module(source, retry + 1)

        return astModule

    def analyze(self, source, old_module=None):
        """Analyze the source provided and create the proper structure."""
        astModule = self._get_valid_module(source)
        if astModule is None:
            return model.Module()
        else:
            self.content = source.split('\n')
            module = model.Module()
            for symbol in astModule.body:
                if symbol.__class__ is ast.Assign:
                    assigns = self._process_assign(symbol)[0]
                    module.add_attributes(assigns)
                elif symbol.__class__ in (ast.Import, ast.ImportFrom):
                    module.add_imports(self._process_import(symbol))
                elif symbol.__class__ is ast.ClassDef:
                    module.add_class(self._process_class(symbol))
                elif symbol.__class__ is ast.FunctionDef:
                    module.add_function(self._process_function(symbol))

            if old_module is not None:
                self._resolve_module(module, old_module)
            self.content = None
            return module

    def _resolve_module(self, module, old_module):
        module.update_classes(old_module.classes)
        module.update_functions(old_module.functions)
        module.update_attributes(old_module.attributes)

    def _assign_disambiguation(self, type_name, line_content):
        """Provide a specific builtin for the cases were ast doesn't work."""
        line = line_content.split('=')
        value = line[1].strip()
        if type_name is _ast.Num and '.' in value:
            type_name = '_ast.Float'
        elif value in ('True', 'False'):
            type_name = '_ast.Bool'
        elif value == 'None':
            type_name = None
        return type_name

    def _process_assign(self, symbol):
        """Process an ast.Assign object to extract the proper info."""
        assigns = []
        attributes = []
        for var in symbol.targets:
            type_value = symbol.value.__class__
            line_content = self.content[(symbol.lineno - 1)]
            if type_value in (_ast.Num, _ast.Name):
                type_value = self._assign_disambiguation(type_value, line_content)
                if type_value is None:
                    continue
            data_type = self.__mapping.get(type_value, model.late_resolution)
            if var.__class__ == ast.Attribute:
                data = (
                 var.attr, symbol.lineno, data_type, line_content,
                 type_value)
                attributes.append(data)
            elif var.__class__ == ast.Name:
                data = (
                 var.id, symbol.lineno, data_type, line_content,
                 type_value)
                assigns.append(data)

        return (assigns, attributes)

    def _process_import(self, symbol):
        """Process an ast.Import and ast.ImportFrom object to extract data."""
        imports = []
        for imp in symbol.names:
            if symbol.__class__ is ast.ImportFrom:
                module_name = '%s.%s' % (symbol.module, imp.name)
            else:
                module_name = imp.name
            name = imp.asname
            if name is None:
                name = imp.name
            imports.append((name, module_name))

        return imports

    def _process_class(self, symbol):
        """Process an ast.ClassDef object to extract data."""
        clazz = model.Clazz(symbol.name)
        for base in symbol.bases:
            if base == 'object':
                continue
            name = expand_attribute(base)
            clazz.add_parent(name)

        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                assigns = self._process_assign(sym)[0]
                clazz.add_attributes(assigns)
            elif sym.__class__ is ast.FunctionDef:
                clazz.add_function(self._process_function(sym, clazz))

        clazz.update_bases()
        clazz.update_with_parent_data()
        return clazz

    def _process_function(self, symbol, parent=None):
        """Process an ast.FunctionDef object to extract data."""
        function = model.Function(symbol.name)
        if symbol.args.vararg is not None:
            assign = model.Assign(symbol.args.vararg)
            assign.add_data(symbol.lineno, '__builtin__.list', None, None)
            function.args[assign.name] = assign
        if symbol.args.kwarg is not None:
            assign = model.Assign(symbol.args.kwarg)
            assign.add_data(symbol.lineno, '__builtin__.dict', None, None)
            function.args[assign.name] = assign
        defaults = []
        for value in symbol.args.defaults:
            type_value = value.__class__
            data_type = self.__mapping.get(type_value, None)
            defaults.append((data_type, type_value))

        for arg in reversed(symbol.args.args):
            if arg.id == 'self':
                continue
            assign = model.Assign(arg.id)
            data_type = (model.late_resolution, None)
            if defaults:
                data_type = defaults.pop()
            assign.add_data(symbol.lineno, data_type[0], None, data_type[1])
            function.args[assign.name] = assign

        for sym in symbol.body:
            if sym.__class__ is ast.Assign:
                result = self._process_assign(sym)
                function.add_attributes(result[0])
                if parent is not None:
                    parent.add_attributes(result[1])
            elif sym.__class__ is ast.FunctionDef:
                function.add_function(self._process_function(sym))
            if sym.__class__ is not ast.Assign:
                self._search_recursive_for_types(function, sym, parent)

        return function

    def _search_recursive_for_types(self, function, symbol, parent=None):
        """Search for return recursively inside the function."""
        if symbol.__class__ is ast.Assign:
            result = self._process_assign(symbol)
            function.add_attributes(result[0])
            if parent is not None:
                parent.add_attributes(result[1])
        elif symbol.__class__ is ast.Return:
            type_value = symbol.value.__class__
            lineno = symbol.lineno
            data_type = self.__mapping.get(type_value, None)
            line_content = self.content[(lineno - 1)]
            if data_type != model.late_resolution:
                type_value = None
            function.add_return(lineno, data_type, line_content, type_value)
        elif symbol.__class__ in (ast.If, ast.For, ast.TryExcept):
            for sym in symbol.body:
                self._search_recursive_for_types(function, sym, parent)

            for else_item in symbol.orelse:
                self._search_recursive_for_types(function, else_item, parent)

        elif symbol.__class__ is ast.TryFinally:
            for sym in symbol.body:
                self._search_recursive_for_types(function, sym, parent)

            for else_item in symbol.finalbody:
                self._search_recursive_for_types(function, else_item, parent)

        return
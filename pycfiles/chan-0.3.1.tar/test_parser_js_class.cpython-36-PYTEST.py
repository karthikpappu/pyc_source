# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/parser/test_parser_js_class.py
# Compiled at: 2017-07-02 17:19:36
# Size of source mod 2**32: 22754 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, pytest, champollion.parser.js_class

@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  '/**\n * Simple class\n */\nclass SimpleClass {}\n',
  {'test.module.SimpleClass': {'id':'test.module.SimpleClass', 
                               'module_id':'test.module', 
                               'exported':False, 
                               'default':False, 
                               'name':'SimpleClass', 
                               'parent':None, 
                               'line_number':4, 
                               'description':'Simple class', 
                               'method':{},  'attribute':{}}}),
 (
  "/**\n * Simple class with attributes\n */\nclass SimpleClass {\n    /**\n     * A static attribute.\n     */\n    static attribute1 = 42;\n\n    /**\n     * An object attribute.\n     */\n    attribute2 = {\n        key1: 'value1',\n        key2: 'value2',\n    };\n\n    /**\n     * A list attribute.\n     */\n    attribute3 = [\n        'value1',\n        'value2',\n    ];\n}\n",
  {'test.module.SimpleClass': {'id':'test.module.SimpleClass', 
                               'module_id':'test.module', 
                               'exported':False, 
                               'default':False, 
                               'name':'SimpleClass', 
                               'parent':None, 
                               'line_number':4, 
                               'description':'Simple class with attributes', 
                               'method':{},  'attribute':{'test.module.SimpleClass.attribute1':{'id':'test.module.SimpleClass.attribute1', 
                                 'class_id':'test.module.SimpleClass', 
                                 'module_id':'test.module', 
                                 'name':'attribute1', 
                                 'prefix':'static', 
                                 'value':'42', 
                                 'line_number':8, 
                                 'description':'A static attribute.'}, 
                                'test.module.SimpleClass.attribute2':{'id':'test.module.SimpleClass.attribute2', 
                                 'class_id':'test.module.SimpleClass', 
                                 'module_id':'test.module', 
                                 'name':'attribute2', 
                                 'prefix':None, 
                                 'value':"{ key1: 'value1', key2: 'value2', }", 
                                 'line_number':13, 
                                 'description':'An object attribute.'}, 
                                'test.module.SimpleClass.attribute3':{'id':'test.module.SimpleClass.attribute3', 
                                 'class_id':'test.module.SimpleClass', 
                                 'module_id':'test.module', 
                                 'name':'attribute3', 
                                 'prefix':None, 
                                 'value':"[ 'value1', 'value2', ]", 
                                 'line_number':21, 
                                 'description':'A list attribute.'}}}}),
 (
  '/**\n * Simple class with getter and setter\n */\nclass SimpleClass {\n    /**\n     * Get the name.\n     *\n     * .. warning::\n     *\n     *     The name is awesome\n     */\n    get name() {\n        return this.name;\n    }\n\n    /**\n     * Set the name.\n     *\n     * .. warning::\n     *\n     *     Keep the name awesome\n     */\n    set name(value) {\n        this.name = value;\n    }\n}\n',
  {'test.module.SimpleClass': {'id':'test.module.SimpleClass', 
                               'module_id':'test.module', 
                               'exported':False, 
                               'default':False, 
                               'name':'SimpleClass', 
                               'parent':None, 
                               'line_number':4, 
                               'description':'Simple class with getter and setter', 
                               'method':{'test.module.SimpleClass.name.get':{'id':'test.module.SimpleClass.name.get', 
                                 'class_id':'test.module.SimpleClass', 
                                 'module_id':'test.module', 
                                 'name':'name', 
                                 'prefix':'get', 
                                 'arguments':[],  'line_number':12, 
                                 'description':'Get the name.\n\n.. warning::\n\n    The name is awesome'}, 
                                'test.module.SimpleClass.name.set':{'id':'test.module.SimpleClass.name.set', 
                                 'class_id':'test.module.SimpleClass', 
                                 'module_id':'test.module', 
                                 'name':'name', 
                                 'prefix':'set', 
                                 'arguments':[
                                  'value'], 
                                 'line_number':23, 
                                 'description':'Set the name.\n\n.. warning::\n\n    Keep the name awesome'}}, 
                               'attribute':{}}}),
 (
  '/**\n * Simple class with constructor\n */\nclass SimpleClass {\n    constructor() {\n    }\n}\n',
  {'test.module.SimpleClass': {'id':'test.module.SimpleClass', 
                               'module_id':'test.module', 
                               'exported':False, 
                               'default':False, 
                               'name':'SimpleClass', 
                               'parent':None, 
                               'line_number':4, 
                               'description':'Simple class with constructor', 
                               'method':{'test.module.SimpleClass.constructor': {'id':'test.module.SimpleClass.constructor', 
                                                                        'class_id':'test.module.SimpleClass', 
                                                                        'module_id':'test.module', 
                                                                        'name':'constructor', 
                                                                        'prefix':None, 
                                                                        'arguments':[],  'line_number':5, 
                                                                        'description':None}}, 
                               'attribute':{}}}),
 (
  "/** Simple class expression */\nexport const CustomWelcome = class Welcome extends Base{\n    static expression= 'Hello World';\n\n    /** Say Hi to the world */\n    greeting() {\n        return this.expression;\n    }\n};\n\n",
  {'test.module.CustomWelcome': {'id':'test.module.CustomWelcome', 
                                 'module_id':'test.module', 
                                 'exported':True, 
                                 'default':False, 
                                 'name':'CustomWelcome', 
                                 'parent':'Base', 
                                 'line_number':2, 
                                 'description':'Simple class expression', 
                                 'method':{'test.module.CustomWelcome.greeting': {'id':'test.module.CustomWelcome.greeting', 
                                                                         'class_id':'test.module.CustomWelcome', 
                                                                         'module_id':'test.module', 
                                                                         'name':'greeting', 
                                                                         'prefix':None, 
                                                                         'arguments':[],  'line_number':6, 
                                                                         'description':'Say Hi to the world'}}, 
                                 'attribute':{'test.module.CustomWelcome.expression': {'id':'test.module.CustomWelcome.expression', 
                                                                           'class_id':'test.module.CustomWelcome', 
                                                                           'module_id':'test.module', 
                                                                           'name':'expression', 
                                                                           'prefix':'static', 
                                                                           'value':"'Hello World'", 
                                                                           'line_number':3, 
                                                                           'description':None}}}}),
 (
  '/** Simple class */\nclass Welcome {\n    /** Say Hi to someone */\n    greeting = who =>\n        `Hello ${who}!`;\n};\n\n',
  {'test.module.Welcome': {'id':'test.module.Welcome', 
                           'module_id':'test.module', 
                           'exported':False, 
                           'default':False, 
                           'name':'Welcome', 
                           'parent':None, 
                           'line_number':2, 
                           'description':'Simple class', 
                           'method':{'test.module.Welcome.greeting': {'id':'test.module.Welcome.greeting', 
                                                             'class_id':'test.module.Welcome', 
                                                             'module_id':'test.module', 
                                                             'name':'greeting', 
                                                             'prefix':None, 
                                                             'arguments':[
                                                              'who'], 
                                                             'line_number':4, 
                                                             'description':'Say Hi to someone'}}, 
                           'attribute':{'test.module.Welcome.greeting': {'id':'test.module.Welcome.greeting', 
                                                             'class_id':'test.module.Welcome', 
                                                             'module_id':'test.module', 
                                                             'name':'greeting', 
                                                             'prefix':None, 
                                                             'value':'who =>`Hello ${who}!`', 
                                                             'line_number':4, 
                                                             'description':'Say Hi to someone'}}}})],
  ids=[
 'valid class',
 'valid class with attributes',
 'valid class with getter and setter methods',
 'valid class with constructor',
 'valid exported class expression with mother class',
 'valid class with arrow-type method and a single argument'])
def test_get_class_environment(content, expected):
    """Return class environment from content."""
    @py_assert1 = champollion.parser
    @py_assert3 = @py_assert1.js_class
    @py_assert5 = @py_assert3.fetch_environment
    @py_assert8 = 'test.module'
    @py_assert10 = @py_assert5(content, @py_assert8)
    @py_assert12 = @py_assert10 == expected
    if not @py_assert12:
        @py_format14 = @pytest_ar._call_reprcompare(('==', ), (@py_assert12,), ('%(py11)s\n{%(py11)s = %(py6)s\n{%(py6)s = %(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.parser\n}.js_class\n}.fetch_environment\n}(%(py7)s, %(py9)s)\n} == %(py13)s', ), (@py_assert10, expected)) % {'py0':@pytest_ar._saferepr(champollion) if 'champollion' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(champollion) else 'champollion',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(@py_assert5),  'py7':@pytest_ar._saferepr(content) if 'content' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(content) else 'content',  'py9':@pytest_ar._saferepr(@py_assert8),  'py11':@pytest_ar._saferepr(@py_assert10),  'py13':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
        @py_format16 = 'assert %(py15)s' % {'py15': @py_format14}
        raise AssertionError(@pytest_ar._format_explanation(@py_format16))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 ('class AwesomeClass', None),
 ("const test= 'class AwesomeClass {}';", None),
 (
  'class AwesomeClass {}',
  {'export':None, 
   'default':None, 
   'class_name':'AwesomeClass', 
   'data_name':None, 
   'mother_class':None, 
   'start_regex':''}),
 (
  'class Awesome_Class extends module.Mother-Class{}',
  {'export':None, 
   'default':None, 
   'class_name':'Awesome_Class', 
   'data_name':None, 
   'mother_class':'module.Mother-Class', 
   'start_regex':''}),
 (
  'export default class AwesomeClass {}',
  {'export':'export ', 
   'default':'default ', 
   'class_name':'AwesomeClass', 
   'data_name':None, 
   'mother_class':None, 
   'start_regex':''}),
 (
  'export const MyClass1= class AwesomeClass {}',
  {'export':'export ', 
   'default':None, 
   'class_name':None, 
   'data_name':'MyClass1', 
   'mother_class':None, 
   'start_regex':''}),
 (
  'let MyClass1= class AwesomeClass extends Test2 {}',
  {'export':None, 
   'default':None, 
   'class_name':None, 
   'data_name':'MyClass1', 
   'mother_class':'Test2', 
   'start_regex':''})],
  ids=[
 'invalid class',
 'invalid class string',
 'valid class',
 'valid class with inheritance',
 'valid class exported by default',
 'valid class expression exported',
 'another valid class expression'])
def test_class_pattern(content, expected):
    """Match a class."""
    match = champollion.parser.js_class._CLASS_PATTERN.search(content)
    if expected is None:
        @py_assert2 = None
        @py_assert1 = match is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (match, @py_assert2)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = match.groupdict
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.groupdict\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  'valid-Method (arg1) {}',
  {'arguments':'arg1', 
   'method_name':'valid-Method', 
   'prefix':None, 
   'start_regex':''}),
 (
  'validMethod (\n    arg1, arg2, arg3, arg4, arg5,\n    arg6, arg7, arg8, arg9, arg10\n) {}',
  {'arguments':'arg1, arg2, arg3, arg4, arg5,\n    arg6, arg7, arg8, arg9, arg10', 
   'method_name':'validMethod', 
   'prefix':None, 
   'start_regex':''}),
 (
  'static valid_method() {}',
  {'arguments':'', 
   'method_name':'valid_method', 
   'prefix':'static ', 
   'start_regex':''}),
 (
  'get valid_method2(){}',
  {'arguments':'', 
   'method_name':'valid_method2', 
   'prefix':'get ', 
   'start_regex':''}),
 (
  "set validMethod( \n    arg1, arg2, arg3, arg4, arg5,\n){\n    console.log('test');\n}\n",
  {'arguments':'arg1, arg2, arg3, arg4, arg5,', 
   'method_name':'validMethod', 
   'prefix':'set ', 
   'start_regex':''}),
 ('function invalidMethod() {}', None),
 ('invalidMethod()', None),
 ('invalidMethod {}', None)],
  ids=[
 'valid method',
 'valid method with many arguments',
 'valid static method',
 'valid getter method',
 'valid setter method',
 "invalid method with 'function' statement",
 'invalid method without nested element',
 'invalid method without argument'])
def test_class_method_pattern(content, expected):
    """Match a class method."""
    match = champollion.parser.js_class._CLASS_METHOD_PATTERN.search(content)
    if expected is None:
        @py_assert2 = None
        @py_assert1 = match is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (match, @py_assert2)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = match.groupdict
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.groupdict\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  'arrow_type_method = (arg1) => {};',
  {'arguments':'arg1', 
   'single_argument':None, 
   'method_name':'arrow_type_method', 
   'prefix':None, 
   'start_regex':''}),
 (
  'arrow_type_method2 = arg1 => {};',
  {'arguments':None, 
   'single_argument':'arg1', 
   'method_name':'arrow_type_method2', 
   'prefix':None, 
   'start_regex':''}),
 (
  'static arrow_type_method = (arg1) => {};',
  {'arguments':'arg1', 
   'single_argument':None, 
   'method_name':'arrow_type_method', 
   'prefix':'static ', 
   'start_regex':''}),
 (
  'arrow_type_method3 = (arg1, arg2) => {};',
  {'arguments':'arg1, arg2', 
   'single_argument':None, 
   'method_name':'arrow_type_method3', 
   'prefix':None, 
   'start_regex':''}),
 (
  "arrow_type_method3 = (\n    arg1, arg2, arg3, arg4, arg5, agr6,\n    arg7\n) => {\n    console.log('youpi');\n};\n",
  {'arguments':'arg1, arg2, arg3, arg4, arg5, agr6,\n    arg7', 
   'single_argument':None, 
   'method_name':'arrow_type_method3', 
   'prefix':None, 
   'start_regex':''}),
 ('const arrow_type_method = (arg1) => {}', None),
 ("const test = 'arrow_type_method = (arg1) => {}'", None),
 ('(arg1) => {}', None),
 ('const arrow_type_method = arg1, arg2 => {};', None)],
  ids=[
 'valid method with one argument and brackets',
 'valid method with one argument and no brackets',
 'valid static method',
 'valid method with two arguments',
 'valid method with multiple arguments',
 'invalid arrow-type method with type',
 'invalid arrow-type method string',
 'invalid unassigned arrow-type method',
 'invalid arrow-type method with multiple argument and no brackets'])
def test_class_method_arrow_pattern(content, expected):
    """Match a class arrow-type method."""
    match = champollion.parser.js_class._CLASS_METHOD_ARROW_PATTERN.search(content)
    if expected is None:
        @py_assert2 = None
        @py_assert1 = match is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (match, @py_assert2)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = match.groupdict
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.groupdict\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None


@pytest.mark.parametrize(('content', 'expected'),
  [
 (
  'attribute_test1 = 42;',
  {'name':'attribute_test1', 
   'value':'42;', 
   'prefix':None, 
   'start_regex':''}),
 (
  "static attribute_test2 = {\n    key: 'value',\n};",
  {'name':'attribute_test2', 
   'value':"{\n    key: 'value',\n};", 
   'prefix':'static ', 
   'start_regex':''}),
 (
  'attribute_test3 = [\n    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n];',
  {'name':'attribute_test3', 
   'value':'[\n    1, 2, 3, 4, 5, 6, 7, 8, 9, 10,\n];', 
   'prefix':None, 
   'start_regex':''}),
 ("const test = 'static attribute = 42';", None),
 ('attribute_test1 = 42', None)],
  ids=[
 'valid attribute',
 'valid static object attribute',
 'valid static object attribute',
 'invalid attribute string',
 'invalid attribute with no semi-colons'])
def test_class_attribute_pattern(content, expected):
    """Match a class attribute."""
    match = champollion.parser.js_class._CLASS_ATTRIBUTE_PATTERN.search(content)
    if expected is None:
        @py_assert2 = None
        @py_assert1 = match is @py_assert2
        if not @py_assert1:
            @py_format4 = @pytest_ar._call_reprcompare(('is', ), (@py_assert1,), ('%(py0)s is %(py3)s', ), (match, @py_assert2)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py3':@pytest_ar._saferepr(@py_assert2)}
            @py_format6 = 'assert %(py5)s' % {'py5': @py_format4}
            raise AssertionError(@pytest_ar._format_explanation(@py_format6))
        @py_assert1 = @py_assert2 = None
    else:
        @py_assert1 = match.groupdict
        @py_assert3 = @py_assert1()
        @py_assert5 = @py_assert3 == expected
        if not @py_assert5:
            @py_format7 = @pytest_ar._call_reprcompare(('==', ), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.groupdict\n}()\n} == %(py6)s', ), (@py_assert3, expected)) % {'py0':@pytest_ar._saferepr(match) if 'match' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(match) else 'match',  'py2':@pytest_ar._saferepr(@py_assert1),  'py4':@pytest_ar._saferepr(@py_assert3),  'py6':@pytest_ar._saferepr(expected) if 'expected' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(expected) else 'expected'}
            @py_format9 = 'assert %(py8)s' % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert1 = @py_assert3 = @py_assert5 = None
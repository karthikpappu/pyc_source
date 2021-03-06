# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/symbol_table_builder_test.py
# Compiled at: 2020-03-05 05:49:41
# Size of source mod 2**32: 3455 bytes
import os, unittest
from antlr4 import *
from pynestml.meta_model.ast_nestml_compilation_unit import ASTNestMLCompilationUnit
from pynestml.meta_model.ast_source_location import ASTSourceLocation
from pynestml.generated.PyNestMLLexer import PyNestMLLexer
from pynestml.generated.PyNestMLParser import PyNestMLParser
from pynestml.symbol_table.symbol_table import SymbolTable
from pynestml.symbols.predefined_functions import PredefinedFunctions
from pynestml.symbols.predefined_types import PredefinedTypes
from pynestml.symbols.predefined_units import PredefinedUnits
from pynestml.symbols.predefined_variables import PredefinedVariables
from pynestml.utils.logger import Logger, LoggingLevel
from pynestml.visitors.ast_builder_visitor import ASTBuilderVisitor
from pynestml.visitors.ast_symbol_table_visitor import ASTSymbolTableVisitor
PredefinedUnits.register_units()
PredefinedTypes.register_types()
PredefinedFunctions.register_functions()
PredefinedVariables.register_variables()
SymbolTable.initialize_symbol_table(ASTSourceLocation(start_line=0, start_column=0, end_line=0, end_column=0))
Logger.init_logger(LoggingLevel.INFO)

class SymbolTableBuilderTest(unittest.TestCase):

    def test(self):
        for filename in os.listdir(os.path.realpath(os.path.join(os.path.dirname(__file__), os.path.join('..', 'models')))):
            if filename.endswith('.nestml'):
                input_file = FileStream(os.path.join(os.path.dirname(__file__), os.path.join(os.path.join('..', 'models'), filename)))
                lexer = PyNestMLLexer(input_file)
                stream = CommonTokenStream(lexer)
                stream.fill()
                parser = PyNestMLParser(stream)
                compilation_unit = parser.nestMLCompilationUnit()
                ast_builder_visitor = ASTBuilderVisitor(stream.tokens)
                ast = ast_builder_visitor.visit(compilation_unit)
                SymbolTable.initialize_symbol_table(ast.get_source_position())
                symbol_table_visitor = ASTSymbolTableVisitor()
                for neuron in ast.get_neuron_list():
                    neuron.accept(symbol_table_visitor)
                    SymbolTable.add_neuron_scope(name=neuron.get_name(), scope=neuron.get_scope())

                self.assertTrue(isinstance(ast, ASTNestMLCompilationUnit))


if __name__ == '__main__':
    unittest.main()
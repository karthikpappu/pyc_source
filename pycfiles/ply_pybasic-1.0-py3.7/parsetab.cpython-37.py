# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/parsetab.py
# Compiled at: 2019-04-20 19:58:08
# Size of source mod 2**32: 21601 bytes
_tabversion = '3.10'
_lr_method = 'LALR'
_lr_signature = 'leftCOMMAleftANDORleftEQUALSNOT_EQUALGREATER_THANLESS_THANEQUAL_GREATER_THANEQUAL_LESS_THANleftASleftPLUSMINUSleftTIMESDIVIDEMODleftEXPrightUMINUSNOTAND AS COMMA CONTINUE DECIMAL DEFUN DIM DIVIDE DO ELSE ELSEIF END EQUALS EQUAL_GREATER_THAN EQUAL_LESS_THAN EXACTDIV EXIT EXP FOR FUNCTION GREATER_THAN ID IF INTEGER LBRACE LESS_THAN LET LOOP LPAREN MINUS MOD NEXT NOT NOT_EQUAL OR PLUS RBRACE RETURN RPAREN STEP STRING SUB THEN TIMES TO UNTIL USE WEND WHILE\n    statement : assignment\n              | declaration\n              | expression\n              | funcall\n              | control\n              | return\n              | defun_statement\n    \n    statement : block_begin\n    \n    statement : block_end\n    \n    statement : if_block_begin\n              | elseif_block_begin\n              | else_statement\n    \n    args_list : args_list COMMA expression\n              | expression\n    \n    params_list : params_list COMMA ID\n               | ID\n    \n    defun_statement : DEFUN ID LPAREN params_list RPAREN EQUALS expression\n    \n    funcall : ID args_list\n    \n    assignment : ID EQUALS expression\n               | LET ID EQUALS expression\n               | ID LPAREN expression RPAREN EQUALS expression\n    \n    declaration : declare_array\n    \n    declare_array : DIM ID LPAREN expression RPAREN AS ID\n    \n    rel_expression : expression GREATER_THAN expression\n                   | expression LESS_THAN expression\n                   | expression EQUAL_GREATER_THAN expression\n                   | expression EQUAL_LESS_THAN expression\n                   | expression EQUALS expression\n                   | expression NOT_EQUAL expression\n                   | rel_expression AND rel_expression\n                   | rel_expression OR rel_expression\n                   | LPAREN rel_expression RPAREN\n                   | NOT rel_expression\n    \n    expression : expression PLUS expression\n               | expression MINUS expression\n               | expression TIMES expression\n               | expression DIVIDE expression\n               | expression EXACTDIV expression\n               | expression MOD expression\n               | expression AS expression\n               | expression EXP expression\n               | MINUS expression %prec UMINUS\n               | LPAREN expression RPAREN\n    \n    expression : ID LPAREN RPAREN\n               | ID LPAREN args_list RPAREN\n    \n    expression : INTEGER\n               | DECIMAL\n    \n    expression : STRING\n    \n    expression : ID\n    \n    expression : LBRACE args_list RBRACE\n    \n    block_begin : while_block_begin\n                | for_block_begin\n                | do_block_begin\n                | function_block_begin\n    \n    if_block_begin : IF rel_expression THEN\n    \n    else_statement : ELSE\n    \n    elseif_block_begin : ELSEIF rel_expression THEN\n    \n    while_block_begin : WHILE rel_expression\n    \n    do_block_begin : DO\n    \n    for_block_begin : FOR ID EQUALS expression TO expression\n                    | FOR ID EQUALS expression TO expression STEP expression\n    \n    function_block_begin : SUB ID LPAREN params_list RPAREN\n                         | FUNCTION ID LPAREN params_list RPAREN\n    \n    block_end : END IF\n    \n    block_end : END WHILE\n              | WEND\n    \n    block_end : END FOR\n              | NEXT ID\n    \n    block_end : LOOP\n              | LOOP WHILE rel_expression\n              | LOOP UNTIL rel_expression\n    \n    block_end : END SUB\n              | END FUNCTION\n    \n    return : RETURN\n           | RETURN expression\n    \n    control : EXIT WHILE\n            | EXIT DO\n            | EXIT FOR\n    \n    control : CONTINUE WHILE\n            | CONTINUE DO\n            | CONTINUE FOR\n    \n    statement : USE ID\n    '
_lr_action_items = {'USE':(
  [
   0], [14]), 
 'ID':([0, 14, 15, 16, 17, 19, 23, 25, 27, 29, 30, 36, 38, 40, 41, 42, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 118, 122, 123, 125, 145, 146, 148, 154, 156, 157], [15, 53, 54, 59, 54, 54, 54, 54, 70, 54, 75, 54, 82, 85, 86, 54, 88, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 54, 140, 140, 140, 54, 54, 54, 155, 54, 159, 54]),  'LET':([0], [16]),  'MINUS':([0, 4, 15, 17, 19, 20, 21, 22, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 56, 57, 60, 61, 67, 68, 69, 74, 83, 84, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 115, 117, 125, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 145, 146, 152, 153, 154, 157, 158, 160], [19, 46, 19, 19, 19, -46, -47, -48, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, 19, -49, 19, 46, 19, 46, -42, 46, 19, 19, 46, 19, 19, -34, -35, -36, -37, 46, -39, 46, -41, 19, 46, 46, -44, 19, 19, -43, -50, 19, 19, 19, 19, 19, 19, 19, 19, 46, 19, 19, -43, -45, 46, 46, 46, 46, 46, 46, 46, 46, 46, 46, 19, 19, 46, 46, 19, 19, 46, 46]),  'LPAREN':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 54, 55, 57, 68, 69, 75, 83, 84, 85, 86, 88, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [17, 57, 17, 17, 17, 68, 17, 68, 68, 17, 17, 17, 17, 17, 17, 17, 17, 97, 17, 17, 68, 68, 118, 68, 68, 122, 123, 125, 17, 17, 17, 68, 68, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17]),  'INTEGER':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20]),  'DECIMAL':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21, 21]),  'STRING':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22, 22]),  'LBRACE':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23, 23]),  'EXIT':([0], [24]),  'CONTINUE':([0], [28]),  'RETURN':([0], [29]),  'DEFUN':([0], [30]),  'END':([0], [35]),  'WEND':([0], [37]),  'NEXT':([0], [38]),  'LOOP':([0], [39]),  'IF':([0, 35], [36, 76]),  'ELSEIF':([0], [42]),  'ELSE':([0], [43]),  'DIM':([0], [44]),  'WHILE':([0, 24, 28, 35, 39], [25, 63, 71, 77, 83]),  'FOR':([0, 24, 28, 35], [27, 65, 73, 78]),  'DO':([0, 24, 28], [26, 64, 72]),  'SUB':([0, 35], [40, 79]),  'FUNCTION':([0, 35], [41, 80]),  '$end':([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 15, 18, 20, 21, 22, 26, 29, 31, 32, 33, 34, 37, 39, 43, 53, 54, 56, 58, 61, 63, 64, 65, 66, 71, 72, 73, 74, 76, 77, 78, 79, 80, 82, 89, 90, 91, 92, 93, 94, 95, 96, 98, 100, 104, 105, 116, 119, 120, 121, 124, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 149, 150, 152, 153, 158, 159, 160], [0, -1, -2, -3, -4, -5, -6, -7, -8, -9, -10, -11, -12, -49, -22, -46, -47, -48, -59, -74, -51, -52, -53, -54, -66, -69, -56, -82, -49, -14, -18, -42, -76, -77, -78, -58, -79, -80, -81, -75, -64, -65, -67, -72, -73, -68, -34, -35, -36, -37, -38, -39, -40, -41, -19, -44, -43, -50, -33, -55, -70, -71, -57, -43, -45, -13, -20, -30, -31, -24, -25, -26, -27, -28, -29, -32, -62, -63, -21, -60, -17, -23, -61]),  'PLUS':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [45, -49, -46, -47, -48, -49, 45, 45, -42, 45, 45, -34, -35, -36, -37, 45, -39, 45, -41, 45, 45, -44, -43, -50, 45, -43, -45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45, 45]),  'TIMES':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [47, -49, -46, -47, -48, -49, 47, 47, -42, 47, 47, 47, 47, -36, -37, 47, -39, 47, -41, 47, 47, -44, -43, -50, 47, -43, -45, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47, 47]),  'DIVIDE':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [48, -49, -46, -47, -48, -49, 48, 48, -42, 48, 48, 48, 48, -36, -37, 48, -39, 48, -41, 48, 48, -44, -43, -50, 48, -43, -45, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48, 48]),  'EXACTDIV':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [49, -49, -46, -47, -48, -49, 49, 49, -42, 49, 49, -34, -35, -36, -37, 49, -39, -40, -41, 49, 49, -44, -43, -50, 49, -43, -45, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49, 49]),  'MOD':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [50, -49, -46, -47, -48, -49, 50, 50, -42, 50, 50, 50, 50, -36, -37, 50, -39, 50, -41, 50, 50, -44, -43, -50, 50, -43, -45, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50]),  'AS':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 151, 152, 153, 158, 160], [51, -49, -46, -47, -48, -49, 51, 51, -42, 51, 51, -34, -35, -36, -37, 51, -39, -40, -41, 51, 51, -44, -43, -50, 51, -43, -45, 51, 51, 51, 51, 51, 51, 51, 51, 51, 51, 156, 51, 51, 51, 51]),  'EXP':([4, 15, 20, 21, 22, 54, 56, 60, 61, 67, 74, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 100, 104, 105, 115, 126, 127, 128, 129, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160], [52, -49, -46, -47, -48, -49, 52, 52, -42, 52, 52, 52, 52, 52, 52, 52, 52, 52, -41, 52, 52, -44, -43, -50, 52, -43, -45, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52, 52]),  'EQUALS':([15, 20, 21, 22, 54, 59, 61, 67, 70, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 126, 127, 147], [55, -46, -47, -48, -49, 103, -42, 112, 117, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 112, 145, -45, 154]),  'COMMA':([20, 21, 22, 54, 56, 58, 61, 62, 89, 90, 91, 92, 93, 94, 95, 96, 99, 100, 101, 104, 105, 126, 127, 128, 140, 141, 142, 143, 155], [-46, -47, -48, -49, -14, 102, -42, 102, -34, -35, -36, -37, -38, -39, -40, -41, -14, -44, 102, -43, -50, -43, -45, -13, -16, 148, 148, 148, -15]),  'RPAREN':([20, 21, 22, 54, 56, 57, 60, 61, 89, 90, 91, 92, 93, 94, 95, 96, 97, 99, 100, 101, 104, 105, 114, 115, 116, 127, 128, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 141, 142, 143, 144, 155], [-46, -47, -48, -49, -14, 100, 104, -42, -34, -35, -36, -37, -38, -39, -40, -41, 100, 126, -44, 127, -43, -50, 138, 104, -33, -45, -13, -30, -31, -24, -25, -26, -27, -28, -29, -32, -16, 147, 149, 150, 151, -15]),  'RBRACE':([20, 21, 22, 54, 56, 61, 62, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 127, 128], [-46, -47, -48, -49, -14, -42, 105, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, -45, -13]),  'GREATER_THAN':([20, 21, 22, 54, 61, 67, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 127], [-46, -47, -48, -49, -42, 108, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 108, -45]),  'LESS_THAN':([20, 21, 22, 54, 61, 67, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 127], [-46, -47, -48, -49, -42, 109, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 109, -45]),  'EQUAL_GREATER_THAN':([20, 21, 22, 54, 61, 67, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 127], [-46, -47, -48, -49, -42, 110, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 110, -45]),  'EQUAL_LESS_THAN':([20, 21, 22, 54, 61, 67, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 127], [-46, -47, -48, -49, -42, 111, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 111, -45]),  'NOT_EQUAL':([20, 21, 22, 54, 61, 67, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 115, 127], [-46, -47, -48, -49, -42, 113, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 113, -45]),  'AND':([20, 21, 22, 54, 61, 66, 81, 87, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 114, 116, 120, 121, 127, 130, 131, 132, 133, 134, 135, 136, 137, 138], [-46, -47, -48, -49, -42, 106, 106, 106, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 106, -33, 106, 106, -45, -30, -31, -24, -25, -26, -27, -28, -29, -32]),  'OR':([20, 21, 22, 54, 61, 66, 81, 87, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 114, 116, 120, 121, 127, 130, 131, 132, 133, 134, 135, 136, 137, 138], [-46, -47, -48, -49, -42, 107, 107, 107, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, 107, -33, 107, 107, -45, -30, -31, -24, -25, -26, -27, -28, -29, -32]),  'THEN':([20, 21, 22, 54, 61, 81, 87, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 116, 127, 130, 131, 132, 133, 134, 135, 136, 137, 138], [-46, -47, -48, -49, -42, 119, 124, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, -33, -45, -30, -31, -24, -25, -26, -27, -28, -29, -32]),  'TO':([20, 21, 22, 54, 61, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 127, 139], [-46, -47, -48, -49, -42, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, -45, 146]),  'STEP':([20, 21, 22, 54, 61, 89, 90, 91, 92, 93, 94, 95, 96, 100, 104, 105, 127, 153], [-46, -47, -48, -49, -42, -34, -35, -36, -37, -38, -39, -40, -41, -44, -43, -50, -45, 157]),  'NOT':([25, 36, 42, 68, 69, 83, 84, 106, 107], [69, 69, 69, 69, 69, 69, 69, 69, 69]),  'UNTIL':([39], [84])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if _x not in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'statement':(
  [
   0], [1]), 
 'assignment':([0], [2]),  'declaration':([0], [3]),  'expression':([0, 15, 17, 19, 23, 25, 29, 36, 42, 45, 46, 47, 48, 49, 50, 51, 52, 55, 57, 68, 69, 83, 84, 97, 102, 103, 106, 107, 108, 109, 110, 111, 112, 113, 117, 125, 145, 146, 154, 157], [4, 56, 60, 61, 56, 67, 74, 67, 67, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 115, 67, 67, 67, 56, 128, 129, 67, 67, 132, 133, 134, 135, 136, 137, 139, 144, 152, 153, 158, 160]),  'funcall':([0], [5]),  'control':([0], [6]),  'return':([0], [7]),  'defun_statement':([0], [8]),  'block_begin':([0], [9]),  'block_end':([0], [10]),  'if_block_begin':([0], [11]),  'elseif_block_begin':([0], [12]),  'else_statement':([0], [13]),  'declare_array':([0], [18]),  'while_block_begin':([0], [31]),  'for_block_begin':([0], [32]),  'do_block_begin':([0], [33]),  'function_block_begin':([0], [34]),  'args_list':([15, 23, 57, 97], [58, 62, 101, 101]),  'rel_expression':([25, 36, 42, 68, 69, 83, 84, 106, 107], [66, 81, 87, 114, 116, 120, 121, 130, 131]),  'params_list':([118, 122, 123], [141, 142, 143])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if _x not in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 ("S' -> statement", "S'", 1, None, None, None),
 ('statement -> assignment', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 30),
 ('statement -> declaration', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 31),
 ('statement -> expression', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 32),
 ('statement -> funcall', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 33),
 ('statement -> control', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 34),
 ('statement -> return', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 35),
 ('statement -> defun_statement', 'statement', 1, 'p_singleline_statement', 'basic_yacc.py',
 36),
 ('statement -> block_begin', 'statement', 1, 'p_multiline_begin_statement', 'basic_yacc.py',
 44),
 ('statement -> block_end', 'statement', 1, 'p_multiline_end_statement', 'basic_yacc.py',
 53),
 ('statement -> if_block_begin', 'statement', 1, 'p_if_else_elseif', 'basic_yacc.py',
 60),
 ('statement -> elseif_block_begin', 'statement', 1, 'p_if_else_elseif', 'basic_yacc.py',
 61),
 ('statement -> else_statement', 'statement', 1, 'p_if_else_elseif', 'basic_yacc.py',
 62),
 ('args_list -> args_list COMMA expression', 'args_list', 3, 'p_args_list', 'basic_yacc.py',
 68),
 ('args_list -> expression', 'args_list', 1, 'p_args_list', 'basic_yacc.py', 69),
 ('params_list -> params_list COMMA ID', 'params_list', 3, 'p_param_list', 'basic_yacc.py',
 79),
 ('params_list -> ID', 'params_list', 1, 'p_param_list', 'basic_yacc.py', 80),
 ('defun_statement -> DEFUN ID LPAREN params_list RPAREN EQUALS expression', 'defun_statement',
 7, 'p_defun', 'basic_yacc.py', 90),
 ('funcall -> ID args_list', 'funcall', 2, 'p_funcall', 'basic_yacc.py', 105),
 ('assignment -> ID EQUALS expression', 'assignment', 3, 'p_assignment', 'basic_yacc.py',
 112),
 ('assignment -> LET ID EQUALS expression', 'assignment', 4, 'p_assignment', 'basic_yacc.py',
 113),
 ('assignment -> ID LPAREN expression RPAREN EQUALS expression', 'assignment', 6, 'p_assignment',
 'basic_yacc.py', 114),
 ('declaration -> declare_array', 'declaration', 1, 'p_declare', 'basic_yacc.py', 125),
 ('declare_array -> DIM ID LPAREN expression RPAREN AS ID', 'declare_array', 7, 'p_declare_array',
 'basic_yacc.py', 131),
 ('rel_expression -> expression GREATER_THAN expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 137),
 ('rel_expression -> expression LESS_THAN expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 138),
 ('rel_expression -> expression EQUAL_GREATER_THAN expression', 'rel_expression', 3,
 'p_rel_expression', 'basic_yacc.py', 139),
 ('rel_expression -> expression EQUAL_LESS_THAN expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 140),
 ('rel_expression -> expression EQUALS expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 141),
 ('rel_expression -> expression NOT_EQUAL expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 142),
 ('rel_expression -> rel_expression AND rel_expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 143),
 ('rel_expression -> rel_expression OR rel_expression', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 144),
 ('rel_expression -> LPAREN rel_expression RPAREN', 'rel_expression', 3, 'p_rel_expression',
 'basic_yacc.py', 145),
 ('rel_expression -> NOT rel_expression', 'rel_expression', 2, 'p_rel_expression', 'basic_yacc.py',
 146),
 ('expression -> expression PLUS expression', 'expression', 3, 'p_expression_calc',
 'basic_yacc.py', 171),
 ('expression -> expression MINUS expression', 'expression', 3, 'p_expression_calc',
 'basic_yacc.py', 172),
 ('expression -> expression TIMES expression', 'expression', 3, 'p_expression_calc',
 'basic_yacc.py', 173),
 ('expression -> expression DIVIDE expression', 'expression', 3, 'p_expression_calc',
 'basic_yacc.py', 174),
 ('expression -> expression EXACTDIV expression', 'expression', 3, 'p_expression_calc',
 'basic_yacc.py', 175),
 ('expression -> expression MOD expression', 'expression', 3, 'p_expression_calc', 'basic_yacc.py',
 176),
 ('expression -> expression AS expression', 'expression', 3, 'p_expression_calc', 'basic_yacc.py',
 177),
 ('expression -> expression EXP expression', 'expression', 3, 'p_expression_calc', 'basic_yacc.py',
 178),
 ('expression -> MINUS expression', 'expression', 2, 'p_expression_calc', 'basic_yacc.py',
 179),
 ('expression -> LPAREN expression RPAREN', 'expression', 3, 'p_expression_calc', 'basic_yacc.py',
 180),
 ('expression -> ID LPAREN RPAREN', 'expression', 3, 'p_inline_funcall', 'basic_yacc.py',
 207),
 ('expression -> ID LPAREN args_list RPAREN', 'expression', 4, 'p_inline_funcall', 'basic_yacc.py',
 208),
 ('expression -> INTEGER', 'expression', 1, 'p_expression_number', 'basic_yacc.py',
 218),
 ('expression -> DECIMAL', 'expression', 1, 'p_expression_number', 'basic_yacc.py',
 219),
 ('expression -> STRING', 'expression', 1, 'p_expression_string', 'basic_yacc.py', 225),
 ('expression -> ID', 'expression', 1, 'p_expression_id', 'basic_yacc.py', 231),
 ('expression -> LBRACE args_list RBRACE', 'expression', 3, 'p_expression_array', 'basic_yacc.py',
 237),
 ('block_begin -> while_block_begin', 'block_begin', 1, 'p_block_begin', 'basic_yacc.py',
 244),
 ('block_begin -> for_block_begin', 'block_begin', 1, 'p_block_begin', 'basic_yacc.py',
 245),
 ('block_begin -> do_block_begin', 'block_begin', 1, 'p_block_begin', 'basic_yacc.py',
 246),
 ('block_begin -> function_block_begin', 'block_begin', 1, 'p_block_begin', 'basic_yacc.py',
 247),
 ('if_block_begin -> IF rel_expression THEN', 'if_block_begin', 3, 'p_if_block_begin',
 'basic_yacc.py', 253),
 ('else_statement -> ELSE', 'else_statement', 1, 'p_else', 'basic_yacc.py', 269),
 ('elseif_block_begin -> ELSEIF rel_expression THEN', 'elseif_block_begin', 3, 'p_elseif',
 'basic_yacc.py', 288),
 ('while_block_begin -> WHILE rel_expression', 'while_block_begin', 2, 'p_while_block_begin',
 'basic_yacc.py', 307),
 ('do_block_begin -> DO', 'do_block_begin', 1, 'p_do_block_begin', 'basic_yacc.py',
 318),
 ('for_block_begin -> FOR ID EQUALS expression TO expression', 'for_block_begin', 6,
 'p_for_block_begin', 'basic_yacc.py', 329),
 ('for_block_begin -> FOR ID EQUALS expression TO expression STEP expression', 'for_block_begin',
 8, 'p_for_block_begin', 'basic_yacc.py', 330),
 ('function_block_begin -> SUB ID LPAREN params_list RPAREN', 'function_block_begin',
 5, 'p_function_block_begin', 'basic_yacc.py', 344),
 ('function_block_begin -> FUNCTION ID LPAREN params_list RPAREN', 'function_block_begin',
 5, 'p_function_block_begin', 'basic_yacc.py', 345),
 ('block_end -> END IF', 'block_end', 2, 'p_if_block_end', 'basic_yacc.py', 358),
 ('block_end -> END WHILE', 'block_end', 2, 'p_while_block_end', 'basic_yacc.py', 366),
 ('block_end -> WEND', 'block_end', 1, 'p_while_block_end', 'basic_yacc.py', 367),
 ('block_end -> END FOR', 'block_end', 2, 'p_for_block_end', 'basic_yacc.py', 375),
 ('block_end -> NEXT ID', 'block_end', 2, 'p_for_block_end', 'basic_yacc.py', 376),
 ('block_end -> LOOP', 'block_end', 1, 'p_do_block_end', 'basic_yacc.py', 387),
 ('block_end -> LOOP WHILE rel_expression', 'block_end', 3, 'p_do_block_end', 'basic_yacc.py',
 388),
 ('block_end -> LOOP UNTIL rel_expression', 'block_end', 3, 'p_do_block_end', 'basic_yacc.py',
 389),
 ('block_end -> END SUB', 'block_end', 2, 'p_function_block_end', 'basic_yacc.py', 404),
 ('block_end -> END FUNCTION', 'block_end', 2, 'p_function_block_end', 'basic_yacc.py',
 405),
 ('return -> RETURN', 'return', 1, 'p_return', 'basic_yacc.py', 414),
 ('return -> RETURN expression', 'return', 2, 'p_return', 'basic_yacc.py', 415),
 ('control -> EXIT WHILE', 'control', 2, 'p_control_exit', 'basic_yacc.py', 431),
 ('control -> EXIT DO', 'control', 2, 'p_control_exit', 'basic_yacc.py', 432),
 ('control -> EXIT FOR', 'control', 2, 'p_control_exit', 'basic_yacc.py', 433),
 ('control -> CONTINUE WHILE', 'control', 2, 'p_control_continue', 'basic_yacc.py',
 443),
 ('control -> CONTINUE DO', 'control', 2, 'p_control_continue', 'basic_yacc.py', 444),
 ('control -> CONTINUE FOR', 'control', 2, 'p_control_continue', 'basic_yacc.py', 445),
 ('statement -> USE ID', 'statement', 2, 'p_use_statement', 'basic_yacc.py', 455)]
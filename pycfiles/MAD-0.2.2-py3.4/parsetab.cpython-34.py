# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mad\parsetab.py
# Compiled at: 2016-04-27 16:21:37
# Size of source mod 2**32: 10287 bytes
_tabversion = '3.8'
_lr_method = 'LALR'
_lr_signature = 'E80E6141C60D1D8ED5A8885F8DCFC64A'
_lr_action_items = {'SERVICE': ([0, 3, 4, 5, 23, 25, 87], [1, -4, -5, 1, -7, -6, -25]),  'TIMEOUT': ([99, 117], [111, 111]),  'FAIL': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [36, 36, -37, 36, -33, -30, -31, -34, -32, -29, -36, 36, -35, 36, -38, -48, -54, -46, 36, -39, -49, -47]),  'TAIL_DROP': ([50], [65]),  'QUERY': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [37, 37, -37, 37, -33, -30, -31, -34, -32, -29, -36, 37, -35, 37, -38, -48, -54, -46, 37, -39, -49, -47]),  'COLON': ([27, 34, 68, 69, 76, 77, 111, 112, 115], [50, 54, 84, 85, 90, 91, 119, 120, 123]),  'CLOSE_CURLY_BRACKET': ([14, 17, 19, 20, 29, 30, 31, 32, 33, 36, 38, 41, 42, 43, 44, 45, 46, 49, 53, 55, 56, 58, 61, 62, 66, 67, 70, 71, 72, 73, 75, 80, 83, 86, 88, 89, 94, 95, 98, 105, 107, 108, 109, 110, 114, 118, 122, 125, 126, 127, 129, 130, 131], [-24, 23, 25, -23, -11, 52, -12, -13, -10, -37, -28, -33, -30, -31, 62, -34, -32, -29, -9, 73, -36, -27, -35, -26, -16, 83, -20, -15, -14, 87, 89, 94, -18, -19, -38, -48, -54, -46, -21, -17, -43, -41, -42, 118, 122, -39, -49, -40, -44, -45, 131, -22, -47]),  'OPEN_SQUARE_BRACKET': ([84], [97]),  'CLOSE_BRACKET': ([78, 79, 96, 101, 103, 121, 128], [92, -51, 105, -52, -50, 128, -53]),  'NUMBER': ([18, 36, 40, 82, 85, 91, 97, 113, 116, 119, 120, 123], [24, 56, 61, 96, 98, 101, 106, 121, 124, 126, 127, 129]),  'AUTOSCALING': ([22, 29, 31, 32, 33, 66, 71, 72, 83, 105], [28, -11, -12, -13, 28, -16, -15, -14, -18, -17]),  'CLOSE_SQUARE_BRACKET': ([124], [130]),  'RETRY': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [39, 39, -37, 39, -33, -30, -31, -34, -32, -29, -36, 39, -35, 39, -38, -48, -54, -46, 39, -39, -49, -47]),  'THINK': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [40, 40, -37, 40, -33, -30, -31, -34, -32, -29, -36, 40, -35, 40, -38, -48, -54, -46, 40, -39, -49, -47]),  'PERIOD': ([51, 70, 98, 130], [69, 69, -21, -22]),  'IDENTIFIER': ([1, 7, 15, 37, 48, 74, 81, 90], [8, 10, 21, 57, 64, 88, 95, 100]),  'PRIORITY': ([99, 104, 117], [112, 115, 112]),  'CLIENT': ([0, 3, 4, 5, 23, 25, 87], [7, -4, -5, 7, -7, -6, -25]),  'OPERATION': ([11, 13, 14, 52, 62], [15, 15, 15, -8, -26]),  'COMMA': ([79, 101, 106, 107, 108, 109, 126, 127, 128], [93, -52, 116, -43, 117, -42, -44, -45, -53]),  'FIFO': ([54], [71]),  'THROTTLING': ([22, 29, 31, 32, 33, 66, 71, 72, 83, 105], [27, -11, -12, -13, 27, -16, -15, -14, -18, -17]),  'NONE': ([50], [66]),  'EVERY': ([12], [18]),  'INVOKE': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [48, 48, -37, 48, -33, -30, -31, -34, -32, -29, -36, 48, -35, 48, -38, -48, -54, -46, 48, -39, -49, -47]),  'LIMITS': ([51, 70, 98, 130], [68, 68, -21, -22]),  'OPEN_CURLY_BRACKET': ([8, 10, 16, 21, 24, 28, 39, 47, 88, 92, 95], [11, 12, 22, 26, 35, 51, 59, 63, 99, 102, 104]),  'SLASH': ([57, 64], [74, 81]),  'IGNORE': ([26, 35, 36, 38, 41, 42, 43, 45, 46, 49, 56, 59, 61, 63, 88, 89, 94, 95, 102, 118, 122, 131], [47, 47, -37, 47, -33, -30, -31, -34, -32, -29, -36, 47, -35, 47, -38, -48, -54, -46, 47, -39, -49, -47]),  '$end': ([2, 3, 4, 5, 6, 9, 23, 25, 87], [0, -4, -5, -3, -1, -2, -7, -6, -25]),  'LIMIT': ([60, 93], [77, 77]),  'OPEN_BRACKET': ([39, 65, 100], [60, 82, 113]),  'QUEUE': ([22, 29, 31, 32, 33, 66, 71, 72, 83, 105],
           [34, -11, -12, -13, 34,
            -16, -15, -14, -18, -17]), 
 'DELAY': ([60, 93], [76, 76]),  'SETTINGS': ([11], [16]),  'LIFO': ([54], [72])}
_lr_action = {}
for _k, _v in _lr_action_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_action:
            _lr_action[_x] = {}
        _lr_action[_x][_k] = _y

del _lr_action_items
_lr_goto_items = {'priority': ([99, 117], [107, 107]),  'unit': ([0], [2]),  'ignore': ([26, 35, 38, 59, 63, 102], [45, 45, 45, 45, 45, 45]),  'retry_option_list': ([60, 93], [78, 103]),  'queue': ([22, 33], [29, 29]),  'autoscaling': ([22, 33], [31, 31]),  'settings': ([11], [13]),  'action': ([26, 35, 38, 59, 63, 102], [38, 38, 38, 38, 38, 38]),  'setting': ([22, 33], [33, 33]),  'definition': ([0, 5], [5, 5]),  'retry': ([26, 35, 38, 59, 63, 102], [41, 41, 41, 41, 41, 41]),  'fail': ([26, 35, 38, 59, 63, 102], [46, 46, 46, 46, 46, 46]),  'think': ([26, 35, 38, 59, 63, 102], [43, 43, 43, 43, 43, 43]),  'definition_list': ([0, 5], [6, 9]),  'define_operation': ([11, 13, 14], [14, 14, 14]),  'action_list': ([26, 35, 38, 59, 63, 102], [44, 55, 58, 75, 80, 114]),  'operation_list': ([11, 13, 14], [17, 19, 20]),  'define_service': ([0, 5], [3, 3]),  'timeout': ([99, 117], [109, 109]),  'query_option_list': ([99, 117], [110, 125]),  'autoscaling_setting_list': ([51, 70], [67, 86]),  'setting_list': ([22, 33], [30, 53]),  'query': ([26, 35, 38, 59, 63, 102], [42, 42, 42, 42, 42, 42]),  'throttling': ([22, 33], [32, 32]),  'query_option': ([99, 117], [108, 108]),  'retry_option': ([60, 93], [79, 79]),  'invoke': ([26, 35, 38, 59, 63, 102], [49, 49, 49, 49, 49, 49]),  'define_client': ([0, 5], [4, 4]),  'autoscaling_setting': ([51, 70], [70, 70])}
_lr_goto = {}
for _k, _v in _lr_goto_items.items():
    for _x, _y in zip(_v[0], _v[1]):
        if not _x in _lr_goto:
            _lr_goto[_x] = {}
        _lr_goto[_x][_k] = _y

del _lr_goto_items
_lr_productions = [
 (
  "S' -> unit", "S'", 1, None, None, None),
 (
  'unit -> definition_list', 'unit', 1, 'p_unit', 'parsing.py', 117),
 (
  'definition_list -> definition definition_list', 'definition_list', 2, 'p_definition_list', 'parsing.py', 124),
 (
  'definition_list -> definition', 'definition_list', 1, 'p_definition_list', 'parsing.py', 125),
 (
  'definition -> define_service', 'definition', 1, 'p_definition', 'parsing.py', 137),
 (
  'definition -> define_client', 'definition', 1, 'p_definition', 'parsing.py', 138),
 (
  'define_service -> SERVICE IDENTIFIER OPEN_CURLY_BRACKET settings operation_list CLOSE_CURLY_BRACKET', 'define_service', 6, 'p_define_service', 'parsing.py', 145),
 (
  'define_service -> SERVICE IDENTIFIER OPEN_CURLY_BRACKET operation_list CLOSE_CURLY_BRACKET', 'define_service', 5, 'p_define_service', 'parsing.py', 146),
 (
  'settings -> SETTINGS OPEN_CURLY_BRACKET setting_list CLOSE_CURLY_BRACKET', 'settings', 4, 'p_settings', 'parsing.py', 157),
 (
  'setting_list -> setting setting_list', 'setting_list', 2, 'p_setting_list', 'parsing.py', 164),
 (
  'setting_list -> setting', 'setting_list', 1, 'p_setting_list', 'parsing.py', 165),
 (
  'setting -> queue', 'setting', 1, 'p_setting', 'parsing.py', 177),
 (
  'setting -> autoscaling', 'setting', 1, 'p_setting', 'parsing.py', 178),
 (
  'setting -> throttling', 'setting', 1, 'p_setting', 'parsing.py', 179),
 (
  'queue -> QUEUE COLON LIFO', 'queue', 3, 'p_queue', 'parsing.py', 186),
 (
  'queue -> QUEUE COLON FIFO', 'queue', 3, 'p_queue', 'parsing.py', 187),
 (
  'throttling -> THROTTLING COLON NONE', 'throttling', 3, 'p_throttling', 'parsing.py', 201),
 (
  'throttling -> THROTTLING COLON TAIL_DROP OPEN_BRACKET NUMBER CLOSE_BRACKET', 'throttling', 6, 'p_throttling', 'parsing.py', 202),
 (
  'autoscaling -> AUTOSCALING OPEN_CURLY_BRACKET autoscaling_setting_list CLOSE_CURLY_BRACKET', 'autoscaling', 4, 'p_autoscaling', 'parsing.py', 212),
 (
  'autoscaling_setting_list -> autoscaling_setting autoscaling_setting_list', 'autoscaling_setting_list', 2, 'p_autoscaling_setting_list', 'parsing.py', 219),
 (
  'autoscaling_setting_list -> autoscaling_setting', 'autoscaling_setting_list', 1, 'p_autoscaling_setting_list', 'parsing.py', 220),
 (
  'autoscaling_setting -> PERIOD COLON NUMBER', 'autoscaling_setting', 3, 'p_autoscaling_setting', 'parsing.py', 232),
 (
  'autoscaling_setting -> LIMITS COLON OPEN_SQUARE_BRACKET NUMBER COMMA NUMBER CLOSE_SQUARE_BRACKET', 'autoscaling_setting', 7, 'p_autoscaling_setting', 'parsing.py', 233),
 (
  'operation_list -> define_operation operation_list', 'operation_list', 2, 'p_operation_list', 'parsing.py', 245),
 (
  'operation_list -> define_operation', 'operation_list', 1, 'p_operation_list', 'parsing.py', 246),
 (
  'define_client -> CLIENT IDENTIFIER OPEN_CURLY_BRACKET EVERY NUMBER OPEN_CURLY_BRACKET action_list CLOSE_CURLY_BRACKET CLOSE_CURLY_BRACKET', 'define_client', 9, 'p_define_client', 'parsing.py', 258),
 (
  'define_operation -> OPERATION IDENTIFIER OPEN_CURLY_BRACKET action_list CLOSE_CURLY_BRACKET', 'define_operation', 5, 'p_define_operation', 'parsing.py', 265),
 (
  'action_list -> action action_list', 'action_list', 2, 'p_action_list', 'parsing.py', 272),
 (
  'action_list -> action', 'action_list', 1, 'p_action_list', 'parsing.py', 273),
 (
  'action -> invoke', 'action', 1, 'p_action', 'parsing.py', 285),
 (
  'action -> query', 'action', 1, 'p_action', 'parsing.py', 286),
 (
  'action -> think', 'action', 1, 'p_action', 'parsing.py', 287),
 (
  'action -> fail', 'action', 1, 'p_action', 'parsing.py', 288),
 (
  'action -> retry', 'action', 1, 'p_action', 'parsing.py', 289),
 (
  'action -> ignore', 'action', 1, 'p_action', 'parsing.py', 290),
 (
  'think -> THINK NUMBER', 'think', 2, 'p_think', 'parsing.py', 297),
 (
  'fail -> FAIL NUMBER', 'fail', 2, 'p_fail', 'parsing.py', 304),
 (
  'fail -> FAIL', 'fail', 1, 'p_fail', 'parsing.py', 305),
 (
  'query -> QUERY IDENTIFIER SLASH IDENTIFIER', 'query', 4, 'p_query', 'parsing.py', 314),
 (
  'query -> QUERY IDENTIFIER SLASH IDENTIFIER OPEN_CURLY_BRACKET query_option_list CLOSE_CURLY_BRACKET', 'query', 7, 'p_query', 'parsing.py', 315),
 (
  'query_option_list -> query_option COMMA query_option_list', 'query_option_list', 3, 'p_query_option_list', 'parsing.py', 325),
 (
  'query_option_list -> query_option', 'query_option_list', 1, 'p_query_option_list', 'parsing.py', 326),
 (
  'query_option -> timeout', 'query_option', 1, 'p_query_option', 'parsing.py', 338),
 (
  'query_option -> priority', 'query_option', 1, 'p_query_option', 'parsing.py', 339),
 (
  'timeout -> TIMEOUT COLON NUMBER', 'timeout', 3, 'p_timeout', 'parsing.py', 346),
 (
  'priority -> PRIORITY COLON NUMBER', 'priority', 3, 'p_priority', 'parsing.py', 353),
 (
  'invoke -> INVOKE IDENTIFIER SLASH IDENTIFIER', 'invoke', 4, 'p_invoke', 'parsing.py', 360),
 (
  'invoke -> INVOKE IDENTIFIER SLASH IDENTIFIER OPEN_CURLY_BRACKET PRIORITY COLON NUMBER CLOSE_CURLY_BRACKET', 'invoke', 9, 'p_invoke', 'parsing.py', 361),
 (
  'retry -> RETRY OPEN_CURLY_BRACKET action_list CLOSE_CURLY_BRACKET', 'retry', 4, 'p_retry', 'parsing.py', 371),
 (
  'retry -> RETRY OPEN_BRACKET retry_option_list CLOSE_BRACKET OPEN_CURLY_BRACKET action_list CLOSE_CURLY_BRACKET', 'retry', 7, 'p_retry', 'parsing.py', 372),
 (
  'retry_option_list -> retry_option COMMA retry_option_list', 'retry_option_list', 3, 'p_retry_option_list', 'parsing.py', 384),
 (
  'retry_option_list -> retry_option', 'retry_option_list', 1, 'p_retry_option_list', 'parsing.py', 385),
 (
  'retry_option -> LIMIT COLON NUMBER', 'retry_option', 3, 'p_retry_option', 'parsing.py', 397),
 (
  'retry_option -> DELAY COLON IDENTIFIER OPEN_BRACKET NUMBER CLOSE_BRACKET', 'retry_option', 6, 'p_retry_option', 'parsing.py', 398),
 (
  'ignore -> IGNORE OPEN_CURLY_BRACKET action_list CLOSE_CURLY_BRACKET', 'ignore', 4, 'p_ignore', 'parsing.py', 410)]
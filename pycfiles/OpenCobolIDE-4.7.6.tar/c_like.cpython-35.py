# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/lexers/c_like.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 23439 bytes
"""
    pygments.lexers.c_like
    ~~~~~~~~~~~~~~~~~~~~~~

    Lexers for other C-like languages.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, include, bygroups, inherit, words, default
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation
from pygments.lexers.c_cpp import CLexer, CppLexer
from pygments.lexers import _mql_builtins
__all__ = [
 'PikeLexer', 'NesCLexer', 'ClayLexer', 'ECLexer', 'ValaLexer',
 'CudaLexer', 'SwigLexer', 'MqlLexer', 'ArduinoLexer']

class PikeLexer(CppLexer):
    __doc__ = '\n    For `Pike <http://pike.lysator.liu.se/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'Pike'
    aliases = ['pike']
    filenames = ['*.pike', '*.pmod']
    mimetypes = ['text/x-pike']
    tokens = {'statements': [
                    (
                     words(('catch', 'new', 'private', 'protected', 'public', 'gauge', 'throw', 'throws',
       'class', 'interface', 'implement', 'abstract', 'extends', 'from', 'this',
       'super', 'constant', 'final', 'static', 'import', 'use', 'extern', 'inline',
       'proto', 'break', 'continue', 'if', 'else', 'for', 'while', 'do', 'switch',
       'case', 'as', 'in', 'version', 'return', 'true', 'false', 'null', '__VERSION__',
       '__MAJOR__', '__MINOR__', '__BUILD__', '__REAL_VERSION__', '__REAL_MAJOR__',
       '__REAL_MINOR__', '__REAL_BUILD__', '__DATE__', '__TIME__', '__FILE__', '__DIR__',
       '__LINE__', '__AUTO_BIGNUM__', '__NT__', '__PIKE__', '__amigaos__', '_Pragma',
       'static_assert', 'defined', 'sscanf'), suffix='\\b'),
                     Keyword),
                    (
                     '(bool|int|long|float|short|double|char|string|object|void|mapping|array|multiset|program|function|lambda|mixed|[a-z_][a-z0-9_]*_t)\\b',
                     Keyword.Type),
                    (
                     '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
                    (
                     '[~!%^&*+=|?:<>/@-]', Operator),
                    inherit], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop'),
                   (
                    '\\s*(?=>)', Text, '#pop')]}


class NesCLexer(CLexer):
    __doc__ = '\n    For `nesC <https://github.com/tinyos/nesc>`_ source code with preprocessor\n    directives.\n\n    .. versionadded:: 2.0\n    '
    name = 'nesC'
    aliases = ['nesc']
    filenames = ['*.nc']
    mimetypes = ['text/x-nescsrc']
    tokens = {'statements': [
                    (
                     words(('abstract', 'as', 'async', 'atomic', 'call', 'command', 'component', 'components',
       'configuration', 'event', 'extends', 'generic', 'implementation', 'includes',
       'interface', 'module', 'new', 'norace', 'post', 'provides', 'signal', 'task',
       'uses'), suffix='\\b'),
                     Keyword),
                    (
                     words(('nx_struct', 'nx_union', 'nx_int8_t', 'nx_int16_t', 'nx_int32_t', 'nx_int64_t',
       'nx_uint8_t', 'nx_uint16_t', 'nx_uint32_t', 'nx_uint64_t'), suffix='\\b'),
                     Keyword.Type),
                    inherit]}


class ClayLexer(RegexLexer):
    __doc__ = '\n    For `Clay <http://claylabs.com/clay/>`_ source.\n\n    .. versionadded:: 2.0\n    '
    name = 'Clay'
    filenames = ['*.clay']
    aliases = ['clay']
    mimetypes = ['text/x-clay']
    tokens = {'root': [
              (
               '\\s', Text),
              (
               '//.*?$', Comment.Singleline),
              (
               '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline),
              (
               '\\b(public|private|import|as|record|variant|instance|define|overload|default|external|alias|rvalue|ref|forward|inline|noinline|forceinline|enum|var|and|or|not|if|else|goto|return|while|switch|case|break|continue|for|in|true|false|try|catch|throw|finally|onerror|staticassert|eval|when|newtype|__FILE__|__LINE__|__COLUMN__|__ARG__)\\b',
               Keyword),
              (
               '[~!%^&*+=|:<>/-]', Operator),
              (
               '[#(){}\\[\\],;.]', Punctuation),
              (
               '0x[0-9a-fA-F]+[LlUu]*', Number.Hex),
              (
               '\\d+[LlUu]*', Number.Integer),
              (
               '\\b(true|false)\\b', Name.Builtin),
              (
               '(?i)[a-z_?][\\w?]*', Name),
              (
               '"""', String, 'tdqs'),
              (
               '"', String, 'dqs')], 
     
     'strings': [
                 (
                  '(?i)\\\\(x[0-9a-f]{2}|.)', String.Escape),
                 (
                  '.', String)], 
     
     'nl': [
            (
             '\\n', String)], 
     
     'dqs': [
             (
              '"', String, '#pop'),
             include('strings')], 
     
     'tdqs': [
              (
               '"""', String, '#pop'),
              include('strings'),
              include('nl')]}


class ECLexer(CLexer):
    __doc__ = '\n    For eC source code with preprocessor directives.\n\n    .. versionadded:: 1.5\n    '
    name = 'eC'
    aliases = ['ec']
    filenames = ['*.ec', '*.eh']
    mimetypes = ['text/x-echdr', 'text/x-ecsrc']
    tokens = {'statements': [
                    (
                     words(('virtual', 'class', 'private', 'public', 'property', 'import', 'delete', 'new',
       'new0', 'renew', 'renew0', 'define', 'get', 'set', 'remote', 'dllexport',
       'dllimport', 'stdcall', 'subclass', '__on_register_module', 'namespace', 'using',
       'typed_object', 'any_object', 'incref', 'register', 'watch', 'stopwatching',
       'firewatchers', 'watchable', 'class_designer', 'class_fixed', 'class_no_expansion',
       'isset', 'class_default_property', 'property_category', 'class_data', 'class_property',
       'thisclass', 'dbtable', 'dbindex', 'database_open', 'dbfield'), suffix='\\b'), Keyword),
                    (
                     words(('uint', 'uint16', 'uint32', 'uint64', 'bool', 'byte', 'unichar', 'int64'), suffix='\\b'),
                     Keyword.Type),
                    (
                     '(class)(\\s+)', bygroups(Keyword, Text), 'classname'),
                    (
                     '(null|value|this)\\b', Name.Builtin),
                    inherit], 
     
     'classname': [
                   (
                    '[a-zA-Z_]\\w*', Name.Class, '#pop'),
                   (
                    '\\s*(?=>)', Text, '#pop')]}


class ValaLexer(RegexLexer):
    __doc__ = '\n    For Vala source code with preprocessor directives.\n\n    .. versionadded:: 1.1\n    '
    name = 'Vala'
    aliases = ['vala', 'vapi']
    filenames = ['*.vala', '*.vapi']
    mimetypes = ['text/x-vala']
    tokens = {'whitespace': [
                    (
                     '^\\s*#if\\s+0', Comment.Preproc, 'if0'),
                    (
                     '\\n', Text),
                    (
                     '\\s+', Text),
                    (
                     '\\\\\\n', Text),
                    (
                     '//(\\n|(.|\\n)*?[^\\\\]\\n)', Comment.Single),
                    (
                     '/(\\\\\\n)?[*](.|\\n)*?[*](\\\\\\n)?/', Comment.Multiline)], 
     
     'statements': [
                    (
                     '[L@]?"', String, 'string'),
                    (
                     "L?'(\\\\.|\\\\[0-7]{1,3}|\\\\x[a-fA-F0-9]{1,2}|[^\\\\\\'\\n])'",
                     String.Char),
                    (
                     '(?s)""".*?"""', String),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+)[eE][+-]?\\d+[lL]?', Number.Float),
                    (
                     '(\\d+\\.\\d*|\\.\\d+|\\d+[fF])[fF]?', Number.Float),
                    (
                     '0x[0-9a-fA-F]+[Ll]?', Number.Hex),
                    (
                     '0[0-7]+[Ll]?', Number.Oct),
                    (
                     '\\d+[Ll]?', Number.Integer),
                    (
                     '[~!%^&*+=|?:<>/-]', Operator),
                    (
                     '(\\[)(Compact|Immutable|(?:Boolean|Simple)Type)(\\])',
                     bygroups(Punctuation, Name.Decorator, Punctuation)),
                    (
                     '(\\[)(CCode|(?:Integer|Floating)Type)',
                     bygroups(Punctuation, Name.Decorator)),
                    (
                     '[()\\[\\],.]', Punctuation),
                    (
                     words(('as', 'base', 'break', 'case', 'catch', 'construct', 'continue', 'default',
       'delete', 'do', 'else', 'enum', 'finally', 'for', 'foreach', 'get', 'if',
       'in', 'is', 'lock', 'new', 'out', 'params', 'return', 'set', 'sizeof', 'switch',
       'this', 'throw', 'try', 'typeof', 'while', 'yield'), suffix='\\b'),
                     Keyword),
                    (
                     words(('abstract', 'const', 'delegate', 'dynamic', 'ensures', 'extern', 'inline', 'internal',
       'override', 'owned', 'private', 'protected', 'public', 'ref', 'requires',
       'signal', 'static', 'throws', 'unowned', 'var', 'virtual', 'volatile', 'weak',
       'yields'), suffix='\\b'),
                     Keyword.Declaration),
                    (
                     '(namespace|using)(\\s+)', bygroups(Keyword.Namespace, Text),
                     'namespace'),
                    (
                     '(class|errordomain|interface|struct)(\\s+)',
                     bygroups(Keyword.Declaration, Text), 'class'),
                    (
                     '(\\.)([a-zA-Z_]\\w*)',
                     bygroups(Operator, Name.Attribute)),
                    (
                     words(('void', 'bool', 'char', 'double', 'float', 'int', 'int8', 'int16', 'int32',
       'int64', 'long', 'short', 'size_t', 'ssize_t', 'string', 'time_t', 'uchar',
       'uint', 'uint8', 'uint16', 'uint32', 'uint64', 'ulong', 'unichar', 'ushort'), suffix='\\b'),
                     Keyword.Type),
                    (
                     '(true|false|null)\\b', Name.Builtin),
                    (
                     '[a-zA-Z_]\\w*', Name)], 
     
     'root': [
              include('whitespace'),
              default('statement')], 
     
     'statement': [
                   include('whitespace'),
                   include('statements'),
                   (
                    '[{}]', Punctuation),
                   (
                    ';', Punctuation, '#pop')], 
     
     'string': [
                (
                 '"', String, '#pop'),
                (
                 '\\\\([\\\\abfnrtv"\\\']|x[a-fA-F0-9]{2,4}|[0-7]{1,3})', String.Escape),
                (
                 '[^\\\\"\\n]+', String),
                (
                 '\\\\\\n', String),
                (
                 '\\\\', String)], 
     
     'if0': [
             (
              '^\\s*#if.*?(?<!\\\\)\\n', Comment.Preproc, '#push'),
             (
              '^\\s*#el(?:se|if).*\\n', Comment.Preproc, '#pop'),
             (
              '^\\s*#endif.*?(?<!\\\\)\\n', Comment.Preproc, '#pop'),
             (
              '.*?\\n', Comment)], 
     
     'class': [
               (
                '[a-zA-Z_]\\w*', Name.Class, '#pop')], 
     
     'namespace': [
                   (
                    '[a-zA-Z_][\\w.]*', Name.Namespace, '#pop')]}


class CudaLexer(CLexer):
    __doc__ = '\n    For NVIDIA `CUDA™ <http://developer.nvidia.com/category/zone/cuda-zone>`_\n    source.\n\n    .. versionadded:: 1.6\n    '
    name = 'CUDA'
    filenames = ['*.cu', '*.cuh']
    aliases = ['cuda', 'cu']
    mimetypes = ['text/x-cuda']
    function_qualifiers = set(('__device__', '__global__', '__host__', '__noinline__',
                               '__forceinline__'))
    variable_qualifiers = set(('__device__', '__constant__', '__shared__', '__restrict__'))
    vector_types = set(('char1', 'uchar1', 'char2', 'uchar2', 'char3', 'uchar3', 'char4',
                        'uchar4', 'short1', 'ushort1', 'short2', 'ushort2', 'short3',
                        'ushort3', 'short4', 'ushort4', 'int1', 'uint1', 'int2',
                        'uint2', 'int3', 'uint3', 'int4', 'uint4', 'long1', 'ulong1',
                        'long2', 'ulong2', 'long3', 'ulong3', 'long4', 'ulong4',
                        'longlong1', 'ulonglong1', 'longlong2', 'ulonglong2', 'float1',
                        'float2', 'float3', 'float4', 'double1', 'double2', 'dim3'))
    variables = set(('gridDim', 'blockIdx', 'blockDim', 'threadIdx', 'warpSize'))
    functions = set(('__threadfence_block', '__threadfence', '__threadfence_system',
                     '__syncthreads', '__syncthreads_count', '__syncthreads_and',
                     '__syncthreads_or'))
    execution_confs = set(('<<<', '>>>'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in CLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.variable_qualifiers:
                    token = Keyword.Type
                else:
                    if value in self.vector_types:
                        token = Keyword.Type
                    else:
                        if value in self.variables:
                            token = Name.Builtin
                        else:
                            if value in self.execution_confs:
                                token = Keyword.Pseudo
                            else:
                                if value in self.function_qualifiers:
                                    token = Keyword.Reserved
                                elif value in self.functions:
                                    token = Name.Function
                yield (
                 index, token, value)


class SwigLexer(CppLexer):
    __doc__ = '\n    For `SWIG <http://www.swig.org/>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'SWIG'
    aliases = ['swig']
    filenames = ['*.swg', '*.i']
    mimetypes = ['text/swig']
    priority = 0.04
    tokens = {'statements': [
                    (
                     '(%[a-z_][a-z0-9_]*)', Name.Function),
                    (
                     '\\$\\**\\&?\\w+', Name),
                    (
                     '##*[a-zA-Z_]\\w*', Comment.Preproc),
                    inherit]}
    swig_directives = set(('%apply', '%define', '%director', '%enddef', '%exception',
                           '%extend', '%feature', '%fragment', '%ignore', '%immutable',
                           '%import', '%include', '%inline', '%insert', '%module',
                           '%newobject', '%nspace', '%pragma', '%rename', '%shared_ptr',
                           '%template', '%typecheck', '%typemap', '%arg', '%attribute',
                           '%bang', '%begin', '%callback', '%catches', '%clear',
                           '%constant', '%copyctor', '%csconst', '%csconstvalue',
                           '%csenum', '%csmethodmodifiers', '%csnothrowexception',
                           '%default', '%defaultctor', '%defaultdtor', '%defined',
                           '%delete', '%delobject', '%descriptor', '%exceptionclass',
                           '%exceptionvar', '%extend_smart_pointer', '%fragments',
                           '%header', '%ifcplusplus', '%ignorewarn', '%implicit',
                           '%implicitconv', '%init', '%javaconst', '%javaconstvalue',
                           '%javaenum', '%javaexception', '%javamethodmodifiers',
                           '%kwargs', '%luacode', '%mutable', '%naturalvar', '%nestedworkaround',
                           '%perlcode', '%pythonabc', '%pythonappend', '%pythoncallback',
                           '%pythoncode', '%pythondynamic', '%pythonmaybecall', '%pythonnondynamic',
                           '%pythonprepend', '%refobject', '%shadow', '%sizeof',
                           '%trackobjects', '%types', '%unrefobject', '%varargs',
                           '%warn', '%warnfilter'))

    def analyse_text(text):
        rv = 0
        matches = re.findall('^\\s*(%[a-z_][a-z0-9_]*)', text, re.M)
        for m in matches:
            if m in SwigLexer.swig_directives:
                rv = 0.98
                break
            else:
                rv = 0.91

        return rv


class MqlLexer(CppLexer):
    __doc__ = '\n    For `MQL4 <http://docs.mql4.com/>`_ and\n    `MQL5 <http://www.mql5.com/en/docs>`_ source code.\n\n    .. versionadded:: 2.0\n    '
    name = 'MQL'
    aliases = ['mql', 'mq4', 'mq5', 'mql4', 'mql5']
    filenames = ['*.mq4', '*.mq5', '*.mqh']
    mimetypes = ['text/x-mql']
    tokens = {'statements': [
                    (
                     words(_mql_builtins.keywords, suffix='\\b'), Keyword),
                    (
                     words(_mql_builtins.c_types, suffix='\\b'), Keyword.Type),
                    (
                     words(_mql_builtins.types, suffix='\\b'), Name.Function),
                    (
                     words(_mql_builtins.constants, suffix='\\b'), Name.Constant),
                    (
                     words(_mql_builtins.colors, prefix='(clr)?', suffix='\\b'),
                     Name.Constant),
                    inherit]}


class ArduinoLexer(CppLexer):
    __doc__ = '\n    For `Arduino(tm) <https://arduino.cc/>`_ source.\n\n    This is an extension of the CppLexer, as the Arduino® Language is a superset\n    of C++\n\n    .. versionadded:: 2.1\n    '
    name = 'Arduino'
    aliases = ['arduino']
    filenames = ['*.ino']
    mimetypes = ['text/x-arduino']
    constants = set(('DIGITAL_MESSAGE', 'FIRMATA_STRING', 'ANALOG_MESSAGE', 'REPORT_DIGITAL',
                     'REPORT_ANALOG', 'INPUT_PULLUP', 'SET_PIN_MODE', 'INTERNAL2V56',
                     'SYSTEM_RESET', 'LED_BUILTIN', 'INTERNAL1V1', 'SYSEX_START',
                     'INTERNAL', 'EXTERNAL', 'DEFAULT', 'OUTPUT', 'INPUT', 'HIGH',
                     'LOW'))
    structure = set(('setup', 'loop'))
    storage = set(('boolean', 'const', 'byte', 'word', 'string', 'String', 'array'))
    functions = set(('KeyboardController', 'MouseController', 'SoftwareSerial', 'EthernetServer',
                     'EthernetClient', 'LiquidCrystal', 'RobotControl', 'GSMVoiceCall',
                     'EthernetUDP', 'EsploraTFT', 'HttpClient', 'RobotMotor', 'WiFiClient',
                     'GSMScanner', 'FileSystem', 'Scheduler', 'GSMServer', 'YunClient',
                     'YunServer', 'IPAddress', 'GSMClient', 'GSMModem', 'Keyboard',
                     'Ethernet', 'Console', 'GSMBand', 'Esplora', 'Stepper', 'Process',
                     'WiFiUDP', 'GSM_SMS', 'Mailbox', 'USBHost', 'Firmata', 'PImage',
                     'Client', 'Server', 'GSMPIN', 'FileIO', 'Bridge', 'Serial',
                     'EEPROM', 'Stream', 'Mouse', 'Audio', 'Servo', 'File', 'Task',
                     'GPRS', 'WiFi', 'Wire', 'TFT', 'GSM', 'SPI', 'SD', 'runShellCommandAsynchronously',
                     'analogWriteResolution', 'retrieveCallingNumber', 'printFirmwareVersion',
                     'analogReadResolution', 'sendDigitalPortPair', 'noListenOnLocalhost',
                     'readJoystickButton', 'setFirmwareVersion', 'readJoystickSwitch',
                     'scrollDisplayRight', 'getVoiceCallStatus', 'scrollDisplayLeft',
                     'writeMicroseconds', 'delayMicroseconds', 'beginTransmission',
                     'getSignalStrength', 'runAsynchronously', 'getAsynchronously',
                     'listenOnLocalhost', 'getCurrentCarrier', 'readAccelerometer',
                     'messageAvailable', 'sendDigitalPorts', 'lineFollowConfig',
                     'countryNameWrite', 'runShellCommand', 'readStringUntil', 'rewindDirectory',
                     'readTemperature', 'setClockDivider', 'readLightSensor', 'endTransmission',
                     'analogReference', 'detachInterrupt', 'countryNameRead', 'attachInterrupt',
                     'encryptionType', 'readBytesUntil', 'robotNameWrite', 'readMicrophone',
                     'robotNameRead', 'cityNameWrite', 'userNameWrite', 'readJoystickY',
                     'readJoystickX', 'mouseReleased', 'openNextFile', 'scanNetworks',
                     'noInterrupts', 'digitalWrite', 'beginSpeaker', 'mousePressed',
                     'isActionDone', 'mouseDragged', 'displayLogos', 'noAutoscroll',
                     'addParameter', 'remoteNumber', 'getModifiers', 'keyboardRead',
                     'userNameRead', 'waitContinue', 'processInput', 'parseCommand',
                     'printVersion', 'readNetworks', 'writeMessage', 'blinkVersion',
                     'cityNameRead', 'readMessage', 'setDataMode', 'parsePacket',
                     'isListening', 'setBitOrder', 'beginPacket', 'isDirectory',
                     'motorsWrite', 'drawCompass', 'digitalRead', 'clearScreen',
                     'serialEvent', 'rightToLeft', 'setTextSize', 'leftToRight',
                     'requestFrom', 'keyReleased', 'compassRead', 'analogWrite',
                     'interrupts', 'WiFiServer', 'disconnect', 'playMelody', 'parseFloat',
                     'autoscroll', 'getPINUsed', 'setPINUsed', 'setTimeout', 'sendAnalog',
                     'readSlider', 'analogRead', 'beginWrite', 'createChar', 'motorsStop',
                     'keyPressed', 'tempoWrite', 'readButton', 'subnetMask', 'debugPrint',
                     'macAddress', 'writeGreen', 'randomSeed', 'attachGPRS', 'readString',
                     'sendString', 'remotePort', 'releaseAll', 'mouseMoved', 'background',
                     'getXChange', 'getYChange', 'answerCall', 'getResult', 'voiceCall',
                     'endPacket', 'constrain', 'getSocket', 'writeJSON', 'getButton',
                     'available', 'connected', 'findUntil', 'readBytes', 'exitValue',
                     'readGreen', 'writeBlue', 'startLoop', 'IPAddress', 'isPressed',
                     'sendSysex', 'pauseMode', 'gatewayIP', 'setCursor', 'getOemKey',
                     'tuneWrite', 'noDisplay', 'loadImage', 'switchPIN', 'onRequest',
                     'onReceive', 'changePIN', 'playFile', 'noBuffer', 'parseInt',
                     'overflow', 'checkPIN', 'knobRead', 'beginTFT', 'bitClear',
                     'updateIR', 'bitWrite', 'position', 'writeRGB', 'highByte',
                     'writeRed', 'setSpeed', 'readBlue', 'noStroke', 'remoteIP',
                     'transfer', 'shutdown', 'hangCall', 'beginSMS', 'endWrite',
                     'attached', 'maintain', 'noCursor', 'checkReg', 'checkPUK',
                     'shiftOut', 'isValid', 'shiftIn', 'pulseIn', 'connect', 'println',
                     'localIP', 'pinMode', 'getIMEI', 'display', 'noBlink', 'process',
                     'getBand', 'running', 'beginSD', 'drawBMP', 'lowByte', 'setBand',
                     'release', 'bitRead', 'prepare', 'pointTo', 'readRed', 'setMode',
                     'noFill', 'remove', 'listen', 'stroke', 'detach', 'attach',
                     'noTone', 'exists', 'buffer', 'height', 'bitSet', 'circle',
                     'config', 'cursor', 'random', 'IRread', 'sizeof', 'setDNS',
                     'endSMS', 'getKey', 'micros', 'millis', 'begin', 'print', 'write',
                     'ready', 'flush', 'width', 'isPIN', 'blink', 'clear', 'press',
                     'mkdir', 'rmdir', 'close', 'point', 'yield', 'image', 'float',
                     'BSSID', 'click', 'delay', 'read', 'text', 'move', 'peek', 'beep',
                     'rect', 'line', 'open', 'seek', 'fill', 'size', 'turn', 'stop',
                     'home', 'find', 'char', 'byte', 'step', 'word', 'long', 'tone',
                     'sqrt', 'RSSI', 'SSID', 'end', 'bit', 'tan', 'cos', 'sin', 'pow',
                     'map', 'abs', 'max', 'min', 'int', 'get', 'run', 'put'))

    def get_tokens_unprocessed(self, text):
        for index, token, value in CppLexer.get_tokens_unprocessed(self, text):
            if token is Name:
                if value in self.constants:
                    yield (
                     index, Keyword.Constant, value)
                else:
                    if value in self.functions:
                        yield (
                         index, Name.Function, value)
                    else:
                        if value in self.storage:
                            yield (
                             index, Keyword.Type, value)
                        else:
                            yield (
                             index, token, value)
            else:
                if token is Name.Function:
                    if value in self.structure:
                        yield (
                         index, Name.Other, value)
                    else:
                        yield (
                         index, token, value)
                else:
                    if token is Keyword:
                        if value in self.storage:
                            yield (
                             index, Keyword.Type, value)
                        else:
                            yield (
                             index, token, value)
                    else:
                        yield (
                         index, token, value)
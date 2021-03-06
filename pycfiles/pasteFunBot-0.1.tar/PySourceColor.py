# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/makina/pasteStage/pasteFunBot/Paste-1.7.2-py2.6.egg/paste/util/PySourceColor.py
# Compiled at: 2009-07-20 09:44:04
"""
PySourceColor: color Python source code
"""
__all__ = [
 'ERRORTOKEN', 'DECORATOR_NAME', 'DECORATOR', 'ARGS', 'EXTRASPACE',
 'NAME', 'NUMBER', 'OPERATOR', 'COMMENT', 'MATH_OPERATOR',
 'DOUBLECOMMENT', 'CLASS_NAME', 'DEF_NAME', 'KEYWORD', 'BRACKETS',
 'SINGLEQUOTE', 'SINGLEQUOTE_R', 'SINGLEQUOTE_U', 'DOUBLEQUOTE',
 'DOUBLEQUOTE_R', 'DOUBLEQUOTE_U', 'TRIPLESINGLEQUOTE', 'TEXT',
 'TRIPLESINGLEQUOTE_R', 'TRIPLESINGLEQUOTE_U', 'TRIPLEDOUBLEQUOTE',
 'TRIPLEDOUBLEQUOTE_R', 'TRIPLEDOUBLEQUOTE_U', 'PAGEBACKGROUND',
 'LINENUMBER', 'CODESTART', 'CODEEND', 'PY', 'TOKEN_NAMES', 'CSSHOOK',
 'null', 'mono', 'lite', 'dark', 'dark2', 'pythonwin', 'idle',
 'viewcvs', 'Usage', 'cli', 'str2stdout', 'path2stdout', 'Parser',
 'str2file', 'str2html', 'str2css', 'str2markup', 'path2file',
 'path2html', 'convert', 'walkdir', 'defaultColors', 'showpage',
 'pageconvert', 'tagreplace', 'MARKUPDICT']
__title__ = 'PySourceColor'
__version__ = '2.1a'
__date__ = '25 April 2005'
__author__ = 'M.E.Farmer Jr.'
__credits__ = b'This was originally based on a python recipe\nsubmitted by J\xfcrgen Hermann to ASPN. Now based on the voices in my head.\nM.E.Farmer 2004, 2005\nPython license\n'
import os, sys, time, glob, getopt, keyword, token, tokenize, traceback
try:
    import cStringIO as StringIO
except:
    import StringIO

NAME = token.NAME
NUMBER = token.NUMBER
COMMENT = tokenize.COMMENT
OPERATOR = token.OP
ERRORTOKEN = token.ERRORTOKEN
ARGS = token.NT_OFFSET + 1
DOUBLECOMMENT = token.NT_OFFSET + 2
CLASS_NAME = token.NT_OFFSET + 3
DEF_NAME = token.NT_OFFSET + 4
KEYWORD = token.NT_OFFSET + 5
SINGLEQUOTE = token.NT_OFFSET + 6
SINGLEQUOTE_R = token.NT_OFFSET + 7
SINGLEQUOTE_U = token.NT_OFFSET + 8
DOUBLEQUOTE = token.NT_OFFSET + 9
DOUBLEQUOTE_R = token.NT_OFFSET + 10
DOUBLEQUOTE_U = token.NT_OFFSET + 11
TRIPLESINGLEQUOTE = token.NT_OFFSET + 12
TRIPLESINGLEQUOTE_R = token.NT_OFFSET + 13
TRIPLESINGLEQUOTE_U = token.NT_OFFSET + 14
TRIPLEDOUBLEQUOTE = token.NT_OFFSET + 15
TRIPLEDOUBLEQUOTE_R = token.NT_OFFSET + 16
TRIPLEDOUBLEQUOTE_U = token.NT_OFFSET + 17
PAGEBACKGROUND = token.NT_OFFSET + 18
DECORATOR = token.NT_OFFSET + 19
DECORATOR_NAME = token.NT_OFFSET + 20
BRACKETS = token.NT_OFFSET + 21
MATH_OPERATOR = token.NT_OFFSET + 22
LINENUMBER = token.NT_OFFSET + 23
TEXT = token.NT_OFFSET + 24
PY = token.NT_OFFSET + 25
CODESTART = token.NT_OFFSET + 26
CODEEND = token.NT_OFFSET + 27
CSSHOOK = token.NT_OFFSET + 28
EXTRASPACE = token.NT_OFFSET + 29
MARKUPDICT = {ERRORTOKEN: 'py_err', 
   DECORATOR_NAME: 'py_decn', 
   DECORATOR: 'py_dec', 
   ARGS: 'py_args', 
   NAME: 'py_name', 
   NUMBER: 'py_num', 
   OPERATOR: 'py_op', 
   COMMENT: 'py_com', 
   DOUBLECOMMENT: 'py_dcom', 
   CLASS_NAME: 'py_clsn', 
   DEF_NAME: 'py_defn', 
   KEYWORD: 'py_key', 
   SINGLEQUOTE: 'py_sq', 
   SINGLEQUOTE_R: 'py_sqr', 
   SINGLEQUOTE_U: 'py_squ', 
   DOUBLEQUOTE: 'py_dq', 
   DOUBLEQUOTE_R: 'py_dqr', DOUBLEQUOTE_U: 'py_dqu', 
   TRIPLESINGLEQUOTE: 'py_tsq', 
   TRIPLESINGLEQUOTE_R: 'py_tsqr', 
   TRIPLESINGLEQUOTE_U: 'py_tsqu', 
   TRIPLEDOUBLEQUOTE: 'py_tdq', 
   TRIPLEDOUBLEQUOTE_R: 'py_tdqr', 
   TRIPLEDOUBLEQUOTE_U: 'py_tdqu', 
   BRACKETS: 'py_bra', 
   MATH_OPERATOR: 'py_mop', 
   LINENUMBER: 'py_lnum', 
   TEXT: 'py_text'}
TOKEN_NAMES = {ERRORTOKEN: 'ERRORTOKEN', 
   DECORATOR_NAME: 'DECORATOR_NAME', 
   DECORATOR: 'DECORATOR', 
   ARGS: 'ARGS', 
   NAME: 'NAME', 
   NUMBER: 'NUMBER', 
   OPERATOR: 'OPERATOR', 
   COMMENT: 'COMMENT', 
   DOUBLECOMMENT: 'DOUBLECOMMENT', 
   CLASS_NAME: 'CLASS_NAME', 
   DEF_NAME: 'DEF_NAME', 
   KEYWORD: 'KEYWORD', 
   SINGLEQUOTE: 'SINGLEQUOTE', 
   SINGLEQUOTE_R: 'SINGLEQUOTE_R', 
   SINGLEQUOTE_U: 'SINGLEQUOTE_U', 
   DOUBLEQUOTE: 'DOUBLEQUOTE', 
   DOUBLEQUOTE_R: 'DOUBLEQUOTE_R', 
   DOUBLEQUOTE_U: 'DOUBLEQUOTE_U', 
   TRIPLESINGLEQUOTE: 'TRIPLESINGLEQUOTE', 
   TRIPLESINGLEQUOTE_R: 'TRIPLESINGLEQUOTE_R', 
   TRIPLESINGLEQUOTE_U: 'TRIPLESINGLEQUOTE_U', 
   TRIPLEDOUBLEQUOTE: 'TRIPLEDOUBLEQUOTE', 
   TRIPLEDOUBLEQUOTE_R: 'TRIPLEDOUBLEQUOTE_R', 
   TRIPLEDOUBLEQUOTE_U: 'TRIPLEDOUBLEQUOTE_U', 
   BRACKETS: 'BRACKETS', 
   MATH_OPERATOR: 'MATH_OPERATOR', 
   LINENUMBER: 'LINENUMBER', 
   TEXT: 'TEXT', 
   PAGEBACKGROUND: 'PAGEBACKGROUND'}
null = {ERRORTOKEN: (
              '', '#000000', ''), 
   DECORATOR_NAME: (
                  '', '#000000', ''), 
   DECORATOR: (
             '', '#000000', ''), 
   ARGS: (
        '', '#000000', ''), 
   NAME: (
        '', '#000000', ''), 
   NUMBER: (
          '', '#000000', ''), 
   OPERATOR: (
            '', '#000000', ''), 
   MATH_OPERATOR: (
                 '', '#000000', ''), 
   BRACKETS: (
            '', '#000000', ''), 
   COMMENT: (
           '', '#000000', ''), 
   DOUBLECOMMENT: (
                 '', '#000000', ''), 
   CLASS_NAME: (
              '', '#000000', ''), 
   DEF_NAME: (
            '', '#000000', ''), 
   KEYWORD: (
           '', '#000000', ''), 
   SINGLEQUOTE: (
               '', '#000000', ''), 
   SINGLEQUOTE_R: (
                 '', '#000000', ''), 
   SINGLEQUOTE_U: (
                 '', '#000000', ''), 
   DOUBLEQUOTE: (
               '', '#000000', ''), 
   DOUBLEQUOTE_R: (
                 '', '#000000', ''), 
   DOUBLEQUOTE_U: (
                 '', '#000000', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#000000', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#000000', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#000000', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#000000', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#000000', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#000000', ''), 
   TEXT: (
        '', '#000000', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
mono = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  'bu', '#000000', ''), 
   DECORATOR: (
             'b', '#000000', ''), 
   ARGS: (
        'b', '#555555', ''), 
   NAME: (
        '', '#000000', ''), 
   NUMBER: (
          'b', '#000000', ''), 
   OPERATOR: (
            'b', '#000000', ''), 
   MATH_OPERATOR: (
                 'b', '#000000', ''), 
   BRACKETS: (
            'b', '#000000', ''), 
   COMMENT: (
           'i', '#999999', ''), 
   DOUBLECOMMENT: (
                 'b', '#999999', ''), 
   CLASS_NAME: (
              'bu', '#000000', ''), 
   DEF_NAME: (
            'b', '#000000', ''), 
   KEYWORD: (
           'b', '#000000', ''), 
   SINGLEQUOTE: (
               '', '#000000', ''), 
   SINGLEQUOTE_R: (
                 '', '#000000', ''), 
   SINGLEQUOTE_U: (
                 '', '#000000', ''), 
   DOUBLEQUOTE: (
               '', '#000000', ''), 
   DOUBLEQUOTE_R: (
                 '', '#000000', ''), 
   DOUBLEQUOTE_U: (
                 '', '#000000', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#000000', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#000000', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#000000', ''), 
   TRIPLEDOUBLEQUOTE: (
                     'i', '#000000', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       'i', '#000000', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       'i', '#000000', ''), 
   TEXT: (
        '', '#000000', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
dark = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  'b', '#FFBBAA', ''), 
   DECORATOR: (
             'b', '#CC5511', ''), 
   ARGS: (
        'b', '#DDDDFF', ''), 
   NAME: (
        '', '#DDDDDD', ''), 
   NUMBER: (
          '', '#FF0000', ''), 
   OPERATOR: (
            'b', '#FAF785', ''), 
   MATH_OPERATOR: (
                 'b', '#FAF785', ''), 
   BRACKETS: (
            'b', '#FAF785', ''), 
   COMMENT: (
           '', '#45FCA0', ''), 
   DOUBLECOMMENT: (
                 'i', '#A7C7A9', ''), 
   CLASS_NAME: (
              'b', '#B666FD', ''), 
   DEF_NAME: (
            'b', '#EBAE5C', ''), 
   KEYWORD: (
           'b', '#8680FF', ''), 
   SINGLEQUOTE: (
               '', '#F8BAFE', ''), 
   SINGLEQUOTE_R: (
                 '', '#F8BAFE', ''), 
   SINGLEQUOTE_U: (
                 '', '#F8BAFE', ''), 
   DOUBLEQUOTE: (
               '', '#FF80C0', ''), 
   DOUBLEQUOTE_R: (
                 '', '#FF80C0', ''), 
   DOUBLEQUOTE_U: (
                 '', '#FF80C0', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#FF9595', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#FF9595', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#FF9595', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#B3FFFF', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#B3FFFF', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#B3FFFF', ''), 
   TEXT: (
        '', '#FFFFFF', ''), 
   LINENUMBER: (
              '>mi#555555', '#bbccbb', '#333333'), 
   PAGEBACKGROUND: '#000000'}
dark2 = {ERRORTOKEN: (
              '', '#FF0000', ''), 
   DECORATOR_NAME: (
                  'b', '#FFBBAA', ''), 
   DECORATOR: (
             'b', '#CC5511', ''), 
   ARGS: (
        'b', '#DDDDDD', ''), 
   NAME: (
        '', '#C0C0C0', ''), 
   NUMBER: (
          'b', '#00FF00', ''), 
   OPERATOR: (
            'b', '#FF090F', ''), 
   MATH_OPERATOR: (
                 'b', '#EE7020', ''), 
   BRACKETS: (
            'b', '#FFB90F', ''), 
   COMMENT: (
           'i', '#D0D000', '#522000'), 
   DOUBLECOMMENT: (
                 'i', '#D0D000', '#522000'), 
   CLASS_NAME: (
              'b', '#DD4080', ''), 
   DEF_NAME: (
            'b', '#FF8040', ''), 
   KEYWORD: (
           'b', '#4726d1', ''), 
   SINGLEQUOTE: (
               '', '#8080C0', ''), 
   SINGLEQUOTE_R: (
                 '', '#8080C0', ''), 
   SINGLEQUOTE_U: (
                 '', '#8080C0', ''), 
   DOUBLEQUOTE: (
               '', '#ADB9F1', ''), 
   DOUBLEQUOTE_R: (
                 '', '#ADB9F1', ''), 
   DOUBLEQUOTE_U: (
                 '', '#ADB9F1', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#00C1C1', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#00C1C1', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#00C1C1', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#33E3E3', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#33E3E3', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#33E3E3', ''), 
   TEXT: (
        '', '#C0C0C0', ''), 
   LINENUMBER: (
              '>mi#555555', '#bbccbb', '#333333'), 
   PAGEBACKGROUND: '#000000'}
lite = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  'b', '#BB4422', ''), 
   DECORATOR: (
             'b', '#3333AF', ''), 
   ARGS: (
        'b', '#000000', ''), 
   NAME: (
        '', '#333333', ''), 
   NUMBER: (
          'b', '#DD2200', ''), 
   OPERATOR: (
            'b', '#000000', ''), 
   MATH_OPERATOR: (
                 'b', '#000000', ''), 
   BRACKETS: (
            'b', '#000000', ''), 
   COMMENT: (
           '', '#007F00', ''), 
   DOUBLECOMMENT: (
                 '', '#608060', ''), 
   CLASS_NAME: (
              'b', '#0000DF', ''), 
   DEF_NAME: (
            'b', '#9C7A00', ''), 
   KEYWORD: (
           'b', '#0000AF', ''), 
   SINGLEQUOTE: (
               '', '#600080', ''), 
   SINGLEQUOTE_R: (
                 '', '#600080', ''), 
   SINGLEQUOTE_U: (
                 '', '#600080', ''), 
   DOUBLEQUOTE: (
               '', '#A0008A', ''), 
   DOUBLEQUOTE_R: (
                 '', '#A0008A', ''), 
   DOUBLEQUOTE_U: (
                 '', '#A0008A', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#337799', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#337799', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#337799', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#1166AA', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#1166AA', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#1166AA', ''), 
   TEXT: (
        '', '#000000', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
idle = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  '', '#900090', ''), 
   DECORATOR: (
             '', '#FF7700', ''), 
   NAME: (
        '', '#000000', ''), 
   NUMBER: (
          '', '#000000', ''), 
   OPERATOR: (
            '', '#000000', ''), 
   MATH_OPERATOR: (
                 '', '#000000', ''), 
   BRACKETS: (
            '', '#000000', ''), 
   COMMENT: (
           '', '#DD0000', ''), 
   DOUBLECOMMENT: (
                 '', '#DD0000', ''), 
   CLASS_NAME: (
              '', '#0000FF', ''), 
   DEF_NAME: (
            '', '#0000FF', ''), 
   KEYWORD: (
           '', '#FF7700', ''), 
   SINGLEQUOTE: (
               '', '#00AA00', ''), 
   SINGLEQUOTE_R: (
                 '', '#00AA00', ''), 
   SINGLEQUOTE_U: (
                 '', '#00AA00', ''), 
   DOUBLEQUOTE: (
               '', '#00AA00', ''), 
   DOUBLEQUOTE_R: (
                 '', '#00AA00', ''), 
   DOUBLEQUOTE_U: (
                 '', '#00AA00', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#00AA00', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#00AA00', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#00AA00', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#00AA00', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#00AA00', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#00AA00', ''), 
   TEXT: (
        '', '#000000', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
pythonwin = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  'b', '#DD0080', ''), 
   DECORATOR: (
             'b', '#000080', ''), 
   ARGS: (
        '', '#000000', ''), 
   NAME: (
        '', '#303030', ''), 
   NUMBER: (
          '', '#008080', ''), 
   OPERATOR: (
            '', '#000000', ''), 
   MATH_OPERATOR: (
                 '', '#000000', ''), 
   BRACKETS: (
            '', '#000000', ''), 
   COMMENT: (
           '', '#007F00', ''), 
   DOUBLECOMMENT: (
                 '', '#7F7F7F', ''), 
   CLASS_NAME: (
              'b', '#0000FF', ''), 
   DEF_NAME: (
            'b', '#007F7F', ''), 
   KEYWORD: (
           'b', '#000080', ''), 
   SINGLEQUOTE: (
               '', '#808000', ''), 
   SINGLEQUOTE_R: (
                 '', '#808000', ''), 
   SINGLEQUOTE_U: (
                 '', '#808000', ''), 
   DOUBLEQUOTE: (
               '', '#808000', ''), 
   DOUBLEQUOTE_R: (
                 '', '#808000', ''), 
   DOUBLEQUOTE_U: (
                 '', '#808000', ''), 
   TRIPLESINGLEQUOTE: (
                     '', '#808000', ''), 
   TRIPLESINGLEQUOTE_R: (
                       '', '#808000', ''), 
   TRIPLESINGLEQUOTE_U: (
                       '', '#808000', ''), 
   TRIPLEDOUBLEQUOTE: (
                     '', '#808000', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       '', '#808000', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       '', '#808000', ''), 
   TEXT: (
        '', '#303030', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
viewcvs = {ERRORTOKEN: (
              's#FF0000', '#FF8080', ''), 
   DECORATOR_NAME: (
                  '', '#000000', ''), 
   DECORATOR: (
             '', '#000000', ''), 
   ARGS: (
        '', '#000000', ''), 
   NAME: (
        '', '#000000', ''), 
   NUMBER: (
          '', '#000000', ''), 
   OPERATOR: (
            '', '#000000', ''), 
   MATH_OPERATOR: (
                 '', '#000000', ''), 
   BRACKETS: (
            '', '#000000', ''), 
   COMMENT: (
           'i', '#b22222', ''), 
   DOUBLECOMMENT: (
                 'i', '#b22222', ''), 
   CLASS_NAME: (
              '', '#000000', ''), 
   DEF_NAME: (
            'b', '#0000ff', ''), 
   KEYWORD: (
           'b', '#a020f0', ''), 
   SINGLEQUOTE: (
               'b', '#bc8f8f', ''), 
   SINGLEQUOTE_R: (
                 'b', '#bc8f8f', ''), 
   SINGLEQUOTE_U: (
                 'b', '#bc8f8f', ''), 
   DOUBLEQUOTE: (
               'b', '#bc8f8f', ''), 
   DOUBLEQUOTE_R: (
                 'b', '#bc8f8f', ''), 
   DOUBLEQUOTE_U: (
                 'b', '#bc8f8f', ''), 
   TRIPLESINGLEQUOTE: (
                     'b', '#bc8f8f', ''), 
   TRIPLESINGLEQUOTE_R: (
                       'b', '#bc8f8f', ''), 
   TRIPLESINGLEQUOTE_U: (
                       'b', '#bc8f8f', ''), 
   TRIPLEDOUBLEQUOTE: (
                     'b', '#bc8f8f', ''), 
   TRIPLEDOUBLEQUOTE_R: (
                       'b', '#bc8f8f', ''), 
   TRIPLEDOUBLEQUOTE_U: (
                       'b', '#bc8f8f', ''), 
   TEXT: (
        '', '#000000', ''), 
   LINENUMBER: (
              '>ti#555555', '#000000', ''), 
   PAGEBACKGROUND: '#FFFFFF'}
defaultColors = lite

def Usage():
    doc = '\n -----------------------------------------------------------------------------\n  PySourceColor.py ver: %s\n -----------------------------------------------------------------------------\n  Module summary:\n     This module is designed to colorize python source code.\n         Input--->python source\n         Output-->colorized (html, html4.01/css, xhtml1.0)\n     Standalone:\n         This module will work from the command line with options.\n         This module will work with redirected stdio.\n     Imported:\n         This module can be imported and used directly in your code.\n -----------------------------------------------------------------------------\n  Command line options:\n     -h, --help\n         Optional-> Display this help message.\n     -t, --test\n         Optional-> Will ignore all others flags but  --profile\n             test all schemes and markup combinations\n     -p, --profile\n         Optional-> Works only with --test or -t\n             runs profile.py and makes the test work in quiet mode.\n     -i, --in, --input\n         Optional-> If you give input on stdin.\n         Use any of these for the current dir (.,cwd)\n         Input can be file or dir.\n         Input from stdin use one of the following (-,stdin)\n         If stdin is used as input stdout is output unless specified.\n     -o, --out, --output\n         Optional-> output dir for the colorized source.\n             default: output dir is the input dir.\n         To output html to stdout use one of the following (-,stdout)\n         Stdout can be used without stdin if you give a file as input.\n     -c, --color\n         Optional-> null, mono, dark, dark2, lite, idle, pythonwin, viewcvs\n             default: dark \n     -s, --show\n         Optional-> Show page after creation.\n             default: no show\n     -m, --markup\n         Optional-> html, css, xhtml\n             css, xhtml also support external stylesheets (-e,--external)\n             default: HTML\n     -e, --external\n         Optional-> use with css, xhtml\n             Writes an style sheet instead of embedding it in the page\n             saves it as pystyle.css in the same directory.\n             html markup will silently ignore this flag.\n     -H, --header\n         Opional-> add a page header to the top of the output\n         -H\n             Builtin header (name,date,hrule)\n         --header\n             You must specify a filename.\n             The header file must be valid html\n             and must handle its own font colors.\n             ex. --header c:/tmp/header.txt\n     -F, --footer\n         Opional-> add a page footer to the bottom of the output\n         -F \n             Builtin footer (hrule,name,date)\n         --footer\n             You must specify a filename.\n             The footer file must be valid html\n             and must handle its own font colors.\n             ex. --footer c:/tmp/footer.txt  \n     -l, --linenumbers\n         Optional-> default is no linenumbers\n             Adds line numbers to the start of each line in the code.\n    --convertpage\n         Given a webpage that has code embedded in tags it will\n             convert embedded code to colorized html. \n             (see pageconvert for details)\n -----------------------------------------------------------------------------\n  Option usage:\n   # Test and show pages\n      python PySourceColor.py -t -s\n   # Test and only show profile results\n      python PySourceColor.py -t -p\n   # Colorize all .py,.pyw files in cwdir you can also use: (.,cwd)\n      python PySourceColor.py -i .\n   # Using long options w/ =\n      python PySourceColor.py --in=c:/myDir/my.py --color=lite --show\n   # Using short options w/out =\n      python PySourceColor.py -i c:/myDir/  -c idle -m css -e\n   # Using any mix\n      python PySourceColor.py --in . -o=c:/myDir --show\n   # Place a custom header on your files\n      python PySourceColor.py -i . -o c:/tmp -m xhtml --header c:/header.txt\n -----------------------------------------------------------------------------\n  Stdio usage:\n   # Stdio using no options\n      python PySourceColor.py < c:/MyFile.py > c:/tmp/MyFile.html\n   # Using stdin alone automatically uses stdout for output: (stdin,-)\n      python PySourceColor.py -i- < c:/MyFile.py > c:/tmp/myfile.html\n   # Stdout can also be written to directly from a file instead of stdin\n      python PySourceColor.py -i c:/MyFile.py -m css -o- > c:/tmp/myfile.html\n   # Stdin can be used as input , but output can still be specified\n      python PySourceColor.py -i- -o c:/pydoc.py.html -s < c:/Python22/my.py\n _____________________________________________________________________________\n '
    print doc % __version__
    sys.exit(1)


def cli():
    """Handle command line args and redirections"""
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hseqtplHFi:o:c:m:h:f:', ['help', 'show', 'quiet',
         'test', 'external', 'linenumbers', 'convertpage', 'profile',
         'input=', 'output=', 'color=', 'markup=', 'header=', 'footer='])
    except getopt.GetoptError:
        Usage()

    input = None
    output = None
    colorscheme = None
    markup = 'html'
    header = None
    footer = None
    linenumbers = 0
    show = 0
    quiet = 0
    test = 0
    profile = 0
    convertpage = 0
    form = None
    for (o, a) in opts:
        if o in ('-h', '--help'):
            Usage()
            sys.exit()
        if o in ('-o', '--output', '--out'):
            output = a
        if o in ('-i', '--input', '--in'):
            input = a
            if input in ('.', 'cwd'):
                input = os.getcwd()
        if o in ('-s', '--show'):
            show = 1
        if o in ('-q', '--quiet'):
            quiet = 1
        if o in ('-t', '--test'):
            test = 1
        if o in ('--convertpage', ):
            convertpage = 1
        if o in ('-p', '--profile'):
            profile = 1
        if o in ('-e', '--external'):
            form = 'external'
        if o in ('-m', '--markup'):
            markup = str(a)
        if o in ('-l', '--linenumbers'):
            linenumbers = 1
        if o in ('--header', ):
            header = str(a)
        elif o == '-H':
            header = ''
        if o in ('--footer', ):
            footer = str(a)
        elif o == '-F':
            footer = ''
        if o in ('-c', '--color'):
            try:
                colorscheme = globals().get(a.lower())
            except:
                traceback.print_exc()
                Usage()

    if test:
        if profile:
            import profile
            profile.run('_test(show=%s, quiet=%s)' % (show, quiet))
        else:
            _test(show, quiet)
    elif input in (None, '-', 'stdin') or output in ('-', 'stdout'):
        if input not in (None, '-', 'stdin'):
            if os.path.isfile(input):
                path2stdout(input, colors=colorscheme, markup=markup, linenumbers=linenumbers, header=header, footer=footer, form=form)
            else:
                raise PathError, 'File does not exists!'
        else:
            try:
                if sys.stdin.isatty():
                    raise InputError, 'Please check input!'
                elif output in (None, '-', 'stdout'):
                    str2stdout(sys.stdin.read(), colors=colorscheme, markup=markup, header=header, footer=footer, linenumbers=linenumbers, form=form)
                else:
                    str2file(sys.stdin.read(), outfile=output, show=show, markup=markup, header=header, footer=footer, linenumbers=linenumbers, form=form)
            except:
                traceback.print_exc()
                Usage()

    elif os.path.exists(input):
        if convertpage:
            pageconvert(input, out=output, colors=colorscheme, show=show, markup=markup, linenumbers=linenumbers)
        else:
            convert(source=input, outdir=output, colors=colorscheme, show=show, markup=markup, quiet=quiet, header=header, footer=footer, linenumbers=linenumbers, form=form)
    else:
        raise PathError, 'File does not exists!'
        Usage()
    return


def _test(show=0, quiet=0):
    """Test the parser and most of the functions.

       There are 19 test total(eight colorschemes in three diffrent markups,
       and a str2file test. Most functions are tested by this.
    """
    fi = sys.argv[0]
    if not fi.endswith('.exe'):
        path2file(fi, '/tmp/null.html', null, show=show, quiet=quiet)
        path2file(fi, '/tmp/null_css.html', null, show=show, markup='css', quiet=quiet)
        path2file(fi, '/tmp/mono.html', mono, show=show, quiet=quiet)
        path2file(fi, '/tmp/mono_css.html', mono, show=show, markup='css', quiet=quiet)
        path2file(fi, '/tmp/lite.html', lite, show=show, quiet=quiet)
        path2file(fi, '/tmp/lite_css.html', lite, show=show, markup='css', quiet=quiet, header='', footer='', linenumbers=1)
        path2file(fi, '/tmp/lite_xhtml.html', lite, show=show, markup='xhtml', quiet=quiet)
        path2file(fi, '/tmp/dark.html', dark, show=show, quiet=quiet)
        path2file(fi, '/tmp/dark_css.html', dark, show=show, markup='css', quiet=quiet, linenumbers=1)
        path2file(fi, '/tmp/dark2.html', dark2, show=show, quiet=quiet)
        path2file(fi, '/tmp/dark2_css.html', dark2, show=show, markup='css', quiet=quiet)
        path2file(fi, '/tmp/dark2_xhtml.html', dark2, show=show, markup='xhtml', quiet=quiet, header='', footer='', linenumbers=1, form='external')
        path2file(fi, '/tmp/idle.html', idle, show=show, quiet=quiet)
        path2file(fi, '/tmp/idle_css.html', idle, show=show, markup='css', quiet=quiet)
        path2file(fi, '/tmp/viewcvs.html', viewcvs, show=show, quiet=quiet, linenumbers=1)
        path2file(fi, '/tmp/viewcvs_css.html', viewcvs, show=show, markup='css', linenumbers=1, quiet=quiet)
        path2file(fi, '/tmp/pythonwin.html', pythonwin, show=show, quiet=quiet)
        path2file(fi, '/tmp/pythonwin_css.html', pythonwin, show=show, markup='css', quiet=quiet)
        teststr = b'"""This is a test of decorators and other things"""\n# This should be line 421...\n@whatever(arg,arg2)\n@A @B(arghh) @C\ndef LlamaSaysNi(arg=\'Ni!\',arg2="RALPH"):\n   """This docstring is deeply disturbed by all the llama references"""\n   print \'%s The Wonder Llama says %s\'% (arg2,arg)\n# So I was like duh!, and he was like ya know?!,\n# and so we were both like huh...wtf!? RTFM!! LOL!!;)\n@staticmethod## Double comments are KewL.\ndef LlamasRLumpy():\n   """This docstring is too sexy to be here.\n   """\n   u"""\n=============================\nA M\xf8\xf8se once bit my sister...\n=============================\n   """\n   ## Relax, this won\'t hurt a bit, just a simple, painless procedure,\n   ## hold still while I get the anesthetizing hammer.\n   m = {\'three\':\'1\',\'won\':\'2\',\'too\':\'3\'}\n   o = r\'fishy\\fishy\\fishy/fish\\oh/where/is\\my/little\\..\'\n   python = uR""" \n No realli! She was Karving her initials \xf8n the m\xf8\xf8se with the sharpened end  \n of an interspace t\xf8\xf8thbrush given her by Svenge - her brother-in-law -an Oslo\n dentist and star of many Norwegian m\xf8vies: "The H\xf8t Hands of an Oslo         \n Dentist", "Fillings of Passion", "The Huge M\xf8lars of Horst Nordfink"..."""\n   RU"""142 MEXICAN WHOOPING LLAMAS"""#<-Can you fit 142 llamas in a red box?\n   n = u\' HERMSGERV\xd8RDENBR\xd8TB\xd8RDA \' + """ YUTTE """\n   t = """SAMALLNIATNUOMNAIRODAUCE"""+"DENIARTYLLAICEPS04"\n   ## We apologise for the fault in the\n   ## comments. Those responsible have been\n   ## sacked.\n   y = \'14 NORTH CHILEAN GUANACOS \\\n(CLOSELY RELATED TO THE LLAMA)\'\n   rules = [0,1,2,3,4,5]\n   print y'
        htmlPath = os.path.abspath('/tmp/strtest_lines.html')
        str2file(teststr, htmlPath, colors=dark, markup='xhtml', linenumbers=420, show=show)
        _printinfo('  wrote %s' % htmlPath, quiet)
        htmlPath = os.path.abspath('/tmp/strtest_nolines.html')
        str2file(teststr, htmlPath, colors=dark, markup='xhtml', show=show)
        _printinfo('  wrote %s' % htmlPath, quiet)
    else:
        Usage()


def str2stdout(sourcestring, colors=None, title='', markup='html', header=None, footer=None, linenumbers=0, form=None):
    """Converts a code(string) to colorized HTML. Writes to stdout.

       form='code',or'snip' (for "<pre>yourcode</pre>" only)
       colors=null,mono,lite,dark,dark2,idle,or pythonwin
    """
    Parser(sourcestring, colors=colors, title=title, markup=markup, header=header, footer=footer, linenumbers=linenumbers).format(form)


def path2stdout(sourcepath, title='', colors=None, markup='html', header=None, footer=None, linenumbers=0, form=None):
    """Converts code(file) to colorized HTML. Writes to stdout.

       form='code',or'snip' (for "<pre>yourcode</pre>" only)
       colors=null,mono,lite,dark,dark2,idle,or pythonwin
    """
    sourcestring = open(sourcepath).read()
    Parser(sourcestring, colors=colors, title=sourcepath, markup=markup, header=header, footer=footer, linenumbers=linenumbers).format(form)


def str2html(sourcestring, colors=None, title='', markup='html', header=None, footer=None, linenumbers=0, form=None):
    """Converts a code(string) to colorized HTML. Returns an HTML string.

       form='code',or'snip' (for "<pre>yourcode</pre>" only)
       colors=null,mono,lite,dark,dark2,idle,or pythonwin
    """
    stringIO = StringIO.StringIO()
    Parser(sourcestring, colors=colors, title=title, out=stringIO, markup=markup, header=header, footer=footer, linenumbers=linenumbers).format(form)
    stringIO.seek(0)
    return stringIO.read()


def str2css(sourcestring, colors=None, title='', markup='css', header=None, footer=None, linenumbers=0, form=None):
    """Converts a code string to colorized CSS/HTML. Returns CSS/HTML string
       
       If form != None then this will return (stylesheet_str, code_str)
       colors=null,mono,lite,dark,dark2,idle,or pythonwin
    """
    if markup.lower() not in ('css', 'xhtml'):
        markup = 'css'
    stringIO = StringIO.StringIO()
    parse = Parser(sourcestring, colors=colors, title=title, out=stringIO, markup=markup, header=header, footer=footer, linenumbers=linenumbers)
    parse.format(form)
    stringIO.seek(0)
    if form != None:
        return (parse._sendCSSStyle(external=1), stringIO.read())
    else:
        return (
         None, stringIO.read())
        return


def str2markup(sourcestring, colors=None, title='', markup='xhtml', header=None, footer=None, linenumbers=0, form=None):
    """ Convert code strings into ([stylesheet or None], colorized string) """
    if markup.lower() == 'html':
        return (None,
         str2html(sourcestring, colors=colors, title=title, header=header, footer=footer, markup=markup, linenumbers=linenumbers, form=form))
    else:
        return str2css(sourcestring, colors=colors, title=title, header=header, footer=footer, markup=markup, linenumbers=linenumbers, form=form)
        return


def str2file(sourcestring, outfile, colors=None, title='', markup='html', header=None, footer=None, linenumbers=0, show=0, dosheet=1, form=None):
    """Converts a code string to a file.

       makes no attempt at correcting bad pathnames
    """
    (css, html) = str2markup(sourcestring, colors=colors, title='', markup=markup, header=header, footer=footer, linenumbers=linenumbers, form=form)
    f = open(outfile, 'wt')
    f.writelines(html)
    f.close()
    if css != None and dosheet:
        dir = os.path.dirname(outfile)
        outcss = os.path.join(dir, 'pystyle.css')
        f = open(outcss, 'wt')
        f.writelines(css)
        f.close()
    if show:
        showpage(outfile)
    return


def path2html(sourcepath, colors=None, markup='html', header=None, footer=None, linenumbers=0, form=None):
    """Converts code(file) to colorized HTML. Returns an HTML string.

       form='code',or'snip' (for "<pre>yourcode</pre>" only)
       colors=null,mono,lite,dark,dark2,idle,or pythonwin
    """
    stringIO = StringIO.StringIO()
    sourcestring = open(sourcepath).read()
    Parser(sourcestring, colors, title=sourcepath, out=stringIO, markup=markup, header=header, footer=footer, linenumbers=linenumbers).format(form)
    stringIO.seek(0)
    return stringIO.read()


def convert(source, outdir=None, colors=None, show=0, markup='html', quiet=0, header=None, footer=None, linenumbers=0, form=None):
    """Takes a file or dir as input and places the html in the outdir.

       If outdir is none it defaults to the input dir
    """
    count = 0
    if not os.path.isdir(source):
        if os.path.isfile(source):
            count += 1
            path2file(source, outdir, colors, show, markup, quiet, form, header, footer, linenumbers, count)
        else:
            raise PathError, 'File does not exist!'
    else:
        fileList = walkdir(source)
        if fileList != None:
            if outdir != None:
                if os.path.splitext(outdir)[1] != '':
                    outdir = os.path.split(outdir)[0]
            for item in fileList:
                count += 1
                path2file(item, outdir, colors, show, markup, quiet, form, header, footer, linenumbers, count)

            _printinfo('Completed colorizing %s files.' % str(count), quiet)
        else:
            _printinfo('No files to convert in dir.', quiet)
    return


def path2file(sourcePath, out=None, colors=None, show=0, markup='html', quiet=0, form=None, header=None, footer=None, linenumbers=0, count=1):
    """ Converts python source to html file"""
    if out == None:
        htmlPath = sourcePath + '.html'
    elif os.path.splitext(out)[1] == '':
        if not os.path.isdir(out):
            os.makedirs(out)
        sourceName = os.path.basename(sourcePath)
        htmlPath = os.path.join(out, sourceName) + '.html'
    else:
        outdir = os.path.split(out)[0]
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        htmlPath = out
    htmlPath = os.path.abspath(htmlPath)
    source = open(sourcePath).read()
    parse = Parser(source, colors, sourcePath, open(htmlPath, 'wt'), markup, header, footer, linenumbers)
    parse.format(form)
    _printinfo('  wrote %s' % htmlPath, quiet)
    if form == 'external' and count == 1 and markup != 'html':
        cssSheet = parse._sendCSSStyle(external=1)
        cssPath = os.path.join(os.path.dirname(htmlPath), 'pystyle.css')
        css = open(cssPath, 'wt')
        css.write(cssSheet)
        css.close()
        _printinfo('    wrote %s' % cssPath, quiet)
    if show:
        showpage(htmlPath)
    return htmlPath


def tagreplace(sourcestr, colors=lite, markup='xhtml', linenumbers=0, dosheet=1, tagstart=('<PY>').lower(), tagend=('</PY>').lower(), stylesheet='pystyle.css'):
    """This is a helper function for pageconvert. Returns css, page.
    """
    if markup.lower() != 'html':
        link = '<link rel="stylesheet" href="%s" type="text/css"/></head>'
        css = link % stylesheet
        if sourcestr.find(css) == -1:
            sourcestr = sourcestr.replace('</head>', css, 1)
    starttags = sourcestr.count(tagstart)
    endtags = sourcestr.count(tagend)
    if starttags:
        if starttags == endtags:
            for _ in range(starttags):
                datastart = sourcestr.find(tagstart)
                dataend = sourcestr.find(tagend)
                data = sourcestr[datastart + len(tagstart):dataend]
                data = unescape(data)
                (css, data) = str2markup(data, colors=colors, linenumbers=linenumbers, markup=markup, form='embed')
                start = sourcestr[:datastart]
                end = sourcestr[dataend + len(tagend):]
                sourcestr = ('').join([start, data, end])

        else:
            raise InputError, 'Tag mismatch!\nCheck %s,%s tags' % tagstart, tagend
    if not dosheet:
        css = None
    return (
     css, sourcestr)


def pageconvert(path, out=None, colors=lite, markup='xhtml', linenumbers=0, dosheet=1, tagstart=('<PY>').lower(), tagend=('</PY>').lower(), stylesheet='pystyle', show=1, returnstr=0):
    """This function can colorize Python source

       that is written in a webpage enclosed in tags.
    """
    if out == None:
        out = os.path.dirname(path)
    infile = open(path, 'r').read()
    (css, page) = tagreplace(sourcestr=infile, colors=colors, markup=markup, linenumbers=linenumbers, dosheet=dosheet, tagstart=tagstart, tagend=tagend, stylesheet=stylesheet)
    if not returnstr:
        newpath = os.path.abspath(os.path.join(out, 'tmp', os.path.basename(path)))
        if not os.path.exists(newpath):
            try:
                os.makedirs(os.path.dirname(newpath))
            except:
                pass

        y = open(newpath, 'w')
        y.write(page)
        y.close()
        if css:
            csspath = os.path.abspath(os.path.join(out, 'tmp', '%s.css' % stylesheet))
            x = open(csspath, 'w')
            x.write(css)
            x.close()
        if show:
            try:
                os.startfile(newpath)
            except:
                traceback.print_exc()

        return newpath
    else:
        return (
         css, page)
        return


def walkdir(dir):
    """Return a list of .py and .pyw files from a given directory.

       This function can be written as a generator Python 2.3, or a genexp
       in Python 2.4. But 2.2 and 2.1 would be left out....
    """
    GLOB_PATTERN = os.path.join(dir, '*.[p][y]*')
    pathlist = glob.glob(GLOB_PATTERN)
    filterlist = [ x for x in pathlist if x.endswith('.py') or x.endswith('.pyw')
                 ]
    if filterlist != []:
        return filterlist
    else:
        return
        return


def showpage(path):
    """Helper function to open webpages"""
    try:
        import webbrowser
        webbrowser.open_new(os.path.abspath(path))
    except:
        traceback.print_exc()


def _printinfo(message, quiet):
    """Helper to print messages"""
    if not quiet:
        print message


def escape(text):
    """escape text for html. similar to cgi.escape"""
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    return text


def unescape(text):
    """unsecape escaped text"""
    text = text.replace('&quot;', '"')
    text = text.replace('&gt;', '>')
    text = text.replace('&lt;', '<')
    text = text.replace('&amp;', '&')
    return text


class PySourceColorError(Exception):

    def __init__(self, msg=''):
        self._msg = msg
        Exception.__init__(self, msg)

    def __repr__(self):
        return self._msg

    __str__ = __repr__


class PathError(PySourceColorError):

    def __init__(self, msg):
        PySourceColorError.__init__(self, 'Path error! : %s' % msg)


class InputError(PySourceColorError):

    def __init__(self, msg):
        PySourceColorError.__init__(self, 'Input error! : %s' % msg)


class Parser(object):
    """MoinMoin python parser heavily chopped :)"""

    def __init__(self, raw, colors=None, title='', out=sys.stdout, markup='html', header=None, footer=None, linenumbers=0):
        """Store the source text & set some flags"""
        if colors == None:
            colors = defaultColors
        self.raw = raw.expandtabs().rstrip()
        self.title = os.path.basename(title)
        self.out = out
        self.line = ''
        self.lasttext = ''
        self.argFlag = 0
        self.classFlag = 0
        self.defFlag = 0
        self.decoratorFlag = 0
        self.external = 0
        self.markup = markup.upper()
        self.colors = colors
        self.header = header
        self.footer = footer
        self.doArgs = 1
        self.doNames = 1
        self.doMathOps = 1
        self.doBrackets = 1
        self.doURL = 1
        self.LINENUMHOLDER = ('___line___').upper()
        self.LINESTART = ('___start___').upper()
        self.skip = 0
        self.extraspace = self.colors.get(EXTRASPACE, '')
        self.dolinenums = self.linenum = abs(linenumbers)
        if linenumbers < 0:
            self.numberlinks = 1
        else:
            self.numberlinks = 0
        return

    def format(self, form=None):
        """Parse and send the colorized source"""
        if form in ('snip', 'code'):
            self.addEnds = 0
        elif form == 'embed':
            self.addEnds = 0
            self.external = 1
        else:
            if form == 'external':
                self.external = 1
            self.addEnds = 1
        self.lines = [
         0, 0]
        pos = 0
        if self.dolinenums:
            start = self.LINENUMHOLDER + ' ' + self.extraspace
        else:
            start = '' + self.extraspace
        newlines = []
        lines = self.raw.splitlines(0)
        for l in lines:
            if l.startswith('#$#') or l.startswith('#%#') or l.startswith('#@#'):
                newlines.append(l)
            elif self.markup in ('XHTML', 'CSS'):
                newlines.append(self.LINESTART + ' ' + start + l)
            else:
                newlines.append(start + l)

        self.raw = ('\n').join(newlines) + '\n'
        while 1:
            pos = self.raw.find('\n', pos) + 1
            if not pos:
                break
            self.lines.append(pos)

        self.lines.append(len(self.raw))
        self.pos = 0
        text = StringIO.StringIO(self.raw)
        if self.addEnds:
            self._doPageStart()
        else:
            self._doSnippetStart()
        try:
            tokenize.tokenize(text.readline, self)
        except tokenize.TokenError, ex:
            msg = ex[0]
            line = ex[1][0]
            self.out.write('<h3>ERROR: %s</h3>%s\n' % (
             msg, self.raw[self.lines[line]:]))

        if self.addEnds:
            self._doPageEnd()
        else:
            self._doSnippetEnd()

    def __call__(self, toktype, toktext, (srow, scol), (erow, ecol), line):
        """Token handler. Order is important do not rearrange."""
        self.line = line
        oldpos = self.pos
        newpos = self.lines[srow] + scol
        self.pos = newpos + len(toktext)
        if toktype in (token.NEWLINE, tokenize.NL):
            self.decoratorFlag = self.argFlag = 0
            if self.markup in ('XHTML', 'CSS'):
                self.out.write('</span>')
            self.out.write('\n')
            return
        if newpos > oldpos:
            if self.raw[oldpos:newpos].isspace():
                if self.lasttext != self.LINESTART and self.lasttext != self.LINENUMHOLDER:
                    self.out.write(self.raw[oldpos:newpos])
                else:
                    self.out.write(self.raw[oldpos + 1:newpos])
            else:
                slash = self.raw[oldpos:newpos].find('\\') + oldpos
                self.out.write(self.raw[oldpos:slash])
                getattr(self, '_send%sText' % self.markup)(OPERATOR, '\\')
                self.linenum += 1
                if self.markup in ('XHTML', 'CSS'):
                    self.out.write('</span>')
                self.out.write(self.raw[slash + 1:newpos])
        if toktype in (token.INDENT, token.DEDENT):
            self.pos = newpos
            return
        if token.LPAR <= toktype and toktype <= token.OP:
            if toktext == '@':
                toktype = DECORATOR
                self.decoratorFlag = self.argFlag = 1
            else:
                if self.doArgs:
                    if toktext == '(' and self.argFlag:
                        self.argFlag = 2
                    elif toktext == ':':
                        self.argFlag = 0
                if self.doBrackets and toktext in ('[', ']', '(', ')', '{', '}'):
                    toktype = BRACKETS
                elif self.doMathOps and toktext in ('*=', '**=', '-=', '+=', '|=',
                                                    '%=', '>>=', '<<=', '=', '^=',
                                                    '/=', '+', '-', '**', '*', '/',
                                                    '%'):
                    toktype = MATH_OPERATOR
                else:
                    toktype = OPERATOR
                    if toktext == '=' and self.argFlag == 2:
                        self.argFlag = 1
                    elif toktext == ',' and self.argFlag == 1:
                        self.argFlag = 2
        elif toktype == NAME and keyword.iskeyword(toktext):
            toktype = KEYWORD
            if toktext in ('class', 'def'):
                if toktext == 'class' and not line[:line.find('class')].endswith('.'):
                    self.classFlag = self.argFlag = 1
                elif toktext == 'def' and not line[:line.find('def')].endswith('.'):
                    self.defFlag = self.argFlag = 1
                else:
                    toktype = ERRORTOKEN
        elif (self.classFlag or self.defFlag or self.decoratorFlag) and self.doNames:
            if self.classFlag:
                self.classFlag = 0
                toktype = CLASS_NAME
            elif self.defFlag:
                self.defFlag = 0
                toktype = DEF_NAME
            elif self.decoratorFlag:
                self.decoratorFlag = 0
                toktype = DECORATOR_NAME
        elif toktype == token.STRING:
            text = toktext.lower()
            if text[:3] == '"""':
                toktype = TRIPLEDOUBLEQUOTE
            elif text[:4] == 'r"""':
                toktype = TRIPLEDOUBLEQUOTE_R
            elif text[:4] == 'u"""' or text[:5] == 'ur"""':
                toktype = TRIPLEDOUBLEQUOTE_U
            elif text[:1] == '"':
                toktype = DOUBLEQUOTE
            elif text[:2] == 'r"':
                toktype = DOUBLEQUOTE_R
            elif text[:2] == 'u"' or text[:3] == 'ur"':
                toktype = DOUBLEQUOTE_U
            elif text[:3] == "'''":
                toktype = TRIPLESINGLEQUOTE
            elif text[:4] == "r'''":
                toktype = TRIPLESINGLEQUOTE_R
            elif text[:4] == "u'''" or text[:5] == "ur'''":
                toktype = TRIPLESINGLEQUOTE_U
            elif text[:1] == "'":
                toktype = SINGLEQUOTE
            elif text[:2] == "r'":
                toktype = SINGLEQUOTE_R
            elif text[:2] == "u'" or text[:3] == "ur'":
                toktype = SINGLEQUOTE_U
            if self.lasttext.lower() == 'ru':
                toktype = ERRORTOKEN
        elif toktype == COMMENT:
            if toktext[:2] == '##':
                toktype = DOUBLECOMMENT
            elif toktext[:3] == '#$#':
                toktype = TEXT
                self.textFlag = 'SPAN'
                toktext = toktext[3:]
            elif toktext[:3] == '#%#':
                toktype = TEXT
                self.textFlag = 'DIV'
                toktext = toktext[3:]
            elif toktext[:3] == '#@#':
                toktype = TEXT
                self.textFlag = 'RAW'
                toktext = toktext[3:]
            if self.doURL:
                url_pos = toktext.find('url(')
                if url_pos != -1:
                    before = toktext[:url_pos]
                    url = toktext[url_pos + 4:]
                    splitpoint = url.find(',')
                    endpoint = url.find(')')
                    after = url[endpoint + 1:]
                    url = url[:endpoint]
                    if splitpoint != -1:
                        urlparts = url.split(',', 1)
                        toktext = '%s<a href="%s">%s</a>%s' % (
                         before, urlparts[0], urlparts[1].lstrip(), after)
                    else:
                        toktext = '%s<a href="%s">%s</a>%s' % (before, url, url, after)
        elif toktype == ERRORTOKEN:
            if self.argFlag and toktext.isspace():
                self.out.write(toktext)
                return
            if toktext.isspace():
                if self.skip:
                    self.skip = 0
                    return
                else:
                    self.out.write(toktext)
                    return
            elif toktext == '@':
                toktype = DECORATOR
                self.decoratorFlag = self.argFlag = 1
        elif self.argFlag == 2 and toktype == NAME and toktext != 'None' and self.doArgs:
            toktype = ARGS
        if toktext in [self.LINENUMHOLDER, self.LINESTART]:
            toktype = LINENUMBER
            if toktext == self.LINESTART and not self.dolinenums or toktext == self.LINENUMHOLDER:
                self.skip = 1
        if toktext == '':
            return
        self.lasttext = toktext
        if toktype in (DOUBLECOMMENT, COMMENT):
            if toktext.find('<a href=') == -1:
                toktext = escape(toktext)
        elif toktype == TEXT:
            pass
        else:
            toktext = escape(toktext)
        getattr(self, '_send%sText' % self.markup)(toktype, toktext)

    def _doSnippetStart(self):
        if self.markup == 'HTML':
            self.out.write('<pre>\n')
        else:
            self.out.write(self.colors.get(CODESTART, '<pre class="py">\n'))

    def _doSnippetEnd(self):
        self.out.write(self.colors.get(CODEEND, '</pre>\n'))

    def _getFile(self, filepath):
        try:
            _file = open(filepath, 'r')
            content = _file.read()
            _file.close()
        except:
            traceback.print_exc()
            content = ''

        return content

    def _doPageStart(self):
        getattr(self, '_do%sStart' % self.markup)()

    def _doPageHeader(self):
        if self.header != None:
            if self.header.find('#$#') != -1 or self.header.find('#$#') != -1 or self.header.find('#%#') != -1:
                self.out.write(self.header[3:])
            else:
                if self.header != '':
                    self.header = self._getFile(self.header)
                getattr(self, '_do%sHeader' % self.markup)()
        return

    def _doPageFooter(self):
        if self.footer != None:
            if self.footer.find('#$#') != -1 or self.footer.find('#@#') != -1 or self.footer.find('#%#') != -1:
                self.out.write(self.footer[3:])
            else:
                if self.footer != '':
                    self.footer = self._getFile(self.footer)
                getattr(self, '_do%sFooter' % self.markup)()
        return

    def _doPageEnd(self):
        getattr(self, '_do%sEnd' % self.markup)()

    def _getLineNumber(self):
        num = self.linenum
        self.linenum += 1
        return str(num).rjust(5) + ' '

    def _getTags(self, key):
        return self.colors.get(key, self.colors[NAME])[0]

    def _getForeColor(self, key):
        color = self.colors.get(key, self.colors[NAME])[1]
        if color[:1] != '#':
            color = '#000000'
        return color

    def _getBackColor(self, key):
        return self.colors.get(key, self.colors[NAME])[2]

    def _getPageColor(self):
        return self.colors.get(PAGEBACKGROUND, '#FFFFFF')

    def _getStyle(self, key):
        return self.colors.get(key, self.colors[NAME])

    def _getMarkupClass(self, key):
        return MARKUPDICT.get(key, MARKUPDICT[NAME])

    def _getDocumentCreatedBy(self):
        return '<!--This document created by %s ver.%s on: %s-->\n' % (
         __title__, __version__, time.ctime())

    def _doHTMLStart(self):
        self.out.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">\n')
        self.out.write('<html><head><title>%s</title>\n' % self.title)
        self.out.write(self._getDocumentCreatedBy())
        self.out.write('<meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1">\n')
        self.out.write('</head><body bgcolor="%s">\n' % self._getPageColor())
        self._doPageHeader()
        self.out.write('<pre>')

    def _getHTMLStyles(self, toktype, toktext):
        (tags, color) = self.colors.get(toktype, self.colors[NAME])[:2]
        tagstart = []
        tagend = []
        if 'b' in tags:
            tagstart.append('<b>')
            tagend.append('</b>')
        if 'i' in tags:
            tagstart.append('<i>')
            tagend.append('</i>')
        if 'u' in tags:
            tagstart.append('<u>')
            tagend.append('</u>')
        tagend.reverse()
        starttags = ('').join(tagstart)
        endtags = ('').join(tagend)
        return (starttags, endtags, color)

    def _sendHTMLText(self, toktype, toktext):
        numberlinks = self.numberlinks
        if toktype == ERRORTOKEN:
            style = ' style="border: solid 1.5pt #FF0000;"'
        else:
            style = ''
        (starttag, endtag, color) = self._getHTMLStyles(toktype, toktext)
        if toktext.count(self.LINENUMHOLDER):
            if toktype == LINENUMBER:
                splittext = toktext.split(self.LINENUMHOLDER)
            else:
                splittext = toktext.split(self.LINENUMHOLDER + ' ')
            store = []
            store.append(splittext.pop(0))
            (lstarttag, lendtag, lcolor) = self._getHTMLStyles(LINENUMBER, toktext)
            count = len(splittext)
            for item in splittext:
                num = self._getLineNumber()
                if numberlinks:
                    numstrip = num.strip()
                    content = '<a name="%s" href="#%s">%s</a>' % (
                     numstrip, numstrip, num)
                else:
                    content = num
                if count <= 1:
                    (endtag, starttag) = ('', '')
                linenumber = ('').join([endtag, '<font color=', lcolor, '>',
                 lstarttag, content, lendtag, '</font>', starttag])
                store.append(linenumber + item)

            toktext = ('').join(store)
        if color != '#000000':
            startfont = '<font color="%s"%s>' % (color, style)
            endfont = '</font>'
        else:
            (startfont, endfont) = ('', '')
        if toktype != LINENUMBER:
            self.out.write(('').join([startfont, starttag,
             toktext, endtag, endfont]))
        else:
            self.out.write(toktext)

    def _doHTMLHeader(self):
        if self.header != '':
            self.out.write('%s\n' % self.header)
        else:
            color = self._getForeColor(NAME)
            self.out.write('<b><font color="%s"># %s                             <br># %s</font></b><hr>\n' % (
             color, self.title, time.ctime()))

    def _doHTMLFooter(self):
        if self.footer != '':
            self.out.write('%s\n' % self.footer)
        else:
            color = self._getForeColor(NAME)
            self.out.write('<b><font color="%s">                             <hr># %s<br># %s</font></b>\n' % (
             color, self.title, time.ctime()))

    def _doHTMLEnd(self):
        self.out.write('</pre>\n')
        self._doPageFooter()
        self.out.write('</body></html>\n')

    def _getCSSStyle(self, key):
        (tags, forecolor, backcolor) = self._getStyle(key)
        style = []
        border = None
        bordercolor = None
        tags = tags.lower()
        if tags:
            if '#' in tags:
                start = tags.find('#')
                end = start + 7
                bordercolor = tags[start:end]
                tags.replace(bordercolor, '', 1)
            if 'b' in tags:
                style.append('font-weight:bold;')
            else:
                style.append('font-weight:normal;')
            if 'i' in tags:
                style.append('font-style:italic;')
            if 'u' in tags:
                style.append('text-decoration:underline;')
            if 'l' in tags:
                size = 'thick'
            elif 'm' in tags:
                size = 'medium'
            elif 't' in tags:
                size = 'thin'
            else:
                size = 'medium'
            if 'n' in tags:
                border = 'inset'
            elif 'o' in tags:
                border = 'outset'
            elif 'r' in tags:
                border = 'ridge'
            elif 'g' in tags:
                border = 'groove'
            elif '=' in tags:
                border = 'double'
            elif '.' in tags:
                border = 'dotted'
            elif '-' in tags:
                border = 'dashed'
            elif 's' in tags:
                border = 'solid'
            seperate_sides = 0
            for side in ['<', '>', '^', 'v']:
                if side in tags:
                    seperate_sides += 1

            if seperate_sides == 0 and border:
                style.append('border: %s %s;' % (border, size))
            else:
                if border == None:
                    border = 'solid'
                if 'v' in tags:
                    style.append('border-bottom:%s %s;' % (border, size))
                if '<' in tags:
                    style.append('border-left:%s %s;' % (border, size))
                if '>' in tags:
                    style.append('border-right:%s %s;' % (border, size))
                if '^' in tags:
                    style.append('border-top:%s %s;' % (border, size))
        else:
            style.append('font-weight:normal;')
        if bordercolor:
            style.append('border-color:%s;' % bordercolor)
        style.append('color:%s;' % forecolor)
        if backcolor:
            style.append('background-color:%s;' % backcolor)
        return (
         self._getMarkupClass(key), (' ').join(style))

    def _sendCSSStyle(self, external=0):
        """ create external and internal style sheets"""
        styles = []
        external += self.external
        if not external:
            styles.append('<style type="text/css">\n<!--\n')
        styles.append('body { background:%s; }\n' % self._getPageColor())
        for key in MARKUPDICT:
            styles.append('.%s { %s }\n' % self._getCSSStyle(key))

        styles.append(self.colors.get(PY, '.py { }\n'))
        styles.append(self.colors.get(CSSHOOK, ''))
        if not self.external:
            styles.append('--></style>\n')
        return ('').join(styles)

    def _doCSSStart(self):
        self.out.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">\n')
        self.out.write('<html><head><title>%s</title>\n' % self.title)
        self.out.write(self._getDocumentCreatedBy())
        self.out.write('<meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1">\n')
        self._doCSSStyleSheet()
        self.out.write('</head>\n<body>\n')
        self._doPageHeader()
        self.out.write(self.colors.get(CODESTART, '<pre class="py">\n'))

    def _doCSSStyleSheet(self):
        if not self.external:
            self.out.write(self._sendCSSStyle())
        else:
            self.out.write('<link rel="stylesheet" href="pystyle.css" type="text/css">')

    def _sendCSSText(self, toktype, toktext):
        markupclass = MARKUPDICT.get(toktype, MARKUPDICT[NAME])
        if toktext == self.LINESTART and toktype == LINENUMBER:
            self.out.write('<span class="py_line">')
            return
        if toktext.count(self.LINENUMHOLDER):
            newmarkup = MARKUPDICT.get(LINENUMBER, MARKUPDICT[NAME])
            lstartspan = '<span class="%s">' % newmarkup
            if toktype == LINENUMBER:
                splittext = toktext.split(self.LINENUMHOLDER)
            else:
                splittext = toktext.split(self.LINENUMHOLDER + ' ')
            store = []
            store.append(splittext.pop(0))
            for item in splittext:
                num = self._getLineNumber()
                if self.numberlinks:
                    numstrip = num.strip()
                    content = '<a name="%s" href="#%s">%s</a>' % (
                     numstrip, numstrip, num)
                else:
                    content = num
                linenumber = ('').join([lstartspan, content, '</span>'])
                store.append(linenumber + item)

            toktext = ('').join(store)
        if toktext.count(self.LINESTART):
            store = []
            parts = toktext.split(self.LINESTART + ' ')
            first = parts.pop(0)
            pos = first.rfind('\n')
            if pos != -1:
                first = first[:pos] + '</span></span>' + first[pos:]
            store.append(first)
            for item in parts:
                if self.dolinenums:
                    item = item.replace('</span>', '</span><span class="%s">' % markupclass)
                else:
                    item = '<span class="%s">%s' % (markupclass, item)
                pos = item.rfind('\n')
                if pos != -1:
                    item = item[:pos] + '</span></span>\n'
                store.append(item)

            toktext = ('<span class="py_line">').join(store)
        if toktype != LINENUMBER:
            if toktype == TEXT and self.textFlag == 'DIV':
                startspan = '<div class="%s">' % markupclass
                endspan = '</div>'
            elif toktype == TEXT and self.textFlag == 'RAW':
                (startspan, endspan) = ('', '')
            else:
                startspan = '<span class="%s">' % markupclass
                endspan = '</span>'
            self.out.write(('').join([startspan, toktext, endspan]))
        else:
            self.out.write(toktext)

    def _doCSSHeader(self):
        if self.header != '':
            self.out.write('%s\n' % self.header)
        else:
            name = MARKUPDICT.get(NAME)
            self.out.write('<div class="%s"># %s <br> # %s</div><hr>\n' % (name, self.title, time.ctime()))

    def _doCSSFooter(self):
        if self.footer != '':
            self.out.write('%s\n' % self.footer)
        else:
            self.out.write('<hr><div class="%s"># %s <br> # %s</div>\n' % (MARKUPDICT.get(NAME), self.title, time.ctime()))

    def _doCSSEnd(self):
        self.out.write(self.colors.get(CODEEND, '</pre>\n'))
        self._doPageFooter()
        self.out.write('</body></html>\n')

    def _doXHTMLStart(self):
        self.out.write('<?xml version="1.0"?>\n <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"\n     "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n <html xmlns="http://www.w3.org/1999/xhtml">\n')
        self.out.write('<head><title>%s</title>\n' % self.title)
        self.out.write(self._getDocumentCreatedBy())
        self.out.write('<meta http-equiv="Content-Type" content="text/html;charset=iso-8859-1"/>\n')
        self._doXHTMLStyleSheet()
        self.out.write('</head>\n<body>\n')
        self._doPageHeader()
        self.out.write(self.colors.get(CODESTART, '<pre class="py">\n'))

    def _doXHTMLStyleSheet(self):
        if not self.external:
            self.out.write(self._sendCSSStyle())
        else:
            self.out.write('<link rel="stylesheet" href="pystyle.css" type="text/css"/>\n')

    def _sendXHTMLText(self, toktype, toktext):
        self._sendCSSText(toktype, toktext)

    def _doXHTMLHeader(self):
        if self.header:
            self.out.write('%s\n' % self.header)
        else:
            name = MARKUPDICT.get(NAME)
            self.out.write('<div class="%s"># %s <br/> # %s</div><hr/>\n ' % (
             name, self.title, time.ctime()))

    def _doXHTMLFooter(self):
        if self.footer:
            self.out.write('%s\n' % self.footer)
        else:
            self.out.write('<hr/><div class="%s"># %s <br/> # %s</div>\n' % (MARKUPDICT.get(NAME), self.title, time.ctime()))

    def _doXHTMLEnd(self):
        self._doCSSEnd()


if __name__ == '__main__':
    cli()
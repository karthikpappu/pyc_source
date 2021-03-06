# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xdis/main.py
# Compiled at: 2020-04-24 01:34:41
"""
CPython independent disassembly routines

There are two reasons we can't use Python's built-in routines
from dis. First, the bytecode we are extracting may be from a different
version of Python (different magic number) than the version of Python
that is doing the extraction.

Second, we need structured instruction information for the
(de)-parsing step. Python 3.4 and up provides this, but we still do
want to run on Python 2.7.
"""
import datetime, re, sys
try:
    from collections import deque
except ImportError:

    class deque:
        __module__ = __name__

        def __init__(self, initial_todo=[]):
            self.todo = initial_todo

        def popleft(self):
            return self.todo.pop()

        def append(self, item):
            return self.todo.append(item)

        def __len__(self):
            return len(self.todo)


import xdis
from xdis import IS_PYPY
from xdis.bytecode import Bytecode
from xdis.codetype import iscode, codeType2Portable
from xdis.load import check_object_path, load_module
from xdis.cross_dis import format_code_info
from xdis.version import VERSION
from xdis.op_imports import op_imports

def get_opcode(version, is_pypy):
    lookup = str(version)
    if is_pypy:
        lookup += 'pypy'
    if lookup in op_imports.keys():
        return op_imports[lookup]
    if is_pypy:
        pypy_str = ' for pypy'
    else:
        pypy_str = ''
    raise TypeError('%s is not a Python version%s I know about' % (version, pypy_str))


def show_module_header(bytecode_version, co, timestamp, out=sys.stdout, is_pypy=False, magic_int=None, source_size=None, sip_hash=None, header=True, show_filename=True):
    real_out = out or sys.stdout
    if is_pypy:
        co_pypy_str = 'PyPy '
    else:
        co_pypy_str = ''
    if IS_PYPY:
        run_pypy_str = 'PyPy '
    else:
        run_pypy_str = ''
    if header:
        magic_str = ''
        if magic_int:
            magic_str = str(magic_int)
        real_out.write('# pydisasm version %s\n# %sPython bytecode %s%s\n# Disassembled from %sPython %s\n' % (VERSION, co_pypy_str, bytecode_version, ' (%s)' % magic_str, run_pypy_str, ('\n# ').join(sys.version.split('\n'))))
    if timestamp is not None:
        value = datetime.datetime.fromtimestamp(timestamp)
        real_out.write('# Timestamp in code: %d' % timestamp)
        real_out.write(value.strftime(' (%Y-%m-%d %H:%M:%S)\n'))
    if source_size is not None:
        real_out.write('# Source code size mod 2**32: %d bytes\n' % source_size)
    if sip_hash is not None:
        real_out.write('# SipHash:           0x%x\n' % sip_hash)
    if show_filename:
        real_out.write('# Embedded file name: %s\n' % co.co_filename)
    return


def disco(bytecode_version, co, timestamp, out=sys.stdout, is_pypy=False, magic_int=None, source_size=None, sip_hash=None, header=True, asm_format=False, show_bytes=False, dup_lines=False):
    """
    diassembles and deparses a given code block 'co'
    """
    assert iscode(co)
    show_module_header(bytecode_version, co, timestamp, out, is_pypy, magic_int, source_size, sip_hash, header, show_filename=False)
    real_out = out or sys.stdout
    if co.co_filename and not asm_format:
        real_out.write(format_code_info(co, bytecode_version) + '\n')
    opc = get_opcode(bytecode_version, is_pypy)
    if asm_format:
        disco_loop_asm_format(opc, bytecode_version, co, real_out, {}, set([]))
    else:
        queue = deque([co])
        disco_loop(opc, bytecode_version, queue, real_out, show_bytes=show_bytes)


def disco_loop(opc, version, queue, real_out, dup_lines=False, show_bytes=False):
    """Disassembles a queue of code objects. If we discover
    another code object which will be found in co_consts, we add
    the new code to the list. Note that the order of code discovery
    is in the order of first encountered which is not amenable for
    the format used by a disassembler where code objects should
    be defined before using them in other functions.
    However this is not recursive and will overall lead to less
    memory consumption at run time.
    """
    while len(queue) > 0:
        co = queue.popleft()
        if co.co_name not in ('<module>', '?'):
            real_out.write('\n' + format_code_info(co, version) + '\n')
        bytecode = Bytecode(co, opc, dup_lines=dup_lines)
        real_out.write(bytecode.dis(show_bytes=show_bytes) + '\n')
        for c in co.co_consts:
            if iscode(c):
                queue.append(c)


def code_uniquify(basename, co_code):
    return '%s_0x%x' % (basename, id(co_code))


def disco_loop_asm_format(opc, version, co, real_out, fn_name_map, all_fns):
    """Produces disassembly in a format more conducive to
    automatic assembly by producing inner modules before they are
    used by outer ones. Since this is recusive, we'll
    use more stack space at runtime.
    """
    co = codeType2Portable(co)
    co_name = co.co_name
    mapped_name = fn_name_map.get(co_name, co_name)
    new_consts = []
    for c in co.co_consts:
        if iscode(c):
            if isinstance(c, types.CodeType):
                c_compat = codeType2Portable(c)
            else:
                c_compat = c
            disco_loop_asm_format(opc, version, c_compat, real_out, fn_name_map, all_fns)
            m = re.match('.* object <(.+)> at', str(c))
            if m:
                basename = m.group(1)
                if basename != 'module':
                    mapped_name = code_uniquify(basename, c.co_code)
                    c_compat.co_name = mapped_name
            c_compat.freeze()
            new_consts.append(c_compat)
        else:
            new_consts.append(c)

    co.co_consts = new_consts
    m = re.match('^<(.+)>$', co.co_name)
    if m or co_name in all_fns:
        if co_name in all_fns:
            basename = co_name
        else:
            basename = m.group(1)
        if basename != 'module':
            mapped_name = code_uniquify(basename, co.co_code)
            co_name = mapped_name
            assert mapped_name not in fn_name_map
        fn_name_map[mapped_name] = basename
        co.co_name = mapped_name
    elif co_name in fn_name_map:
        mapped_name = code_uniquify(co_name, co.co_code)
        fn_name_map[mapped_name] = co_name
        co.co_name = mapped_name
    co = co.freeze()
    all_fns.add(co_name)
    if co.co_name != '<module>' or co.co_filename:
        real_out.write('\n' + format_code_info(co, version, mapped_name) + '\n')
    bytecode = Bytecode(co, opc, dup_lines=True)
    real_out.write(bytecode.dis(asm_format=True) + '\n')


def disassemble_file(filename, outstream=sys.stdout, asm_format=False, header=False, show_bytes=False):
    """
    disassemble Python byte-code file (.pyc)

    If given a Python source file (".py") file, we'll
    try to find the corresponding compiled object.
    """
    filename = check_object_path(filename)
    (version, timestamp, magic_int, co, is_pypy, source_size, sip_hash) = load_module(filename)
    if header:
        show_module_header(version, co, timestamp, outstream, is_pypy, magic_int, source_size, sip_hash, show_filename=True)
    else:
        disco(version, co, timestamp, outstream, is_pypy, magic_int, source_size, sip_hash, asm_format=asm_format, show_bytes=show_bytes)
    return (
     filename, co, version, timestamp, magic_int, is_pypy, source_size, sip_hash)


def _test():
    """Simple test program to disassemble a file."""
    argc = len(sys.argv)
    if argc != 2:
        if argc == 1 and xdis.PYTHON3:
            fn = __file__
        else:
            sys.stderr.write('usage: %s [-|CPython compiled file]\n' % __file__)
            sys.exit(2)
    else:
        fn = sys.argv[1]
    disassemble_file(fn)


if __name__ == '__main__':
    _test()
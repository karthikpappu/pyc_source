# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xpython/pyvm2.py
# Compiled at: 2020-05-08 06:20:17
"""A pure-Python Python bytecode interpreter."""
from __future__ import print_function, division
import linecache, logging, operator, sys, six
from six.moves import reprlib
from xdis import PYTHON3, PYTHON_VERSION, IS_PYPY, op_has_argument
from xdis.util import code2num, CO_NEWLOCALS
from xdis.op_imports import get_opcode_module
from xpython.pyobj import Frame, Block, traceback_from_frame
from xpython.byteop import get_byteop
PY2 = not PYTHON3
log = logging.getLogger(__name__)
if PYTHON3:
    byteint = lambda b: b
else:
    byteint = ord
repr_obj = reprlib.Repr()
repr_obj.maxother = 120
repper = repr_obj.repr

class VMError(Exception):
    """For raising errors in the operation of the VM."""
    pass


class VMRuntimeError(Exception):
    """RuntimeError in operation of the VM."""
    pass


class VirtualMachine(object):

    def __init__(self, python_version=PYTHON_VERSION, vmtest_testing=False, is_pypy=IS_PYPY):
        self.frames = []
        self.frame = None
        self.return_value = None
        self.last_exception = None
        self.last_traceback_limit = None
        self.last_traceback = None
        self.version = python_version
        self.is_pypy = is_pypy
        self.vmtest_testing = vmtest_testing
        self.last_exception = None
        self.fn2native = {}
        self.in_exception_processing = False
        self.VMError = VMError
        int_vers = int(python_version * 10)
        version_info = (int_vers // 10, int_vers % 10)
        self.opc = get_opcode_module(version_info)
        self.byteop = get_byteop(self, python_version, is_pypy)
        return

    def top(self):
        """Return the value at the top of the stack, with no changes."""
        return self.frame.stack[(-1)]

    def pop(self, i=0):
        """Pop a value from the stack.

        Default to the top of the stack, but `i` can be a count from the top
        instead.

        """
        return self.frame.stack.pop(-1 - i)

    def push(self, *vals):
        """Push values onto the value stack."""
        self.frame.stack.extend(vals)

    def popn(self, n):
        """Pop a number of values from the value stack.

        A list of `n` values is returned, the deepest value first.

        """
        if n:
            ret = self.frame.stack[-n:]
            self.frame.stack[(-n):] = []
            return ret
        else:
            return []

    def peek(self, n):
        """Get a value `n` entries down in the stack, without changing the stack."""
        return self.frame.stack[(-n)]

    def push_block(self, type, handler=None, level=None):
        if level is None:
            level = len(self.frame.stack)
        self.frame.block_stack.append(Block(type, handler, level))
        return

    def pop_block(self):
        return self.frame.block_stack.pop()

    def top_block(self):
        return self.frame.block_stack[(-1)]

    def jump(self, jump):
        """Move the bytecode pointer to `jump`, so it will execute next."""
        self.frame.f_lasti = jump

    def make_frame(self, code, callargs={}, f_globals=None, f_locals=None):
        log.debug('make_frame: code=%r, callargs=%s, f_globals=%r, f_locals=%r', code, repper(callargs), (
         type(f_globals), id(f_globals)), (
         type(f_locals), id(f_locals)))
        if f_globals is not None:
            f_globals = f_globals
            if f_locals is None:
                f_locals = f_globals
        elif self.frames:
            f_globals = self.frame.f_globals
            if f_locals is None:
                f_locals = {}
        else:
            f_globals = f_locals = {'__builtins__': __builtins__, 
               '__name__': '__main__', 
               '__doc__': None, 
               '__package__': None}
        if code.co_flags & CO_NEWLOCALS:
            f_locals = {'__locals__': {}}
        f_locals.update(callargs)
        frame = Frame(code, f_globals, f_locals, self.frame)
        log.debug('%r', frame)
        return frame

    def push_frame(self, frame):
        self.frames.append(frame)
        self.frame = frame

    def pop_frame(self):
        self.frames.pop()
        if self.frames:
            self.frame = self.frames[(-1)]
        else:
            self.frame = None
        return

    def print_frames(self):
        """Print the call stack for debugging. Note that the
        format exactly the same as in traceback.print_tb()
        """
        for f in self.frames:
            filename = f.f_code.co_filename
            lineno = f.line_number()
            print('  File "%s", line %d, in %s' % (filename, lineno, f.f_code.co_name))
            linecache.checkcache(filename)
            line = linecache.getline(filename, lineno, f.f_globals)
            if line:
                print('    ' + line.strip())

    def resume_frame(self, frame):
        frame.f_back = self.frame
        log.debug('resume_frame: %r', frame)
        val = self.run_frame(frame)
        frame.f_back = None
        return val

    def run_code(self, code, f_globals=None, f_locals=None):
        """run code using f_globals and f_locals in our VM"""
        frame = self.make_frame(code, f_globals=f_globals, f_locals=f_locals)
        try:
            val = self.run_frame(frame)
        except Exception:
            if self.vmtest_testing:
                raise
            if self.last_traceback:
                self.last_traceback.print_tb()
                print('%s' % self.last_exception[0].__name__, end='')
                exc_value = self.last_exception[1]
                tail = ': %s' % ('\n').join(self.last_exception[1].args) if self.last_exception[1].args else ''
                print(tail)
            raise VMRuntimeError

        if self.frames:
            raise VMError('Frames left over!')
        if self.frame and self.frame.stack:
            raise VMError('Data left on stack! %r' % self.frame.stack)
        return val

    def instruction_info(self, byteName, arguments, opoffset):
        frame = self.frame
        code = frame.f_code
        return '%d: %s %s\n\t%s in %s:%s' % (
         opoffset,
         byteName,
         arguments,
         code.co_name,
         code.co_filename,
         frame.f_lineno)

    def unwind_block(self, block):
        if block.type == 'except-handler':
            offset = 3
        else:
            offset = 0
        while len(self.frame.stack) > block.level + offset:
            self.pop()

        if block.type == 'except-handler':
            tb, value, exctype = self.popn(3)
            self.last_exception = (exctype, value, tb)

    def parse_byte_and_args(self):
        """ Parse 1 - 3 bytes of bytecode into
        an instruction and optionally arguments."""
        f = self.frame
        f_code = f.f_code
        co_code = f_code.co_code
        extended_arg = 0
        while True:
            opoffset = f.f_lasti
            line_number = self.linestarts.get(opoffset, None)
            byteCode = byteint(co_code[opoffset])
            byteName = self.opc.opname[byteCode]
            f.f_lasti += 1
            arg = None
            arguments = []
            if op_has_argument(byteCode, self.opc):
                if PYTHON_VERSION >= 3.6:
                    intArg = code2num(co_code, f.f_lasti) | extended_arg
                    f.f_lasti += 1
                    if byteCode == self.opc.EXTENDED_ARG:
                        extended_arg = intArg << 8
                        continue
                    else:
                        extended_arg = 0
                else:
                    intArg = code2num(co_code, f.f_lasti) + code2num(co_code, f.f_lasti + 1) * 256 + extended_arg
                    f.f_lasti += 2
                    if byteCode == self.opc.EXTENDED_ARG:
                        extended_arg = intArg * 65536
                        continue
                    else:
                        extended_arg = 0
                if byteCode in self.opc.CONST_OPS:
                    arg = f_code.co_consts[intArg]
                elif byteCode in self.opc.FREE_OPS:
                    if intArg < len(f_code.co_cellvars):
                        arg = f_code.co_cellvars[intArg]
                    else:
                        var_idx = intArg - len(f.f_code.co_cellvars)
                        arg = f_code.co_freevars[var_idx]
                elif byteCode in self.opc.NAME_OPS:
                    arg = f_code.co_names[intArg]
                elif byteCode in self.opc.JREL_OPS:
                    arg = f.f_lasti + intArg
                elif byteCode in self.opc.JABS_OPS:
                    arg = intArg
                elif byteCode in self.opc.LOCAL_OPS:
                    arg = f_code.co_varnames[intArg]
                else:
                    arg = intArg
                arguments = [
                 arg]
            elif PYTHON_VERSION >= 3.6:
                f.f_lasti += 1
            break

        return (
         byteName, arguments, opoffset, line_number)

    def log(self, byteName, arguments, opoffset, line_number):
        """ Log arguments, block stack, and data stack for each opcode."""
        if line_number is not None:
            op = 'Line %4d, ' % line_number
        else:
            op = '           '
        op += '%3d: %s' % (opoffset, byteName)
        if arguments:
            op += ' %r' % (arguments[0],)
        indent = '    ' * (len(self.frames) - 1)
        stack_rep = repper(self.frame.stack)
        block_stack_rep = repper(self.frame.block_stack)
        log.debug('  %sframe.stack: %s' % (indent, stack_rep))
        log.debug('  %sblocks     : %s' % (indent, block_stack_rep))
        log.info('%s%s' % (indent, op))
        return

    def dispatch(self, byteName, arguments, opoffset):
        """ Dispatch by bytename to the corresponding methods.
        Exceptions are caught and set on the virtual machine."""
        why = None
        self.in_exception_processing = False
        try:
            if byteName.startswith('UNARY_'):
                self.unaryOperator(byteName[6:])
            elif byteName.startswith('BINARY_'):
                self.binaryOperator(byteName[7:])
            elif byteName.startswith('INPLACE_'):
                self.inplaceOperator(byteName[8:])
            elif 'SLICE+' in byteName:
                self.sliceOperator(byteName)
            else:
                if hasattr(self.byteop, byteName):
                    bytecode_fn = getattr(self.byteop, byteName, None)
                if not bytecode_fn:
                    raise VMError('Unknown bytecode type: %s\n\t%s' % (
                     self.instruction_info(byteName, arguments, opoffset),
                     byteName))
                why = bytecode_fn(*arguments)
        except:
            self.last_exception = sys.exc_info()
            if not self.in_exception_processing:
                if self.last_exception[0] != SystemExit:
                    log.info('exception in the execution of instruction:\n\t%s' % self.instruction_info(byteName, arguments, opoffset))
                self.last_traceback = traceback_from_frame(self.frame)
                self.in_exception_processing = True
            why = 'exception'

        return why

    def manage_block_stack(self, why):
        """ Manage a frame's block stack.
        Manipulate the block stack and data stack for looping,
        exception handling, or returning."""
        assert why != 'yield'
        block = self.frame.block_stack[(-1)]
        if block.type == 'loop' and why == 'continue':
            self.jump(self.return_value)
            why = None
            return why
        else:
            self.pop_block()
            self.unwind_block(block)
            if block.type == 'loop' and why == 'break':
                why = None
                self.jump(block.handler)
                return why
            if self.version < 3.0:
                if block.type == 'finally' or block.type == 'setup-except' and why == 'exception' or block.type == 'with':
                    if why == 'exception':
                        exctype, value, tb = self.last_exception
                        self.push(tb, value, exctype)
                    else:
                        if why in ('return', 'continue'):
                            self.push(self.return_value)
                        self.push(why)
                    why = None
                    self.jump(block.handler)
                    return why
            else:
                if why == 'exception' and block.type in ('setup-except', 'finally'):
                    self.push_block('except-handler')
                    exctype, value, tb = self.last_exception
                    self.push(tb, value, exctype)
                    self.push(tb, value, exctype)
                    why = None
                    self.jump(block.handler)
                    return why
                if block.type == 'finally':
                    if why in ('return', 'continue'):
                        self.push(self.return_value)
                    self.push(why)
                    why = None
                    self.jump(block.handler)
                    return why
            return why

    def run_frame(self, frame):
        """Run a frame until it returns (somehow).

        Exceptions are raised, the return value is returned.

        """
        self.push_frame(frame)
        self.f_code = self.frame.f_code
        self.linestarts = dict(self.opc.findlinestarts(self.f_code, dup_lines=True))
        opoffset = 0
        while True:
            byteName, arguments, opoffset, line_number = self.parse_byte_and_args()
            if log.isEnabledFor(logging.INFO):
                self.log(byteName, arguments, opoffset, line_number)
            why = self.dispatch(byteName, arguments, opoffset)
            if why == 'exception':
                if not self.in_exception_processing:
                    if self.last_exception[0] != SystemExit:
                        log.info('exception in the execution of instruction:\n\t%s' % self.instruction_info(byteName, arguments, opoffset))
                    self.last_traceback = traceback_from_frame(self.frame)
                    self.in_exception_processing = True
            if why == 'reraise':
                why = 'exception'
            if why != 'yield':
                while why and frame.block_stack:
                    why = self.manage_block_stack(why)

            if why:
                break

        self.pop_frame()
        if why == 'exception':
            if self.last_exception and self.last_exception[0]:
                six.reraise(*self.last_exception)
            else:
                raise VMError('Borked exception recording')
        self.in_exception_processing = False
        return self.return_value

    UNARY_OPERATORS = {'POSITIVE': operator.pos, 
       'NEGATIVE': operator.neg, 
       'NOT': operator.not_, 
       'CONVERT': repr, 
       'INVERT': operator.invert}

    def unaryOperator(self, op):
        x = self.pop()
        self.push(self.UNARY_OPERATORS[op](x))

    BINARY_OPERATORS = {'POWER': pow, 
       'MULTIPLY': operator.mul, 
       'DIVIDE': getattr(operator, 'div', lambda x, y: None), 
       'FLOOR_DIVIDE': operator.floordiv, 
       'TRUE_DIVIDE': operator.truediv, 
       'MODULO': operator.mod, 
       'ADD': operator.add, 
       'SUBTRACT': operator.sub, 
       'SUBSCR': operator.getitem, 
       'LSHIFT': operator.lshift, 
       'RSHIFT': operator.rshift, 
       'AND': operator.and_, 
       'XOR': operator.xor, 
       'OR': operator.or_}
    if PYTHON_VERSION >= 3.5:
        BINARY_OPERATORS['MATRIX_MULTIPLY'] = operator.matmul

    def binaryOperator(self, op):
        x, y = self.popn(2)
        self.push(self.BINARY_OPERATORS[op](x, y))

    def inplaceOperator(self, op):
        x, y = self.popn(2)
        if op == 'POWER':
            x **= y
        elif op == 'MULTIPLY':
            x *= y
        elif op in ('DIVIDE', 'FLOOR_DIVIDE'):
            x //= y
        elif op == 'TRUE_DIVIDE':
            x /= y
        elif op == 'MODULO':
            x %= y
        elif op == 'ADD':
            x += y
        elif op == 'SUBTRACT':
            x -= y
        elif op == 'LSHIFT':
            x <<= y
        elif op == 'RSHIFT':
            x >>= y
        elif op == 'AND':
            x &= y
        elif op == 'XOR':
            x ^= y
        elif op == 'OR':
            x |= y
        elif op == 'MATRIX_MULTIPLY':
            operator.imatmul(x, y)
        else:
            raise VMError('Unknown in-place operator: %r' % op)
        self.push(x)

    def sliceOperator(self, op):
        start = 0
        end = None
        op, count = op[:-2], int(op[(-1)])
        if count == 1:
            start = self.pop()
        elif count == 2:
            end = self.pop()
        elif count == 3:
            end = self.pop()
            start = self.pop()
        l = self.pop()
        if end is None:
            end = len(l)
        if op.startswith('STORE_'):
            l[start:end] = self.pop()
        elif op.startswith('DELETE_'):
            del l[start:end]
        else:
            self.push(l[start:end])
        return
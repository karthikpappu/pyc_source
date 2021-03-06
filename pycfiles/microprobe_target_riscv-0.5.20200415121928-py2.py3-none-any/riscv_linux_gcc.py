# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rbertra/workspace/repos/github.com/IBM/microprobe/targets/riscv/env/riscv_linux_gcc.py
# Compiled at: 2020-03-29 13:02:20
"""
Docstring
"""
from __future__ import absolute_import
from microprobe.code.address import InstructionAddress
from microprobe.target.env import GenericEnvironment

class riscv64_linux_gcc(GenericEnvironment):
    _elf_code = ''

    def __init__(self, isa):
        super(riscv64_linux_gcc, self).__init__('riscv64_linux_gcc', 'RISC-V architecture (64bit addressing mode), Linux operating system, GCC compiler', isa)
        self._default_wrapper = 'CInfGen'

    @property
    def stack_pointer(self):
        """ """
        return self.isa.registers['X2']

    @property
    def stack_direction(self):
        """ """
        return 'increase'

    def elf_abi(self, stack_size, start_symbol, **kwargs):
        return super(riscv64_linux_gcc, self).elf_abi(stack_size, start_symbol, stack_alignment=16, **kwargs)

    def function_call(self, target, return_address_reg=None):
        if return_address_reg is None:
            return_address_reg = self.target.isa.registers['X1']
        if isinstance(target, str):
            target = InstructionAddress(base_address=target)
        jal_ins = self.target.new_instruction('JAL_V0')
        jal_ins.set_operands([target, return_address_reg])
        return [
         jal_ins]

    def function_return(self, return_address_reg=None):
        if return_address_reg is None:
            return_address_reg = self.target.isa.registers['X1']
        ret_ins = self.target.new_instruction('JALR_V0')
        ret_ins.set_operands([0,
         return_address_reg,
         self.target.isa.registers['X0']])
        return [ret_ins]
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/foxylib/tools/flowcontrol/condition_tools.py
# Compiled at: 2019-04-01 15:58:20
# Size of source mod 2**32: 436 bytes


class ConditionStatementToolkit:

    @classmethod
    def ternary(cls, v, f_cond=lambda x: x, f_null=None, f_true=lambda x: x, f_false=lambda x: x):
        c = f_cond(v)
        if c is None:
            if f_null is not None:
                return f_null(v)
        if c:
            return f_true(v)
        return f_false(v)


ternary = ConditionStatementToolkit.ternary
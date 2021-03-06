# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/expression/condition.py
# Compiled at: 2019-05-21 17:58:56
# Size of source mod 2**32: 3528 bytes
import uuid
from norm.executable import NormError
from norm.executable.constant import Constant
from norm.grammar.literals import COP, ConstantType, LOP
from norm.executable.expression import NormExpression
from norm.executable.schema.variable import VariableName
import logging
logger = logging.getLogger(__name__)

class ConditionExpr(NormExpression):

    def __init__(self, op, lexpr, rexpr):
        super().__init__()
        self.op = op
        self.lexpr = lexpr
        self.rexpr = rexpr
        self._condition = None
        assert self.lexpr is not None
        assert self.rexpr is not None
        assert self.op is not None

    def __str__(self):
        if self._condition is None:
            msg = 'Compile the condition expression first'
            logger.error(msg)
            raise NormError(msg)
        return self._condition

    def compile(self, context):
        if self.op == COP.LK:
            if not isinstance(self.lexpr, VariableName):
                raise AssertionError
            else:
                assert isinstance(self.rexpr, Constant)
                if not self.rexpr.type_ is ConstantType.STR:
                    if not self.rexpr.type_ is ConstantType.PTN:
                        raise AssertionError
            self._condition = '{}.str.contains({})'.format(self.lexpr, self.rexpr)
        else:
            self._condition = '({}) {} ({})'.format(self.lexpr, self.op, self.rexpr)
        self.eval_lam = self.lexpr.lam
        from norm.models import Lambda
        self.lam = Lambda((context.context_namespace), (context.TMP_VARIABLE_STUB + str(uuid.uuid4())), variables=(self.eval_lam.variables))
        self.lam.cloned_from = self.eval_lam
        return self

    def execute(self, context):
        self.lam.data = self.eval_lam.data.query((self._condition), engine='python')
        return self.lam.data


class CombinedConditionExpr(ConditionExpr):

    def __init__(self, op, lexpr, rexpr):
        super().__init__(op, lexpr, rexpr)

    def compile(self, context):
        if self._condition is not None:
            return self
        self.lexpr = self.lexpr.compile(context)
        self.rexpr = self.rexpr.compile(context)
        self._condition = '({}) {} ({})'.format(self.lexpr, self.op, self.rexpr)
        if not self.lexpr.eval_lam is self.rexpr.eval_lam:
            assert self.lexpr.eval_lam is self.rexpr.eval_lam.cloned_from
        self.eval_lam = self.lexpr.eval_lam
        from norm.models import Lambda
        self.lam = Lambda((context.context_namespace), (context.TMP_VARIABLE_STUB + str(uuid.uuid4())), variables=(self.eval_lam.variables))
        self.lam.cloned_from = self.eval_lam
        return self

    def execute(self, context):
        self.lam.data = self.eval_lam.data.query((self._condition), engine='python')
        return self.lam.data
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/mutator.py
# Compiled at: 2020-05-08 13:24:17
# Size of source mod 2**32: 4192 bytes
from typing import Iterable, Mapping, MutableMapping, Optional, Tuple, TypeVar, Union
import collections, logging, operator, types
from haoda import ir
from soda import tensor
import soda.visitor
_logger = logging.getLogger().getChild(__name__)

def shift(obj, offset, excluded=(), op=operator.sub, verbose=False):
    """Shift soda.ir.Ref with the given offset.

  All soda.ir.Ref, excluding the given names, will be shifted with the
  given offset using the given operator. The operator will be applied pointwise
  on the original index and the given offset.

  Args:
    obj: A haoda.ir.Node or a tensor.Tensor object.
    offset: Second operand given to the operator.
    excluded: Sequence of names to be excluded from the mutation. Default to ().
    op: Shifting operator. Should be either add or sub. Default to sub.
    verbose: Whether to log shiftings. Default to False.
  Returns:
    Mutated obj. If obj is an IR node, it will be a different object than the
    input. If obj is a tensor, it will be the same object but with fields
    mutated.
  """
    if op not in (operator.add, operator.sub):
        _logger.warn('shifting with neither + nor -, which most likely is an error')

    def visitor(obj, args):
        if isinstance(obj, ir.Ref):
            if obj.name not in excluded:
                new_idx = tuple(op(a, b) for a, b in zip(obj.idx, offset))
                if verbose:
                    _logger.debug('reference %s(%s) shifted to %s(%s)', obj.name, ', '.join(map(str, obj.idx)), obj.name, ', '.join(map(str, new_idx)))
                obj.idx = new_idx

    if isinstance(obj, ir.Node):
        return obj.visit(visitor)
    else:
        if isinstance(obj, tensor.Tensor):
            obj.mutate(visitor)
        else:
            raise TypeError('argument is not an IR node or a tensor')
        return obj


def normalize(obj: Union[(ir.Node, Iterable[ir.Node])], references: Optional[Mapping[(str, Tuple[(int, ...)])]]=None):
    """Make the least access index 0.

  Works on an ir.Node or an iterable of ir.Nodes. If it is shifted, a different
  object is constructed and returned. Otherwise, obj will be returned as-is.

  Args:
    obj: A node or an iterable of nodes.
  Returns:
    Normalized node or iterable.
  Raises:
    TypeError: If argument is not an ir.Node or an iterable of ir.Nodes.
  """
    if isinstance(obj, types.GeneratorType):
        return normalize(tuple(obj))
    else:
        norm_idx = soda.visitor.get_normalize_index(obj, references)
        shifter = lambda x: shift(x, norm_idx) if any(norm_idx) else x
        if isinstance(obj, collections.Iterable):
            return type(obj)(map(shifter, obj))
        if isinstance(obj, ir.Node):
            return shifter(obj)
    raise TypeError('argument is not an ir.Node or an iterable of ir.Nodes')


NodeT = TypeVar('NodeT', bound=(ir.Node))

def replace_expressions(obj: NodeT, cses: MutableMapping[(NodeT, ir.Ref)], used: Optional[MutableMapping[(NodeT, NodeT)]]=None, references: Optional[Mapping[(str, Tuple[(int, ...)])]]=None) -> NodeT:
    """Get AST with common subexpression elimination.

  Get AST with the given common subexpressions. If used is not None, the used
  common subexpressions will be added to used.

  Args:
    obj: An ir.Node.
    cses: Dict mapping normalized common subexpressions to the new ir.Ref.
    used: Set of used common subexpressions, or None.
  Returns:
    The ir.Node as the AST.
  """

    def visitor(obj, args):
        cses, used = args
        norm_idx = soda.visitor.get_normalize_index(obj, references)
        normalized = shift(obj, norm_idx) if any(norm_idx) else obj
        if normalized in cses:
            if used is not None:
                if normalized not in used:
                    used[normalized] = replace_expressions(normalized, {k:v for k, v in cses.items() if k != normalized}, used)
            new_obj = shift((cses[normalized]), norm_idx, op=(operator.add))
            _logger.debug('replacing %s with %s', obj, new_obj)
            return new_obj
        else:
            return obj

    return obj.visit(visitor, (cses, used))
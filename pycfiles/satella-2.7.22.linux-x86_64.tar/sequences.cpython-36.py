# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.6.7/lib/python3.6/site-packages/satella/coding/sequences/sequences.py
# Compiled at: 2020-05-04 17:22:35
# Size of source mod 2**32: 3669 bytes
import typing as tp
__all__ = ['is_last', 'add_next', 'half_cartesian', 'group_quantity']
T = tp.TypeVar('T')
U = tp.TypeVar('U')

def is_last(lst: tp.Iterable[T]) -> tp.Generator[(tp.Tuple[(bool, T)], None, None)]:
    """
    Return every element of the list, alongside a flag telling is this the last element.

    Use like:

    >>> for is_last, element in is_last(my_list):
    >>> if is_last:
    >>>     ...

    :param lst: list to iterate thru
    :return: a generator returning (bool, T)
    """
    iterable = iter(lst)
    ret_var = next(iterable)
    for val in iterable:
        yield (
         False, ret_var)
        ret_var = val

    yield (
     True, ret_var)


def add_next(lst: tp.Iterable[T], wrap_over: bool=False, skip_last: bool=False) -> tp.Iterator[tp.Tuple[(T, tp.Optional[T])]]:
    """
    Yields a 2-tuple of given iterable, presenting the next element as second element of the tuple.

    The last element will be the last element alongside with a None, if wrap_over is False, or the
    first element if wrap_over was True

    Example:

    >>> list(add_next([1, 2, 3, 4, 5])) == [(1, 2), (2, 3), (3, 4), (4, 5), (5, None)]
    >>> list(add_next([1, 2, 3, 4, 5], True)) == [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]

    :param lst: iterable to iterate over
    :param wrap_over: whether to attach the first element to the pair of the last element instead
        of None
    :param skip_last: if this is True, then last element, alongside with a None, won't be output
    """
    iterator = iter(lst)
    try:
        first_val = prev_val = next(iterator)
    except StopIteration:
        return
    else:
        for val in iterator:
            yield (
             prev_val, val)
            prev_val = val

        if wrap_over:
            yield (
             prev_val, first_val)
        elif not skip_last:
            yield (
             prev_val, None)


def half_cartesian(seq1: tp.Iterable[T], include_same_pairs: bool=True) -> tp.Iterator[tp.Tuple[(T, T)]]:
    """
    Generate half of the Cartesian product of both sequences.

    Useful when you have a commutative operation that you'd like to execute on both elements
    (eg. checking for collisions).

    Example:

    >>> list(half_cartesian([1, 2, 3], [1, 2, 3])) ==     >>>     [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]

    :param seq1: First sequence
    :param seq2: Second sequence
    :param include_same_pairs: if True, then pairs returning two of the same objects will be returned.
        Ie. if False, the following will be true:

    >>> list(half_cartesian([1, 2, 3], [1, 2, 3], include_same_pairs=False)) ==     >>>     [(1, 2), (1, 3), (2, 3)]

    """
    for i, elem1 in enumerate(seq1):
        for j, elem2 in enumerate(seq1):
            if include_same_pairs:
                if j >= i:
                    yield (
                     elem1, elem2)
                else:
                    if j > i:
                        yield (
                         elem1, elem2)


def group_quantity(length: int, seq: tp.Iterable[T]) -> tp.Generator[(tp.List[T], None, None)]:
    """
    Slice an iterable into lists containing at most len entries.

    Eg.

    >>> assert list(group_quantity(3, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])) == [[1, 2, 3], [4, 5, 6],
    >>>                                                                     [7, 8, 9], [10]]

    :param length: length for the returning sequences
    :param seq: sequence to split
    """
    entries = []
    for elem in seq:
        if len(entries) < length:
            entries.append(elem)
        else:
            yield entries
            entries = [elem]

    if entries:
        yield entries
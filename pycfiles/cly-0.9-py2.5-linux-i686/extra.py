# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cly/extra.py
# Compiled at: 2007-11-27 03:52:23
"""Useful functions for use in conjunction with CLY."""
__all__ = [
 'cull_candidates', 'static_candidates']
__docformat__ = 'restructuredtext en'

def cull_candidates(candidates, text):
    """Cull candidates that do not start with ``text``."""
    return filter(None, [ c + ' ' for c in candidates if c.startswith(text) ])


def static_candidates(*candidates):
    """Convenience function to provide candidates matching a prefix.

    Returns a callable that can be used directly with ``Node.candidates=``.

    >>> from cly.parser import Parser
    >>> from cly.builder import Grammar, Node
    >>> static_candidates('foo', 'bar')(None, 'f')
    ['foo ']
    >>> parser = Parser(Grammar(node=Node('Test', candidates=static_candidates('foo', 'fuzz', 'bar'))))
    >>> list(parser.parse('f').candidates())
    ['foo ', 'fuzz ']
    """

    def cull_candidates(context, text):
        return filter(None, [ c + ' ' for c in candidates if c.startswith(text) ])

    return cull_candidates


if __name__ == '__main__':
    import doctest
    doctest.testmod()
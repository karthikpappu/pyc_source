# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/cpip/core/CppCond.py
# Compiled at: 2017-10-03 13:07:15
r"""Provides a state stack of booleans to facilitate conditional compilation as:
:title-reference:`ISO/IEC 9899:1999(E) section 6.10.1` ('C') and
:title-reference:`ISO/IEC 14882:1998(E) section 16.1 ('C++') \[cpp.cond\]`

This does not interpret any semantics of either standard but instead provides
a state class that callers that do interpret the language semantics can use.

In particular this provides state change operations that might be triggered by
the following six pre-processing directives:

.. code-block:: c

    #if constant-expression new-line group opt
    #ifdef identifier new-line group opt
    #ifndef identifier new-line group opt
    #elif constant-expression new-line group opt
    #else new-line group opt
    #endif new-line

In this module a single :py:class:`CppCond` object has a stack of ConditionalState objects.
The latter has both a boolean state and an 'explanation' of that state at any
point in the translation.
The latter is represented by a list of string representations of either
constant-expression or identifier tokens.

The stack i.e. :py:class:`CppCond` can also be queried for its net boolean state and its
net 'explanation'.

Basic boolean stack operations:

.. code-block:: sh

    Directive   Argument                Stack, s, boolean operation
    ---------   --------                -----------------------
    #if         constant-expression     s.push(bool)
    #ifdef      identifier              s.push(bool)
    #ifndef     identifier              s.push(!bool)
    #elif       constant-expression     s.pop(), s.push(bool)
    #else       N/A                     Either s.push(!s.pop()) or s.flip()
    #endif      N/A                     s.pop()

Basic boolean 'explanation' string operations:

The ``'!'`` prefix is parameterised as :py:const:`TOKEN_NEGATION` so that any
subsequent processing can recognise ``'!!'`` as ``''`` and ``'!!!'`` as ``'!'``:

.. code-block:: none

        Directive   Argument                Matrix, m, strings
        ---------   --------                ------------------
        #if         constant-expression     m.push(['%s' % tokens,])
        #ifdef      identifier              m.push(['(defined %s)' % identifier)])
        #ifndef     identifier              m.push(['!(defined %s)' % identifier)])
        #elif       constant-expression     m[-1].push('!%s' % m[-1].pop()),
                                            m[-1].push(['%s' % tokens,])
                                            Note: Here we flip the existing state via
                                            a push(!pop())) then push the additional
                                            condition so that we have multiple
                                            contitions that are and'd together.
        #else       N/A                     m[-1].push('!%s' % m[-1].pop())
                                            Note: This is the negation of the sum of
                                            the previous #if, #elif statements.
        #endif      N/A                     m.pop()

.. note::
    The above does not include error checking such as pop() from an empty stack.

Stringifying the matrix m: ::

    flatList = []
    for aList in m:
        assert(len(aList) > 0)
        if len(aList) > 1:
            # Add parenthesis so that when flatList is flattened then booleans are
            # correctly protected.
            flatList.append('(%s)' % ' && '.join(aList))
        else:
            flatList.append(aList[0])
    return ' && '.join(flatList)

This returns for something like m is: ``[['a < 0',], ['!b', 'c > 45'], ['d < 27',],]``

Then this gives: ``"a < 0 && (!b && c > 45) && d < 27"``
"""
__author__ = 'Paul Ross'
__date__ = '2011-07-10'
__rights__ = 'Copyright (c) 2008-2017 Paul Ross'
import logging, collections, bisect
from cpip import ExceptionCpip
from cpip.core.FileLocation import START_LINE
CPP_COND_DIRECTIVES = ('if', 'ifdef', 'ifndef', 'elif', 'else', 'endif')
CPP_COND_IF_DIRECTIVES = ('if', 'ifdef', 'ifndef')
CPP_COND_ALT_DIRECTIVES = ('else', 'elif')
CPP_COND_END_DIRECTIVE = 'endif'
TOKEN_NEGATION = '!'
TOKEN_AND = '&&'
TOKEN_OR = '||'
TOKEN_PAD = ' '
TOKEN_JOIN_AND = '%s%s%s' % (TOKEN_PAD, TOKEN_AND, TOKEN_PAD)
TOKEN_JOIN_OR = '%s%s%s' % (TOKEN_PAD, TOKEN_OR, TOKEN_PAD)

class ExceptionCppCond(ExceptionCpip):
    """Simple specialisation of an exception class for the CppCond."""
    pass


class ExceptionCppCondGraph(ExceptionCppCond):
    """Simple specialisation of an exception class for the CppCondGraph."""
    pass


class ExceptionCppCondGraphElif(ExceptionCppCondGraph):
    """When the CppCondGraph sees an #elif preprocessing directive in the wrong sequence."""
    pass


class ExceptionCppCondGraphElse(ExceptionCppCondGraph):
    """When the CppCondGraph sees an #endif preprocessing directive in the wrong sequence."""
    pass


class ExceptionCppCondGraphNode(ExceptionCppCondGraph):
    """When the :py:class:`CppCondGraphNode` sees an preprocessing directive in the wrong sequence."""
    pass


class ExceptionCppCondGraphIfSection(ExceptionCppCondGraph):
    """Exception for a :py:class:`CppCondGraphIfSection`."""
    pass


class ConditionalState(object):
    """Holds a single conditional state."""

    def __init__(self, theState, theIdOrCondExpr):
        """theState is a boolean and theIdOrCondExpr is a string representing
        a constant-expression or identifier.
        The boolean state of this has restrictions appropriate to
        ``#if/#elif/#else`` processing in that the can not transition
        ``True->False->True`` i.e. can only have one True state.
        
        Of course ``False->True->False`` is permitted."""
        self._state = theState
        self._hasBeenTrue = self._state
        self._condList = []
        self._add(theIdOrCondExpr)

    def _add(self, theConstExpr):
        """Add a string to the list of constant expressions. Newline is replaced
        with a single space."""
        self._condList.append(theConstExpr.replace('\n', ' '))

    @property
    def state(self):
        """Returns boolean state of self."""
        assert len(self._condList) > 0
        return self._state

    @property
    def hasBeenTrue(self):
        """Return True if the state has been True at any time in the lifetime
        of this object."""
        return self._hasBeenTrue

    def flip(self):
        """Inverts the boolean such as for #else directive."""
        assert len(self._condList) > 0
        if not self._hasBeenTrue or self._state:
            self._state = not self._state
            if self._state:
                self._hasBeenTrue = True
        self.negateLastState()

    def flipAndAdd(self, theBool, theConstExpr):
        """This handles an #elif command on this item in the stack.
        This flips the state (if theBool is True) and negates the last
        expression on the condition list then appends theConstExpr
        onto the condition list."""
        assert len(self._condList) > 0
        if not self._hasBeenTrue or self._state:
            if theBool:
                self.flip()
            else:
                self.negateLastState()
                self._state = theBool
        else:
            self.negateLastState()
        self._add(theConstExpr)

    def negateLastState(self):
        """Inverts the state of the last item on the stack."""
        myStr = self._condList.pop()
        if not (myStr.startswith('(') and myStr.endswith(')')):
            myStr = '(%s)' % myStr
        self._condList.append('%s%s' % (TOKEN_NEGATION, myStr))

    def constExprStr(self, invert=False):
        """Returns self as a string which is the concatenation of constant-expressions."""
        assert len(self._condList) > 0
        if invert:
            return '%s(%s)' % (TOKEN_NEGATION, TOKEN_JOIN_OR.join(self._condList))
        if len(self._condList) > 1:
            return '(%s)' % TOKEN_JOIN_AND.join(self._condList)
        return self._condList[0]


class CppCond(object):
    """Provides a state stack to handle conditional compilation.
    This could be used by an implementation of conditional inclusion e.g.
    :title-reference:`ISO/IEC 14882:1998(E) section 16.1 Conditional inclusion [cpp.cond]`
    
    Essentially this class provides a state machine that can be created altered
    and queried.
    The APIs available to the caller correspond to the if-section part of the
    the applicable standard (i.e. ``#if`` ``#elif`` etc). Most APIs take two arguments;
    
    *theBool*
        Is a boolean that is the result of the callers evaluation of a
        constant-expression.
        
    *theIce*
        A string that represents the identifier or constant-expression
        in a way that the caller sees fit (i.e. this is not evaluated
        locally in any way).
        Combinations of such strings _are_ merged by use of boolean
        logic (``'!'``) and ``LPAREN`` and ``RPAREN``.
    """

    def __init__(self):
        """Constructor, this just initialise the internal state."""
        self._stateStack = []

    def close(self):
        """Finalisation, may raise :py:class:`ExceptionCppCond` is stack non-empty."""
        if len(self._stateStack) > 0:
            raise ExceptionCppCond('CppCond.close() on stack %s' % str(self))

    def __str__(self):
        """Returns a string representation of the stack.
        
        .. note::

            This returns a string that says 'if my state were True
            then this is why. This string does not explain actual state, for
            that consult :py:meth:`isTrue()`.
        """
        return '%s' % TOKEN_JOIN_AND.join([ x.constExprStr() for x in self._stateStack ])

    @property
    def stackDepth(self):
        """Returns the depth of the conditional stack as an integer."""
        return len(self._stateStack)

    def _push(self, theBool, theIce):
        """Pushes a new :py:class:`ConditionalState` object onto the stack."""
        self._stateStack.append(ConditionalState(theBool, theIce))

    def _pop(self):
        """Removes a :py:class:`ConditionalState` object from the stack.
        The removed object is returned."""
        if len(self._stateStack) == 0:
            raise ExceptionCppCond('CppCond._pop() on empty stack.')
        return self._stateStack.pop()

    def _flip(self):
        """Changes the state of the top :py:class:`ConditionalState` object on the stack."""
        if len(self._stateStack) == 0:
            raise ExceptionCppCond('CppCond._flip() on empty stack.')
        self._stateStack[(-1)].flip()

    def oIf(self, theBool, theConstExpr):
        """Deal with the result of a ``#if``.
        
        *theBool*
            Is a boolean that is the result of the callers evaluation of a
            constant-expression.
        
        *theConstExpr*
            A string that represents the identifier or
            constant-expression in a way that the caller sees fit (i.e. this is not
            evaluated locally in any way).
            Combinations of such strings _are_ merged by use of boolean
            logic ('!') and ``LPAREN`` and ``RPAREN``.
        """
        self._push(theBool, theConstExpr)

    def oIfdef(self, theBool, theConstExpr):
        """Deal with the result of a ``#ifdef``.
        
        *theBool*
            Is a boolean that is the result of the callers evaluation of a
            constant-expression.
        
        *theConstExpr*
            A string that represents the identifier or
            constant-expression in a way that the caller sees fit (i.e. this is not
            evaluated locally in any way).
            Combinations of such strings _are_ merged by use of boolean
            logic ('!') and ``LPAREN`` and ``RPAREN``.
        """
        self._push(theBool, theConstExpr)

    def oIfndef(self, theBool, theConstExpr):
        """Deal with the result of a ``#ifndef``.
        
        *theBool*
            Is a boolean that is the result of the callers evaluation of a
            constant-expression.
        
        *theConstExpr*
            A string that represents the identifier or
            constant-expression in a way that the caller sees fit (i.e. this is not
            evaluated locally in any way).
            Combinations of such strings _are_ merged by use of boolean
            logic ('!') and ``LPAREN`` and ``RPAREN``.
        """
        self._push(not theBool, theConstExpr)

    def oElif(self, theBool, theConstExpr):
        """Deal with the result of a ``#elif``.
        
        *theBool*
            Is a boolean that is the result of the callers evaluation of a
            constant-expression.
        
        *theConstExpr*
            A string that represents the identifier or
            constant-expression in a way that the caller sees fit (i.e. this is not
            evaluated locally in any way).
            Combinations of such strings _are_ merged by use of boolean
            logic ('!') and ``LPAREN`` and ``RPAREN``.
        """
        if len(self._stateStack) == 0:
            raise ExceptionCppCond('CppCond.oElif() on empty stack.')
        self._stateStack[(-1)].flipAndAdd(theBool, theConstExpr)

    def oElse(self):
        """Deal with the result of a ``#else``."""
        self._flip()

    def oEndif(self):
        """Deal with the result of a ``#endif``."""
        if len(self._stateStack) == 0:
            raise ExceptionCppCond('CppCond.oEndif() on empty stack.')
        self._pop()

    def __bool__(self):
        """Syntactic sugar for truth testing, wraps isTrue()."""
        return self.isTrue()

    def isTrue(self):
        """Returns True if all of the states in the stack are True, False otherwise."""
        if len(self._stateStack) == 0:
            return True
        for anObj in self._stateStack:
            if not anObj.state:
                return False

        return True

    def hasBeenTrueAtCurrentDepth(self):
        """Return True if the :py:class:`ConditionalState` at the current depth has ever been
        ``True``. This is used to decide whether to evaluate ``#elif`` expressions. They
        don't need to be if the :py:class:`ConditionalState` has already been True, and in
        fact, the C Rationale (6.10) says that bogus ``#elif`` expressions should
        **not** be evaluated in this case - i.e. ignore syntax errors."""
        if len(self._stateStack) == 0:
            return True
        return self._stateStack[(-1)].hasBeenTrue


StateConstExprFileLine = collections.namedtuple('StateConstExprLoc', 'fileId lineNum tuIndex state const_expr', verbose=False)

class CppCondGraphVisitorBase(object):
    """Base class for a CppCondGraph visitor object."""

    def visitPre(self, theCcgNode, theDepth):
        """Pre-traversal call with a :py:class:`CppCondGraphNode` and the integer depth in
        the tree."""
        raise NotImplementedError('CppCondGraphVisitorBase.visitPre() not implemented.')

    def visitPost(self, theCcgNode, theDepth):
        """Post-traversal call with a :py:class:`CppCondGraphNode` and the integer depth in
        the tree."""
        raise NotImplementedError('CppCondGraphVisitorBase.visitPost() not implemented.')


class CppCondGraph(object):
    """Represents a graph of conditional preprocessing directives."""

    def __init__(self):
        super(CppCondGraph, self).__init__()
        self._ifSectS = []

    def __str__(self):
        return ('\n').join(self.retStrList(0))

    def visit(self, theVisitor):
        """Take a visitor object and pass it around giving it each
        :py:class:`CppCondGraphNode` object."""
        for anIfSect in self._ifSectS:
            anIfSect.visit(theVisitor, 0)

    def retStrList(self, theDepth):
        retList = []
        for aSibling in self._ifSectS:
            retList.extend(aSibling.retStrList(theDepth))

        return retList

    @property
    def isComplete(self):
        """True if the last if-section, if present is completed with an ``#endif``."""
        logging.debug('CppCondGraph.isComplete(): %s', str(self._ifSectS))
        return len(self._ifSectS) == 0 or self._ifSectS[(-1)].isSectionComplete

    def _raiseIfComplete(self, theCppD):
        """Raise an exception if I can not accept this directive, does not
        apply to #if statements so should not be called for them."""
        assert theCppD in CPP_COND_ALT_DIRECTIVES or theCppD == CPP_COND_END_DIRECTIVE
        if self.isComplete:
            raise ExceptionCppCondGraph('Graph can not handle #%s when complete' % theCppD)

    def _oIfIfDefIfndef(self, theCppD, theFlc, theTuIdx, theBool, theCe):
        assert theCppD in CPP_COND_IF_DIRECTIVES
        if self.isComplete:
            logging.debug('CppCondGraph._oIfIfDefIfndef(): adding new sibling "%s" %s %s %s', theFlc, theTuIdx, theBool, theCe)
            self._ifSectS.append(CppCondGraphIfSection(theCppD, theFlc, theTuIdx, theBool, theCe))
        else:
            logging.debug('CppCondGraph._oIfIfDefIfndef(): passing "%s" to child %s %s %s', theFlc, theTuIdx, theBool, theCe)
            if theCppD == 'if':
                self._ifSectS[(-1)].oIf(theFlc, theTuIdx, theBool, theCe)
            elif theCppD == 'ifdef':
                self._ifSectS[(-1)].oIfdef(theFlc, theTuIdx, theBool, theCe)
            elif theCppD == 'ifndef':
                self._ifSectS[(-1)].oIfndef(theFlc, theTuIdx, theBool, theCe)

    def oIf(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#if``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.

        *theCe*
            The constant expression as a string (not evaluated).
        """
        logging.debug('CppCondGraph.oIf():     %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('if', theFlc, theTuIdx, theBool, theCe)

    def oIfdef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifdef``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.

        *theCe*
            The constant expression as a string (not evaluated).
        """
        logging.debug('CppCondGraph.oIfdef():  %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifdef', theFlc, theTuIdx, theBool, theCe)

    def oIfndef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifndef``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.

        *theCe*
            The constant expression as a string (not evaluated).
        """
        logging.debug('CppCondGraph.oIfndef(): %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifndef', theFlc, theTuIdx, theBool, theCe)

    def oElif(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#elif``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.

        *theCe*
            The constant expression as a string (not evaluated).
        """
        logging.debug('CppCondGraph.oElif():   %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._raiseIfComplete('elif')
        assert len(self._ifSectS) > 0
        self._ifSectS[(-1)].oElif(theFlc, theTuIdx, theBool, theCe)

    def oElse(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#else``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.
        """
        logging.debug('CppCondGraph.oElse():   %s %s', theFlc, theTuIdx)
        self._raiseIfComplete('else')
        assert len(self._ifSectS) > 0
        self._ifSectS[(-1)].oElse(theFlc, theTuIdx, theBool)

    def oEndif(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#endif``.

        *theFlc*
            A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
            identifies the position in the file.

        *theTuIndex*
            An integer that represents the position in the translation unit.

        *theBool*
            The current state of the conditional stack.
        """
        logging.debug('CppCondGraph.oEndif():  %s %s', theFlc, theTuIdx)
        self._raiseIfComplete('endif')
        assert len(self._ifSectS) > 0
        self._ifSectS[(-1)].oEndif(theFlc, theTuIdx, theBool)


class CppCondGraphNode(object):
    """Base class for all nodes in the :py:class:`CppCondGraph`."""
    DUMP_PAD_SPACES = 4

    def __init__(self, theCppDirective, theFileLineCol, theTuIdx, theBool, theConstExpr=None):
        super(CppCondGraphNode, self).__init__()
        assert theCppDirective in CPP_COND_DIRECTIVES, 'Unknown directive: %s' % theCppDirective
        self._cppDir = theCppDirective
        if theBool:
            theBool = True
        else:
            theBool = False
        self._cppDirLoc = StateConstExprFileLine(theFileLineCol.fileId, theFileLineCol.lineNum, theTuIdx, theBool, theConstExpr)
        self._childIfSectS = []

    def visit(self, theVisitor, theDepth):
        """Take a visitor object make the pre/post calls."""
        theVisitor.visitPre(self, theDepth)
        for aChild in self._childIfSectS:
            aChild.visit(theVisitor, theDepth + 1)

        theVisitor.visitPost(self, theDepth)

    def padStr(self, depth):
        return ' ' * (depth * self.DUMP_PAD_SPACES)

    def retStrList(self, theDepth):
        """Returns a list of string representation."""
        retList = [
         '%s%s %s' % (
          self.padStr(theDepth),
          self.cppDirString,
          self.commentString)]
        for aChild in self._childIfSectS:
            retList.extend(aChild.retStrList(theDepth + 1))

        return retList

    @property
    def cppDirective(self):
        return self._cppDir

    @property
    def fileId(self):
        return self._cppDirLoc.fileId

    @property
    def lineNum(self):
        return self._cppDirLoc.lineNum

    @property
    def tuIndex(self):
        return self._cppDirLoc.tuIndex

    @property
    def state(self):
        return self._cppDirLoc.state

    @property
    def constExpr(self):
        return self._cppDirLoc.const_expr

    @property
    def cppDirString(self):
        if self._cppDirLoc.const_expr is None:
            return '#%s' % self._cppDir
        else:
            return '#%s %s' % (self._cppDir, self._cppDirLoc.const_expr)

    @property
    def commentString(self):
        return '/* %s "%s" %s %s */' % (
         self._cppDirLoc.state,
         self._cppDirLoc.fileId,
         self._cppDirLoc.lineNum,
         self._cppDirLoc.tuIndex)

    def canAccept(self, theCppD):
        """True if I can accept a Preprocessing Directive; theCppD."""
        assert theCppD in CPP_COND_DIRECTIVES
        if self.cppDirective == CPP_COND_END_DIRECTIVE:
            assert len(self._childIfSectS) == 0
            return False
        if theCppD in CPP_COND_IF_DIRECTIVES:
            return True
        assert theCppD in CPP_COND_ALT_DIRECTIVES or theCppD == CPP_COND_END_DIRECTIVE
        if len(self._childIfSectS) == 0:
            return False
        return not self._childIfSectS[(-1)].isSectionComplete

    def _raiseIfCanNotAccept(self, theCppD):
        """Raise an exception if I can not accept this directive."""
        if not theCppD in CPP_COND_DIRECTIVES:
            raise AssertionError
            raise (self.canAccept(theCppD) or ExceptionCppCondGraphNode)('Can not handle #%s when complete' % theCppD)

    def _oIfIfDefIfndef(self, theCppD, theFlc, theTuIdx, theBool, theCe):
        assert theCppD in CPP_COND_IF_DIRECTIVES
        self._raiseIfCanNotAccept(theCppD)
        if len(self._childIfSectS) == 0 or self._childIfSectS[(-1)].isSectionComplete:
            self._childIfSectS.append(CppCondGraphIfSection(theCppD, theFlc, theTuIdx, theBool, theCe))
        else:
            assert len(self._childIfSectS) > 0
            if theCppD == 'if':
                self._childIfSectS[(-1)].oIf(theFlc, theTuIdx, theBool, theCe)
            elif theCppD == 'ifdef':
                self._childIfSectS[(-1)].oIfdef(theFlc, theTuIdx, theBool, theCe)
            elif theCppD == 'ifndef':
                self._childIfSectS[(-1)].oIfndef(theFlc, theTuIdx, theBool, theCe)

    def oIf(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#if``."""
        logging.debug('CppCondGraphNode.oIf():     %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('if', theFlc, theTuIdx, theBool, theCe)

    def oIfdef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifdef``."""
        logging.debug('CppCondGraphNode.oIfdef():  %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifdef', theFlc, theTuIdx, theBool, theCe)

    def oIfndef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifndef``."""
        logging.debug('CppCondGraphNode.oIfndef(): %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifndef', theFlc, theTuIdx, theBool, theCe)

    def oElif(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#elif``."""
        logging.debug('CppCondGraphNode.oElif():   %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._raiseIfCanNotAccept('elif')
        assert len(self._childIfSectS) > 0
        self._childIfSectS[(-1)].oElif(theFlc, theTuIdx, theBool, theCe)

    def oElse(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#else``."""
        logging.debug('CppCondGraphNode.oElse():   %s %s', theFlc, theTuIdx)
        self._raiseIfCanNotAccept('else')
        assert len(self._childIfSectS) > 0
        self._childIfSectS[(-1)].oElse(theFlc, theTuIdx, theBool)

    def oEndif(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#endif``."""
        logging.debug('CppCondGraphNode.oEndif():  %s %s', theFlc, theTuIdx)
        self._raiseIfCanNotAccept('endif')
        assert len(self._childIfSectS) > 0
        self._childIfSectS[(-1)].oEndif(theFlc, theTuIdx, theBool)


class CppCondGraphIfSection(object):
    """Class that represents a conditionally compiled section starting with
    #if... and ending with ``#endif``.
    
    *theIfCppD*
        A string, one of '#if', '#ifdef', '#ifndef'.
        
    *theFlc*
        A :py:class:`cpip.core.FileLocation.FileLineColumn` object that
        identifies the position in the file.
        
    *theTuIndex*
        An integer that represents the position in the translation unit.
        
    *theBool*
        The current state of the conditional stack.
        
    *theCe*
        The constant expression as a string (not evaluated).
    """

    def __init__(self, theIfCppD, theFlc, theTuIdx, theBool, theCe):
        super(CppCondGraphIfSection, self).__init__()
        assert theIfCppD in CPP_COND_IF_DIRECTIVES
        self._siblingNodeS = [
         CppCondGraphNode(theIfCppD, theFlc, theTuIdx, theBool, theCe)]

    def __str__(self):
        return ('\n').join(self.retStrList(0))

    def visit(self, theVisitor, theDepth):
        """Take a visitor object make the pre/post calls."""
        for aSibling in self._siblingNodeS:
            aSibling.visit(theVisitor, theDepth)

    def retStrList(self, theDepth):
        retList = []
        for aSibling in self._siblingNodeS:
            retList.extend(aSibling.retStrList(theDepth))

        return retList

    @property
    def isSectionComplete(self):
        assert len(self._siblingNodeS) > 0
        retVal = self._siblingNodeS[(-1)].cppDirective == 'endif'
        logging.debug('CppCondGraphIfSection.isSectionComplete(): %s %s', retVal, str(self._siblingNodeS))
        return retVal

    def _raiseIfSectionComplete(self, theCppD):
        if self.isSectionComplete:
            raise ExceptionCppCondGraphIfSection('CppCondGraphIfSection: #%s in if-section that is complete.' % theCppD)

    def _oIfIfDefIfndef(self, theCppD, theFlc, theTuIdx, theBool, theCe):
        assert theCppD in CPP_COND_IF_DIRECTIVES
        assert len(self._siblingNodeS) > 0
        self._raiseIfSectionComplete(theCppD)
        if theCppD == 'if':
            self._siblingNodeS[(-1)].oIf(theFlc, theTuIdx, theBool, theCe)
        elif theCppD == 'ifdef':
            self._siblingNodeS[(-1)].oIfdef(theFlc, theTuIdx, theBool, theCe)
        elif theCppD == 'ifndef':
            self._siblingNodeS[(-1)].oIfndef(theFlc, theTuIdx, theBool, theCe)

    def oIf(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#if``."""
        logging.debug('CppCondGraphIfSection.oIf():     %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('if', theFlc, theTuIdx, theBool, theCe)

    def oIfdef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifdef``."""
        logging.debug('CppCondGraphIfSection.oIfdef():  %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifdef', theFlc, theTuIdx, theBool, theCe)

    def oIfndef(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#ifndef``."""
        logging.debug('CppCondGraphIfSection.oIfndef(): %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        self._oIfIfDefIfndef('ifndef', theFlc, theTuIdx, theBool, theCe)

    def oElif(self, theFlc, theTuIdx, theBool, theCe):
        """Deal with the result of a ``#elif``."""
        logging.debug('CppCondGraphIfSection.oElif():   %s %s %s "%s"', theFlc, theTuIdx, theBool, theCe)
        assert len(self._siblingNodeS) > 0
        self._raiseIfSectionComplete('elif')
        if self._siblingNodeS[(-1)].canAccept('elif'):
            self._siblingNodeS[(-1)].oElif(theFlc, theTuIdx, theBool, theCe)
        elif self._siblingNodeS[(-1)].cppDirective == 'else':
            raise ExceptionCppCondGraphElif('#elif followed %s File: %s line: %d column: %d' % (
             self._siblingNodeS[(-1)].cppDirective, theFlc.fileId, theFlc.lineNum, theFlc.colNum))
        else:
            self._siblingNodeS.append(CppCondGraphNode('elif', theFlc, theTuIdx, theBool, theCe))

    def oElse(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#else``."""
        logging.debug('CppCondGraphIfSection.oElse():   %s %s', theFlc, theTuIdx)
        assert len(self._siblingNodeS) > 0
        self._raiseIfSectionComplete('else')
        if self._siblingNodeS[(-1)].canAccept('else'):
            self._siblingNodeS[(-1)].oElse(theFlc, theTuIdx, theBool)
        elif self._siblingNodeS[(-1)].cppDirective == 'else':
            raise ExceptionCppCondGraphElse('#else followed %s File: %s line: %d column: %d' % (
             self._siblingNodeS[(-1)].cppDirective, theFlc.fileId, theFlc.lineNum, theFlc.colNum))
        else:
            self._siblingNodeS.append(CppCondGraphNode('else', theFlc, theTuIdx, theBool))

    def oEndif(self, theFlc, theTuIdx, theBool):
        """Deal with the result of a ``#endif``."""
        logging.debug('CppCondGraphIfSection.oEndif():  %s %s', theFlc, theTuIdx)
        assert len(self._siblingNodeS) > 0
        self._raiseIfSectionComplete('endif')
        if self._siblingNodeS[(-1)].canAccept('endif'):
            self._siblingNodeS[(-1)].oEndif(theFlc, theTuIdx, theBool)
        else:
            self._siblingNodeS.append(CppCondGraphNode('endif', theFlc, theTuIdx, theBool))


class LineConditionalInterpretation(object):
    """Class that represents the conditional compilation state of every line in
    a file. This takes a list of ``[(line_num, boolean), ...]`` and interprets
    individual line numbers as to whether they are compiled or not.

    If the same file is included twice with a different macro environment then
    it is entirely possible that line_num is not monotonic. In any case not every
    line number is present, the state of any unmentioned line is the state of the
    last mentioned line. Thus a simple dict is not useful.

    We have to sort theList by line_num and if there are duplicate line_num
    with different boolean values then the conditional compilation state at
    that point is ambiguous.
    """

    def __init__(self, theList):
        self._lines = []
        self._bools = []
        for l, b in sorted(set(theList)):
            if l < START_LINE:
                raise ValueError(('LineConditionalInterpretation: line number {:d} can not be < {:d}').format(l, START_LINE))
            self._lines.append(l)
            self._bools.append(b)

    def isCompiled(self, lineNum):
        """Returns 1 if this line is compiled, 0 if not or -1 if it is ambiguous
        i.e. sometimes it is and sometimes not when multiply included.

        This requires a search for the previously mentioned line state.

        Will raise a ValueError if no prior state can be found, for example if there
        are no conditional compilation directives in the file. In this case it is up
        to the caller to handle this. ``CppCondGraphVisitorConditionalLines`` does
        this during ``visitPre()`` by artificially inserting line 1.
        See ``CppCondGraphVisitorConditionalLines.isCompiled()``"""
        idx = bisect.bisect_right(self._lines, lineNum)
        if idx == 0:
            raise ValueError('LineConditionInterpretation.isCompiled(): Can not find %s in %s' % (lineNum, self._lines))
        idx -= 1
        if idx > 0 and self._lines[(idx - 1)] == self._lines[idx] and self._bools[(idx - 1)] != self._bools[idx]:
            return -1
        if self._bools[idx]:
            return 1
        return 0

    def __str__(self):
        return str(list(zip(self._lines, self._bools)))


class CppCondGraphVisitorConditionalLines(CppCondGraphVisitorBase):
    """Allows you to find out if any particular line in a file is compiled or
    not. This is useful to be handed to the ITU to HTML generator that can
    colourize the HTML depending if any line is compiled or not.
    
    This is a visitor class that walks the graph creating a dict of:
    ``{file_id : [(line_num, boolean), ...], ...}``
    It then decomposes those into a map of ``{file_id : LineConditionalInterpretation(), ...}``
    which can perfom the actual conditional state determination.
    
    API is really :py:meth:`isCompiled()` and this returns -1 or 0 or 1.
    0 means NO. 1 means YES and -1 means sometimes - for re-included files in a
    different macro environment perhaps.
    """

    def __init__(self):
        super(CppCondGraphVisitorConditionalLines, self).__init__()
        self._fileMap = {}
        self._prevFile = None
        self._prevState = True
        self._fileLineCondition = None
        return

    def visitPre(self, theCcgNode, theDepth):
        """Capture the fileID, line number and state."""
        if self._prevFile != theCcgNode.fileId:
            self._addFileLineState(theCcgNode.fileId, START_LINE, self._prevState)
        self._prevFile = theCcgNode.fileId
        self._prevState = theCcgNode.state
        self._addFileLineState(theCcgNode.fileId, theCcgNode.lineNum, theCcgNode.state)

    def _addFileLineState(self, file, line, state):
        try:
            self._fileMap[file].append((line, state))
        except KeyError:
            self._fileMap[file] = [
             (
              line, state)]

    def visitPost(self, theCcgNode, theDepth):
        pass

    @property
    def fileIdS(self):
        """An unordered list of file IDs."""
        return self._fileMap.keys()

    @property
    def fileLineCondition(self):
        if self._fileLineCondition is None:
            self._fileLineCondition = dict((k, LineConditionalInterpretation(v)) for k, v in self._fileMap.items())
        return self._fileLineCondition

    def _lineCondition(self, theFile):
        """An ordered list of (line_num, boolean)."""
        return self._fileMap[theFile]

    def isCompiled(self, fileId, lineNum):
        """Returns 1 if this line is compiled, 0 if not or -1 if it is ambiguous
        i.e. sometimes it is and somtimes not when multiple inclusions."""
        if fileId not in self.fileLineCondition:
            return 1
        return self.fileLineCondition[fileId].isCompiled(lineNum)
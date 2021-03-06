# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/lancelot/constraints.py
# Compiled at: 2009-02-20 10:42:02
"""
Functionality for expressing the constraints on behaviour (with should...)

Intended public interface:
 Classes:  Raise, Not, CollaborateWith 
 Functions: -
 Variables: -
 
Intended for internal use:
 Classes: Constraint

Copyright 2009 by the author(s). All rights reserved 
"""
from lancelot.comparators import Nothing, Anything, EqualsEquals, ExceptionValue
from lancelot.verification import UnmetSpecification

class Constraint(object):
    """ Base constraint class """

    def __init__(self, comparator=Nothing()):
        """ Specify the comparator that is used in verification """
        self._comparator = comparator
        self._result = None
        return

    def verify(self, callable_result):
        """ Invoke callable_result() and _verify() it meets the constraint """
        value_to_verify = self._invoke(callable_result)
        if self.verify_value(value_to_verify):
            return
        msg = '%s, not %r' % (self.describe_constraint(), value_to_verify)
        raise UnmetSpecification(msg)

    def _invoke(self, callable_result):
        """ Invoke the callable and store away the result.
        Please call from subclasses that need to override verify() itself. """
        self._result = callable_result()
        return self._result

    def verify_value(self, value_to_verify):
        """ True if value meets the constraint, False otherwise."""
        return self._comparator.compares_to(value_to_verify)

    def describe_constraint(self):
        """ Describe this constraint """
        return 'should be %s' % self._comparator.description()


class Raise(Constraint):
    """ Constraint specifying should... "raise exception..." behaviour """

    def __init__(self, specified):
        """ Specify the exception that should raised.
        May be an exception type or instance """
        super(Raise, self).__init__(ExceptionValue(specified))
        self._specified = specified
        if isinstance(specified, type):
            self._specified_type = specified
            self._description = 'should raise %s' % specified.__name__
        else:
            self._specified_type = type(specified)
            self._description = 'should raise %r' % specified

    def verify(self, callable_result):
        """ Invoke callable_result() and it raises an exception that 
        meets the constraint """
        try:
            self._invoke(callable_result)
        except self._specified_type, raised_exception:
            if self.verify_value(raised_exception):
                return
            msg = '%s, not %r' % (self.describe_constraint(), raised_exception)
            raise UnmetSpecification(msg)

        raise UnmetSpecification(self.describe_constraint())

    def describe_constraint(self):
        """ Describe this constraint """
        return self._description


class Not(Constraint):
    """ Constraint specifying should... "not..." behaviour """

    def __init__(self, constraint):
        """ Specify what other constraint it should not be """
        super(Not, self).__init__()
        self._constraint = constraint

    def verify(self, callable_result):
        """ Check that the constraint is met """
        try:
            self._constraint.verify(callable_result)
        except UnmetSpecification:
            return

        raise UnmetSpecification(self.describe_constraint())

    def describe_constraint(self):
        """ Describe this constraint """
        msg = self._constraint.describe_constraint()
        if msg.startswith('should not '):
            return msg.replace('should not ', 'should ', 1)
        elif msg.startswith('should '):
            return msg.replace('should ', 'should not ', 1)
        return 'Not: ' + msg


class CollaborateWith(Constraint):
    """ Constraint specifying should... "collaborate with" behaviour """

    def __init__(self, *collaborations, **result_spec):
        """ Specify what MockSpec collaborations should occur """
        super(CollaborateWith, self).__init__()
        self._collaborations = collaborations
        try:
            self._and_result = result_spec['and_result']
        except (KeyError, TypeError):
            self._and_result = Anything()

    def verify(self, callable_result):
        """ Check that the constraint is met, including end result if any """
        mock_specs = [ collaboration.start_collaborating() for collaboration in self._collaborations
                     ]
        end_result = self._invoke(callable_result)
        for mock_spec in mock_specs:
            mock_spec.verify()

        Constraint(EqualsEquals(self._and_result)).verify(lambda : end_result)

    def describe_constraint(self):
        """ Describe this constraint """
        descriptions = [ collaboration.description() for collaboration in self._collaborations
                       ]
        return (',').join(descriptions)
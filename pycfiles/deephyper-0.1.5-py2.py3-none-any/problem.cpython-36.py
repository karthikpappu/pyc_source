# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/core/exceptions/problem.py
# Compiled at: 2019-07-11 14:24:06
# Size of source mod 2**32: 4077 bytes
"""Exceptions related with problem definition.
"""
from deephyper.core.exceptions import DeephyperError

class SpaceDimNameMismatch(DeephyperError):
    __doc__ = '"Raised when 2 set of keys are not corresponding for a given Problem.\n    '

    def __init__(self, ref, space):
        self.ref, self.space = ref, space

    def __str__(self):
        return f"Some reference's dimensions doesn't exist in this space: {filter((lambda k: k in self.space), (self.ref.keys()))}"


class SpaceNumDimMismatch(DeephyperError):
    __doc__ = "Raised when 2 set of keys doesn't have the same number of keys for a given\n    Problem."

    def __init__(self, ref, space):
        self.ref, self.space = ref, space

    def __str__(self):
        return f"The reference has {len(self.ref)} dimensions when the space has {len(self.space)}. Both should have the same number of dimensions."


class SpaceDimNameOfWrongType(DeephyperError):
    __doc__ = 'Raised when a dimension name of the space is not a string.'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Dimension name: '{self.value}' is of type == {type(self.value)} when should be 'str'!"


class SpaceDimValueOfWrongType(DeephyperError):
    __doc__ = 'Raised when a dimension value of the space is not a string.'

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"Dimension value: '{self.value}' is of type == {type(self.value)} when should be either 'tuple' or 'list'!"


class SpaceDimValueNotInSpace(DeephyperError):
    __doc__ = "Raised when a dimension value of the space is in the coresponding dimension's space."

    def __init__(self, value, name_dim, space_dim):
        self.value = value
        self.name_dim = name_dim
        self.space_dim = space_dim

    def __str__(self):
        return f"Dimension value: '{self.value}' is not in dim['{self.name_dim}':{self.space_dim}!"


class NaProblemError(DeephyperError):
    __doc__ = 'Raise when an error occurs in a NaProblem instance.'

    def __init__(self, msg: str):
        self.msg = msg

    def __str__(self):
        return self.msg


class SearchSpaceBuilderIsNotCallable(NaProblemError):
    __doc__ = 'Raised when a search space builder is not a callable.'

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        raise f"The search space builder {self.parameter} should be a callable when it is not!"


class SearchSpaceBuilderMissingParameter(NaProblemError):
    __doc__ = 'Raised when a missing parameter is detected in a callable which creates a Structure.\n\n        Args:\n            missing_parameter (str): name of the missing parameter.\n    '

    def __init__(self, missing_parameter):
        self.missing_parameter = missing_parameter

    def __str__(self):
        return f"The callable which creates a Structure is missing a '{self.missing_parameter}' parameter!"


class SearchSpaceBuilderMissingDefaultParameter(NaProblemError):
    __doc__ = 'Raised when a parameter of a search space builder is missing a default value.'

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The parameter {self.parameter} must have a default value!"


class ProblemPreprocessingIsNotCallable(NaProblemError):
    __doc__ = 'Raised when the preprocessing parameter is not callable.'

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The parameter {self.parameter} must be a callable."


class ProblemLoadDataIsNotCallable(NaProblemError):
    __doc__ = 'Raised when the load_data parameter is not callable.'

    def __init__(self, parameter):
        self.parameter = parameter

    def __str__(self):
        return f"The parameter {self.parameter} must be a callable."


class WrongProblemObjective(NaProblemError):
    __doc__ = 'Raised when the objective parameter is neither a callable nor a string.'

    def __init__(self, objective):
        self.objective = objective

    def __str__(self):
        return str(self.objective)
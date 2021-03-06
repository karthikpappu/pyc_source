# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/move_by_regex.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 1921 bytes
from typing import List, Union, Optional
from uuid import UUID
from datalogue.errors import DtlError, _invalid_parameter_error, _property_not_found
from datalogue.models.transformations.commons import Transformation, _array_from_dict, RegexTransformation

class MoveByRegex(RegexTransformation):
    __doc__ = '\n    Finds all nodes that has a label matching to the given regex \n    and moves them as children of a new parent identified by the given to path\n    '
    type_str = 'MoveByRegex'

    def __init__(self, regex: Optional[str], regex_id: Optional[UUID], to: List[str]):
        """
        :param regex: a string input to find which nodes should be split into two
        :param to: array of string
        """
        RegexTransformation.__init__(self, regex, regex_id, MoveByRegex.type_str)
        self.to = to
        self.regex = regex
        self.regex_id = regex_id

    def __eq__(self, other: 'MoveByRegex'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"MoveByRegex(regex: {self.regex}, regex_id: {self.regex_id}, to: {'.'.join(self.to)})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        if self.regex is not None:
            base['regex'] = self.regex
        if self.regex_id is not None:
            base['regexId'] = str(self.regex_id)
        base['to'] = self.to
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'MoveByRegex')]:
        regex = json.get('regex')
        regex_id = json.get('regexId')
        if regex is None:
            if regex_id is None:
                return _property_not_found("neither 'regex' nor 'regexId", json)
        to = _array_from_dict(json, MoveByRegex.type_str, 'to')
        if isinstance(to, DtlError):
            return to
        else:
            return MoveByRegex(regex, regex_id, to)
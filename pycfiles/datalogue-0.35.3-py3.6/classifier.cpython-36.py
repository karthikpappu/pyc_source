# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/classifier.py
# Compiled at: 2020-05-13 11:17:34
# Size of source mod 2**32: 14202 bytes
from typing import List, Union, Optional
from abc import ABC, abstractmethod
from datalogue.dtl_utils import _parse_list, _parse_uuid, map_option, _parse_datetime, is_valid_uuid
from uuid import UUID
from datetime import datetime
from datalogue.errors import DtlError, _invalid_parameter_error, _property_not_found
from datalogue.models.ontology import OntologyNode

class ClassificationMethod(ABC):
    __doc__ = '\n    Abstract class containing the three subclasses:\n\n    - MLMethod, for classification based on a machine learning model\n    - RegexOnValueMethod, for classification based on regex matching on data values\n    - RegexOnFieldNameMethod, for classification based on regex matching on field names\n    '
    type_field = 'type'

    def __init__(self, transformation_type):
        self.type = transformation_type
        super().__init__()

    def _base_payload(self) -> dict:
        return dict([(ClassificationMethod.type_field, self.type)])

    @abstractmethod
    def _as_payload(self) -> dict:
        """
        Represents the Classification method as a json payload

        :return:
        """
        pass

    @staticmethod
    @abstractmethod
    def _from_payload(json: dict) -> 'ClassificationMethod':
        """
        Represents the Classification method as a json payload

        :return:
        """
        pass


class RegexMap(object):

    def __init__(self, regex_ids: List[Union[(UUID, str)]], class_id: Union[(UUID, str)]):
        """
        Build a mapping between an ontological class and one or more regexes. The mapping will be used by a
            RegexOnFieldNameMethod or RegexOnValueMethod to apply classifications.

        :param class_id: the id of the ontological class that a regex match should maps to
        :param regex_ids: a list of regex ids whose matches map to the ontological class

        """
        self.regex_ids = regex_ids
        self.class_id = class_id

    def __repr__(self):
        pairs = ''
        for id in self.regex_ids:
            pairs += '\n  regex_id(' + str(id) + ') --> class_id(' + str(self.class_id) + ')'

        return f"RegexMap({pairs})"

    def __eq__(self, other: 'RegexMap'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> dict:
        return {'regexes':list(map(lambda i: str(i), self.regex_ids)), 
         'class':str(self.class_id)}

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'RegexMap')]:
        regexes = json.get('regexes')
        if regexes is None:
            return _property_not_found('regexes', json)
        else:
            class_id = json.get('class')
            if regexes is None:
                return _property_not_found('class', json)
            return RegexMap(regexes, class_id)


class MLMethod(ClassificationMethod):
    type_str = 'MLMethod'

    def __init__(self, model_id: Union[(UUID, str)], threshold: Optional[float]=None):
        """
        Builds a local Machine learning classification method

        note: please deploy the model before using this method

        :param model_id: id of the machine learning model to be used
        :param threshold: optionally set a score threshold between 0 and 1, under which classification
            by this method fails
        """
        ClassificationMethod.__init__(self, MLMethod.type_str)
        self.model_id = model_id
        self.threshold = threshold
        if threshold is not None:
            if threshold < 0:
                raise DtlError('Invalid threshold. Confidence scores are positive numbers. Please set a threshold within that range.')

    def __repr__(self):
        return f"MLMethod(\n model_id: {self.model_id}, threshold: {self.threshold}\n)"

    def __eq__(self, other: 'MLMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['model'] = str(self.model_id)
        if self.threshold is not None:
            base['threshold'] = self.threshold
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'MLMethod')]:
        model = json.get('model')
        if model is None:
            return _property_not_found('model', json)
        else:
            threshold = json.get('threshold')
            return MLMethod(model, threshold)


class RegexOnFieldNameMethod(ClassificationMethod):
    type_str = 'RegexOnFieldNameMethod'

    def __init__(self, regex_name_maps: List[RegexMap]):
        """
        Build a classification method based on regexes applied to field names.
        This classification method will apply classes when a match is found between a data point’s field name
            and a supplied regex.

        note: the classification score supplied by a regex match is 1.0

        :param regex_name_maps: a list of the mappings between regexes and the classes they map to
        """
        ClassificationMethod.__init__(self, RegexOnFieldNameMethod.type_str)
        self.regex_name_maps = regex_name_maps

    def __repr__(self):
        pairs = repr(self.regex_name_maps)
        return f"\nRegexOnFieldNameMethod({pairs}\n  - Regexes above used to target data \x1b[1mfield names\x1b[0m for classification\n)"

    def __eq__(self, other: 'RegexOnFieldNameMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['regexNameMaps'] = list(map(lambda m: m._as_payload(), self.regex_name_maps))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'RegexOnFieldNameMethod')]:
        regex_name_maps = json.get('regexNameMaps')
        if regex_name_maps is None:
            return _property_not_found('regexNameMaps', json)
        else:
            regex_name_maps = _parse_list(RegexMap._from_payload)(regex_name_maps)
            if isinstance(regex_name_maps, DtlError):
                return regex_name_maps
            return RegexOnFieldNameMethod(regex_name_maps)


class RegexOnValueMethod(ClassificationMethod):
    type_str = 'RegexOnValueMethod'

    def __init__(self, regex_value_maps: List[RegexMap]):
        """
        Build a classification method based on regexes applied to data values.
        This classification method will apply classes when a match is found between a data point’s value and a
         supplied regex.

        note: the classification score supplied by a regex match is 1.0

        :param regex_value_maps: a list of the mappings between regexes and the classes they map to
        """
        ClassificationMethod.__init__(self, RegexOnValueMethod.type_str)
        self.regex_value_maps = regex_value_maps

    def __repr__(self):
        pairs = repr(self.regex_value_maps)
        return f"\nRegexOnValueMethod({pairs}\n  - Regexes above used to target data \x1b[1mvalues\x1b[0m for classification\n)"

    def __eq__(self, other: 'RegexOnValueMethod'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['regexValueMaps'] = list(map(lambda m: m._as_payload(), self.regex_value_maps))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'RegexOnValueMethod')]:
        regex_name_maps = json.get('regexValueMaps')
        if regex_name_maps is None:
            return _property_not_found('regexValueMaps', json)
        else:
            regex_name_maps = _parse_list(RegexMap._from_payload)(regex_name_maps)
            if isinstance(regex_name_maps, DtlError):
                return regex_name_maps
            return RegexOnValueMethod(regex_name_maps)


class Classifier(object):

    def __init__(self, name: str, classification_methods: List[ClassificationMethod], description: str='', default_class_id: Optional[Union[(UUID, str)]]=None, id: Optional[UUID]=None, owner: Optional[UUID]=None, editors: Optional[List[UUID]]=None, created_at: Optional[datetime]=None, created_by: Optional[UUID]=None, updated_at: Optional[datetime]=None, updated_by: Optional[UUID]=None, domain: Optional[List[OntologyNode]]=None):
        """
        Build a local Classifier

        :param classification_methods: ordered list of Classification Methods
        :param default_class_id: allows the user to specify the class to be defaulted to, if all classification methods
            fail. Default value is `Unknown`. (currently part of replace_class, see below)
        """
        self.name = name
        self.classification_methods = classification_methods
        self.description = description
        self.default_class_id = default_class_id
        self.id = id
        self.owner = owner
        self.editors = editors
        self.created_at = created_at
        self.created_by = created_by
        self.updated_at = updated_at
        self.updated_by = updated_by
        self.domain = domain

    def __repr__(self):
        return 'Classifier(' + (f"id={self.id!r}, " if self.id is not None else '') + f"name={self.name!r}, default_class={self.default_class_id!r}, classification_methods={self.classification_methods!r}" + (f", domain={self.domain!r}, " if self.domain is not None else '') + ')'

    def __eq__(self, other: 'Classifier'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def _as_payload(self) -> dict:
        payload = {'name':self.name, 
         'description':self.description, 
         'classificationMethods':list(map(lambda m: m._as_payload(), self.classification_methods))}
        if self.default_class_id is not None:
            if is_valid_uuid(self.default_class_id):
                payload['defaultClassId'] = str(self.default_class_id)
            else:
                raise DtlError('default_class_id provided is not a valid UUID format.')
        if self.id is not None:
            payload['id'] = self.id
        if self.owner is not None:
            payload['owner'] = self.owner
        if self.editors is not None:
            payload['editors'] = self.editors
        if self.created_at is not None:
            payload['createdAt'] = self.created_at
        if self.updated_at is not None:
            payload['updatedAt'] = self.updated_at
        if self.updated_by is not None:
            payload['lastUpdateBy'] = self.updated_by
        return payload

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'Classifier')]:
        name = json.get('name')
        if name is None or not isinstance(name, str):
            return DtlError("'name' is missing or not a string")
        description = json.get('description')
        if description is None or not isinstance(description, str):
            return DtlError("'description' is missing or not a string")
        id = map_option(json.get('id'), _parse_uuid)
        owner = map_option(json.get('owner'), _parse_uuid)
        editors = json.get('editors')
        if editors is not None:
            editors = _parse_list(_parse_uuid)(editors)
            if isinstance(editors, DtlError):
                return DtlError(f"'editors has at least one invalid value: {json.get('editors')}", editors)
        created_at = map_option(json.get('createdAt'), _parse_datetime)
        if isinstance(created_at, DtlError):
            return created_at
        created_by = map_option(json.get('createdBy'), _parse_uuid)
        if isinstance(created_by, DtlError):
            return created_by
        updated_at = map_option(json.get('updatedAt'), _parse_datetime)
        if isinstance(updated_at, DtlError):
            return updated_at
        updated_by = map_option(json.get('lastUpdateBy'), _parse_uuid)
        if isinstance(updated_by, DtlError):
            return updated_by
        classification_methods = json.get('classificationMethods')
        if classification_methods is None:
            return _property_not_found('classificationMethods', json)
        else:
            classification_methods = _parse_list(_classification_method_from_payload)(classification_methods)
            if isinstance(classification_methods, DtlError):
                return classification_methods
            default_class = json.get('defaultClassId')
            return Classifier(name=name,
              classification_methods=classification_methods,
              description=description,
              default_class_id=default_class,
              id=id,
              owner=owner,
              editors=editors,
              created_at=created_at,
              created_by=created_by,
              updated_at=updated_at,
              updated_by=updated_by)


_ml_methods = dict([
 (
  MLMethod.type_str, MLMethod._from_payload),
 (
  RegexOnFieldNameMethod.type_str, RegexOnFieldNameMethod._from_payload),
 (
  RegexOnValueMethod.type_str, RegexOnValueMethod._from_payload)])

def _classification_method_from_payload(json: dict) -> Union[(DtlError, ClassificationMethod)]:
    type_field = json.get(ClassificationMethod.type_field)
    if type_field is None:
        return DtlError("The json object doesn't have a '%s' property" % ClassificationMethod.type_field)
    else:
        parsing_function = _ml_methods.get(type_field)
        if parsing_function is None:
            return DtlError("Looks like '%s' Classification method is not handled by the SDK" % type_field)
        return parsing_function(json)
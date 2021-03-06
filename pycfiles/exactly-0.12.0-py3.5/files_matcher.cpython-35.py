# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/type_system/logic/files_matcher.py
# Compiled at: 2020-01-30 14:42:21
# Size of source mod 2**32: 1440 bytes
import pathlib
from abc import ABC, abstractmethod
from typing import Iterator
from exactly_lib.symbol.logic.matcher import MatcherSdv
from exactly_lib.type_system.data.path_ddv import DescribedPath
from exactly_lib.type_system.logic.file_matcher import FileMatcher, FileMatcherModel
from exactly_lib.type_system.logic.matcher_base_class import MatcherAdv, MatcherWTraceAndNegation, MatcherDdv

class FileModel(ABC):

    @property
    @abstractmethod
    def path(self) -> DescribedPath:
        pass

    @property
    @abstractmethod
    def relative_to_root_dir(self) -> pathlib.Path:
        pass

    @abstractmethod
    def as_file_matcher_model(self) -> FileMatcherModel:
        pass


class FilesMatcherModel(ABC):

    @abstractmethod
    def files(self) -> Iterator[FileModel]:
        pass

    @abstractmethod
    def sub_set(self, selector: FileMatcher) -> 'FilesMatcherModel':
        """
        :return a new object that represents a sub set of this object.
        """
        pass

    @abstractmethod
    def prune(self, dir_selector: FileMatcher) -> 'FilesMatcherModel':
        """
        :return a new object that represents a variant of this object with pruned directories.
        """
        pass


FilesMatcher = MatcherWTraceAndNegation[FilesMatcherModel]
FilesMatcherAdv = MatcherAdv[FilesMatcherModel]
FilesMatcherDdv = MatcherDdv[FilesMatcherModel]
GenericFilesMatcherSdv = MatcherSdv[FilesMatcherModel]
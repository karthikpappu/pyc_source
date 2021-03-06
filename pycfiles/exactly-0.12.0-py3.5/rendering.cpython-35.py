# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/err_msg/rendering.py
# Compiled at: 2019-11-06 08:59:56
# Size of source mod 2**32: 660 bytes
import functools
from typing import List
from exactly_lib.common.err_msg.definitions import Blocks
from exactly_lib.util import file_printables
from exactly_lib.util.collection import intersperse_list
from exactly_lib.util.file_printer import FilePrintable

def blocks_as_lines(blocks: Blocks) -> List[str]:
    return functools.reduce(lambda x, y: x + y, intersperse_list([''], blocks), [])


def blocks_as_str(blocks: Blocks) -> str:
    return '\n'.join(blocks_as_lines(blocks))


def blocks_as_printable(blocks: Blocks) -> FilePrintable:
    return file_printables.of_string(blocks_as_str(blocks))
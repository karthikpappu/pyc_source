# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\baker\template.py
# Compiled at: 2018-05-21 11:17:45
# Size of source mod 2**32: 3552 bytes
import os, shutil
from string import Template
from baker import settings
from baker import logger
from baker.storage import Storage

class ReplaceTemplate:
    __doc__ = '\n    Replace items in template file based on recipe mapping\n    '

    def __init__(self, instructions):
        self.instructions = instructions

    def replace(self):
        """
        Replace variables in template file based on recipe instructions
        """
        for instruction in self.instructions:
            target = instruction.template
            template_path = instruction.template
            replaced = Storage.file(template_path)
            if instruction.variables:
                template = BakerTemplate(replaced)
                replaced = template.replace(instruction.variables)
            if hasattr(instruction, 'path'):
                target = instruction.path
            if settings.get('TEMPLATE_EXT'):
                if target.endswith(settings.get('TEMPLATE_EXT')):
                    ext_size = len(settings.get('TEMPLATE_EXT')) + 1
                    target = target[:-ext_size]
            Storage.file(target, content=replaced)
            self._add_file_permission(instruction, target)
            logger.log(instruction.name, instruction.template, target)

    @staticmethod
    def _add_file_permission(instruction, path):
        """
        Add permission and owner for templates files after replace
        """
        if hasattr(instruction, 'user') or hasattr(instruction, 'group'):
            user = instruction.user if hasattr(instruction, 'user') else None
            group = instruction.group if hasattr(instruction, 'group') else None
            shutil.chown(path, user, group)
        if hasattr(instruction, 'mode'):
            os.chmod(path, int(instruction.mode, 8))


class BakerTemplate(Template):
    __doc__ = '\n    Template with baker pattern of variables\n    '
    delimiter = '{{'
    pattern = '\n        \\{\\{\\ *(?:\n        (?P<escaped>\\\\)                     | # escape with {{\\escape}} or {{\\ escape }}}\n        (?P<named>[_a-z][_a-z0-9]*)\\ *}}    | # identifier {{var}} or {{ var }}\n        \\b\\B(?P<braced>)                    | # braced identifier disabled\n        (?P<invalid>)                         # ill-formed delimiter expr\n        )\n    '

    def replace(self, mapping):
        try:
            if settings.get('RECIPE_CASE_SENSITIVE'):
                return super(BakerTemplate, self).substitute(mapping)
            else:
                return self.ignore_case_substitute(mapping)
        except KeyError as e:
            raise KeyError('Missing variable %s' % e)

    def ignore_case_substitute(self, mapping):
        """
        Substitution of values in replace ignoring case sensitive of variables
        """
        if not mapping:
            raise TypeError("Descriptor 'ignore_case_substitute' of 'BakerTemplate' object needs an argument.")

        def convert(mo):
            named = mo.group('named')
            if named is not None:
                return str(mapping[named.lower()])
            if mo.group('escaped') is not None:
                return self.delimiter
            if mo.group('invalid') is not None:
                self._invalid(mo)
            raise ValueError('Unrecognized named group in pattern', self.pattern)

        return self.pattern.sub(convert, self.template)
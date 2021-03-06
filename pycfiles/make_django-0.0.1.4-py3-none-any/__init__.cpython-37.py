# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Program Files\Python 3.7\lib\site-packages\make_django\batteries\__init__.py
# Compiled at: 2018-11-15 13:19:35
# Size of source mod 2**32: 2495 bytes
from make_django.lib.path_util import Path

class BaseBattery:
    arg = None
    arg_found = False
    packages = []
    apps = []

    def __init__(self, dm):
        self.dm = dm
        self.name = self.__class__.__name__.lower()
        self.path = dm.paths.self / f"batteries/{self.name}"

    @staticmethod
    def remove_entries(text, entries):
        result = list()[:]
        for ln in text.split('\n'):
            skip = False
            for entry in entries:
                if entry in ln:
                    skip = True

            if skip:
                continue
            result.append(ln)

        return '\n'.join(result)

    def copy_settings(self):
        battery_name = self.name
        settings_path = self.dm.paths.self / f"./batteries/{battery_name}/settings.py"
        if settings_path.exists():
            deploy_path = self.dm.paths.settings / f"{battery_name}.py"
            settings_path.copy_to(deploy_path)

    def patch_settings(self, red, text):
        return (red, text)

    def patch_urls(self, red, text):
        return (
         red, text)

    def final_patch(self):
        pass

    def deploy(self):
        if self.arg_found:
            deploy_map = {'data/application':self.dm.paths.application,  'data/app':self.dm.paths.app}
            print('\ndeploy battery:', self.name)
            for path_from, path_to in deploy_map.items():
                path = self.path.j(path_from)
                if path.exists():
                    for item in path.iterdir():
                        if item.name in ('static', 'templates'):
                            for sub_item in item.iterdir():
                                sub_item.copy_to(path_to.j(item.name, self.dm.project_name, sub_item.name))

                        elif item.is_dir():
                            item.copy_to(path_to / item.name)
                        else:
                            item.copy_to(path_to)


def load_batteries():
    batteries_path = Path(__file__).parent
    batteries_classes = []
    for item in batteries_path.iterdir():
        if item.is_dir():
            class_str = item.name.startswith('__') or item.name.capitalize()
            import_str = f"from .{item.name} import {class_str}"
            print(f"import battery: {class_str}")
            exec(import_str)
            batteries_classes.append(locals()[class_str])

    return batteries_classes
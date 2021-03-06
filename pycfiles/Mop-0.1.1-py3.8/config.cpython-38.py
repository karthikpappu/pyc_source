# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mop/config.py
# Compiled at: 2020-04-05 20:53:54
# Size of source mod 2**32: 3939 bytes
import os, sys, json, textwrap, importlib
from pathlib import Path
__all__ = [
 'CONFIG_DIR', 'Config', 'getConfig', 'getState']
CONFIG_DIR = Path('~/.config/Mop/').expanduser()
CACHE_DIR = Path('~/.cache/Mop/').expanduser()
_config = None
_state = None

class _ConfigFile:
    __doc__ = '\n    Not a subclass of pathlib.Path but implements its interface.\n    '

    def __init__(self, filename, default: str=None, mode=None):
        self._path = Path(str(filename)).expanduser()
        if (self.exists() or default) is not None:
            if not self.parent.exists():
                self.parent.mkdir(parents=True)
            umask = os.umask(0)
            os.umask(umask)
            mode = mode or 438 ^ umask
            self.touch(mode=mode)
            self.write_text(default, encoding='utf8')
        else:
            if not self.exists():
                raise FileNotFoundError(str(self))

    def __getattr__(self, attr):
        return getattr(self._path, attr)


class _Config:
    DEFAULT_PATH = None
    DEFAULT_CONFIG = None

    def __init__(self, filename, **kwargs):
        self._cfg_file = _ConfigFile(filename, **kwargs)


class _PyConfig(_Config):
    DEFAULT_PATH = CONFIG_DIR / 'mop_cfg.py'
    DEFAULT_CONFIG = textwrap.dedent('\n    from eyed3.id3 import ID3_ANY_VERSION, ID3_V2_4, ID3_V2_3, ID3_V1_1, ID3_V1_0\n\n    preferred_id3_version = ID3_ANY_VERSION\n    ').lstrip()

    def __init__(self):
        super().__init__((self.DEFAULT_PATH), default=(self.DEFAULT_CONFIG))
        sys_path = list(sys.path)
        try:
            sys.path.append(str(self._cfg_file.parent.resolve()))
            self._cfg_mod = importlib.import_module(self._cfg_file.stem)
        finally:
            sys.path.clear()
            sys.path.extend(sys_path)

    def __getattr__(self, attr):
        if hasattr(self._cfg_mod, attr):
            return getattr(self._cfg_mod, attr)
        return super().__getattr__(attr)


Config = _PyConfig

def getConfig() -> Config:
    """Get application config instance"""
    global _config
    if _config is None:
        _config = Config()
    return _config


class State:
    DEFAULT_PATH = CACHE_DIR / 'mop.json'
    MAIN_WINDOW = 'main_window'

    def __init__(self):
        self._state_file = _ConfigFile((self.DEFAULT_PATH), default='{}', mode=384)
        self._state = json.load(self._state_file.open())

    def save(self):
        self._state_file.write_text(json.dumps(self._state), 'utf8')

    @property
    def main_window_size(self) -> tuple:
        return self._getMainWindowTuple(('width', 'height'))

    @main_window_size.setter
    def main_window_size(self, size: tuple) -> None:
        self._setMainWindowTuple(('width', 'height'), size)

    @property
    def main_window_position(self) -> tuple:
        return self._getMainWindowTuple(('x', 'y'))

    @main_window_position.setter
    def main_window_position(self, pos: tuple) -> None:
        self._setMainWindowTuple(('x', 'y'), pos)

    def _getMainWindowTuple(self, what: tuple) -> tuple:
        if self.MAIN_WINDOW not in self._state:
            self._state[self.MAIN_WINDOW] = {}
        return (
         self._state[self.MAIN_WINDOW].get(what[0], None),
         self._state[self.MAIN_WINDOW].get(what[1], None))

    def _setMainWindowTuple(self, what: tuple, value: tuple) -> None:
        if self.MAIN_WINDOW not in self._state:
            self._state[self.MAIN_WINDOW] = {}
        for i in (0, 1):
            if value[i] is None and what[i] in self._state[self.MAIN_WINDOW]:
                del self._state[self.MAIN_WINDOW][what[i]]
            else:
                self._state[self.MAIN_WINDOW][what[i]] = value[i]


def getState() -> State:
    """Get application state instance"""
    global _state
    if _state is None:
        _state = State()
    return _state
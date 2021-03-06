# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./vendor/chardet/escprober.py
# Compiled at: 2019-11-10 08:27:46
# Size of source mod 2**32: 3950 bytes
from .charsetprober import CharSetProber
from .codingstatemachine import CodingStateMachine
from .enums import LanguageFilter, ProbingState, MachineState
from .escsm import HZ_SM_MODEL, ISO2022CN_SM_MODEL, ISO2022JP_SM_MODEL, ISO2022KR_SM_MODEL

class EscCharSetProber(CharSetProber):
    __doc__ = '\n    This CharSetProber uses a "code scheme" approach for detecting encodings,\n    whereby easily recognizable escape or shift sequences are relied on to\n    identify these encodings.\n    '

    def __init__(self, lang_filter=None):
        super(EscCharSetProber, self).__init__(lang_filter=lang_filter)
        self.coding_sm = []
        if self.lang_filter & LanguageFilter.CHINESE_SIMPLIFIED:
            self.coding_sm.append(CodingStateMachine(HZ_SM_MODEL))
            self.coding_sm.append(CodingStateMachine(ISO2022CN_SM_MODEL))
        if self.lang_filter & LanguageFilter.JAPANESE:
            self.coding_sm.append(CodingStateMachine(ISO2022JP_SM_MODEL))
        if self.lang_filter & LanguageFilter.KOREAN:
            self.coding_sm.append(CodingStateMachine(ISO2022KR_SM_MODEL))
        self.active_sm_count = None
        self._detected_charset = None
        self._detected_language = None
        self._state = None
        self.reset()

    def reset(self):
        super(EscCharSetProber, self).reset()
        for coding_sm in self.coding_sm:
            if not coding_sm:
                pass
            else:
                coding_sm.active = True
                coding_sm.reset()
        else:
            self.active_sm_count = len(self.coding_sm)
            self._detected_charset = None
            self._detected_language = None

    @property
    def charset_name(self):
        return self._detected_charset

    @property
    def language(self):
        return self._detected_language

    def get_confidence(self):
        if self._detected_charset:
            return 0.99
        return 0.0

    def feed(self, byte_str):
        for c in byte_str:
            for coding_sm in self.coding_sm:
                if coding_sm:
                    if not coding_sm.active:
                        pass
                    else:
                        coding_state = coding_sm.next_state(c)
                        if coding_state == MachineState.ERROR:
                            coding_sm.active = False
                            self.active_sm_count -= 1
                            if self.active_sm_count <= 0:
                                self._state = ProbingState.NOT_ME
                                return self.state
                        elif coding_state == MachineState.ITS_ME:
                            self._state = ProbingState.FOUND_IT
                            self._detected_charset = coding_sm.get_coding_state_machine()
                            self._detected_language = coding_sm.language
                            return self.state
            else:
                return self.state
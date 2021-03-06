# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbtexmf/dblatex/xetex/fcfallback.py
# Compiled at: 2017-04-03 18:58:57
from fontspec import FontSpec
from fcmanager import FcManager

class DefaultFontSpec(FontSpec):
    """
    The default fontspec gives priority to its children, and 
    contains any character.
    """

    def __init__(self):
        FontSpec.__init__(self, subfont_first=True)

    def contains(self, char):
        return True


class FcFallbackFontSpec(DefaultFontSpec):
    """
    Default fontspec that finds fonts from fontconfig 
    if the preexisting fontspecs don't match.

    Currently this class is the only interface between the
    two worlds (fontspec and fontconfig).
    """

    def __init__(self):
        DefaultFontSpec.__init__(self)
        self.fcmanager = FcManager()
        self.fccache = {}
        self.fcmissed = []
        try:
            self.fcmanager.build_fonts(partial=True)
        except:
            self.fcmanager = None

        return

    def _loghas(self, id, char):
        pass

    def _loghas2(self, id, char):
        DefaultFontSpec._loghas(self, id, char)

    def match(self, char, excluded=None):
        fontspec = DefaultFontSpec.match(self, char, excluded)
        if fontspec != self or not self.fcmanager:
            self._loghas2(fontspec.id, char)
            return fontspec
        if self.isignored(char):
            self._loghas2(self.id, char)
            return self
        for fontspec in self.fontspecs:
            if fontspec in self.fcmissed:
                print "Specified font '%s' is missing in the system!" % fontspec.mainfont()
                continue
            fcfont = self.fccache.get(fontspec.mainfont()) or self.fcmanager.get_font(fontspec.mainfont())
            if not fcfont:
                self.fcmissed.append(fontspec)
                continue
            if fcfont.has_char(char):
                fontspec.add_char(char)
                self._loghas2(fontspec.id + '[fc]', char)
                return fontspec

        fcfonts = {}
        for font_type in ('serif', 'sans-serif', 'monospace'):
            fcfonts[font_type] = self.fcmanager.get_font_handling(char, family_type=font_type)

        if not fcfont:
            self._loghas2(self.id + '[?fc]', char)
            return self
        fontspec = self.spawn_fontspec_from_fcfonts(fcfonts, char)
        self._loghas2(fontspec.id + '[A fc]', char)
        return fontspec

    def spawn_fontspec_from_fcfonts(self, fcfonts, char):
        self.log.info("New fontspec '%s' matching U%X from fontconfig" % (
         fcfonts['serif'].family, ord(char)))
        fontspec = FontSpec()
        fontspec.id = fcfont.family
        fontspec.transitions['enter']['main'] = fcfonts['serif'].family
        fontspec.transitions['enter']['sans'] = fcfonts['sans-serif'].family
        fontspec.transitions['enter']['mono'] = fcfonts['monospace'].family
        fontspec.add_char(char)
        fontspec.add_ignored(self._ignored)
        for fcfont in fcfonts.values():
            self.fccache[fcfont.name] = fcfont

        self.add_subfont(fontspec)
        return fontspec
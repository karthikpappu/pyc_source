# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Editra/src/syntax/_sh.py
# Compiled at: 2011-08-30 21:43:46
"""
FILE: sh.py
AUTHOR: Cody Precord
@summary: Lexer configuration file for Bourne, Bash, Kornshell and
          C-Shell scripts.

"""
__author__ = 'Cody Precord <cprecord@editra.org>'
__svnid__ = '$Id: _sh.py 68798 2011-08-20 17:17:05Z CJP $'
__revision__ = '$Revision: 68798 $'
import wx.stc as stc, synglob, syndata
COMM_KEYWORDS = 'break eval newgrp return ulimit cd exec pwd shift umask chdir exit read test wait continue kill readonly trap contained elif else then case esac do done for in if fi until while set export unset'
EXT_KEYWORDS = 'function alias fg integer printf times autoload functions jobs r true bg getopts let stop type false hash nohup suspend unalias fc history print time whence typeset while select'
BSH_KEYWORDS = 'bind disown local popd shopt builtin enable logout pushd source dirs help declare'
BCMD_KEYWORDS = 'chmod chown chroot clear du egrep expr fgrep find gnufind gnugrep grep install less ls mkdir mv reload restart rm rmdir rpm sed su sleep start status sort strip tail touch complete stop echo'
KSH_KEYWORDS = 'login newgrp'
KCMD_KEYWORDS = 'cat chmod chown chroot clear cp du egrep expr fgrep find grep install killall less ls mkdir mv nice printenv rm rmdir sed sort strip stty su tail touch tput'
CSH_KEYWORDS = 'alias cd chdir continue dirs echo break breaksw foreach end eval exec exit glob goto case default history kill login logout nice nohup else endif onintr popd pushd rehash repeat endsw setenv shift source time umask switch unalias unhash unsetenv wait'
SYNTAX_ITEMS = [
 (
  stc.STC_SH_DEFAULT, 'default_style'),
 (
  stc.STC_SH_BACKTICKS, 'scalar_style'),
 (
  stc.STC_SH_CHARACTER, 'char_style'),
 (
  stc.STC_SH_COMMENTLINE, 'comment_style'),
 (
  stc.STC_SH_ERROR, 'error_style'),
 (
  stc.STC_SH_HERE_DELIM, 'here_style'),
 (
  stc.STC_SH_HERE_Q, 'here_style'),
 (
  stc.STC_SH_IDENTIFIER, 'default_style'),
 (
  stc.STC_SH_NUMBER, 'number_style'),
 (
  stc.STC_SH_OPERATOR, 'operator_style'),
 (
  stc.STC_SH_PARAM, 'scalar_style'),
 (
  stc.STC_SH_SCALAR, 'scalar_style'),
 (
  stc.STC_SH_STRING, 'string_style'),
 (
  stc.STC_SH_WORD, 'keyword_style')]
FOLD = ('fold', '1')
FLD_COMMENT = ('fold.comment', '1')
FLD_COMPACT = ('fold.compact', '0')

class SyntaxData(syndata.SyntaxDataBase):
    """SyntaxData object for various shell scripting languages"""

    def __init__(self, langid):
        super(SyntaxData, self).__init__(langid)
        self.SetLexer(stc.STC_LEX_BASH)

    def GetKeywords(self):
        """Returns Specified Keywords List """
        keywords = list()
        keyw_str = [COMM_KEYWORDS]
        if self.LangId == synglob.ID_LANG_CSH:
            keyw_str.append(CSH_KEYWORDS)
        else:
            if self.LangId != synglob.ID_LANG_BOURNE:
                keyw_str.append(EXT_KEYWORDS)
            if self.LangId == synglob.ID_LANG_BASH:
                keyw_str.append(BSH_KEYWORDS)
                keyw_str.append(BCMD_KEYWORDS)
            elif self.LangId == synglob.ID_LANG_KSH:
                keyw_str.append(KSH_KEYWORDS)
                keyw_str.append(KCMD_KEYWORDS)
        keywords.append((0, (' ').join(keyw_str)))
        return keywords

    def GetSyntaxSpec(self):
        """Syntax Specifications """
        return SYNTAX_ITEMS

    def GetProperties(self):
        """Returns a list of Extra Properties to set """
        return [
         FOLD, FLD_COMMENT, FLD_COMPACT]

    def GetCommentPattern(self):
        """Returns a list of characters used to comment a block of code """
        return [
         '#']
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/editor/code.py
# Compiled at: 2019-09-09 02:52:13
# Size of source mod 2**32: 21017 bytes
from noval import GetApp
import noval.editor.text as texteditor, os, re, string, sys, noval.python.parser.config as parserconfig, noval.util.strutils as strutils, noval.consts as consts, noval.util.appdirs as appdirs, noval.util.utils as utils, noval.syntax.syntax as syntax, noval.constants as constants
from noval.syntax.syndata import BaseSyntaxcolorer
from noval.python.parser.utils import py_sorted
import noval.autocomplete as autocomplete, noval.calltip as calltip

class CodeDocument(texteditor.TextDocument):

    def OnOpenDocument(self, filename):
        if not texteditor.TextDocument.OnOpenDocument(self, filename):
            return False
        return True


class CodeView(texteditor.TextView):

    def GetCtrlClass(self):
        """ Used in split window to instantiate new instances """
        return CodeCtrl

    def OnChangeFilename(self):
        texteditor.TextView.OnChangeFilename(self)

    def LoadOutLine(self, outlineView, force=False, lineNum=-1):
        pass

    def GenCheckSum(self):
        """ Poor man's checksum.  We'll assume most changes will change the length of the file.
        """
        text = self.GetValue()
        if text:
            return len(text)
        else:
            return 0

    def GetAutoCompleteHint(self):
        """ Replace this method with Editor specific method """
        line, col = self.GetCtrl().GetCurrentPos()
        if line == 0 and col == 0:
            return (None, None)
        if self.GetCtrl().GetCharAt(line, col) == '.':
            col = col - 1
            hint = None
        else:
            hint = ''
        validLetters = self.GetCtrl().DEFAULT_WORD_CHARS + '.'
        word = ''
        while True:
            col = col - 1
            if col < 0:
                break
            char = self.GetCtrl().GetCharAt(line, col)
            if char not in validLetters:
                break
            word = char + word

        context = word
        if hint is not None:
            lastDot = word.rfind('.')
            if lastDot != -1:
                context = word[0:lastDot]
                hint = word[lastDot + 1:]
        else:
            hint = word
        return (
         context, hint)

    def GetAutoCompleteDefaultKeywords(self):
        """ Replace this method with Editor specific keywords """
        lexer = self.GetCtrl().GetLangLexer()
        return lexer.GetKeywords()

    def GetAutoCompleteKeywords(self, line):
        return self.GetAutoCompleteDefaultKeywords()

    def GetAutoCompleteKeywordList(self, context, hint, line):
        """ Replace this method with Editor specific keywords """
        kw = self.GetAutoCompleteKeywords(line)
        if not kw:
            return
        if hint and len(hint):
            lowerHint = hint.lower()
            filterkw = filter(lambda item: item.lower().startswith(lowerHint), kw)
            kw = filterkw
        if hint:
            replaceLen = len(hint)
        else:
            replaceLen = 0
        kw = py_sorted(kw, cmp_func=strutils.caseInsensitiveCompare)
        return (kw, replaceLen)

    def OnCleanWhiteSpace(self):
        newText = ''
        for lineNo in self._GetSelectedLineNumbers():
            lineText = string.rstrip(self.GetCtrl().GetLine(lineNo))
            indent = 0
            lstrip = 0
            for char in lineText:
                if char == '\t':
                    indent = indent + self.GetCtrl().GetIndent()
                    lstrip = lstrip + 1
                else:
                    if char in string.whitespace:
                        indent = indent + 1
                        lstrip = lstrip + 1
                    else:
                        break

            if self.GetCtrl().GetUseTabs():
                indentText = indent / self.GetCtrl().GetIndent() * '\t' + indent % self.GetCtrl().GetIndent() * ' '
            else:
                indentText = indent * ' '
            lineText = indentText + lineText[lstrip:] + '\n'
            newText = newText + lineText

        self._ReplaceSelectedLines(newText)

    def OnSetIndentWidth(self):
        dialog = wx.TextEntryDialog(self._GetParentFrame(), _('Enter new indent width (2-10):'), _('Set Indent Width'), '%i' % self.GetCtrl().GetIndent())
        dialog.CenterOnParent()
        if dialog.ShowModal() == wx.ID_OK:
            try:
                indent = int(dialog.GetValue())
                if indent >= 2 and indent <= 10:
                    self.GetCtrl().SetIndent(indent)
                    self.GetCtrl().SetTabWidth(indent)
            except:
                pass

        dialog.Destroy()

    def GetIndentWidth(self):
        return self.GetCtrl().GetIndent()

    def OnCommentLines(self):
        lexer = self.GetCtrl().GetLangLexer()
        comment_pattern_list = lexer.GetCommentPattern()
        if 0 == len(comment_pattern_list):
            return
        newText = ''
        comment_block = False
        if len(comment_pattern_list) > 1:
            comment_block = True
        if not comment_block:
            for lineNo in self._GetSelectedLineNumbers():
                lineText = self.GetCtrl().GetLine(lineNo)
                if len(lineText) > 1 and lineText.startswith(comment_pattern_list[0]):
                    newText = newText + lineText
                else:
                    newText = newText + comment_pattern_list[0] + lineText

        else:
            selected_line_nums = self._GetSelectedLineNumbers()
            for i, lineNo in enumerate(selected_line_nums):
                lineText = self.GetCtrl().GetLine(lineNo)
                if i == 0:
                    newText = newText + comment_pattern_list[0] + lineText
                else:
                    if i == len(selected_line_nums) - 1:
                        if lineText.endswith(consts.CR_LF_EOL_CHAR):
                            lineText = lineText[0:len(lineText) - len(consts.CR_LF_EOL_CHAR)] + comment_pattern_list[1] + consts.CR_LF_EOL_CHAR
                        else:
                            if lineText.endswith(consts.CR_EOL_CHAR) or lineText.endswith(consts.LF_EOL_CHAR):
                                lineText = lineText[0:len(lineText) - 1] + comment_pattern_list[1] + lineText[(-1)]
                            else:
                                lineText = lineText + comment_pattern_list[1]
                        newText = newText + lineText
                    else:
                        newText = newText + lineText

        self._ReplaceSelectedLines(newText)

    def OnUncommentLines(self):
        lexer = self.GetCtrl().GetLangLexer()
        comment_pattern_list = lexer.GetCommentPattern()
        if 0 == len(comment_pattern_list):
            return
        comment_block = False
        if len(comment_pattern_list) > 1:
            comment_block = True
        newText = ''
        if not comment_block:
            for lineNo in self._GetSelectedLineNumbers():
                lineText = self.GetCtrl().GetLine(lineNo)
                if len(lineText) > 1 and lineText.startswith(comment_pattern_list[0]):
                    lineText = lineText[len(comment_pattern_list[0]):]
                newText = newText + lineText

        else:
            selected_line_nums = self._GetSelectedLineNumbers()
            for i, lineNo in enumerate(selected_line_nums):
                lineText = self.GetCtrl().GetLine(lineNo)
                if i == 0 and lineText.startswith(comment_pattern_list[0]):
                    lineText = lineText[len(comment_pattern_list[0]):]
                else:
                    if i == len(selected_line_nums) - 1 and lineText.strip().endswith(comment_pattern_list[1]):
                        if lineText.endswith(consts.CR_LF_EOL_CHAR):
                            lineText = lineText[0:len(lineText) - len(comment_pattern_list[1]) - len(consts.CR_LF_EOL_CHAR)] + consts.CR_LF_EOL_CHAR
                    else:
                        if lineText.endswith(consts.CR_EOL_CHAR) or lineText.endswith(consts.LF_EOL_CHAR):
                            lineText = lineText[0:len(lineText) - len(comment_pattern_list[1]) - len(consts.LF_EOL_CHAR)] + lineText[(-1)]
                        else:
                            lineText = lineText[0:len(lineText) - len(comment_pattern_list[1])]
                newText = newText + lineText

        self._ReplaceSelectedLines(newText)

    def _GetSelectedLineNumbers(self):
        selStart, selEnd, is_last_line = self._GetPositionsBoundingSelectedLines()
        endLine = self.GetCtrl().LineFromPosition(selEnd)
        if is_last_line:
            endLine += 1
        return range(self.GetCtrl().LineFromPosition(selStart), endLine)

    def _GetPositionsBoundingSelectedLines(self):
        startPos = self.GetCtrl().GetCurrentPos()
        endPos = self.GetCtrl().GetAnchor()
        if startPos > endPos:
            temp = endPos
            endPos = startPos
            startPos = temp
        if endPos == self.GetCtrl().PositionFromLine(self.GetCtrl().LineFromPosition(endPos)):
            endPos = endPos - 1
        selStart = self.GetCtrl().PositionFromLine(self.GetCtrl().LineFromPosition(startPos))
        line_num = self.GetCtrl().LineFromPosition(endPos)
        selEnd = self.GetCtrl().PositionFromLine(line_num + 1)
        return (
         selStart, selEnd, line_num == self.GetCtrl().LineFromPosition(selEnd))

    def _ReplaceSelectedLines(self, text):
        if len(text) == 0:
            return
        selStart, selEnd, _is_last_line = self._GetPositionsBoundingSelectedLines()
        self.GetCtrl().SetSelection(selStart, selEnd)
        self.GetCtrl().ReplaceSelection(text)
        self.GetCtrl().SetSelection(selStart + len(text), selStart)

    def OnUpdate(self, sender=None, hint=None):
        if texteditor.TextView.OnUpdate(self, sender, hint):
            return

    def GetLangId(self):
        lexer = self.GetCtrl().GetLangLexer()
        return lexer.GetLangId()

    def comment_region(self):
        lexer = self.GetCtrl().GetLangLexer()
        comment_pattern_list = lexer.GetCommentPattern()
        if 0 == len(comment_pattern_list):
            return
        comment_block = False
        if len(comment_pattern_list) > 1:
            comment_block = True
        head, tail, chars, lines = self.GetCtrl()._get_region()
        for pos in range(len(lines) - 1):
            line = lines[pos]
            if not comment_block:
                lines[pos] = comment_pattern_list[0] * 2 + line
            else:
                if pos == 0:
                    lines[pos] = comment_pattern_list[0] + line
                if pos == len(lines) - 2:
                    lines[pos] = lines[pos] + comment_pattern_list[1]

        self.GetCtrl()._set_region(head, tail, chars, lines)

    def uncomment_region(self):
        lexer = self.GetCtrl().GetLangLexer()
        comment_pattern_list = lexer.GetCommentPattern()
        if 0 == len(comment_pattern_list):
            return
        comment_block = False
        if len(comment_pattern_list) > 1:
            comment_block = True
        head, tail, chars, lines = self.GetCtrl()._get_region()
        for pos in range(len(lines)):
            line = lines[pos]
            if not line:
                pass
            elif not comment_block:
                if line[:2] == comment_pattern_list[0] * 2:
                    line = line[2:]
                elif line[:1] == comment_pattern_list[0]:
                    line = line[1:]
                lines[pos] = line

        self.GetCtrl()._set_region(head, tail, chars, lines)

    def UpdateUI(self, command_id):
        if command_id == constants.ID_INSERT_COMMENT_TEMPLATE:
            langid = self.GetLangId()
            lexer = syntax.SyntaxThemeManager().GetLexer(langid)
            enabled = lexer.IsCommentTemplateEnable()
            return enabled
        if command_id == constants.ID_INSERT_DECLARE_ENCODING:
            return False
        if command_id in [constants.ID_COMMENT_LINES, constants.ID_UNCOMMENT_LINES, constants.ID_AUTO_COMPLETE]:
            return True
        return texteditor.TextView.UpdateUI(self, command_id)


class CodeCtrl(texteditor.SyntaxTextCtrl):
    CURRENT_LINE_MARKER_NUM = 2
    BREAKPOINT_MARKER_NUM = 1
    CURRENT_LINE_MARKER_MASK = 4
    BREAKPOINT_MARKER_MASK = 4
    TYPE_BLANK_WORD = ' '
    if utils.is_py2():
        DEFAULT_WORD_CHARS = string.letters + string.digits + '_'
    elif utils.is_py3_plus():
        DEFAULT_WORD_CHARS = string.ascii_letters + string.digits + '_'

    def __init__(self, master=None, cnf={}, **kw):
        texteditor.SyntaxTextCtrl.__init__(self, master, cnf=cnf, **kw)
        self._lang_lexer = None
        self.bindtags(self.bindtags() + ('CodeCtrl', ))
        self.fixwordbreaks(GetApp())
        self.autocompleter = None
        self.calltip = None
        self.tag_configure('before', syntax.SyntaxThemeManager().get_syntax_options_for_tag('active_focus'))

    def CreatePopupMenu(self):
        texteditor.TextCtrl.CreatePopupMenu(self)
        self._popup_menu.add_separator()
        self._popup_menu.AppendMenuItem(GetApp().Menubar.GetFormatMenu().FindMenuItem(consts.ID_COMMENT_LINES), handler=self.master.master.GetView().comment_region)
        self._popup_menu.AppendMenuItem(GetApp().Menubar.GetFormatMenu().FindMenuItem(consts.ID_UNCOMMENT_LINES), handler=self.master.master.GetView().uncomment_region)

    def DoIndent(self):
        self.AddText(self.GetEOLChar())
        self.EnsureCaretVisible()

    def GetLangLexer(self):
        if self._lang_lexer is None:
            document = self.master.master.GetView().GetDocument()
            file_ext = document.GetDocumentTemplate().GetDefaultExtension()
            self._lang_lexer = syntax.SyntaxThemeManager().GetLangLexerFromExt(file_ext)
        return self._lang_lexer

    def SetLangLexer(self, lexer):
        self._lang_lexer = lexer

    def SetSyntax(self, syntax_options):
        for tag_name in syntax_options:
            if tag_name == 'TEXT':
                self.configure(**syntax_options[tag_name])
            else:
                self.tag_configure(tag_name, **syntax_options[tag_name])

        self.tag_configure(list(BaseSyntaxcolorer.BASE_TAGDEFS)[0], {'background': None, 'foreground': None})
        self.tag_configure(list(BaseSyntaxcolorer.BASE_TAGDEFS)[1], {'background': None, 'foreground': None})
        self.SetOtherOptions(syntax_options)

    def GetColorClass(self):
        lexer = self.GetLangLexer()
        return lexer.GetColorClass()

    def SetKeyWords(self, kw_lst):
        """Sets the keywords from a list of keyword sets
        @param kw_lst: [ (KWLVL, "KEWORDS"), (KWLVL2, "KEYWORDS2"), ect...]

        """
        kwlist = ''
        for keyw in kw_lst:
            if len(keyw) != 2:
                continue
            elif not not isinstance(keyw[0], int):
                if not isinstance(keyw[1], basestring):
                    continue
                else:
                    kwlist += keyw[1]
                    super(CodeCtrl, self).SetKeyWords(keyw[0], keyw[1])

        if '?' in kwlist:
            kwlist.replace('?', '')
        kwlist = kwlist.split()
        kwlist = list(set(kwlist))
        kwlist.sort()

    def GetCharAt(self, line, col):
        return self.get('%d.%d' % (line, col), '%d.%d' % (line, col + 1))

    def fixwordbreaks(self, root):
        """
            重新设定单词分割,默认把括号等都当做单词
        """
        root.tk.call('tcl_wordBreakAfter', 'a b', 0)
        root.tk.call('set', 'tcl_wordchars', '[a-zA-Z0-9_À-ÖØ-öø-ÿĀ-ſƀ-ɏА-я]')
        root.tk.call('set', 'tcl_nonwordchars', '[^a-zA-Z0-9_À-ÖØ-öø-ÿĀ-ſƀ-ɏА-я]')

    def AutoCompShow(self, replaceLen, chars):
        if self.autocompleter is None:
            self.autocompleter = autocomplete.Completer(self)
        self.autocompleter._present_completions(chars, replaceLen)

    def AutoCompActive(self):
        if self.autocompleter is None:
            return False
        return self.autocompleter._is_visible()

    def OnChar(self, event):
        pass

    def CallTipShow(self, pos, tip):
        """
            显示提示信息框
        """
        if self.calltip is None:
            self.calltip = calltip.CalltipBox(self)
        self.calltip._show_box(pos, tip)

    def CallTipHide(self):
        """
            隐藏提示信息框
        """
        if self.calltip is None:
            return
        self.calltip._close()

    def ClearCurrentLineMarkers(self):
        """
            调试下一步时,先要删除所有断点调试的标记,以便标记下一行
        """
        self.remove_focus_tags()

    def MarkerAdd(self, line):
        """
            标记并高亮断点调试的当前行
        """
        self._tag_range(line, line, 'active_focus')

    def _tag_range(self, start_line, end_line, tag):
        line_prefix = self.GetLineText(start_line)
        if line_prefix.strip():
            first_line = start_line
            last_line = end_line
            self.tag_add(tag, '%d.0' % first_line, '%d.end' % last_line)
        else:
            first_line, first_col, last_line = self._get_text_range_block(text_range)
            for lineno in range(first_line, last_line + 1):
                self._text.tag_add(tag, '%d.%d' % (lineno, first_col), '%d.0' % (lineno + 1))

        self.update_idletasks()
        self.see('%d.0' % last_line)
        self.see('%d.0' % first_line)
        if last_line - first_line < 3:
            self.update_idletasks()
            self.see('%d.0' % (first_line + 3))

    def remove_focus_tags(self):
        for name in [
         'exception_focus',
         'active_focus',
         'completed_focus',
         'suspended_focus',
         'sel']:
            self.tag_remove(name, '0.0', 'end')


CodeCtrl.perform_midline_tab = autocomplete.patched_perform_midline_tab
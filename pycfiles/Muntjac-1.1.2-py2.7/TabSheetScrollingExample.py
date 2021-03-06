# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/tabsheets/TabSheetScrollingExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, Label, TabSheet
from muntjac.terminal.theme_resource import ThemeResource
from muntjac.ui.tab_sheet import ISelectedTabChangeListener

class TabSheetScrollingExample(VerticalLayout, ISelectedTabChangeListener):
    _icon1 = ThemeResource('../sampler/icons/action_save.gif')
    _icon2 = ThemeResource('../sampler/icons/comment_yellow.gif')
    _icon3 = ThemeResource('../sampler/icons/icon_info.gif')

    def __init__(self):
        super(TabSheetScrollingExample, self).__init__()
        l1 = VerticalLayout()
        l1.setMargin(True)
        l1.addComponent(Label('There are no previously saved actions.'))
        l2 = VerticalLayout()
        l2.setMargin(True)
        l2.addComponent(Label('There are no saved notes.'))
        l3 = VerticalLayout()
        l3.setMargin(True)
        l3.addComponent(Label('There are currently no issues.'))
        l4 = VerticalLayout()
        l4.setMargin(True)
        l4.addComponent(Label('There are no comments.'))
        l5 = VerticalLayout()
        l5.setMargin(True)
        l5.addComponent(Label('There is no new feedback.'))
        self._t = TabSheet()
        self._t.setHeight('200px')
        self._t.setWidth('400px')
        self._t.addTab(l1, 'Saved actions', self._icon1)
        self._t.addTab(l2, 'Notes', self._icon2)
        self._t.addTab(l3, 'Issues', self._icon3)
        self._t.addTab(l4, 'Comments', self._icon2)
        self._t.addTab(l5, 'Feedback', self._icon2)
        self._t.addListener(self, ISelectedTabChangeListener)
        self.addComponent(self._t)

    def selectedTabChange(self, event):
        tabsheet = event.getTabSheet()
        tab = tabsheet.getTab(tabsheet.getSelectedTab())
        if tab is not None:
            self.getWindow().showNotification('Selected tab: ' + tab.getCaption())
        return
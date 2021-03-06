# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Tabs/FileOpenTab.py
# Compiled at: 2020-04-29 16:25:24
# Size of source mod 2**32: 2762 bytes
import CIDAN.GUI.Tabs.Tab as Tab
from PySide2.QtWidgets import *
import CIDAN.GUI.Inputs.FileInput as FileInput
from CIDAN.GUI.Data_Interaction.loadDataset import *
import CIDAN.GUI.ListWidgets.TrialListWidget as TrialListWidget

class FileOpenTab(Tab):

    def __init__(self, main_widget):
        self.trial_list_widget = TrialListWidget()
        dataset_file_input = FileInput('Dataset File:', '', None, '', 'Select a file to load in', isFolder=2, forOpen=True)
        dataset_folder_input = FileInput('Dataset Folder:', '', (lambda x: self.add_trial_selection(x)), '', 'Select a folder to load in', isFolder=1, forOpen=True)
        save_dir_new_file = FileInput('Save Directory Location:', None, '', '', 'Select a place to save outputs', isFolder=1, forOpen=False)
        save_dir_new_folder = FileInput('Save Directory Location:', None, '', '', 'Select a place to save outputs', isFolder=1, forOpen=False)
        save_dir_load = FileInput('Previous Session Location:', '', '', '', 'Select the save directory for a previous session',
          isFolder=1, forOpen=True)
        file_open_button = QPushButton()
        file_open_button.setText('Load')
        file_open_button.clicked.connect(lambda : load_new_dataset(main_widget, dataset_file_input, save_dir_new_file))
        folder_open_button = QPushButton()
        folder_open_button.setText('Load')
        folder_open_button.clicked.connect(lambda : load_new_dataset(main_widget, dataset_folder_input, save_dir_new_folder, trials=(self.trial_list_widget.selectedTrials())))
        prev_session_open_button = QPushButton()
        prev_session_open_button.setText('Load')
        prev_session_open_button.clicked.connect(lambda : load_prev_session(main_widget, save_dir_load))
        file_open = Tab('File Open', column_2=[], column_2_display=False, column_1=[dataset_file_input, save_dir_new_file, file_open_button])
        folder_open = Tab('Folder Open', column_2=[self.trial_list_widget], column_2_display=True, column_1=[dataset_folder_input, save_dir_new_folder, folder_open_button])
        prev_session_open = Tab('Previous Session Open', column_2=[], column_2_display=False, column_1=[save_dir_load, prev_session_open_button])
        self.tab_selector = QTabWidget()
        self.tab_selector.addTab(file_open, file_open.name)
        self.tab_selector.addTab(folder_open, folder_open.name)
        self.tab_selector.addTab(prev_session_open, prev_session_open.name)
        super().__init__('FileOpenTab', column_1=[self.tab_selector], column_2=[], column_2_display=False)

    def add_trial_selection(self, path):
        self.trial_list_widget.setItems(path)
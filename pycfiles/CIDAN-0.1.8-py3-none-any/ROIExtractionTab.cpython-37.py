# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/CIDAN/GUI/Tabs/ROIExtractionTab.py
# Compiled at: 2020-04-29 16:53:56
# Size of source mod 2**32: 26173 bytes
from PySide2 import QtCore
import CIDAN.GUI.Tabs.Tab as Tab
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import numpy as np, pyqtgraph as pg
import CIDAN.GUI.Data_Interaction.ROIExtractionThread as ROIExtractionThread
from CIDAN.GUI.SettingWidget.SettingsModule import roi_extraction_settings
import CIDAN.GUI.ListWidgets.ROIListModule as ROIListModule
import CIDAN.GUI.Inputs.OptionInput as OptionInput
import CIDAN.GUI.ListWidgets.TrialListWidget as TrialListWidget
from CIDAN.LSSC.functions.roi_extraction import combine_rois

class ROIExtractionTab(Tab):
    """ROIExtractionTab"""

    def __init__(self, main_widget):
        self.main_widget = main_widget
        self.data_handler = main_widget.data_handler
        self.click_event = False
        self.add_image = False
        self.outlines = True
        self.select_pixel_on = False
        self.brush_size = 0
        self.current_selected_pixels_list = []
        self.current_selected_pixels_mask = np.zeros((self.data_handler.shape[1],
         self.data_handler.shape[2]),
          dtype=bool)
        self.previous_values = {}
        self.select_pixel_color = [0, 255, 0]
        self.select_mode = 'add'
        self.image_item = self.main_widget.roi_image_view.image_view.getImageItem()
        self.image_item.mouseClickEvent = lambda x: self.roi_view_click(x)
        self.image_item.mouseDragEvent = lambda x: self.roi_view_drag(x)
        tab_selector_roi = QTabWidget()
        tab_selector_roi.setStyleSheet('QTabWidget {font-size: 20px;}')
        roi_modification_tab = QWidget()
        roi_modification_tab.setStyleSheet('margin:0px; padding: 0px;')
        roi_modification_tab_layout = QVBoxLayout()
        roi_modification_tab.setLayout(roi_modification_tab_layout)
        self.roi_list_module = ROIListModule(main_widget.data_handler, self)
        roi_modification_tab_layout.addWidget(self.roi_list_module)
        roi_modification_button_top_layout = QHBoxLayout()
        roi_modification_tab_layout.addLayout(roi_modification_button_top_layout)
        add_new_roi = QPushButton(text='New ROI from Selection')
        add_to_roi = QPushButton(text='Add to ROI')
        add_to_roi.clicked.connect(lambda x: self.modify_roi(self.roi_list_module.current_selected_roi, 'add'))
        sub_to_roi = QPushButton(text='Subtract from ROI')
        sub_to_roi.clicked.connect(lambda x: self.modify_roi(self.roi_list_module.current_selected_roi, 'subtract'))
        delete_roi = QPushButton(text='Delete ROI')
        roi_modification_button_top_layout.addWidget(add_to_roi)
        roi_modification_button_top_layout.addWidget(sub_to_roi)
        roi_modification_button_top_layout.addWidget(add_new_roi)
        roi_modification_button_top_layout.addWidget(delete_roi)
        painter_button_group = QButtonGroup()
        off_button = QRadioButton(text='Off')
        off_button.setChecked(True)
        on_button = QRadioButton(text='Add to Selection')
        sub_button = QRadioButton(text='Subtract from Selection')
        painter_button_group.addButton(off_button)
        painter_button_group.addButton(on_button)
        painter_button_group.addButton(sub_button)
        off_button.clicked.connect(lambda x: self.setSelectorBrushType('off'))
        on_button.clicked.connect(lambda x: self.setSelectorBrushType('add'))
        sub_button.clicked.connect(lambda x: self.setSelectorBrushType('subtract'))
        painter_layout = QHBoxLayout()
        painter_layout.addWidget(QLabel(text='Selector Brush: '))
        painter_layout.addWidget(off_button)
        painter_layout.addWidget(on_button)
        painter_layout.addWidget(sub_button)
        roi_modification_tab_layout.addLayout(painter_layout)
        clear_from_selection = QPushButton(text='Clear Selection')
        clear_from_selection.clicked.connect(lambda x: self.clearPixelSelection())
        roi_modification_tab_layout.addWidget(clear_from_selection)
        brush_size_options = OptionInput('Brush Size:', '', lambda x, y: self.setBrushSize(y), 0, 'Sets the brush size', ['1', '3', '5', '7', '9',
         '11', '15', '21', '27',
         '35'])
        roi_modification_tab_layout.addWidget(brush_size_options)
        process_button = QPushButton()
        process_button.setText('Apply Settings')
        self.thread = ROIExtractionThread(main_widget, process_button, self.roi_list_module, self)
        self.main_widget.thread_list.append(self.thread)
        process_button.clicked.connect(lambda : self.thread.runThread())
        self.roi_settings = QWidget()
        self.roi_settings_layout = QVBoxLayout()
        self.roi_settings.setLayout(self.roi_settings_layout)
        self.roi_settings_layout.addWidget(roi_extraction_settings(main_widget))
        self.roi_settings_layout.addWidget(process_button)
        tab_selector_roi.addTab(self.roi_settings, 'ROI Creation')
        tab_selector_roi.addTab(roi_modification_tab, 'ROI Modification')
        self.current_foreground_intensity = 1
        self.set_background('', 'Max Image', update_image=False)
        if self.main_widget.data_handler.rois_loaded:
            self.thread.endThread(True)
        display_settings_layout = QVBoxLayout()
        display_settings = QWidget()
        display_settings.setLayout(display_settings_layout)
        image_chooser = OptionInput('ROI Display type::', '', on_change_function=(self.set_image),
          default_index=0,
          tool_tip='Choose background to display',
          val_list=[
         'Outlines', 'Blob'])
        display_settings_layout.addWidget(image_chooser)
        self.background_chooser = OptionInput('Background:', '', on_change_function=(self.set_background),
          default_index=2,
          tool_tip='Choose background to display',
          val_list=[
         'Blank Image', 'Mean Image', 'Max Image', 'Temporal Correlation Image', 'Eigen Norm Image'])
        display_settings_layout.addWidget(self.background_chooser)
        background_slider_layout = QHBoxLayout()
        background_slider_layout.addWidget(QLabel('0'))
        self.foreground_slider = QSlider(Qt.Horizontal)
        self.foreground_slider.setMinimum(0)
        self.foreground_slider.setMaximum(100)
        self.foreground_slider.setSingleStep(1)
        self.foreground_slider.valueChanged.connect(self.intensity_slider_changed)
        try:
            self.foreground_slider.setValue(80)
        except AttributeError:
            pass

        background_slider_layout.addWidget(self.foreground_slider)
        background_slider_layout.addWidget(QLabel('10'))
        display_settings_layout.addWidget(QLabel('Change foreground intensity:'))
        display_settings_layout.addLayout(background_slider_layout)
        tab_selector_time_trace = QTabWidget()
        tab_selector_time_trace.setStyleSheet('QTabWidget {font-size: 20px;}')
        tab_selector_time_trace.setMaximumHeight(200)
        self.time_plot = pg.PlotWidget()
        self.time_plot.showGrid(x=True, y=True, alpha=0.3)
        tab_selector_time_trace.addTab(self.time_plot, 'Time Trace Plot')
        time_trace_settings = QWidget()
        time_trace_settings_layout = QVBoxLayout()
        time_trace_settings.setLayout(time_trace_settings_layout)
        time_trace_settings_layout.addWidget(OptionInput('Time Trace Type', '', (lambda x: x + x),
          default_index=0, tool_tip='Select way to calculate time trace',
          val_list=[
         'Normal', 'DeltaF/F', 'More']),
          stretch=1)
        time_trace_trial_select_list = TrialListWidget()
        time_trace_trial_select_list.setItems(self.data_handler.dataset_params['dataset_path'])
        time_trace_settings_layout.addWidget(time_trace_trial_select_list, stretch=5)
        tab_selector_time_trace.addTab(time_trace_settings, 'Time Trace Settings')
        roi_view_tabs = QTabWidget()
        roi_view_tabs.setStyleSheet('QTabWidget {font-size: 20px;}')
        self.main_widget.roi_image_view.setStyleSheet('margin:0px; border:0px  solid rgb(50, 65, 75); padding: 0px;')
        roi_view_tabs.addTab(self.main_widget.roi_image_view, 'ROI Display')
        roi_view_tabs.addTab(display_settings, 'Display Settings')
        self.column_2 = [roi_view_tabs, tab_selector_time_trace]
        super().__init__('ROI Extraction', column_1=[
         tab_selector_roi],
          column_2=(self.column_2),
          column_2_display=True)

    def setSelectorBrushType(self, type):
        if type == 'off':
            self.select_pixel_on = False
        else:
            self.select_pixel_on = True
            self.select_mode = type

    def modify_roi(self, roi_num, add_subtract='add'):
        """
        Add/subtracts the currently selected pixels from an ROI
        Parameters
        ----------
        roi_num roi to modify starting at 1
        add_subtract either add or subtract depending on operation wanted

        Returns
        -------
        Nothing
        """
        if roi_num == None:
            print('Please select an roi')
            return
        else:
            shape = self.main_widget.data_handler.edge_roi_image_flat.shape
            roi_num = roi_num - 1
            if add_subtract == 'add':
                print('Adding Selection to ROI #' + str(roi_num + 1))
                self.data_handler.clusters[roi_num] = combine_rois(self.data_handler.clusters[roi_num], self.current_selected_pixels_list)
                self.data_handler.gen_roi_display_variables()
                self.data_handler.calculate_time_trace(roi_num)
            if add_subtract == 'subtract':
                print('Subtracting Selection from ROI #' + str(roi_num + 1))
                self.data_handler.clusters[roi_num] = [x for x in self.data_handler.clusters[roi_num] if x not in self.current_selected_pixels_list]
                self.data_handler.gen_roi_display_variables()
                self.data_handler.calculate_time_trace(roi_num)
            if self.outlines:
                self.roi_image_flat = np.hstack([self.data_handler.edge_roi_image_flat,
                 np.zeros(shape),
                 np.zeros(shape)])
            else:
                self.roi_image_flat = self.main_widget.data_handler.pixel_with_rois_color_flat
        self.select_image_flat = np.zeros([shape[0], 3])
        self.clearPixelSelection(update_display=False)
        self.updateImageDisplay()

    def draw(self, pos):
        pass

    def intensity_slider_changed(self):
        self.current_foreground_intensity = 10 - float(self.foreground_slider.value()) / 10
        self.updateImageDisplay()

    def set_background(self, name, func_name, update_image=True):
        shape = self.main_widget.data_handler.shape
        if func_name == 'Mean Image':
            self.current_background = self.main_widget.data_handler.mean_image.reshape([-1, 1])
        if func_name == 'Max Image':
            self.current_background = self.main_widget.data_handler.max_image.reshape([-1, 1])
        if func_name == 'Blank Image':
            self.current_background = np.zeros([shape[1] * shape[2], 1])
        if func_name == 'Temporal Correlation Image':
            self.current_background = self.data_handler.temporal_correlation_image.reshape([-1, 1])
        if func_name == 'Eigen Norm Image':
            self.current_background = self.data_handler.eigen_norm_image.reshape([-1, 1])
        if update_image:
            self.updateImageDisplay()

    def set_image(self, name, func_name, update_image=True):
        shape = self.main_widget.data_handler.edge_roi_image_flat.shape
        if func_name == 'Outlines':
            self.outlines = True
            self.roi_image_flat = np.hstack([self.data_handler.edge_roi_image_flat,
             np.zeros(shape),
             np.zeros(shape)])
        if func_name == 'Blob':
            self.outlines = False
            self.roi_image_flat = self.main_widget.data_handler.pixel_with_rois_color_flat
        if update_image:
            self.updateImageDisplay()

    def updateImageDisplay(self, new=False):
        try:
            shape = self.main_widget.data_handler.dataset_filtered.shape
            if not hasattr(self, 'select_image_flat'):
                self.select_image_flat = np.zeros([shape[1] * shape[2], 3])
            else:
                range_list = self.main_widget.roi_image_view.image_view.view.viewRange()
                shape = self.main_widget.data_handler.dataset_filtered.shape
                background_max = self.current_background.max()
                background_image_scaled = self.current_foreground_intensity * 255 / (background_max if background_max != 0 else 1) * self.current_background
                background_image_scaled_3_channel = np.hstack([background_image_scaled, background_image_scaled, background_image_scaled])
                if new:
                    combined = self.roi_image_flat + background_image_scaled_3_channel + self.select_image_flat
                    combined_reshaped = combined.reshape((shape[1], shape[2], 3))
                    self.main_widget.roi_image_view.setImage(combined_reshaped)
                    self.clearPixelSelection(update_display=False)
                else:
                    self.image_item.image = background_image_scaled_3_channel.reshape((shape[1], shape[2], 3))
                    self.image_item.updateImage(autoLevels=True)
                    combined = (self.roi_image_flat + self.select_image_flat).reshape((
                     shape[1], shape[2], 3))
                    self.image_item.image += combined
                    self.image_item.image[self.current_selected_pixels_mask] += self.select_pixel_color
                    self.image_item.updateImage(autoLevels=False)
        except AttributeError:
            pass

    def selectRoi(self, num):
        try:
            color_select = (245, 249, 22)
            color_roi = self.main_widget.data_handler.color_list[((num - 1) % len(self.main_widget.data_handler.color_list))]
            shape = self.main_widget.data_handler.dataset_filtered.shape
            self.select_image_flat[self.main_widget.data_handler.clusters[(num - 1)]] = color_select
            self.updateImageDisplay()
        except AttributeError:
            pass

    def deselectRoi(self, num):
        color = self.main_widget.data_handler.color_list[((num - 1) % len(self.main_widget.data_handler.color_list))]
        shape = self.main_widget.data_handler.dataset_filtered.shape
        shape_flat = self.data_handler.edge_roi_image_flat.shape
        self.select_image_flat[self.main_widget.data_handler.clusters[(num - 1)]] = color if not self.outlines else np.hstack([self.data_handler.edge_roi_image_flat,
         np.zeros(shape_flat),
         np.zeros(shape_flat)])[self.main_widget.data_handler.clusters[(num - 1)]]
        self.updateImageDisplay()

    def selectRoiTime(self, num):
        try:
            color_select = (245, 249, 22)
            color_roi = self.main_widget.data_handler.color_list[((num - 1) % len(self.main_widget.data_handler.color_list))]
            shape = self.main_widget.data_handler.dataset_filtered.shape
            if self.roi_list_module.roi_time_check_list[(num - 1)]:
                pen = pg.mkPen(color=color_roi, width=3)
                self.time_plot.plot((self.main_widget.data_handler.get_time_trace(num)), pen=pen)
                self.time_plot.enableAutoRange(axis=0)
        except AttributeError:
            pass

    def deselectRoiTime(self, num):
        color = self.main_widget.data_handler.color_list[((num - 1) % len(self.main_widget.data_handler.color_list))]
        shape = self.main_widget.data_handler.dataset_filtered.shape
        shape_flat = self.data_handler.edge_roi_image_flat.shape
        self.time_plot.clear()
        self.time_plot.enableAutoRange(axis=0)
        for num2, x in zip(range(1, len(self.roi_list_module.roi_time_check_list)), self.roi_list_module.roi_time_check_list):
            if x:
                color_roi = self.main_widget.data_handler.color_list[((num2 - 1) % len(self.main_widget.data_handler.color_list))]
                pen = pg.mkPen(color=color_roi, width=3)
                self.time_plot.plot((self.main_widget.data_handler.get_time_trace(num2)),
                  pen=pen)

    def zoomRoi(self, num):
        """
        Zooms in to a certain roi
        Parameters
        ----------
        num : int
            roi num starts at 1

        Returns
        -------
        Nothing
        """
        num = num - 1
        max_cord = self.main_widget.data_handler.cluster_max_cord_list[num] + 15
        min_cord = self.main_widget.data_handler.cluster_min_cord_list[num] - 15
        self.main_widget.roi_image_view.image_view.getView().setXRange(min_cord[1], max_cord[1])
        self.main_widget.roi_image_view.image_view.getView().setYRange(min_cord[0], max_cord[0])

    def roi_view_click(self, event):
        if event.button() == QtCore.Qt.RightButton:
            if self.image_item.raiseContextMenu(event):
                event.accept()
        else:
            event.accept()
            pos = event.pos()
            x = int(pos.x())
            y = int(pos.y())
            if self.select_pixel_on:
                self.pixel_paint(x, y)
            else:
                self.click_event = True
                pixel_with_rois_flat = self.main_widget.data_handler.pixel_with_rois_flat
                shape = self.main_widget.data_handler.dataset_filtered.shape
                roi_num = int(pixel_with_rois_flat[(shape[2] * x + y)])
                if roi_num != 0:
                    self.roi_list_module.set_current_select(roi_num)

    def roi_view_drag(self, event):
        event.accept()
        pos = event.pos()
        x = int(pos.x())
        y = int(pos.y())
        if self.select_pixel_on:
            self.pixel_paint(x, y)

    def pixel_paint(self, x, y):
        try:
            if self.select_mode == 'add':
                shape = self.main_widget.data_handler.dataset_filtered.shape
                for x_dif in range(self.brush_size * 2 + 1):
                    for y_dif in range(self.brush_size * 2 + 1):
                        x_new = x - self.brush_size - 1 + x_dif
                        y_new = y - self.brush_size - 1 + y_dif
                        if shape[2] * x_new + y_new not in self.current_selected_pixels_list:
                            self.image_item.image[(x_new, y_new)] += [0, 255, 0]
                            self.current_selected_pixels_list.append(shape[2] * x_new + y_new)
                            self.current_selected_pixels_mask[(x_new, y_new)] = True

            if self.select_mode == 'subtract':
                shape = self.main_widget.data_handler.dataset_filtered.shape
                for x_dif in range(self.brush_size * 2 + 1):
                    for y_dif in range(self.brush_size * 2 + 1):
                        x_new = x - self.brush_size - 1 + x_dif
                        y_new = y - self.brush_size - 1 + y_dif
                        if shape[2] * x_new + y_new in self.current_selected_pixels_list:
                            self.image_item.image[(x_new, y_new)] -= [0, 255, 0]
                            self.current_selected_pixels_list.remove(shape[2] * x_new + y_new)
                            self.current_selected_pixels_mask[(x_new, y_new)] = False

            self.image_item.updateImage()
        except IndexError:
            pass

    def clearPixelSelection(self, update_display=True):
        shape = self.main_widget.data_handler.dataset_filtered.shape
        self.current_selected_pixels_mask = np.zeros([shape[1], shape[2]], dtype=bool)
        self.current_selected_pixels_list = []
        if update_display:
            self.updateImageDisplay()

    def check_pos_in_image(self, x, y):
        pass

    def setBrushSize(self, size):
        """
        Sets the brush size

        self.brush_size is the additional size on all dimensions in addition to middle
        point
        Parameters
        ----------
        size from option input

        Returns
        -------
        nothing
        """
        self.brush_size = int((int(size) - 1) / 2)
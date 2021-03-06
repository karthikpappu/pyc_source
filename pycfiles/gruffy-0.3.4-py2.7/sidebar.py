# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/gruffy/sidebar.py
# Compiled at: 2013-01-27 09:02:16
import copy
from gruffy import base
from pgmagick import Color, DrawableFillColor, DrawableFillOpacity, DrawableFont, DrawableGravity, DrawableLine, DrawableList, DrawablePointSize, DrawableRectangle, DrawableScaling, DrawableStrokeAntialias, DrawableStrokeColor, DrawableStrokeOpacity, DrawableStrokeWidth, DrawableText, GravityType, StretchType, StyleType

class SideBar(base.Base):
    """Side Bar Graph Object"""
    bar_spacing = None

    def draw(self):
        self.has_left_labels = True
        SideBar.__base__.draw(self)
        if not self.has_gdata:
            return
        self.draw_bars()

    def draw_bars(self):
        self.dl = DrawableList()
        self.bar_spacing = self.bar_spacing or 0.9
        self.bars_width = self.graph_height / float(self.column_count)
        self.bar_width = self.bars_width * self.bar_spacing / len(self.norm_data)
        self.dl.append(DrawableStrokeOpacity(0.0))
        height = [ 0 for i in range(self.column_count) ]
        length = [ self.graph_left for i in range(self.column_count) ]
        padding = self.bar_width * (1 - self.bar_spacing) / 2
        for row_index, data_row in enumerate(self.norm_data):
            for point_index, data_point in enumerate(data_row['values']):
                self.dl.append(DrawableFillColor(Color(data_row['color'])))
                if type(self.transparent) is float:
                    self.dl.append(DrawableFillOpacity(self.transparent))
                elif self.transparent is True:
                    self.dl.append(DrawableFillOpacity(base.DEFAULT_TRANSPARENCY))
                temp1 = self.graph_left + (self.graph_width - data_point * self.graph_width - height[point_index])
                temp2 = self.graph_left + self.graph_width - height[point_index]
                difference = temp2 - temp1
                left_x = length[point_index] - 1
                left_y = self.graph_top + self.bars_width * point_index + self.bar_width * row_index + padding
                right_x = left_x + difference
                right_y = left_y + self.bar_width
                height[point_index] += data_point * self.graph_width
                self.dl.append(DrawableRectangle(left_x, left_y, right_x, right_y))
                label_center = self.graph_top + (self.bars_width * point_index + self.bars_width / 2)
                self.draw_label(label_center, point_index)
                if self.additional_line_values:
                    _gdata = self.find_label(data_row['label'])
                    self.draw_values(left_y + self.bar_width / 2, _gdata['values'][point_index])

        self.dl.append(DrawableScaling(self.scale, self.scale))
        self.base_image.draw(self.dl)

    def find_label(self, label):
        for i in self.gdata:
            if i['label'] == label:
                return copy.copy(i)

    def draw_line_markers(self):
        if self.hide_line_markers:
            return
        dl = DrawableList()
        dl.append(DrawableStrokeAntialias(False))
        dl.append(DrawableFillColor(Color(self.marker_color)))
        dl.append(DrawableStrokeWidth(1))
        number_of_lines = 5
        increment = self.significant(float(self.maximum_value) / number_of_lines)
        for index in range(number_of_lines + 1):
            line_diff = (self.graph_right - self.graph_left) / number_of_lines
            x = self.graph_right - line_diff * index - 1
            dl.append(DrawableLine(x, self.graph_bottom, x, self.graph_top))
            diff = index - number_of_lines
            marker_label = abs(diff) * increment
            if not self.hide_line_numbers:
                dl.append(DrawableFillColor(Color(self.font_color)))
                font = self.font if self.font else base.DEFAULT_FONT
                dl.append(DrawableFont(font, StyleType.NormalStyle, 400, StretchType.NormalStretch))
                dl.append(DrawableStrokeColor(Color('transparent')))
                dl.append(DrawablePointSize(self.marker_font_size))
                dl.append(DrawableGravity(GravityType.NorthWestGravity))
                text_width = self.calculate_width(self.marker_font_size, str(marker_label))
                x -= text_width / 2
                y = self.graph_bottom + base.LABEL_MARGIN * 2.0
                if type(marker_label) is int:
                    dl.append(DrawableText(x, y, '%d' % marker_label))
                else:
                    dl.append(DrawableText(x, y, '%.1f' % marker_label))
            dl.append(DrawableStrokeAntialias(True))

        dl.append(DrawableScaling(self.scale, self.scale))
        self.base_image.draw(dl)

    def draw_label(self, y_offset, index):
        if index in self.labels and index not in self.labels_seen:
            dl = DrawableList()
            dl.append(DrawableFillColor(self.font_color))
            font = self.font if self.font else base.DEFAULT_FONT
            dl.append(DrawableGravity(GravityType.NorthEastGravity))
            dl.append(DrawableFont(font, StyleType.NormalStyle, 400, StretchType.NormalStretch))
            dl.append(DrawableStrokeColor(Color('transparent')))
            dl.append(DrawablePointSize(self.marker_font_size))
            font_hight = self.calculate_caps_height(self.marker_font_size)
            x = self.raw_columns - self.graph_left + base.LABEL_MARGIN
            y = y_offset + font_hight / 2.0
            dl.append(DrawableText(x, y, self.labels[index]))
            self.labels_seen[index] = 1
            dl.append(DrawableScaling(self.scale, self.scale))
            self.base_image.draw(dl)

    def draw_values(self, y_offset, point):
        self.dl.append(DrawableFillColor(self.font_color))
        font = self.font if self.font else base.DEFAULT_FONT
        self.dl.append(DrawableGravity(GravityType.NorthWestGravity))
        self.dl.append(DrawableFont(font, StyleType.ItalicStyle, 400, StretchType.NormalStretch))
        self.dl.append(DrawableStrokeColor(Color('transparent')))
        marker_font_size = self.marker_font_size * 0.7
        self.dl.append(DrawablePointSize(marker_font_size))
        font_hight = self.calculate_caps_height(marker_font_size)
        x = self.graph_left + base.LABEL_MARGIN
        y = y_offset + font_hight / 2.0
        self.dl.append(DrawableText(x, y, '%.2lf' % point))
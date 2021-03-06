# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrpl/widgets/attribute_widgets.py
# Compiled at: 2017-08-29 09:44:06
"""
AttributeWidgets' hierarchy is parallel to Attribute' hierarchy

An instance attr of Attribute can create its AttributeWidget counterPart
by calling attr.create_widget(name, parent).
"""
import numpy as np
from qtpy import QtCore, QtWidgets
import pyqtgraph as pg
from .spinbox import NumberSpinBox, IntSpinBox, FloatSpinBox, ComplexSpinBox
from .. import pyrpl_utils
from ..curvedb import CurveDB
import sys

class BaseAttributeWidget(QtWidgets.QWidget):
    """
    Base class for attribute widgets.

    The widget usually contains a label and a subwidget (property 'widget'
    of the instance), corresponding to the associated attribute. The subwidget
    is the created by the function make_widget.

    AttributeWidgets are always contained in a ModuleWidget and should be
    fully managed by this ModuleWidget.

    If widget_name=="", then only the subwidget is shown without label.

    A minimum widget should implmenet set_widget, _update,
    and possibly module_value.
    """
    value_changed = QtCore.Signal()

    def __init__(self, module, attribute_name, widget_name=None):
        super(BaseAttributeWidget, self).__init__()
        self.module = module
        self.attribute_name = attribute_name
        if widget_name is None:
            self.widget_name = self.attribute_name
        else:
            self.widget_name = widget_name
        self.setToolTip(self.attribute_descriptor.__doc__)
        self.layout_v = QtWidgets.QVBoxLayout()
        self.layout = self.layout_v
        if self.widget_name != '':
            self.label = QtWidgets.QLabel(self.widget_name)
            self.layout.addWidget(self.label, 0)
            self.layout.addStretch(1)
        self.layout_v.setContentsMargins(0, 0, 0, 0)
        self._make_widget()
        self.layout.addWidget(self.widget, 0)
        self.layout.addStretch(1)
        self.setLayout(self.layout)
        self.write_attribute_value_to_widget()
        setattr(self.module, '_' + self.attribute_name + '_widget', self)
        return

    @property
    def attribute_descriptor(self):
        return getattr(self.module.__class__, self.attribute_name)

    @property
    def attribute_value(self):
        return getattr(self.module, self.attribute_name)

    @attribute_value.setter
    def attribute_value(self, v):
        setattr(self.module, self.attribute_name, v)

    @property
    def widget_value(self):
        """ Property for the current value of the widget.

        The associated setter takes care of not re-emitting signals when the
        gui value is modified through the setter. """
        return self._get_widget_value()

    @widget_value.setter
    def widget_value(self, v):
        if not self.widget.hasFocus():
            try:
                self.widget.blockSignals(True)
                self._set_widget_value(v)
            finally:
                self.widget.blockSignals(False)

    def write_widget_value_to_attribute(self):
        self.attribute_value = self.widget_value
        self.value_changed.emit()

    def write_attribute_value_to_widget(self):
        """ trivial helper function, updates widget value from the attribute"""
        current_value = self.attribute_value
        if current_value is None:
            self.module._logger.warning("Cannot set widget %s of attribute %s.%s to the current value 'None'.", self.widget_name, self.module.name, self.attribute_name)
        else:
            self.widget_value = current_value
        return

    def editing(self):
        """
        User is editing the property graphically don't mess up with him
        :return:
        """
        return self.widget.editing()

    def set_horizontal(self):
        """ puts the label to the left of the widget instead of atop """
        self.layout_h = QtWidgets.QHBoxLayout()
        if hasattr(self, 'label'):
            self.layout_v.removeWidget(self.label)
            self.layout_h.addWidget(self.label)
            self.layout.addStretch(1)
        self.layout_v.removeWidget(self.widget)
        self.layout_h.addWidget(self.widget)
        self.layout.addStretch(1)
        self.layout_v.addLayout(self.layout_h)
        self.layout = self.layout_h

    def _make_widget(self):
        """
        create the new widget.

        Overwrite in derived class.
        """
        self.widget = None
        return

    def _get_widget_value(self):
        """
        returns the current value shown by the widget.

        The type that is returned is understood by the underlying attribute.

        Overwrite in derived class.
        """
        return self.widget.value()

    def _set_widget_value(self, new_value):
        """
        Changes the value displayed in the widget.

        Overwrite in derived class.
        """
        self.widget.setValue(new_value)

    def wheelEvent(self, event):
        """
        Handle mouse wheel event.
        """
        return super(BaseAttributeWidget, self).wheelEvent(event)


class StringAttributeWidget(BaseAttributeWidget):
    """
    Widget for string values.
    """

    def _make_widget(self):
        self.widget = QtWidgets.QLineEdit()
        self.widget.setMaximumWidth(200)
        self.widget.textChanged.connect(self.write_widget_value_to_attribute)

    def _get_widget_value(self):
        return str(self.widget.text())

    def _set_widget_value(self, new_value):
        self.widget.setText(new_value)


class TextAttributeWidget(StringAttributeWidget):
    """
    Property for multiline string values.
    """

    def _make_widget(self):
        self.widget = QtWidgets.QTextEdit()
        self.widget.textChanged.connect(self.write_widget_value_to_attribute)

    def _get_widget_value(self):
        return str(self.widget.toPlainText())


class NumberAttributeWidget(BaseAttributeWidget):
    """
    Base widget for float and int.
    """
    SpinBox = NumberSpinBox

    def _make_widget(self):
        super(NumberAttributeWidget, self)._make_widget()
        self.widget = self.SpinBox(None)
        self.widget.value_changed.connect(self.write_widget_value_to_attribute)
        self.widget.setSingleStep(self.attribute_descriptor.increment)
        self.widget.setMaximum(self.attribute_descriptor.max)
        self.widget.setMinimum(self.attribute_descriptor.min)
        if self.attribute_descriptor.log_increment:
            self.widget.set_log_increment()
        return

    def _get_widget_value(self):
        return self.widget.value()

    def editing(self):
        return self.widget.line.hasFocus()

    def set_per_second(self, val):
        self.widget.set_per_second(val)

    def set_log_increment(self):
        self.widget.set_log_increment()

    def keyPressEvent(self, event):
        """ forwards all key events to spinbox """
        return self.widget.keyPressEvent(event)

    def keyReleaseEvent(self, event):
        """ forwards all key events to spinbox """
        return self.widget.keyReleaseEvent(event)


class IntAttributeWidget(NumberAttributeWidget):
    """
    Widget for integer values.
    """
    SpinBox = IntSpinBox


class FloatAttributeWidget(NumberAttributeWidget):
    """
    Widget for float values
    """
    SpinBox = FloatSpinBox


class ComplexAttributeWidget(FloatAttributeWidget):
    """
    Widget for complex values
    """
    SpinBox = ComplexSpinBox


class ListElementWidget(BaseAttributeWidget):
    """
    this is a wrapper class to embed any AttributeWidget as an element of
    BasePropertyListPropertyWidget. Its usage is found in the property
    element_widget_cls of BasePropertyListPropertyWidget.
    """

    def __init__(self, parent, startindex, *args, **kwargs):
        self.parent = parent
        self.startindex = startindex
        super(ListElementWidget, self).__init__(*args, **kwargs)
        self.set_horizontal()
        self.button_remove = QtWidgets.QPushButton('-')
        self.button_remove.clicked.connect(self.remove_this_element)
        self.button_remove.setFixedWidth(30)
        self.layout.addWidget(self.button_remove, 0)
        self.layout.addStretch(1)
        setattr(self.module, '_' + self.attribute_name + '_widget', self.parent)

    def remove_this_element(self):
        self.parent.attribute_value.__delitem__(index=self.index)

    @property
    def index(self):
        if self in self.parent.widgets:
            return self.parent.widgets.index(self)
        else:
            return self.startindex

    @property
    def attribute_value(self):
        return getattr(self.module, self.attribute_name)[self.index]

    @attribute_value.setter
    def attribute_value(self, v):
        getattr(self.module, self.attribute_name)[self.index] = v

    def mousePressEvent(self, event):
        self.parent.attribute_value.selected = self.index
        return super(ListElementWidget, self).mousePressEvent(event)

    def focusInEvent(self, QFocusEvent):
        self.parent.attribute_value.selected = self.index


class BasePropertyListPropertyWidget(BaseAttributeWidget):
    """
    A widget for a list of Attributes, deriving its functionality from the
    underlying widgets
    """

    def _make_widget(self):
        self.widget = QtWidgets.QFrame()
        self.widget_layout = QtWidgets.QVBoxLayout()
        self.widget.setLayout(self.widget_layout)
        self.widgets = []
        self.button_add = QtWidgets.QPushButton('+')
        self.button_add.clicked.connect(self.append_default)
        self.widget_layout.addWidget(self.button_add)
        self.widget_layout.addStretch(1)
        self.widget_layout.setContentsMargins(0, 0, 0, 0)
        self.selected = None
        self.update_widget_names()
        return

    @property
    def element_widget_cls(self):
        return type('ElementWidget', (
         ListElementWidget,
         self.attribute_descriptor.element_cls._widget_class), {})

    def update_attribute_by_name(self, new_value_list):
        current_list, operation, index, value = new_value_list
        if operation == 'insert':
            self.insert(index, value)
        elif operation == 'setitem':
            self.setitem(index, value)
        elif operation == 'delitem':
            self.delitem(index)
        elif operation == 'select':
            self.select(index)
        else:
            self.module._logger.error('%s.%s_widget.update_attribute_by_name was called with wrong arguments: %s', self.module.name, self.name, new_value_list)

    def append_default(self):
        self.attribute_value.append()

    def insert(self, index, value):
        """"
        make a new element widget - this function is called by the attribute
        """
        element_widget = self.element_widget_cls(self, index, self.module, self.attribute_name, widget_name=str(index))
        self.widgets.insert(index, element_widget)
        if index + 1 >= len(self.widgets):
            insert_before = self.button_add
        else:
            insert_before = self.widgets[(index + 1)]
        self.widget_layout.insertWidget(self.widget_layout.indexOf(insert_before), element_widget)
        self.update_widget_names()

    def setitem(self, index, value):
        self.widgets[index].widget_value = value

    def delitem(self, index=-1):
        if self.selected == index:
            self.selected = None
        widget = self.widgets.pop(index)
        widget.hide()
        self.widget_layout.removeWidget(widget)
        widget.deleteLater()
        self.update_widget_names()
        self.module._logger.error('delitem concluded')
        return

    def select(self, index):
        for i, widget in enumerate(self.widgets):
            if i == index:
                widget.setStyleSheet('background-color: yellow')
                widget.setFocus()
            else:
                widget.setStyleSheet('')

    def update_widget_names(self):
        for widget in self.widgets:
            if hasattr(widget, 'label'):
                widget.label.setText('(' + str(widget.index) + ')')

    def _get_widget_value(self):
        return [ widget.widget_value for widget in self.widgets ]

    def _set_widget_value(self, new_values):
        for index, new_value in enumerate(new_values):
            try:
                self.setitem(index, new_value)
            except IndexError:
                self.insert(index, new_value)

            while len(self) > len(new_values):
                self.delitem()

    def editing(self):
        edit = False
        for widget in self.widgets:
            edit = edit or widget.editing()

        return edit

    @property
    def number(self):
        return self.__len__()

    def __len__(self):
        return len(self.widgets)


class ListComboBox(QtWidgets.QWidget):
    value_changed = QtCore.Signal()

    def __init__(self, number, name, options, decimals=3):
        super(ListComboBox, self).__init__()
        self.setToolTip('First order filter frequencies \nnegative values are for high-pass \npositive for low pass')
        self.lay = QtWidgets.QHBoxLayout()
        self.lay.setContentsMargins(0, 0, 0, 0)
        self.combos = []
        self.options = options
        self.decimals = decimals
        for i in range(number):
            combo = QtWidgets.QComboBox()
            self.combos.append(combo)
            combo.addItems(self.options)
            combo.currentIndexChanged.connect(self.value_changed)
            self.lay.addWidget(combo)

        self.setLayout(self.lay)

    def change_options(self, new_options):
        self.options = new_options
        for combo in self.combos:
            combo.blockSignals(True)
            combo.clear()
            combo.addItems(new_options)
            combo.blockSignals(False)

    def get_list(self):
        return [ float(combo.currentText()) for combo in self.combos ]

    def set_max_cols(self, n_cols):
        """
        If more than n boxes are required, go to next line
        """
        if len(self.combos) <= n_cols:
            return
        for item in self.combos:
            self.lay.removeWidget(item)

        self.v_layouts = []
        n = len(self.combos)
        n_rows = int(np.ceil(n * 1.0 / n_cols))
        j = 0
        for i in range(n_cols):
            layout = QtWidgets.QVBoxLayout()
            self.lay.addLayout(layout)
            for j in range(n_rows):
                index = i * n_rows + j
                if index >= n:
                    break
                layout.addWidget(self.combos[index])

    def set_list(self, val):
        if not np.iterable(val):
            val = [
             val]
        for i, v in enumerate(val):
            v = ('{:.' + str(self.decimals) + 'e}').format(float(v))
            index = self.options.index(v)
            self.combos[i].setCurrentIndex(index)


class FilterAttributeWidget(BaseAttributeWidget):
    """
    Property for list of floats (to be chosen in a list of valid_frequencies)
    The attribute descriptor needs to expose a function valid_frequencies(module)
    """
    decimals = 3

    def __init__(self, module, attribute_name, widget_name=None):
        val = getattr(module, attribute_name)
        if np.iterable(val):
            self.number = len(val)
        else:
            self.number = 1
        self.options = getattr(module.__class__, attribute_name).valid_frequencies(module)
        super(FilterAttributeWidget, self).__init__(module, attribute_name, widget_name=widget_name)

    def _make_widget(self):
        """
        Sets up the widget (here a QDoubleSpinBox)
        :return:
        """
        self.widget = ListComboBox(self.number, '', self._format_options(), decimals=self.decimals)
        self.widget.value_changed.connect(self.write_widget_value_to_attribute)

    def _format_options(self):
        return [ ('{:.' + str(self.decimals) + 'e}').format(float(option)) for option in self.options
               ]

    def refresh_options(self, module):
        self.options = getattr(module.__class__, self.attribute_name).valid_frequencies(module)
        self.widget.change_options(self._format_options())

    def _get_widget_value(self):
        return self.widget.get_list()

    def _set_widget_value(self, new_value):
        if isinstance(new_value, str) or not np.iterable(new_value):
            new_value = [
             new_value]
        self.widget.set_list(new_value)

    def set_max_cols(self, n_cols):
        self.widget.set_max_cols(n_cols)


class SelectAttributeWidget(BaseAttributeWidget):
    """
    Multiple choice property.
    """

    def _make_widget(self):
        self.widget = QtWidgets.QComboBox()
        self.widget.addItems(self.options)
        self.widget.currentIndexChanged.connect(self.write_widget_value_to_attribute)

    @property
    def options(self):
        opt = self.attribute_descriptor.options(self.module).keys()
        opt = [ str(v) for v in opt ]
        if len(opt) == 0:
            opt = [
             '']
        return opt

    def _get_widget_value(self):
        return str(self.widget.currentText())

    def _set_widget_value(self, new_value):
        try:
            index = self.options.index(str(new_value))
        except (IndexError, ValueError):
            self.module._logger.warning('SelectWidget %s could not find current value %s in the options %s', self.attribute_name, new_value, self.options)
            index = 0

        self.widget.setCurrentIndex(index)

    def change_options(self, new_options=None):
        """
        The options of the combobox can be changed dynamically.

        new_options is an argument that is ignored, since the new options
        are available as a property to the widget already.
        """
        self.widget.blockSignals(True)
        self.widget.clear()
        self.widget.addItems(self.options)
        self.widget_value = self.attribute_value
        self.widget.blockSignals(False)


class LedAttributeWidget(BaseAttributeWidget):
    """ Boolean property with a button whose text and color indicates whether """

    def _make_widget(self):
        desc = pyrpl_utils.recursive_getattr(self.module, '__class__.' + self.attribute_name)
        val = pyrpl_utils.recursive_getattr(self.module, self.attribute_name)
        self.widget = QtWidgets.QPushButton('setting up...')
        self.widget.clicked.connect(self.button_clicked)

    def _set_widget_value(self, new_value):
        if new_value == True:
            color = 'green'
            text = 'stop'
        else:
            color = 'red'
            text = 'start'
        self.widget.setStyleSheet('background-color:%s' % color)
        self.widget.setText(text)

    def button_clicked(self):
        self.attribute_value = not self.attribute_value


class BoolAttributeWidget(BaseAttributeWidget):
    """
    Checkbox for boolean attributes
    """

    def _make_widget(self):
        self.widget = QtWidgets.QCheckBox()
        self.widget.stateChanged.connect(self.write_widget_value_to_attribute)

    def _get_widget_value(self):
        return self.widget.checkState() == 2

    def _set_widget_value(self, new_value):
        self.widget.setCheckState(new_value * 2)


class BoolIgnoreAttributeWidget(BoolAttributeWidget):
    """
    Like BoolAttributeWidget with additional option 'ignore' that is
    shown as a grey check in GUI
    """
    _gui_to_attribute_mapping = pyrpl_utils.Bijection({0: False, 1: 'ignore', 
       2: True})

    def _make_widget(self):
        """
        Sets the widget (here a QCheckbox)
        :return:
        """
        self.widget = QtWidgets.QCheckBox()
        self.widget.setTristate(True)
        self.widget.stateChanged.connect(self.write_widget_value_to_attribute)
        self.setToolTip('Checked:\t    on\nUnchecked: off\nGrey:\t    ignore')

    def _get_widget_value(self):
        return self._gui_to_attribute_mapping[self.widget.checkState()]

    def _set_widget_value(self, new_value):
        self.widget.setCheckState(self._gui_to_attribute_mapping.inverse[new_value])


class DataWidget(pg.GraphicsWindow):
    """
    A widget to plot real or complex datasets. To plot data, use the
    function _set_widget_value(new_value, transform_magnitude)

    new_value is a a tuple (x, y), with x the x values, y, a 1D array for a
    single curve or a 2D array for multiple curves. If at least one of the
    curve is complex, magnitude and phases will be plotted.

    transform_magnitude is the function to transform magnitude data.
    """
    _defaultcolors = [
     'm', 'b', 'g', 'r', 'y', 'c', 'o', 'w']

    def __init__(self, title=None):
        super(DataWidget, self).__init__(title=title)
        self.plot_item = self.addPlot(title='Curve')
        self.plot_item_phase = self.addPlot(row=1, col=0, title='Phase (deg)')
        self.plot_item_phase.setXLink(self.plot_item)
        self.plot_item.showGrid(y=True, alpha=1.0)
        self.plot_item_phase.showGrid(y=True, alpha=1.0)
        self.curves = []
        self.curves_phase = []
        self._is_real = True
        self._set_real(True)

    def _set_widget_value(self, new_value, transform_magnitude=lambda data: 20.0 * np.log10(np.abs(data) + sys.float_info.epsilon)):
        if new_value is None:
            return
        else:
            x, y = new_value
            shape = np.shape(y)
            if len(shape) > 2:
                raise ValueError('Data cannot be larger than 2 dimensional')
            if len(shape) == 1:
                y = [
                 y]
            self._set_real(np.isreal(y).all())
            for i, values in enumerate(y):
                self._display_curve_index(x, values, i, transform_magnitude=transform_magnitude)

            while i + 1 < len(self.curves):
                i += 1
                self.curves[i].hide()

            return

    def _display_curve_index(self, x, values, i, transform_magnitude):
        y_mag = transform_magnitude(values)
        y_phase = np.zeros(len(values)) if self._is_real else self._phase(values)
        if len(self.curves) <= i:
            color = self._defaultcolors[(i % len(self._defaultcolors))]
            self.curves.append(self.plot_item.plot(pen=color))
            self.curves_phase.append(self.plot_item_phase.plot(pen=color))
        self.curves[i].setData(x, y_mag)
        self.curves_phase[i].setData(x, y_phase)

    def _set_real(self, bool):
        self._is_real = bool
        if bool:
            self.plot_item_phase.hide()
            self.plot_item.setTitle('')
        else:
            self.plot_item_phase.show()
            self.plot_item.setTitle('Magnitude (dB)')

    def _phase(self, data):
        """ little helpers """
        return np.angle(data, deg=True)

    def setRange(self, *args, **kwds):
        self.plot_item.setRange(*args, **kwds)


class PlotAttributeWidget(BaseAttributeWidget):
    _defaultcolors = [
     'g', 'r', 'b', 'y', 'c', 'm', 'o', 'w']

    def time(self):
        return pyrpl_utils.time()

    def _make_widget(self):
        """
        Sets the widget (here a QCheckbox)
        :return:
        """
        self.widget = pg.GraphicsWindow(title='Plot')
        legend = getattr(self.module.__class__, self.attribute_name).legend
        self.pw = self.widget.addPlot(title='%s vs. time (s)' % legend)
        self.plot_start_time = self.time()
        self.curves = {}
        setattr(self.module.__class__, '_' + self.attribute_name + '_pw', self.pw)

    def _set_widget_value(self, new_value):
        try:
            args, kwargs = new_value
        except:
            if isinstance(new_value, dict):
                args, kwargs = [], new_value
            elif isinstance(new_value, list):
                args, kwargs = new_value, {}
            else:
                args, kwargs = [
                 new_value], {}

        for k in kwargs.keys():
            v = kwargs.pop(k)
            kwargs[k[0]] = v

        i = 0
        for value in args:
            while self._defaultcolors[i] in kwargs:
                i += 1

            kwargs[self._defaultcolors[i]] = value

        t = self.time() - self.plot_start_time
        for color, value in kwargs.items():
            if value is not None:
                if color not in self.curves:
                    self.curves[color] = self.pw.plot(pen=color)
                curve = self.curves[color]
                x, y = curve.getData()
                if x is None or y is None:
                    x, y = np.array([t]), np.array([value])
                else:
                    x, y = np.append(x, t), np.append(y, value)
                curve.setData(x, y)

        return

    def _magnitude(self, data):
        """ little helpers """
        return 20.0 * np.log10(np.abs(data) + sys.float_info.epsilon)

    def _phase(self, data):
        """ little helpers """
        return np.angle(data, deg=True)


class DataAttributeWidget(PlotAttributeWidget):
    """
    Plots a curve (complex or real), with an array as input.
    """

    def _make_widget(self):
        self.widget = pg.GraphicsWindow(title='Curve')
        self.plot_item = self.widget.addPlot(title='Curve')
        self.plot_item_phase = self.widget.addPlot(row=1, col=0, title='Phase (deg)')
        self.plot_item_phase.setXLink(self.plot_item)
        self.plot_item.showGrid(y=True, alpha=1.0)
        self.plot_item_phase.showGrid(y=True, alpha=1.0)
        self.curve = self.plot_item.plot(pen='g')
        self.curve_phase = self.plot_item_phase.plot(pen='g')
        self._is_real = True
        self._set_real(True)

    def _set_real(self, bool):
        self._is_real = bool
        if bool:
            self.plot_item_phase.hide()
            self.plot_item.setTitle('')
        else:
            self.plot_item_phase.show()
            self.plot_item.setTitle('Magnitude (dB)')


class CurveAttributeWidget(DataAttributeWidget):
    """
    Plots a curve (complex or real), with an id number as input.
    """

    def get_xy_data(self, new_value):
        """ helper function to extract xy data from a curve object"""
        if new_value is None:
            return (None, None, None)
        else:
            try:
                data = getattr(self.module, '_' + self.attribute_name + '_object').data
                name = getattr(self.module, '_' + self.attribute_name + '_object').params['name']
            except:
                return (None, None, None)

            x, y = data
            return (x, y, name)
            return

    def _set_widget_value(self, new_value):
        x, y, name = self.get_xy_data(new_value)
        if x is not None:
            if not np.isreal(y).all():
                self.curve.setData(x, self._magnitude(y))
                self.curve_phase.setData(x, self._phase(y))
                self.plot_item_phase.show()
                self.plot_item.setTitle(name + ' - Magnitude (dB)')
            else:
                self.curve.setData(x, np.real(y))
                self.plot_item_phase.hide()
                self.plot_item.setTitle(name)
        return


class CurveSelectAttributeWidget(SelectAttributeWidget):
    """
    Select one or many curves.
    """

    def _make_widget(self):
        """
        Sets up the widget (here a QComboBox)

        :return:
        """
        self.widget = QtWidgets.QListWidget()
        self.widget.addItems(self.options)
        self.widget.currentItemChanged.connect(self.write_widget_value_to_attribute)

    def _get_widget_value(self):
        return int(self.widget.currentItem().text())

    def _set_widget_value(self, new_value):
        """ should be much simpler here. all this logic should be in the
        attribute """
        if new_value is None:
            new_value = -1
        if hasattr(new_value, 'pk'):
            new_value = new_value.pk
        try:
            index = self.options.index(str(new_value))
        except IndexError:
            self.module._logger.warning('SelectWidget %s could not find current value %s in the options %s', self.attribute_name, self.new_value, self.options)
            index = 0

        self.widget.setCurrentRow(index)
        return
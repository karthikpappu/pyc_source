# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/widgets/label.py
# Compiled at: 2020-04-24 23:12:07
# Size of source mod 2**32: 22219 bytes
"""
Module that contains classes to create different kind of labels
"""
from __future__ import print_function, division, absolute_import
from Qt.QtCore import *
from Qt.QtWidgets import *
from Qt.QtGui import *
from tpDcc.libs.qt.core import qtutils
from tpDcc.libs.qt.widgets import graphicseffects

class BaseLabel(QLabel, object):

    class Levels(object):
        H1 = 1
        H2 = 2
        H3 = 3
        H4 = 4

    class Types(object):
        SECONDARY = 'secondary'
        WARNING = 'warning'
        DANGER = 'danger'

    def __init__(self, text='', parent=None, flags=0):
        super(BaseLabel, self).__init__(text, parent, flags)
        self._actual_text = text
        self._underline = False
        self._mark = False
        self._delete = False
        self._strong = False
        self._code = False
        self._elide_mode = Qt.ElideNone
        self._type = ''
        self._level = 0
        self.setTextInteractionFlags(Qt.TextBrowserInteraction | Qt.LinksAccessibleByMouse)
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setProperty('label_text', text)

    def _get_type(self):
        """
        Returns label type
        :return: str, BaseLabel.Types
        """
        return self._type

    def _set_type(self, value):
        """
        Sets label type
        :param value: BaseLabel.Types
        """
        self._type = value
        self.style().polish(self)

    def _get_level(self):
        """
        Returns label level
        :return: str
        """
        return self._level

    def _set_level(self, value):
        """
        Sets label level
        :param value: itn (BaseLabel.Levels)
        """
        self._level = value
        self.style().polish(self)

    def _get_underline(self):
        """
        Returns whether or not label is using an underline style
        :return: bool
        """
        return self._underline

    def _set_underline(self, flag):
        """
         Sets label to use an underline style
         :return: bool
         """
        self._underline = flag
        self.style().polish(self)

    def _get_delete(self):
        """
        Returns whether or not label is using a delete style
        :return: bool
        """
        return self._delete

    def _set_delete(self, flag):
        """
         Sets label to use a delete style
         :return: bool
         """
        self._delete = flag
        self.style().polish(self)

    def _get_strong(self):
        """
        Returns whether or not label is using a strong style
        :return: bool
        """
        return self._strong

    def _set_strong(self, flag):
        """
         Sets label to use a strong style
         :return: bool
         """
        self._strong = flag
        self.style().polish(self)

    def _get_mark(self):
        """
        Returns whether or not label is using a mark style
        :return: bool
        """
        return self._mark

    def _set_mark(self, flag):
        """
         Sets label to use a mark style
         :return: bool
         """
        self._mark = flag
        self.style().polish(self)

    def _get_code(self):
        """
        Returns whether or not label is using a code style
        :return: bool
        """
        return self._code

    def _set_code(self, flag):
        """
         Sets label to use a code style
         :return: bool
         """
        self._code = flag
        self.style().polish(self)

    def _get_elide_mode(self):
        """
        Returns which elide mode label is using
        :return: Qt.ElideLeft/Qt.ElideMiddle/Qt.ElideRight/Qt.ElideNone
        """
        return self._elide_mode

    def _set_elide_mode(self, value):
        """
        Sets elide mode used by the label
        :param value: Qt.ElideLeft/Qt.ElideMiddle/Qt.ElideRight/Qt.ElideNone
        """
        self._elide_mode = value
        self._update_elided_text()

    theme_type = Property(str, _get_type, _set_type)
    theme_level = Property(int, _get_level, _set_level)
    theme_underline = Property(bool, _get_underline, _set_underline)
    theme_delete = Property(bool, _get_delete, _set_delete)
    theme_mark = Property(bool, _get_mark, _set_mark)
    theme_strong = Property(bool, _get_strong, _set_strong)
    theme_code = Property(bool, _get_code, _set_code)
    theme_elide_mode = Property(bool, _get_elide_mode, _set_elide_mode)

    def minimumSizeHint(self):
        """
         Overrides base QObject minimumSizeHint function
         :return: QSize
         """
        return QSize(1, self.fontMetrics().height())

    def resizeEvent(self, event):
        """
        Overrides base QObject resizeEvent function
        """
        self._update_elided_text()

    def text(self):
        """
        Overrides base QLabel text function
        :return: str
        """
        return self._actual_text

    def setText(self, text):
        """
        Overrides base QLabel setText function
        :return: str
        """
        self._actual_text = text
        self._update_elided_text()
        self.setToolTip(text)

    def h1(self):
        """
        Sets label with h1 type
        """
        self.theme_level = self.Levels.H1
        return self

    def h2(self):
        """
        Sets label with h2 type
        """
        self.theme_level = self.Levels.H2
        return self

    def h3(self):
        """
        Sets label with h3 type
        """
        self.theme_level = self.Levels.H3
        return self

    def h4(self):
        """
        Sets label with h4 type
        """
        self.theme_level = self.Levels.H4
        return self

    def secondary(self):
        """
        Sets label with secondary type
        """
        self.theme_type = self.Types.SECONDARY
        return self

    def warning(self):
        """
        Sets label with warning type
        """
        self.theme_type = self.Types.WARNING
        return self

    def danger(self):
        """
        Sets label with danger type
        """
        self.theme_type = self.Types.DANGER
        return self

    def strong(self, flag=True):
        """
        Sets label with strong type
        :param flag:
        """
        self.theme_strong = flag
        return self

    def mark(self, flag=True):
        """
        Sets label with mark type
        :param flag:
        """
        self.theme_mark = flag
        return self

    def code(self, flag=True):
        """
        Sets label with code type
        :param flag:
        """
        self.theme_code = flag
        return self

    def delete(self, flag=True):
        """
        Sets label with delete type
        :param flag:
        """
        self.theme_delete = flag
        return self

    def underline(self, flag=True):
        """
        Sets label with underline type
        :param flag:
        """
        self.theme_underline = flag
        return self

    def _update_elided_text(self):
        font_metrics = self.fontMetrics()
        elided_text = font_metrics.elidedText(self._actual_text, self._elide_mode, self.width() - 4)
        super(BaseLabel, self).setText(elided_text)


class DragDropLine(QLineEdit, object):
    __doc__ = '\n    QLineEdit that supports drag and drop behaviour\n    '

    def __init__(self, parent=None):
        super(DragDropLine, self).__init__(parent)
        self.setDragEnabled(True)
        self.setReadOnly(True)

    def dragEnterEvent(self, event):
        """
        Overrides QWidget dragEnterEvent to enable drop behaviour with file
        :param event: QDragEnterEvent
        :return:
        """
        data = event.mimeData()
        urls = data.urls()
        if urls:
            if urls[0].scheme() == 'file':
                event.acceptProposedAction()

    def dragMoveEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            if urls[0].scheme() == 'file':
                event.acceptProposedAction()

    def dropEvent(self, event):
        data = event.mimeData()
        urls = data.urls()
        if urls:
            if urls[0].scheme() == 'file':
                self.setText(urls[0].toLocalFile())


class ClickLabel(QLabel, object):
    __doc__ = '\n    This label emits a clicked signal when the user clicks on it\n    '
    clicked = Signal()

    def mousePressEvent(self, event):
        self.clicked.emit()
        super(ClickLabel, self).mousePressEvent(event)


class RightElidedLabel(QLabel, object):
    __doc__ = '\n    Custom label which supports elide right\n    '

    def __init__(self, *args):
        (super(RightElidedLabel, self).__init__)(*args)
        self._text = ''

    def setText(self, text):
        self._text = text
        super(RightElidedLabel, self).setText(text)

    def resizeEvent(self, event):
        metrics = QFontMetrics(self.font())
        elided = metrics.elidedText(self._text, Qt.ElideRight, self.width())
        super(RightElidedLabel, self).setText(elided)


class ElidedLabel(QLabel, object):
    __doc__ = '\n    This label elides text and adds ellipses if the text does not fit\n    properly withing the widget frame\n    '

    def __init__(self, parent=None):
        super(ElidedLabel, self).__init__(parent=parent)
        self._elide_mode = Qt.ElideRight
        self._actual_text = ''
        self._line_width = 0
        self._ideal_width = None
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    def sizeHint(self):
        base_size_hint = super(ElidedLabel, self).sizeHint()
        return QSize(self._get_width_hint(), base_size_hint.height())

    def _get_width_hint(self):
        if not self._ideal_width:
            doc = QTextDocument()
            try:
                try:
                    doc.setHtml(self._actual_text + '&nbsp;')
                    doc.setDefaultFont(self.font())
                    width = doc.idealWidth()
                except Exception:
                    width = self.width()

            finally:
                qtutils.safe_delete_later(doc)

            self._ideal_width = width
        return self._ideal_width

    def _get_elide_mode(self):
        """
        Returns current elide mode
        """
        return self._elide_mode

    def _set_elide_mode(self, value):
        """
        Set the current elide mode.
        """
        if value != Qt.ElideLeft:
            if value != Qt.ElideRight:
                raise ValueError('elide_mode must be set to either QtCore.Qt.ElideLeft or QtCore.Qt.ElideRight')
        self._elide_mode = value
        self._update_elided_text()

    elide_mode = property(_get_elide_mode, _set_elide_mode)

    def text(self):
        """
        Overridden base method to return the original unmodified text
        """
        return self._actual_text

    def setText(self, text):
        self._ideal_width = None
        self._actual_text = text
        self._update_elided_text()
        if super(ElidedLabel, self).text() != self._actual_text:
            self.setToolTip('<p>%s</p>' % (self._actual_text,))
        else:
            self.setToolTip('')

    def resizeEvent(self, event):
        """
        Overridden base method called when the widget is resized.
        """
        self._update_elided_text()

    def _update_elided_text(self):
        """
        Update the elided text on the label
        """
        text = self._elide_text(self._actual_text, self._elide_mode)
        QLabel.setText(self, text)

    def _elide_text(self, text, elide_mode):
        """
        Elide the specified text using the specified mode
        :param text:        The text to elide
        :param elide_mode:  The elide mode to use
        :returns:           The elided text.
        """
        target_width = self.width()
        doc = QTextDocument()
        try:
            doc.setHtml(text)
            doc.setDefaultFont(self.font())
            line_width = doc.idealWidth()
            if line_width <= target_width:
                self._line_width = line_width
                return text
            cursor = QTextCursor(doc)
            ellipses = ''
            if elide_mode != Qt.ElideNone:
                ellipses = '...'
                if elide_mode == Qt.ElideLeft:
                    cursor.setPosition(0)
                else:
                    if elide_mode == Qt.ElideRight:
                        char_count = doc.characterCount()
                        cursor.setPosition(char_count - 1)
                cursor.insertText(ellipses)
            ellipses_len = len(ellipses)
            while line_width > target_width:
                start_line_width = line_width
                char_count = doc.characterCount()
                if char_count <= ellipses_len:
                    self._line_width = 0
                    return ''
                line_width = doc.idealWidth()
                p = target_width / line_width
                chars_to_delete = max(1, char_count - int(float(char_count) * p) - 2)
                if elide_mode == Qt.ElideLeft:
                    start = ellipses_len
                    end = chars_to_delete + ellipses_len
                else:
                    start = max(0, char_count - chars_to_delete - ellipses_len - 1)
                    end = max(0, char_count - ellipses_len - 1)
                cursor.setPosition(start)
                cursor.setPosition(end, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()
                line_width = doc.idealWidth()
                if line_width == start_line_width:
                    break

            self._line_width = line_width
            return doc.toHtml()
        finally:
            qtutils.safe_delete_later(doc)

    @property
    def line_width(self):
        """
        :returns: int, width of the line of text in pixels
        """
        return self._line_width


class ThumbnailLabel(QLabel, object):

    def __init__(self, parent=None):
        super(ThumbnailLabel, self).__init__(parent=parent)

    def setPixmap(self, pixmap):
        if pixmap.height() > 55 or pixmap.width() > 80:
            pixmap = pixmap.scaled(QSize(80, 55), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        super(ThumbnailLabel, self).setPixmap(pixmap)


class AnimatedLabel(QLabel, object):

    def __init__(self, text='', duration=800, parent=None):
        super(AnimatedLabel, self).__init__(text, parent=parent)
        font = self.font()
        font.setPointSize(18)
        font.setBold(True)
        self.setFont(font)
        self.opacity_effect = graphicseffects.OpacityEffect(target=self, duration=duration)
        self.opacity_effect.animation.valueChanged.connect(self._set_label_opacity)
        self.opacity_effect.animation.finished.connect(self.hide)

    def get_duration(self):
        return self.opacity_effect.duration

    def set_duration(self, value):
        self.opacity_effect.duration = value

    duration = property(get_duration, set_duration)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setOpacity(self.opacity_effect.animation.currentValue())
        if self.text():
            painter.drawText(event.rect(), self.text())

    def show_message(self, text):
        self.setText(text)
        parent = self.parent()
        if parent:
            self.move(10, parent.size().height() - self.fontMetrics().height() - 10)
        self.opacity_effect.fade_in_out()

    def _set_label_opacity(self, value):
        if self.opacity_effect.animation.state() == QPropertyAnimation.Running:
            self.setVisible(value > 0)
            self.update()


class IconLabel(QLabel, object):
    __doc__ = '\n    Displays an icon beside a standard label\n    '
    clicked = Signal()

    def __init__(self, *args, **kwargs):
        self._icon = kwargs.pop('icon') if 'icon' in kwargs else None
        self._press = False
        self._two_sided = True
        (super(IconLabel, self).__init__)(*args, **kwargs)
        self.setContentsMargins(20, 0, 0, 0)
        self._value_a = self.text()
        self._value_b = self.text()

    def get_value_a(self):
        return self._value_a

    def get_value_b(self):
        return self._value_b

    value_a = property(get_value_a)
    value_b = property(get_value_b)

    def mousePressEvent(self, event):
        if self._two_sided:
            self._press = True
            self.setText(self._value_a, False)
            self.update()
        self.clicked.emit()

    def mouseReleaseEvent(self, event):
        if self._two_sided:
            self._press = False
            self.setText(self._value_b, False)
            self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        if self._icon:
            self._icon.paint(p, QRect(0, self.height() * 0.5 - 5, 12, 12))
        super(IconLabel, self).paintEvent(event)

    def setText(self, text, update=True):
        super(IconLabel, self).setText('<font>%s</font>' % text)
        if update:
            self._value_b = text

    def set_icon(self, icon):
        self._icon = icon


class ClippedLabel(QLabel, object):

    def __init__(self, text='', width=0, ellipsis=True, always_show_all=False, parent=None):
        super(ClippedLabel, self).__init__(text, parent)
        self._always_show_all = always_show_all
        self._ellipsis = ellipsis
        self._width = None
        self._text = None
        self._elided = None
        self.setMinimumWidth(width if width else 0)

    def paintEvent(self, event):
        painter = QPainter(self)
        self.drawFrame(painter)
        margin = self.margin()
        rect = self.contentsRect()
        rect.adjust(margin, margin, -margin, -margin)
        text = self.text()
        width = rect.width()
        if text != self._text or width != self._width:
            self._text = text
            self._width = width
            self._elided = self.fontMetrics().elidedText(text, Qt.ElideRight, width)
        else:
            option = QStyleOption()
            option.initFrom(self)
            if self._always_show_all:
                if self._width >= self.sizeHint().width():
                    self.style().drawItemText(painter, rect, self.alignment(), option.palette, self.isEnabled(), self.text(), self.foregroundRole())
            else:
                if self._ellipsis:
                    self.style().drawItemText(painter, rect, self.alignment(), option.palette, self.isEnabled(), self._elided, self.foregroundRole())
                else:
                    self.style().drawItemText(painter, rect, self.alignment(), option.palette, self.isEnabled(), self.text(), self.foregroundRole())
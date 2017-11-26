"""This module defines the ButtonView class."""


from .view import View
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPainter, QBrush, QPen, QColor
from PyQt5.QtCore import Qt, QPoint


class SwitchView(View):
    """The Switch view creates a clickable switch for triggering actions."""

    _SCALE = 150

    def __init__(self, on=False):
        """Initialize the switch view.

        :param on: the state of the button"""
        super().__init__()
        self._state = on
        self.mousePressEvent = self._mouse_press_event
        self._on_toggle = None

    def paintEvent(self, event):
        paint = QPainter()
        paint.begin(self)

        paint.setBrush(Qt.lightGray)
        scale_x = self.width() / self._SCALE
        scale_y = self.height() / self._SCALE
        paint.drawRect(0, 0, 95*scale_x, 45*scale_y)

        paint.setBrush(Qt.darkGray)
        paint.drawRect(10 * scale_x, 10 * scale_y, 80 * scale_x, 25 * scale_y)

        if self._state:
            paint.setBrush(Qt.green)
            paint.drawRect(50 * scale_x, 10 * scale_y, 40 * scale_x, 25 * scale_y)
        else:
            paint.setBrush(Qt.red)
            paint.drawRect(10 * scale_x, 10 * scale_y, 40 * scale_x, 25 * scale_y)

        paint.end()

    @property
    def on(self):
        self.repaint()
        return self._state

    @on.setter
    def on(self, to):
        self._state = to

    def toggle(self):
        self._state = not self._state

        if self._on_toggle is not None:
            self._on_toggle()

        self.repaint()

    def on_toggle(self, callback):
        self._on_toggle = callback

    def _mouse_press_event(self, event):
        self.toggle()


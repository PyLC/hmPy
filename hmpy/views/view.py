from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize


class View(QWidget):

    _DEFAULT_SIZE = 200

    def __init__(self, x_scale=1, y_scale=1, parent=None):
        super().__init__(parent)
        self._x_scale = x_scale
        self._y_scale = y_scale

        self._resize()

    def _resize(self):
        x_size = self._DEFAULT_SIZE * self._x_scale
        y_size = self._DEFAULT_SIZE * self._y_scale
        self._size = QSize(x_size, y_size)
        self.resize(self._size)

    def set_x_scale(self, scale):
        self._x_scale = scale
        self._resize()

    def set_y_scale(self, scale):
        self._y_scale = scale
        self._resize()

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self._size

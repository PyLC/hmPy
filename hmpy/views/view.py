from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize


class View(QWidget):

    _DEFAULT_SIZE = 200

    def __init__(self, x_scale=1, y_scale=1, parent=None):
        super().__init__(parent)
        x_size = self._DEFAULT_SIZE * x_scale
        y_size = self._DEFAULT_SIZE * y_scale
        self._size = QSize(x_size, y_size)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self._size

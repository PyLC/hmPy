from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize


class View(QWidget):

    _DEFAULT_SIZE = 200

    def __init__(self, scale=1, parent=None):
        super().__init__(parent)
        size = self._DEFAULT_SIZE * scale
        self._size = QSize(size, size)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self._size

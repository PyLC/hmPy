from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QSize


class View(QWidget):

    _VIEW_SIZE = QSize(200, 200)

    def __init__(self, parent=None):
        super().__init__(parent)

    def sizeHint(self):
        return self.minimumSizeHint()

    def minimumSizeHint(self):
        return self._VIEW_SIZE

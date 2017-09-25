from PyQt5.QtWidgets import QLayout, QSizePolicy
from PyQt5.QtCore import QPoint, QRect, QSize, Qt


class InterfaceLayout(QLayout):
    """The Interface layout."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._items = []

    def __del__(self):
        while self.takeAt(0):
            pass

    def addItem(self, item):
        self._items.append(item)

    def count(self):
        return len(self._items)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        rect = self.contentsRect()
        x = rect.x()
        y = rect.y()
        line_height = 0

        for item in self._items:
            wid = item.widget()

            spacing_x = self.spacing() + \
                wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spacing_y = self.spacing() + \
                wid.style().layoutSpacing(QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            x_next = x + item.sizeHint().width() + spacing_x

            if x_next - spacing_x > rect.right() and line_height > 0:
                x = rect.x()
                y = y + line_height + spacing_y
                x_next = x + item.sizeHint().width() + spacing_y
                line_height = 0

            item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = x_next
            line_height = max(line_height, item.sizeHint().height())

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()

        for item in self._items:
            size.width()
            size = size.expandedTo(item.minimumSize())
        margin, _, _, _ = self.getContentsMargins()

        size += QSize(2 * margin, 2 * margin)
        return size

    def itemAt(self, index):
        if 0 <= index < len(self._items):
            return self._items[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self._items):
            return self._items.pop(index)
        return None

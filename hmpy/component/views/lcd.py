from PyQt5.QtWidgets import QLCDNumber, QWidget
from PyQt5.QtCore import QRect


class LCDView(QWidget):

    def __init__(self, parent=None, num_digits=3):
        super().__init__(parent)
        self.lcd = QLCDNumber(num_digits, self)

    def paintEvent(self, event):
        rect = event.rect()

        # Get drawing size and center
        slider_rect = QRect(rect)
        size = slider_rect.size()

        self.lcd.resize(size)

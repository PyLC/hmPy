from PyQt5.QtWidgets import QWidget, QSlider
from PyQt5.QtCore import Qt, QRect


class SliderView(QWidget):

    def __init__(self, parent=None, min_val=0, max_val=100, step_val=5):
        super().__init__(parent)
        self.slider = QSlider(Qt.Horizontal, self)
        self.slider.setMinimum(min_val)
        self.slider.setMaximum(max_val)
        self.slider.setTickInterval(step_val)
        self.slider.setValue(10)

    @property
    def value(self):
        return self.slider.value()

    def paintEvent(self, event):
        rect = event.rect()

        # Get drawing size and center
        slider_rect = QRect(rect)
        size = slider_rect.size()

        self.slider.resize(size)


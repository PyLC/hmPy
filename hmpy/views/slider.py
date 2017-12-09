"""This module defines the Slider View class."""


from .view import View
from PyQt5.QtWidgets import QSlider,QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

class SliderView(View):
    """The Slider view creates a slider for input.

    :param minimum: minimum int value of slider.
    :param maximum: maximum int value of slider.
    :param interval: distance each tick will travel on slider.
    """
    def __init__(self, minimum=0, maximum=100,interval=1):
        """Initialize the slider view."""

        super().__init__()
        self.slider = QSlider(self)
        self.slider.setMinimum(minimum)
        self.slider.setMaximum(maximum)
        self.slider.setTickInterval(interval)


    @property
    def tick_interval(self):
        return self.slider.tickInterval()

    @tick_interval.setter
    def tick_interval(self,interval):
        if interval <= 0:
            self.slider.setTickInterval(self.slider.tickInterval())
        else:
            self.slider.setTickInterval(interval)

    @property
    def maximum_value(self):
        return self.slider.maximum()

    @maximum_value.setter
    def maximum_value(self,maximum):
        if maximum < 0:
            self.slider.setMaximum(self.slider.maximum())
        else:
            self.slider.setMaximum(maximum)

    @property
    def minimum_value(self):
        return self.slider.minimum()

    @minimum_value.setter
    def minimum_value(self, minimum):
        if minimum >= 0:
            self.slider.setMinimum(minimum)
        else:
            self.slider.setMinimum(0)

    def set_horizontal_orientation(self):
        self.slider.setOrientation(Qt.Horizontal)

    def set_vertical_orientation(self):
        self.slider.setOrientation(Qt.Vertical)

    def on_change(self, callback):
        self.slider.valueChanged.connect(callback)

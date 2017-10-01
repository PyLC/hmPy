"""This module defines the LCDView class."""


import math
from .view import View
from PyQt5.QtWidgets import QLCDNumber


class LCDView(View):
    """The LCD view creates a simple numeric display."""

    def __init__(self, value=0):
        """Initialize the LCDView.

        :param value: The initial value of the display"""
        super().__init__()
        self.lcd = QLCDNumber(self)
        self.value = value

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.lcd.size():
            self.lcd.resize(size)

    @property
    def value(self):
        return self.lcd.value()

    @value.setter
    def value(self, value):
        if value > 0:
            digits = int(math.log10(value)) + 1
        elif value == 0:
            digits = 1
        else:
            digits = int(math.log10(-value)) + 2

        self.lcd.setDigitCount(digits)
        self.lcd.display(value)

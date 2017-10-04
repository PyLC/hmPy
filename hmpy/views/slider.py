"""This module defines the Slider View class."""


from .view import View
from PyQt5.QtWidgets import QSlider,QLabel
from PyQt5.QtCore import Qt

class SliderView(View):
    """The Slider view creates a slider for input."""

    def __init__(self,text,max,min,cur):
        """Initialize the slider view.

        :param text: The text to display on the slider"""
        super().__init__()
        self.slider = QSlider()
        self.slider.setRange(min, max)
        self.slider.setValue(cur)
        self.slider.valueChanged.connect(self.slider_changed)
        self.text = text;


    @property
    def text(self):
        self.slider.text()

    @text.setter
    def text(self, text):
        self.slider.setText(text)


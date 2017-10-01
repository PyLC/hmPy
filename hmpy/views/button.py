"""This module defines the ButtonView class."""


from .view import View
from PyQt5.QtWidgets import QPushButton


class ButtonView(View):
    """The Button view creates a clickable button for triggering actions."""

    def __init__(self, text):
        """Initialize the button view.

        :param text: The text to display on the button"""
        super().__init__()
        self.btn = QPushButton(self)
        self.text = text

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.btn.size():
            self.btn.resize(size)

    @property
    def text(self):
        self.btn.text()

    @text.setter
    def text(self, text):
        self.btn.setText(text)

    def on_click(self, callback):
        self.btn.clicked.connect(callback)

    def on_release(self, callback):
        self.btn.released.connect(callback)

    def on_press(self, callback):
        self.btn.pressed.connect(callback)

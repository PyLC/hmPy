from .view import View
from PyQt5.QtWidgets import QPushButton


class ButtonView(View):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.btn = QPushButton(text, self)

    def paintEvent(self, event):
        size = event.rect().size()
        if size != self.btn.size():
            self.btn.resize(size)

    def on_click(self, callback):
        self.btn.clicked.connect(callback)

    def on_release(self, callback):
        self.btn.released.connect(callback)

    def on_press(self, callback):
        self.btn.pressed.connect(callback)
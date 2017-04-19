from PyQt5.QtWidgets import QWidget, QPushButton


class ButtonView(QWidget):

    def __init__(self, text="Button", parent=None):
        """Initialize the ButtonView QWidget.

        :param text: The button text.  Defaults to 'Button'.
        :param parent: The parent QWidget."""
        super().__init__(parent)
        self.button = QPushButton(text, self)

    def paintEvent(self, event):
        """Resize the button to match the widget size.

        :param event: The paint event.
        """
        size = event.rect().size()
        if size != self.button.size():
            self.button.resize(size)

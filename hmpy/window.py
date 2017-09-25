from PyQt5.QtWidgets import QMainWindow, QWidget
from .layout import InterfaceLayout


class InterfaceWindow(QMainWindow):
    """The main window QWidget of the Interface"""

    def __init__(self):
        """Initialize the InterfaceWindow"""
        super().__init__()
        self._root = QWidget()
        self._layout = InterfaceLayout()
        self._root.setLayout(self._layout)
        self.setCentralWidget(self._root)

    def add_view(self, view):
        """Add a view to the Interface window

        :param view: The view to be added to the Interface
        """
        self._layout.addWidget(view)

from PyQt5.QtWidgets import QApplication
from .window import InterfaceWindow


class Interface:
    """The base Interface"""

    def __init__(self):
        """Initialize the Interface

        :raise Exception: When another Interface already exists"""
        # TODO - Fix single interface limitation
        if QApplication.instance() is not None:
            raise Exception("No more than 1 instance of Interface can exist")

        self._app = QApplication([])
        self._app.setStyle('Fusion')
        self._root = InterfaceWindow()

    def start(self):
        """Launch the GUI"""
        self._root.showMaximized()
        self._app.exec_()

    def add_view(self, view):
        """Add a view to the Interface

        :param view: The view to be added to the Interface"""
        self._root.add_view(view)

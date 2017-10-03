from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer

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
        self._timers = []

    def start(self):
        """Launch the GUI"""
        self._root.showMaximized()
        self._app.exec_()

    def after(self, delay, action):
        """Schedule an action to be executed some time in the future.

        :param delay: Time to wait (in milliseconds)
        :param action: The function to execute"""
        timer = QTimer()
        timer.timeout.connect(action)
        timer.setInterval(delay)
        timer.setSingleShot(True)
        timer.start()
        self._timers.append(timer)

    def every(self, interval, action):
        """Schedule an action to be executed at a set interval.

        :param interval: The execution interval (in milliseconds)
        :param action: The function to execute"""
        timer = QTimer()
        timer.timeout.connect(action)
        timer.setInterval(interval)
        timer.start()
        self._timers.append(timer)

    def add_view(self, view):
        """Add a view to the Interface

        :param view: The view to be added to the Interface"""
        self._root.add_view(view)

    def quit(self):
        """Close the Interface"""
        self._app.quit()

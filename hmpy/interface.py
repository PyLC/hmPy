from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from hmpy.util.timer import Timer
from hmpy.window import InterfaceWindow
import os


ICON_PATH = os.path.dirname(os.path.realpath(__file__)) + os.sep + 'res' + os.sep + 'icon.png'


class Interface:
    """The base Interface"""

    def __init__(self, title='hmPy'):
        """Initialize the Interface

        :raise Exception: When another Interface already exists"""
        # TODO - Fix single interface limitation
        if QApplication.instance() is not None:
            raise Exception("No more than 1 instance of Interface can exist")

        self._app = QApplication([])
        self._app.setStyle('Fusion')
        self._app.setWindowIcon(QIcon(ICON_PATH))
        self._root = InterfaceWindow()
        self._root.setWindowTitle(title)
        self._windowState = Qt.WindowMaximized
        self._timers = []

    def set_size(self, width, height):
        """Set the window size

        :param width: window width
        :param height: window height"""
        self._windowState = Qt.WindowNoState
        self._root.setMinimumWidth(width)
        self._root.setMinimumHeight(height)
        self._root.setWindowState(self._windowState)

    def start(self):
        """Launch the GUI"""
        if self._windowState == Qt.WindowMaximized:
            self._root.showMaximized()
        else:
            self._root.show()

        self._app.exec_()

    def after(self, delay, action):
        """Schedule an action to be executed some time in the future.

        :param delay: Time to wait (in milliseconds)
        :param action: The function to execute"""
        timer = Timer(delay, action, False)
        timer.start()
        self._timers.append(timer)
        return timer

    def every(self, interval, action):
        """Schedule an action to be executed at a set interval.

        :param interval: The execution interval (in milliseconds)
        :param action: The function to execute"""
        timer = Timer(interval, action)
        timer.start()
        self._timers.append(timer)
        return timer

    def add_view(self, view):
        """Add a view to the Interface

        :param view: The view to be added to the Interface"""
        self._root.add_view(view)

    def set_title(self, title):
        """ Set the InterfaceWindow title

        :param title: The new window title"""
        self._root.setWindowTitle(title)

    def quit(self):
        """Close the Interface"""
        self._app.quit()

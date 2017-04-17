from PyQt5.QtWidgets import QMainWindow
from hmpy.gui.dashboard import ComponentDashboard
from hmpy.gui.menus.file import FileMenu
from hmpy.gui.menus.config import ConfigureMenu
from hmpy.connection.manager import ConnectionManager
from hmpy.component.manager import ComponentManager


class MainWindow(QMainWindow):
    """The main window for hmpy."""

    def __init__(self):
        """Initialize the MainWindow."""
        super().__init__()
        self.connection_manager = ConnectionManager()
        self.component_manager = ComponentManager()
        self.init_ui()

    def init_ui(self):
        """Initialize the MainWindow widget ui."""
        self.setWindowTitle("hmPy")
        self.init_menu()
        self.setCentralWidget(ComponentDashboard(self))
        self.showMaximized()

    def init_menu(self):
        """Initialize and populate the QMenuBar."""
        menu_bar = self.menuBar()
        menu_bar.addMenu(FileMenu(self))
        menu_bar.addMenu(ConfigureMenu(self))


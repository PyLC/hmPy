from PyQt5.QtWidgets import QMenu, QAction, qApp


class FileMenu(QMenu):
    """File QMenu for hmpy."""

    def __init__(self, parent=None):
        """Initialize and populate FileMenu.

        :param parent: The parent QMenuBar. Defaults to None
        """
        super().__init__("&File", parent)
        self.__actions = []
        self.set_actions()
        for action in self.__actions:
            self.addAction(action)

    def set_actions(self):
        """Initialize all QActions for the FileMenu. Populate __actions."""
        exit_action = QAction('&Quit', self)
        exit_action.triggered.connect(qApp.quit)

        self.__actions.append(exit_action)
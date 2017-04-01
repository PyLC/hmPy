from PyQt5.QtWidgets import QMenu, QAction
from hmpy.gui.dialogs.config_plcs import ConfigurePLCsDialog


class ConfigureMenu(QMenu):
    """Configuration QMenu for hmpy."""

    def __init__(self, parent=None):
        """Initialize and populate ConfigureMenu.

        :param parent: The parent QMenuBar. Defaults to None
        """
        super(ConfigureMenu, self).__init__("&Configure", parent)
        self.__actions = []
        self.set_actions()
        for action in self.__actions:
            self.addAction(action)

    def set_actions(self):
        """Initialize all QActions for the ConfigureMenu. Populate __actions"""
        plcs_action = QAction("&PLCs", self)
        plcs_action.triggered.connect(ConfigurePLCsDialog(self).exec_)

        self.__actions.append(plcs_action)

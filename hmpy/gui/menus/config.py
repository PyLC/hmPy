from PyQt5.QtWidgets import QMenu, QAction
from hmpy.gui.dialogs.config_plcs import ConfigurePLCsDialog
from hmpy.gui.dialogs.config_components import ConfigureComponentsDialog


class ConfigureMenu(QMenu):
    """Configuration QMenu for hmpy."""

    def __init__(self, parent=None):
        """Initialize and populate ConfigureMenu.

        :param parent: The parent QMenuBar. Defaults to None
        """
        super().__init__("&Configure", parent)
        self.gui = parent
        self.__actions = []
        self.set_actions()
        for action in self.__actions:
            self.addAction(action)

    def set_actions(self):
        """Initialize all QActions for the ConfigureMenu. Populate __actions"""
        plcs_action = QAction("&PLCs", self)
        plcs_action.triggered.connect(ConfigurePLCsDialog(self.gui).exec_)

        components_action = QAction("&Components", self)
        components_action.triggered.connect(ConfigureComponentsDialog(self.gui).exec_)

        self.__actions.append(plcs_action)
        self.__actions.append(components_action)

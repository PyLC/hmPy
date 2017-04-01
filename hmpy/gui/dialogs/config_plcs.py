from PyQt5.QtWidgets import QDialog


class ConfigurePLCsDialog(QDialog):
    """QDialog for managing/configuring PLCs"""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super(ConfigurePLCsDialog, self).__init__(parent)

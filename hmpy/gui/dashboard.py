from PyQt5.QtWidgets import QWidget, QGridLayout


class ComponentDashboard(QWidget):
    """Dashboard QWidget, displays all of the Components"""

    def __init__(self, parent=None):
        """Initialize the dashboard QWidget

        :param parent: The parent QWidget. Defaults to None.
        """
        super().__init__(parent)

        grid = QGridLayout()
        self.setLayout(grid)

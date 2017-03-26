from PyQt5.QtWidgets import QWidget, QGridLayout


class ComponentDashboard(QWidget):
    """Dashboard QWidget, displays all of the Components"""

    def __init__(self, parent=None):
        """Initialize the dashboard QWidget

        Args:
            parent: The parent QWidget. Defaults to None.
        """
        super(ComponentDashboard, self).__init__(parent)

        grid = QGridLayout()
        self.setLayout(grid)

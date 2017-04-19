from PyQt5.QtWidgets import QWidget, QGridLayout


class ComponentDashboard(QWidget):
    """Dashboard QWidget, displays all of the Components"""

    MIN_COMPONENT_SIZE = 250
    """Minimum height/width of a component (in pixels)."""

    def __init__(self, parent=None):
        """Initialize the dashboard QWidget

        :param parent: The parent QWidget. Defaults to None.
        """
        super().__init__(parent)
        self.gui = parent
        self.gui.component_manager.components_changed.connect(self.on_component_changed)
        self.grid = QGridLayout()
        self.setLayout(self.grid)

    def on_component_changed(self):
        """Redraw/rearrange the dashboard when components are added or removed."""
        components = list(self.gui.component_manager.get_components().values())
        comp_count = len(components)

        # Calculate col/row count given the minimum component size and the window size
        width = self.gui.frameGeometry().width()
        height = self.gui.frameGeometry().height()
        cols = width // self.MIN_COMPONENT_SIZE
        rows = height // self.MIN_COMPONENT_SIZE

        # Add component widgets
        for i in range(0, comp_count):
            r = i // 4
            c = i % 4
            # Remove item from cell if exists
            cell = self.grid.itemAt(i)
            if cell is not None:
                self.grid.removeItem(cell)
            # Add widget view
            self.grid.addWidget(components[r * 10 + c].view, r, c)

        # Fill empty cells with empty widgets
        for r in range(comp_count // 4, rows):
            for c in range(comp_count % 4, cols):
                self.grid.addWidget(QWidget(), r, c)

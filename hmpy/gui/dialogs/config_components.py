from PyQt5.QtWidgets import QDialog, QTreeWidget, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt


class ConfigureComponentsDialog(QDialog):

    """QDialog for managing/configuring Components"""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super().__init__(parent)
        self.gui = parent
        self.init_ui()

    def init_ui(self):
        """Initialize and populate the Configure Components dialog"""

        # create main display tree widget
        self.component_display = QTreeWidget()
        self.component_display.setObjectName("component_display")
        self.component_display.currentItemChanged.connect(self.selection_changed)

        # Set component display list to show appropriate information
        self.component_display.headerItem().setText(0, "Name")
        self.component_display.headerItem().setText(1, "Type")
        self.component_display.setMinimumSize(self.get_component_display_width(), 150)

        # create add button
        self.btn_add = QPushButton("Add")
        self.btn_add.setObjectName("btn_add")

        # create modify button
        self.btn_modify = QPushButton("Modify")
        self.btn_modify.setObjectName("btn_modify")
        self.btn_modify.setEnabled(False)

        # create remove button
        self.btn_remove = QPushButton("Remove")
        self.btn_remove.setObjectName("btn_remove")
        self.btn_remove.setEnabled(False)

        # create back button
        self.btn_back = QPushButton("Back")
        self.btn_back.setObjectName("btn_back")
        self.btn_back.clicked.connect(self.accept)

        # create vertical button box
        self.vertical_btns = QVBoxLayout()
        self.vertical_btns.setObjectName("vertical_btns")

        # populate vertical button box
        self.vertical_btns.addWidget(self.btn_add, alignment=Qt.AlignCenter)
        self.vertical_btns.addWidget(self.btn_modify, alignment=Qt.AlignCenter)
        self.vertical_btns.addWidget(self.btn_remove, alignment=Qt.AlignCenter)
        self.vertical_btns.addStretch()
        self.vertical_btns.addWidget(self.btn_back, alignment=Qt.AlignCenter)

        # Create/populate main layout
        self.main_layout = QHBoxLayout()
        self.main_layout.addWidget(self.component_display)
        self.main_layout.addLayout(self.vertical_btns)

        # set window properties
        self.setObjectName("component_config")
        self.setWindowTitle("Configure Components")
        self.setLayout(self.main_layout)

    def get_component_display_width(self):
        """Calculate the minimum width of the component_display.

        :return: Sum of the section sizes."""
        col_count = self.component_display.columnCount()
        section_sizes = list(map(lambda i: self.component_display.header().sectionSize(i), range(0, col_count)))
        return sum(section_sizes)

    def selection_changed(self, current, previous):
        """Enable/disable buttons based on component_display selection"""
        if current is None:
            self.btn_remove.setEnabled(False)
            self.btn_modify.setEnabled(False)
        elif previous is None:
            self.btn_modify.setEnabled(True)
            self.btn_remove.setEnabled(True)


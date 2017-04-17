from PyQt5.QtWidgets import QDialog,  QTreeWidget, QTreeWidgetItem, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt
from hmpy.gui.dialogs.add_plc import AddPLCDialog


class ConfigurePLCsDialog(QDialog):

    """QDialog for managing/configuring PLCs"""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super().__init__(parent)
        self.gui = parent
        self.gui.connection_manager.connections_changed.connect(self.connections_changed)
        self.init_ui()

    def init_ui(self):
        """Initialize and populate the Configure PLCs dialog"""

        # create main display tree widget
        self.plc_display = QTreeWidget()
        self.plc_display.setObjectName("plc_display")

        # Set plc display list to show appropriate information
        self.plc_display.headerItem().setText(0,"Name")
        self.plc_display.headerItem().setText(1, "Address")
        self.plc_display.headerItem().setText(2, "Port")
        self.plc_display.headerItem().setText(3, "Connection Type")
        self.plc_display.headerItem().setText(4, "Status")
        self.plc_display.currentItemChanged.connect(self.selection_changed)
        self.plc_display.setMinimumSize(self.get_plc_display_width(), 150)

        # create add button
        self.btn_add = QPushButton("Add")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(self.on_add)

        # create modify button
        self.btn_modify = QPushButton("Modify")
        self.btn_modify.setObjectName("btn_modify")
        self.btn_modify.setEnabled(False)

        # create remove button
        self.btn_remove = QPushButton("Remove")
        self.btn_remove.setObjectName("btn_remove")
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self.on_remove)

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
        self.main_layout.addWidget(self.plc_display)
        self.main_layout.addLayout(self.vertical_btns)

        # set window properties
        self.setObjectName("plc_config")
        self.setWindowTitle("Configure PLCs")
        self.setLayout(self.main_layout)

    def get_plc_display_width(self):
        """Calculate the minimum width of the plc_display.

        :return: Sum of the section sizes."""
        col_count = self.plc_display.columnCount()
        section_sizes = list(map(lambda i: self.plc_display.header().sectionSize(i), range(0, col_count)))
        return sum(section_sizes)

    def selection_changed(self, current, previous):
        """Enable/disable buttons based on plc_display selection"""
        if current is None:
            self.btn_remove.setEnabled(False)
            self.btn_modify.setEnabled(False)
        elif previous is None:
            self.btn_modify.setEnabled(True)
            self.btn_remove.setEnabled(True)

    def on_add(self):
        """Open an AddPLCDialog."""
        AddPLCDialog(self.gui).exec_()

    def on_remove(self):
        """Remove the selected connection."""
        selected = self.plc_display.currentItem()
        name = selected.text(0)

        conf_dialog = QMessageBox()
        conf_dialog.setText("Are you sure you want to remove %s?" % name)
        conf_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        conf_result = conf_dialog.exec_()
        if not conf_result == QMessageBox.Yes:
            return

        self.gui.connection_manager.destroy(name)

    def connections_changed(self):
        """Repopulate the plc_display, triggered by the connection managers connections_changed signal."""
        connections = self.gui.connection_manager.get_connections()
        self.plc_display.clear()
        for key, con in connections.items():
            self.plc_display.addTopLevelItem(QTreeWidgetItem([key, con.get_address(), con.get_port(), type(con).__name__, 'Connected' if con.connected else 'Disconnected']))

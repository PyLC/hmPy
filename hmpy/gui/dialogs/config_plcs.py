from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidget, QTreeWidgetItem, QGridLayout, QVBoxLayout, \
    QPushButton, QMessageBox, QHeaderView
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

        # set object name for future reference
        self.setObjectName("ComponentConfig")

        # create grid layout
        grid = QGridLayout()
        grid.setSpacing(10)

        # create button box for ok and cancel buttons
        self.ok_btn_box = QDialogButtonBox()
        self.ok_btn_box.setOrientation(Qt.Horizontal)
        self.ok_btn_box.setStandardButtons(QDialogButtonBox.Ok)
        self.ok_btn_box.setObjectName("ok_btn")

        # create main display ie tree widget
        self.plc_display = QTreeWidget()
        self.plc_display.setObjectName("plc_display")

        # Set plc display list to show appropriate information
        self.plc_display.headerItem().setText(0,"Name")
        self.plc_display.headerItem().setText(1, "Address")
        self.plc_display.headerItem().setText(2, "Port")
        self.plc_display.headerItem().setText(3, "Connection Type")
        self.plc_display.headerItem().setText(4, "Status")
        self.plc_display.setMinimumSize(500, 150)
        self.plc_display.currentItemChanged.connect(self.selection_changed)

        # create add button
        self.btn_add = QPushButton()
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setText("Add")
        self.btn_add.clicked.connect(self.on_add)

        # create modify button
        self.btn_modify = QPushButton()
        self.btn_modify.setObjectName("btn_modify")
        self.btn_modify.setText("Modify")
        self.btn_modify.setEnabled(False)

        # create remove button
        self.btn_remove = QPushButton()
        self.btn_remove.setObjectName("btn_remove")
        self.btn_remove.setText("Remove")
        self.btn_remove.setEnabled(False)
        self.btn_remove.clicked.connect(self.on_remove)

        # create vertical button box
        self.vertical_btns = QVBoxLayout()
        self.vertical_btns.setContentsMargins(10, 10, 10, 10)
        self.vertical_btns.setSpacing(10)
        self.vertical_btns.setObjectName("vertical_btns")

        # populate vertical button box
        self.vertical_btns.addWidget(self.btn_add, alignment=Qt.AlignCenter)
        self.vertical_btns.addWidget(self.btn_modify, alignment=Qt.AlignCenter)
        self.vertical_btns.addWidget(self.btn_remove, alignment=Qt.AlignCenter)
        self.vertical_btns.addStretch()

        # set layout for components in grid layout
        grid.addWidget(self.plc_display, 0, 0)
        grid.addWidget(self.ok_btn_box, 1, 0)
        grid.addItem(self.vertical_btns, 0, 1)

        # set button actions for cancel and ok buttons
        self.ok_btn_box.accepted.connect(self.accept)

        # set window properties
        self.setWindowTitle("Configure PLC's")
        self.setLayout(grid)

    def selection_changed(self, current, previous):
        """Enable/disable buttons based on plc_view selection"""
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
        """Repopulate the plc_view, triggered by the connection managers connections_changed signal."""
        connections = self.gui.connection_manager.get_connections()
        self.plc_display.clear()
        for key, con in connections.items():
            self.plc_display.addTopLevelItem(QTreeWidgetItem([key, con.get_address(), con.get_port(), type(con).__name__, 'Connected' if con.connected else 'Disconnected']))

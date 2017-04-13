from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QTreeWidget, QGridLayout, QVBoxLayout, QPushButton


class ConfigurePLCsDialog(QDialog):

    """QDialog for managing/configuring PLCs"""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super().__init__(parent)
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

        # Set plc display list to show approprate information
        self.plc_display.headerItem().setText(0,"Name")
        self.plc_display.headerItem().setText(1, "Address")
        self.plc_display.headerItem().setText(2, "Port")
        self.plc_display.headerItem().setText(3, "Connection Type")
        self.plc_display.headerItem().setText(4, "Status")
        self.plc_display.setMinimumSize(500,150)

        # create add button
        self.btn_add = QPushButton()
        self.btn_add.setObjectName("btn_add")
        self.btn_add.setText("Add")

        # create modify button
        self.btn_modify = QPushButton()
        self.btn_modify.setObjectName("btn_modify")
        self.btn_modify.setText("Modify")

        # create remove button
        self.btn_remove = QPushButton()
        self.btn_remove.setObjectName("btn_remove")
        self.btn_remove.setText("Remove")

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

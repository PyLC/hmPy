from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QDialogButtonBox, QComboBox, QLabel


class AddPLCDialog(QDialog):
    """QDialog for adding a PLC"""


    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QDialog. Defaults to None
        """
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """Initialize and populate add PLC dialog"""

        # Create button box
        self.buttonBox = QDialogButtonBox()
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        # Create label for name textbox
        self.name_textbox_label = QLabel("PLC name: ")
        self.name_textbox_label.setObjectName("name_textbox_label")

        # Create name textbox
        self.name_textbox = QLineEdit()
        self.name_textbox.setObjectName("name_textbox")

        # Create label for address textbox
        self.address_textbox_label = QLabel("Address: ")
        self.address_textbox_label.setObjectName("address_textbox_label")

        # Create address textbox
        self.address_textbox = QLineEdit()
        self.address_textbox.setObjectName("address_textbox")

        # Create label for port textbox
        self.port_textbox_label = QLabel("Port: ")
        self.port_textbox_label.setObjectName("port_textbox_label")

        # Create port textbox
        self.port_textbox = QLineEdit()
        self.port_textbox.setObjectName("port_textbox")

        # Create label for connection type list
        self.connection_list_textbox_label = QLabel("Connection: ")
        self.connection_list_textbox_label.setObjectName("connection_list_textbox_label")

        # Create connection type list
        self.connection_type_combobox = QComboBox()
        self.connection_type_combobox.setObjectName("connection_type_combobox")

        # set layout and spacing of dialog
        grid = QGridLayout()
        grid.setSpacing(10)

        # set name textbox position
        grid.addWidget(self.name_textbox_label,1,0)
        grid.addWidget(self.name_textbox, 1, 1)

        # set address textbox position
        grid.addWidget(self.address_textbox_label, 2, 0)
        grid.addWidget(self.address_textbox, 2, 1)

        # set port position
        grid.addWidget(self.port_textbox_label, 3, 0)
        grid.addWidget(self.port_textbox, 3, 1)

        # set connection list drop down menu position
        grid.addWidget(self.connection_list_textbox_label, 4, 0)
        grid.addWidget(self.connection_type_combobox, 4, 1)

        # set button position
        grid.addWidget(self.buttonBox, 5,1)

        # set window properties
        self.setWindowTitle("Add PLC")
        self.setLayout(grid)
        self.setFixedSize(self.sizeHint())




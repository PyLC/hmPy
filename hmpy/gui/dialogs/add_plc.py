from PyQt5.QtWidgets import QDialog, QGridLayout, QLineEdit, QDialogButtonBox, QMessageBox, QComboBox, QLabel
from PyQt5.QtGui import QRegExpValidator, QIntValidator
from PyQt5.QtCore import QRegExp
from hmpy.connection import get_connection_types


class AddPLCDialog(QDialog):
    """QDialog for adding a PLC"""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QDialog. Defaults to None
        """
        super().__init__(parent)
        self.gui = parent
        self.connection_types = get_connection_types()
        self.init_ui()
        self.exec_()

    def init_ui(self):
        """Initialize and populate add PLC dialog"""

        # Create button box
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.button_box.setObjectName("button_box")

        # Connect button box signals to actions
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Create label for name textbox
        self.name_textbox_label = QLabel("PLC name: ")
        self.name_textbox_label.setObjectName("name_textbox_label")

        # Create name textbox
        self.name_textbox = QLineEdit()
        self.name_textbox.setObjectName("name_textbox")

        # Create label for address textbox
        self.address_textbox_label = QLabel("Address: ")
        self.address_textbox_label.setObjectName("address_textbox_label")

        # Create validator for address textbox
        rx = QRegExp("^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])|localhost$|")
        self.address_textbox_validator = QRegExpValidator(rx)

        # Create address textbox, set validator
        self.address_textbox = QLineEdit()
        self.address_textbox.setObjectName("address_textbox")
        self.address_textbox.setValidator(self.address_textbox_validator)

        # Create label for port textbox
        self.port_textbox_label = QLabel("Port: ")
        self.port_textbox_label.setObjectName("port_textbox_label")

        # Create validator for port textbox
        self.port_textbox_validator = QIntValidator(0, 65535)

        # Create port textbox, set validator
        self.port_textbox = QLineEdit()
        self.port_textbox.setObjectName("port_textbox")
        self.port_textbox.setValidator(self.port_textbox_validator)

        # Create label for connection type list
        self.connection_list_textbox_label = QLabel("Connection: ")
        self.connection_list_textbox_label.setObjectName("connection_list_textbox_label")

        # Create and populate connection type list
        self.connection_type_combobox = QComboBox()
        self.connection_type_combobox.setObjectName("connection_type_combobox")
        self.connection_type_combobox.addItems(self.connection_types.keys())

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
        grid.addWidget(self.button_box, 5,1)

        # set window properties
        self.setWindowTitle("Add PLC")
        self.setLayout(grid)
        self.setFixedSize(self.sizeHint())

    def accept(self):
        """Ok clicked, process form"""
        if self.add_plc():
            QDialog.accept(self)

    def reject(self):
        """Cancel clicked, close dialog"""
        QDialog.reject(self)

    def add_plc(self):
        """"Create a new PLC based on the provided input

        :return: boolean indicating the result of the operation
        """

        # Fetch values form form inputs
        name = self.name_textbox.text().strip()
        address = self.address_textbox.text().strip()
        port = self.port_textbox.text().strip()
        connection_type = self.connection_types[self.connection_type_combobox.currentText()]

        # Validate input values
        if not name:
            return self.input_error("The name field cannot be empty")
        if not address or self.address_textbox_validator.validate(address, 0)[0] != QRegExpValidator.Acceptable:
            return self.input_error("Please input a valid IP address")
        if not port or self.port_textbox_validator.validate(port, 0)[0] != QIntValidator.Acceptable:
            return self.input_error("Please input a valid port")

        # Check for an existing connection with the same name
        if self.gui.connection_manager.has_connection(name):
            return self.input_error("A PLC named %s already exists" % name)

        self.gui.connection_manager.add(name, address, port, connection_type)
        return True

    def input_error(self, msg):
        """Display an error message in a dialog.

        :param msg: string containing the error message.
        :return: False
        """
        msg_box = QMessageBox()
        msg_box.setText(msg)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDefaultButton(QMessageBox.Ok)
        msg_box.setWindowTitle("Error")
        msg_box.exec_()

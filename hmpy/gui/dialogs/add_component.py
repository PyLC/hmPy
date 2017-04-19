from PyQt5.QtWidgets import QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox, \
    QMessageBox
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import Qt
from hmpy.component.types import get_component_types
from hmpy.connection import RegisterTypes


class AddComponentDialog(QDialog):
    """QDialog for adding a component."""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super().__init__(parent)
        self.gui = parent
        self.static_rows = 0
        self.inputs = dict()
        self.outputs = dict()
        self.connections = self.gui.connection_manager.get_connections()
        self.component_types = get_component_types()

        if len(self.component_types) == 0:
            self.input_error("No valid component types found!")
        elif len(self.connections) == 0:
            self.input_error("You must create a PLC before you can create a component")
        else:
            self.init_ui()
            # Invoke manually to initialize first component
            self.on_type_changed()
            self.exec_()

    def init_ui(self):
        """Initialize the dialogs ui."""

        # Create form layout
        self.form_layout = QFormLayout()
        self.form_layout.setObjectName("form_layout")

        # Create name field
        self.txt_name = QLineEdit()
        self.txt_name.setObjectName("txt_name")
        self.add_row("Name", self.txt_name)

        # Create component type field

        self.cmb_component_type = QComboBox()
        self.cmb_component_type.setObjectName("cmb_component_type")
        self.cmb_component_type.addItems(self.component_types.keys())
        self.cmb_component_type.currentIndexChanged.connect(self.on_type_changed)
        self.add_row("Type", self.cmb_component_type)

        # Set the number of static rows in the form
        self.static_rows = self.form_layout.rowCount()

        # Create dialog button box
        self.btn_box_ok_cancel = QDialogButtonBox()
        self.btn_box_ok_cancel.setOrientation(Qt.Horizontal)
        self.btn_box_ok_cancel.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.btn_box_ok_cancel.setObjectName("btn_box_ok_cancel")

        # Connect button box signals to actions
        self.btn_box_ok_cancel.accepted.connect(self.accept)
        self.btn_box_ok_cancel.rejected.connect(self.reject)

        # Create and populate main dialog layout
        self.main_layout = QVBoxLayout()
        self.main_layout.setObjectName("main_layout")
        self.main_layout.addLayout(self.form_layout)
        self.main_layout.addWidget(self.btn_box_ok_cancel)

        # set window properties
        self.setObjectName("dialog_add_component")
        self.setWindowTitle("Add Component")
        self.setLayout(self.main_layout)
        self.resize(self.sizeHint())

    def accept(self):
        """Ok clicked, process form."""
        if self.add_component():
            QDialog.accept(self)

    def reject(self):
        """"Close dialog."""
        QDialog.reject(self)

    def on_type_changed(self):
        """Regenerate the i/o fields for the selected Component type."""
        for row in range(self.static_rows * 2, self.form_layout.rowCount() * 2):
            self.form_layout.removeRow(self.static_rows * 2)

        cls = self.component_types[self.cmb_component_type.currentText()]

        self.inputs = dict()
        self.outputs = dict()
        if len(cls.input_names) != 0:
            self.add_row("Inputs")
        for name in cls.input_names:
            self.inputs[name] = {
                "name": self.add_row("Name", QLineEdit()),
                "interval": self.add_row("Interval", QLineEdit()),
                "register_type": self.add_row("Register", QComboBox()),
                "address": self.add_row("Address", QLineEdit()),
                "connection": self.add_row("Connection", QComboBox())
            }

            self.inputs[name]['name'].setText(name)
            self.inputs[name]['name'].setEnabled(False)
            i_validator = QIntValidator()
            i_validator.setBottom(1)
            self.inputs[name]['interval'].setValidator(i_validator)
            a_validator = QIntValidator()
            a_validator.setBottom(0)
            self.inputs[name]['address'].setValidator(a_validator)
            self.inputs[name]['register_type'].addItems(RegisterTypes.__members__.keys())
            self.inputs[name]['connection'].addItems(self.connections.keys())

        if len(cls.output_names) != 0:
            self.add_row("Outputs")
        for name in cls.output_names:
            self.outputs[name] = {
                "name": self.add_row("Name", QLineEdit()),
                "address": self.add_row("Address", QLineEdit()),
                "connection": self.add_row("Connection", QComboBox())
            }

            self.outputs[name]['name'].setText(name)
            self.outputs[name]['name'].setEnabled(False)
            a_validator = QIntValidator()
            a_validator.setBottom(0)
            self.outputs[name]['address'].setValidator(a_validator)
            self.outputs[name]['connection'].addItems(self.connections.keys())

    def add_component(self):
        """Create a new Component based on the input values.

        :return: boolean indicating the result of the operation
        """

        name = self.txt_name.text().strip()
        component_type = self.component_types[self.cmb_component_type.currentText()]

        if not name:
            return self.input_error("The name field cannot be empty")

        # Check for existing component with same name
        if self.gui.component_manager.has_component(name):
            return self.input_error("A component named %s already exists" % name)

        config = dict(inputs=dict(), outputs=dict())

        # Validate/construct io config
        for key, obj in self.inputs.items():
            # Validate numeric input fields
            if not obj['interval'].text().strip():
                return self.input_error("The interval field for input '%s' must not be empty" % key)
            if not obj['address'].text().strip():
                return self.input_error("The address field for input '%s' must not be empty" % key)

            config['inputs'][key] = dict()
            config['inputs'][key]['interval'] = int(obj['interval'].text().strip())
            config['inputs'][key]['address'] = int(obj["address"].text().strip())
            config['inputs'][key]['register_type'] = RegisterTypes[obj["register_type"].currentText()]
            config['inputs'][key]['connection'] = self.gui.connection_manager.get_connection(obj["connection"].currentText())

        for key, obj in self.outputs.items():
            # Validate address field
            if not obj['address'].text().strip():
                return self.input_error("The address field for output '%s' must not be empty" % key)
            config['outputs'][key] = dict()
            config['outputs'][key]['address'] = int(obj["address"].text().strip())
            config['outputs'][key]['connection'] = self.gui.connection_manager.get_connection(obj["connection"].currentText())

        self.gui.component_manager.add(name, component_type, config)
        return True

    def add_row(self, label, field=None):
        """Adds a label/field to the next row in the form.

        :param label: Label text for row
        :param field: Input field element for row. Defaults to None.
        :return: The form field, used for chaining.
        """
        row = self.form_layout.rowCount()
        self.form_layout.setWidget(row, QFormLayout.LabelRole, QLabel(label))
        if field is not None:
            self.form_layout.setWidget(row, QFormLayout.FieldRole, field)
        return field

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

from PyQt5.QtWidgets import QDialog, QFormLayout, QVBoxLayout, QLabel, QLineEdit, QComboBox, QDialogButtonBox
from PyQt5.QtCore import Qt


class AddComponentDialog(QDialog):
    """QDialog for adding a component."""

    def __init__(self, parent=None):
        """Initialize and populate the QDialog

        :param parent: The parent QWidget. Defaults to None
        """
        super().__init__(parent)
        self.form_row = 0
        self.static_rows = 0
        self.init_ui()

    def init_ui(self):
        """Initialize the dialogs ui."""

        # Create form layout
        self.form_layout = QFormLayout()
        self.form_layout.setObjectName("form_layout")

        # Create name field
        self.lbl_name = QLabel()
        self.lbl_name.setObjectName("lbl_name")
        self.lbl_name.setText("Name")
        self.txt_name = QLineEdit()
        self.txt_name.setObjectName("txt_name")
        self.add_row(self.lbl_name, self.txt_name)

        # Create component type field
        self.lbl_component_type = QLabel()
        self.lbl_component_type.setObjectName("lbl_component_type")
        self.lbl_component_type.setText("Component Type")
        self.cmb_component_type = QComboBox()
        self.cmb_component_type.setObjectName("cmb_component_type")
        self.add_row(self.lbl_component_type, self.cmb_component_type)

        # Set the number of static rows in the form
        self.static_rows = self.form_row

        # Create dialog button box
        self.btn_box_ok_cancel = QDialogButtonBox()
        self.btn_box_ok_cancel.setOrientation(Qt.Horizontal)
        self.btn_box_ok_cancel.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
        self.btn_box_ok_cancel.setObjectName("btn_box_ok_cancel")

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

    def add_row(self, label, field=None):
        """Adds a label/field to the next row in the form.

        :param label: Label element for row.
        :param field: Input field element for row. Defaults to None.
        """
        self.form_layout.setWidget(self.form_row, QFormLayout.LabelRole, label)
        if field is not None:
            self.form_layout.setWidget(self.form_row, QFormLayout.FieldRole, field)
        self.form_row += 1

from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QVBoxLayout, QPushButton


class StudentDialog(QDialog):
    def __init__(self, parent=None):
        super(StudentDialog, self).__init__(parent)

        self.layout = QVBoxLayout(self)

        # Create form layout
        self.formLayout = QFormLayout()

        # Create and add line edits with placeholder text to the form layout
        self.sidLineEdit = QLineEdit(self)
        self.sidLineEdit.setPlaceholderText("Enter Student ID")
        self.formLayout.addRow("SID: ", self.sidLineEdit)

        self.firstNameLineEdit = QLineEdit(self)
        self.firstNameLineEdit.setPlaceholderText("Enter First Name")
        self.formLayout.addRow("First Name: ", self.firstNameLineEdit)

        self.lastNameLineEdit = QLineEdit(self)
        self.lastNameLineEdit.setPlaceholderText("Enter Last Name")
        self.formLayout.addRow("Last Name: ", self.lastNameLineEdit)

        self.emailLineEdit = QLineEdit(self)
        self.emailLineEdit.setPlaceholderText("Enter Email")
        self.formLayout.addRow("Email: ", self.emailLineEdit)

        # Add form layout to the dialog layout
        self.layout.addLayout(self.formLayout)

        # Create and add a button to the dialog layout
        self.button = QPushButton("Add Student", self)
        self.button.clicked.connect(self.accept)
        self.layout.addWidget(self.button)

    def getDetails(self):
        return [
            self.sidLineEdit.text(),
            self.firstNameLineEdit.text(),
            self.lastNameLineEdit.text(),
            self.emailLineEdit.text()
        ]

from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt



class LoginDialog(QDialog):
    def __init__(self):
        super(LoginDialog, self).__init__()

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Usuario")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Senha")
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout = QFormLayout()
        form_layout.addRow("Usuario:", self.username_entry)
        form_layout.addRow("Senha:", self.password_entry)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def get_username_password(self):
        return self.username_entry.text(), self.password_entry.text()
    

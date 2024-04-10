from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
from database import mysql_connection


class RegisterDialog(QDialog):
    def __init__(self, host, user, passwd, database=None):
        super(RegisterDialog, self).__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()

        self.setWindowTitle("Registro")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Usuário")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Senha")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.email_entry = QLineEdit(self)
        self.email_entry.setPlaceholderText("Email")

        form_layout = QFormLayout()
        form_layout.addRow("Usuário:", self.username_entry)
        form_layout.addRow("Senha:", self.password_entry)
        form_layout.addRow("Email:", self.email_entry)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.register_user)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def register_user(self):
        username, password, email = self.get_username_password_email()
        if not username or not password or not email:
            return

        try:
            self.cursor = self.conexao.cursor()
            query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (username, password, email))
            self.conexao.commit()
            self.conexao.close()
            QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
            self.accept()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao registrar usuário: {e}")

    def get_username_password_email(self):
        print(self.username_entry.text(), self.password_entry.text(), self.email_entry.text())
        return self.username_entry.text(), self.password_entry.text(), self.email_entry.text()
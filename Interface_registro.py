from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox, QMessageBox
from PyQt5.QtCore import Qt
from database import mysql_connection
import bcrypt


class RegisterDialog(QDialog):
    def __init__(self, host, user, passwd, database=None):
        super(RegisterDialog, self).__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.setupUI()

    def setupUI(self):
        self.setWindowTitle("Registro")
        self.setGeometry(300, 300, 300, 200)

        layout = QVBoxLayout()

        self.username_entry = QLineEdit()
        self.username_entry.setPlaceholderText("Usuário")
        self.password_entry = QLineEdit()
        self.password_entry.setPlaceholderText("Senha")
        self.password_entry.setEchoMode(QLineEdit.Password)
        self.email_entry = QLineEdit()
        self.email_entry.setPlaceholderText("Email")

        form_layout = QFormLayout()
        form_layout.addRow("Usuário:", self.username_entry)
        form_layout.addRow("Senha:", self.password_entry)
        form_layout.addRow("Email:", self.email_entry)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.register_user)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def register_user(self):
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()
        email = self.email_entry.text().strip()

        if not username or not password or not email:
            QMessageBox.warning(self, "Erro", "Todos os campos são obrigatórios.")
            return

        hashed_password = self.hash_password(password)

        try:
            with self.conexao.cursor() as cursor:
                query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
                cursor.execute(query, (username, hashed_password, email))
                self.conexao.commit()
                QMessageBox.information(self, "Sucesso", "Usuário registrado com sucesso!")
                self.accept()
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao registrar usuário: {e}")
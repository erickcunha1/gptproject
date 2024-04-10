from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox, QPushButton, QLabel, QApplication, QMessageBox
from PyQt5.QtCore import Qt
import mysql.connector
from Interface_registro import RegisterDialog
from database import mysql_connection


class LoginDialog(QDialog):
    def __init__(self, host, user, passwd, database):
        super(LoginDialog, self).__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database

        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()

        self.setWindowTitle("Login")
        self.setGeometry(300, 300, 300, 150)

        layout = QVBoxLayout()

        self.username_entry = QLineEdit(self)
        self.username_entry.setPlaceholderText("Usuário")
        self.password_entry = QLineEdit(self)
        self.password_entry.setPlaceholderText("Senha")
        self.password_entry.setEchoMode(QLineEdit.Password)

        form_layout = QFormLayout()
        form_layout.addRow("Usuário:", self.username_entry)
        form_layout.addRow("Senha:", self.password_entry)

        register_button = QPushButton("Registrar")
        register_button.clicked.connect(self.open_register_dialog)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        buttons.accepted.connect(self.login)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def open_register_dialog(self):
        register_dialog = RegisterDialog(
            self.host,
            self.user,
            self.passwd, 
            self.database
        )

        register_dialog.exec_()

    def login(self):
        username = self.username_entry.text()
        password = self.password_entry.text()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            account = self.cursor.fetchone()
            self.conexao.close()
            if account:
                self.accept()
            else:
                QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao fazer login: {e}")


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = LoginDialog()
    dialog.show()
    sys.exit(app.exec_())

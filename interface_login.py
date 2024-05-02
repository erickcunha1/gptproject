from PyQt5.QtWidgets import QDialog, QLineEdit, QVBoxLayout, QFormLayout, QDialogButtonBox, QPushButton, QMessageBox, QApplication
from PyQt5.QtCore import Qt
import mysql.connector
from Interface_registro import RegisterDialog
from database import mysql_connection
import bcrypt
from datetime import datetime
import requests

class LoginDialog(QDialog):
    def __init__(self, host, user, passwd, database):
        super(LoginDialog, self).__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.conexao = mysql_connection(host, user, passwd, database)
        self.setupUI()

    def setupUI(self):
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

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, Qt.Horizontal, self)
        buttons.accepted.connect(self.login)
        buttons.rejected.connect(self.reject)

        layout.addLayout(form_layout)
        layout.addWidget(register_button)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def open_register_dialog(self):
        register_dialog = RegisterDialog(self.host, self.user, self.passwd, self.database)
        register_dialog.exec_()

    def get_public_ip_address(self):
        try:
            response = requests.get("https://api.ipify.org?format=json")
            if response.status_code == 200:
                ip_address = response.json()["ip"]
                return ip_address
            return "Desconhecido"
        except:
            ...

    def registrar_log(self, username):
        # Registro do log de login bem-sucedido
        data_hora_atual = datetime.now()
        ip_address = self.get_public_ip_address()
        # acao = "Login bem-sucedido"

        with self.conexao.cursor() as cursor:
            log_query = """
                INSERT INTO LoginLog (username, data, hora, ip_address)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(log_query, (
            username,
            data_hora_atual.date(),
            data_hora_atual.time(),
            ip_address,
            ))
            self.conexao.commit()


    def login(self):
        username = self.username_entry.text().strip()
        password = self.password_entry.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            with self.conexao.cursor() as cursor:
                query = "SELECT password FROM users WHERE username = %s"
                cursor.execute(query, (username,))
                result = cursor.fetchone()
                if result:
                    stored_password = result[0].encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                        QMessageBox.information(self, "Login", "Login bem-sucedido.")
                        self.registrar_log(username)
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")
                else:
                    QMessageBox.warning(self, "Erro", "Usuário ou senha incorretos.")
                    self.clear_fields()
        except mysql.connector.Error as e:
            QMessageBox.warning(self, "Erro", f"Erro ao acessar o banco de dados: {e}")

    def clear_fields(self):
        self.password_entry.clear()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    dialog = LoginDialog('host', 'user', 'password', 'db')
    dialog.show()
    sys.exit(app.exec_())
import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from interface_login import LoginDialog
from interface_grafica import InterfaceGrafica
from Interface_registro import RegisterDialog


def execute(host, user, passwd, database):
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dados_sql = (host, user, passwd, database)

    login_dialog = LoginDialog(*dados_sql)

    # Executar o diálogo de login
    result = login_dialog.exec_()
    if result == LoginDialog.Accepted:
        window = InterfaceGrafica(*dados_sql)
        window.setGeometry(100, 100, 800, 400)
        window.show()
        sys.exit(app.exec_())
    else:
        register_dialog = RegisterDialog(*dados_sql)
        register_result = register_dialog.exec_()
        if register_result == RegisterDialog.Accepted:
            QMessageBox.information(None, 'Registro', 'Registro bem-sucedido.')
        sys.exit()

if __name__ == "__main__":
    execute('localhost', 'root', 'Erick1@3$55', 'gdl')
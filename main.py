import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from interface_login import LoginDialog
from interface_grafica import InterfaceGrafica
from Interface_registro import RegisterDialog


def execute(host, user, passwd, database):
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    dados_sql = (host, user, passwd, database)
    # Criar instâncias dos diálogos de login e registro
    login_dialog = LoginDialog(*dados_sql)
    register_dialog = RegisterDialog(*dados_sql)

    # Executar o diálogo de login
    result = login_dialog.exec_()
    if result == login_dialog.Accepted:
        login_dialog.login()
        window = InterfaceGrafica(*dados_sql)
        window.setGeometry(100, 100, 800, 400)
        window.show()
        sys.exit(app.exec_())
    elif result == login_dialog.Rejected:
        # Se o usuário cancelou o login, mostrar o diálogo de registro
        register_dialog.exec_()
        sys.exit()
    else: 
        QMessageBox.critical(None, 'Autenticação falhou.', 'Usuário ou senha inválido.')

if __name__ == "__main__":
    execute('localhost', 'root', 'Erick1@3$55', 'gdl')

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QHBoxLayout
from database import mysql_connection

class UnidadeObjeto(QWidget):
    def __init__(self, host, user, passwd, database=None):
        super().__init__()
        self.host   = host
        self.user   = user
        self.passwd = passwd
        self.database = database
        self.conn = mysql_connection(self.host, self.user, self.passwd, self.database)
        self.cursor = self.conn.cursor()

        # Configurando a janela principal
        self.setWindowTitle('Lista de Itens')
        self.setGeometry(600, 100, 500, 300)  # Adjusted height to fit the lists and buttons

        # Layout vertical
        main_layout = QVBoxLayout()

        # Layout horizontal para os botões
        button_layout = QHBoxLayout()

        # Botão "Objeto"
        self.button_objeto = QPushButton('Objeto', self)
        self.button_objeto.clicked.connect(self.show_objeto_list)

        # Botão "Unidade"
        self.button_unidade = QPushButton('Unidade', self)
        self.button_unidade.clicked.connect(self.show_unidade_list)

        # Adicionando os botões ao layout horizontal
        button_layout.addWidget(self.button_objeto)
        button_layout.addWidget(self.button_unidade)

        # Botão "Continuar"
        self.button_continuar = QPushButton('Continuar', self)
        self.button_continuar.clicked.connect(self.continue_action)
        button_layout.addWidget(self.button_continuar)

        # Adicionando o layout dos botões ao layout principal
        main_layout.addLayout(button_layout)

        # Lista de itens para "Objeto"
        self.list_widget_objeto = QListWidget()
        self.list_widget_objeto.setSelectionMode(QListWidget.MultiSelection)
        
        # Mostrar itens selecionados de "Objeto"
        cod_item = '04.99.00.00067224-6'
        query = "SELECT cod_unidade FROM prompt_etp WHERE cod_item = %s"
        self.cursor.execute(query, (cod_item,))
        selected_items = self.cursor.fetchall()
        print(selected_items)

        objeto_items = [item[0] for item in selected_items]
        self.list_widget_objeto.addItems(objeto_items)
        self.list_widget_objeto.itemSelectionChanged.connect(self.objeto_items_selected)
        self.list_widget_objeto.hide()  # Escondendo a lista inicialmente

        # Lista de itens para "Unidade"
        self.list_widget_unidade = QListWidget()
        self.list_widget_unidade.setSelectionMode(QListWidget.MultiSelection)
        query = "SELECT descricao_unidade FROM unidade"
        self.cursor.execute(query)
        selected_items = self.cursor.fetchall()
        unidade_items = [item[0] for item in selected_items]
        print(selected_items)
        self.list_widget_unidade.addItems(unidade_items)
        self.list_widget_unidade.itemSelectionChanged.connect(self.unidade_items_selected)
        self.list_widget_unidade.hide()  # Escondendo a lista inicialmente

        # Adicionando as listas ao layout principal
        main_layout.addWidget(self.list_widget_objeto)
        main_layout.addWidget(self.list_widget_unidade)

        # Configurando o layout principal
        self.setLayout(main_layout)

    def show_objeto_list(self):
        # Alternar visibilidade da lista de itens de "Objeto"
        if self.list_widget_objeto.isVisible():
            self.list_widget_objeto.hide()
        else:
            self.list_widget_objeto.show()
            self.list_widget_unidade.hide()  # Escondendo a outra lista

    def show_unidade_list(self):
        # Alternar visibilidade da lista de itens de "Unidade"
        if self.list_widget_unidade.isVisible():
            self.list_widget_unidade.hide()
        else:
            self.list_widget_unidade.show()
            self.list_widget_objeto.hide()  # Escondendo a outra lista

    def objeto_items_selected(self):
        # Mostrar itens selecionados de "Objeto"
        selected_items = [item.text() for item in self.list_widget_objeto.selectedItems()]
        print(f'Itens "Unidade" selecionados: {selected_items}')

    def unidade_items_selected(self):
        # Mostrar itens selecionados de "Unidade"
        selected_items = [item.text() for item in self.list_widget_unidade.selectedItems()]
        print(f'Itens "Unidade" selecionados: {selected_items}')

    def continue_action(self):
        # Ação ao clicar em "Continuar"
        selected_objeto_items = [item.text() for item in self.list_widget_objeto.selectedItems()]
        selected_unidade_items = [item.text() for item in self.list_widget_unidade.selectedItems()]

        if selected_objeto_items or selected_unidade_items:
            QMessageBox.information(self, 'Itens Selecionados', f'Você selecionou:\nObjeto: {selected_objeto_items}\nUnidade: {selected_unidade_items}')
            return True
        else:
            QMessageBox.warning(self, 'Nenhum Item Selecionado', 'Por favor, selecione pelo menos um item de qualquer lista.')
            return False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UnidadeObjeto('localhost', 'root', 'Erick1@3$5', 'gdl')
    window.show()
    sys.exit(app.exec_())
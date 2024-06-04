import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QMessageBox, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Configurando a janela principal
        self.setWindowTitle('Lista de Itens')
        self.setGeometry(100, 100, 400, 300)

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

        # Adicionando o layout dos botões ao layout principal
        main_layout.addLayout(button_layout)

        # Lista de itens para "Objeto"
        self.list_widget_objeto = QListWidget()
        objeto_items = ['Item A', 'Item B', 'Item C', 'Item D']
        self.list_widget_objeto.addItems(objeto_items)
        self.list_widget_objeto.itemClicked.connect(self.objeto_item_selected)
        self.list_widget_objeto.hide()  # Escondendo a lista inicialmente

        # Lista de itens para "Unidade"
        self.list_widget_unidade = QListWidget()
        unidade_items = ['Unidade 1', 'Unidade 2', 'Unidade 3', 'Unidade 4']
        self.list_widget_unidade.addItems(unidade_items)
        self.list_widget_unidade.itemClicked.connect(self.unidade_item_selected)
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

    def objeto_item_selected(self, item):
        # Mostrar mensagem quando um item de "Objeto" é selecionado
        QMessageBox.information(self, 'Item Selecionado', f'Você selecionou: {item.text()}')

    def unidade_item_selected(self, item):
        # Mostrar mensagem quando um item de "Unidade" é selecionado
        QMessageBox.information(self, 'Item Selecionado', f'Você selecionou: {item.text()}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
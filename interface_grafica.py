from database import mysql_connection
from PyQt5.QtWidgets import QProgressBar, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QListWidget
from gerador_doc import GeradorDocumentos
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import pyqtSlot


class InterfaceGrafica(QMainWindow):
    def __init__(self, host, user, passwd, database):
        super().__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()
        self.bd_open = False
        
        self.setWindowTitle("Gerador de Documentos Licitatórios")
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Selecione a origem dos dados de referência (PAC):")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2C3E50;")

        self.button = QPushButton("Carregar Banco de Dados", self)
        self.button.setStyleSheet("font-size: 12px; background-color: #3498DB; color: white;")
        self.button.clicked.connect(self.abrir_arquivo)

        self.output_label = QLabel("", self)
        self.output_label.setStyleSheet("font-size: 12px; color: #27AE60;")

        self.search_entry = QLineEdit(self)
        self.search_entry.setPlaceholderText("Pesquisar")
        self.search_entry.setStyleSheet("font-size: 12px;")
        self.search_entry.textChanged.connect(self.filtrar_itens)

        self.item_list = QListWidget(self)
        self.item_list.setSelectionMode(QListWidget.MultiSelection)
        self.item_list.setStyleSheet("font-size: 12px;")
        self.item_list.itemSelectionChanged.connect(self.atualizar_dados_selecionados)

        self.mostrar_dados_button = QPushButton("Gerar Estudo Técnico Preliminar - ETP", self)
        self.mostrar_dados_button.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button.clicked.connect(self.gerar_documento_etp)

        self.mostrar_dados_button2 = QPushButton("Gerar Termo de Referência - TR", self)
        self.mostrar_dados_button2.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button2.clicked.connect(self.gerar_documentos_tr)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.item_list)
        layout.addWidget(self.mostrar_dados_button)
        layout.addWidget(self.mostrar_dados_button2)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("font-size: 12px;")
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(0)

        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

        self.gerador_documentos = GeradorDocumentos(host, user, passwd, database)  # Instanciando GeradorDocumentos

    def filtrar_itens(self):
        filtro = self.search_entry.text().strip().lower()
        comando_sql = f"SELECT * FROM item WHERE LOWER(descricao_item) LIKE '%{filtro}%' order by descricao_item"
        self.cursor.execute(comando_sql)

        dados_lidos = self.cursor.fetchall()
        itens_filtrados = [item[1] for item in dados_lidos]
        itens_selecionados = [item.text() for item in self.item_list.selectedItems()]

        self.item_list.clear()
        self.item_list.addItems(itens_filtrados)

        for index in range(self.item_list.count()):
            item = self.item_list.item(index)
            if item.text() in itens_selecionados:
                item.setSelected(True)

    def gerar_documento_etp(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if selected_items:
            self.gerador_documentos.gerar_documento_etp(selected_items)
        else:
            QMessageBox.warning(self, 'Nenhum item selecionado', 'Selecione pelo menos um item antes de gerar os documentos.')


    def gerar_documentos_tr(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if selected_items:
            self.gerador_documentos.gerar_documentos_tr(selected_items)
        else:
            QMessageBox.warning(self, 'Nenhum item selecionado', 'Selecione pelo menos um item antes de gerar os documentos.')

    def abrir_arquivo(self):
        if not self.bd_open:
            try:
                self.cursor.execute('SELECT descricao_item FROM item order by descricao_item;')
                itens = self.cursor.fetchall()
                for item in itens:
                    valor = item[0]  # Obter o valor da coluna
                    valor_sem_parenteses = valor.strip('()')  # Remover os parênteses
                    self.item_list.addItem(valor_sem_parenteses)
                    self.bd_open = True  # Adicionar o valor à lista na interface gráfica
            except Exception as e:
                QMessageBox.warning(self, 'Erro ao abrir arquivo', f'Ocorreu um erro ao abrir o arquivo: {str(e)}')

    @pyqtSlot()
    def atualizar_dados_selecionados(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        print("Itens selecionados:", selected_items)
        self.progress_bar.setValue(len(selected_items))
        if len(selected_items) > 30:
            # Se o limite de 30 itens for ultrapassado, desmarcar o último item selecionado
            last_item = self.item_list.selectedItems()[-1]
            last_item.setSelected(False)
            QMessageBox.warning(self, 'Atenção', 'Limite de 30 itens selecionados alcançado.')
                
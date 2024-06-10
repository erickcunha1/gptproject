from PyQt5.QtWidgets import (
    QProgressBar,
    QMainWindow,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QListWidget,
    QMessageBox,
)
from PyQt5.QtCore import pyqtSlot
from database import mysql_connection
from gerador_doc import GeradorDocumentos
from threads import BackgroundWorkThread, ProgressBar
from unidade_Objeto import UnidadeObjeto


class InterfaceGrafica(QMainWindow):
    def __init__(self, host: str, user: str, passwd: str, database: str = None) -> None:
        super().__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()
        self.bd_open = False
        self.setupUI()

    def iniciar_processo(self, function, *args) -> None:
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado.")
            return

        self.background_thread = BackgroundWorkThread(
            work_function=function,
            items=args
        )

        total_time = 50
        self.progress_thread = ProgressBar(total_time, len(selected_items))

        self.progress_thread.update_progress.connect(self.progress_bar.setValue)
        self.background_thread.task_finished.connect(self.on_task_finished)

        self.background_thread.start()
        self.progress_thread.start()

    @pyqtSlot()
    def on_task_finished(self) -> None:
        QMessageBox.information(self, "Concluído", "Documento gerado com sucesso!")
        self.progress_bar.setValue(0)

    def setupUI(self) -> None:
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

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.item_list)
        layout.addWidget(self.mostrar_dados_button)
        layout.addWidget(self.mostrar_dados_button2)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

        self.gerador_documentos = GeradorDocumentos(self.host, self.user, self.passwd, self.database)

    def reset_progress_bar(self) -> None:
        self.progress_bar.setValue(0)

    def gerar_documento_etp(self) -> None:
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado.")
            return

        self.unidade_objeto_window = UnidadeObjeto(selected_items, self.host, self.user, self.passwd, self.database, self.on_unidade_objeto_selecionado_etp)
        self.unidade_objeto_window.show()

    def on_unidade_objeto_selecionado_etp(self, selected_objeto_items) -> None:
        if not selected_objeto_items:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione pelo menos um objeto e uma unidade.")
            return

        selected_items = [item.text() for item in self.item_list.selectedItems()]
        self.iniciar_processo(self.gerador_documentos.gerar_documento_etp, selected_items, selected_objeto_items)
        self.unidade_objeto_window.close()

    def gerar_documentos_tr(self) -> None:
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado.")
            return

        self.unidade_objeto_window = UnidadeObjeto(selected_items, self.host, self.user, self.passwd, self.database)
        self.unidade_objeto_window.show()

    def on_unidade_objeto_selecionado_tr(self, selected_objeto_items) -> None:
        if not selected_objeto_items:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione pelo menos um objeto e uma unidade.")
            return

        selected_items = [item.text() for item in self.item_list.selectedItems()]
        self.iniciar_processo(self.gerador_documentos.gerar_documentos_tr, selected_items, selected_objeto_items)
        self.unidade_objeto_window.close()

    def filtrar_itens(self) -> None:
        filtro = self.search_entry.text().strip().lower()
        comando_sql = f"SELECT * FROM item WHERE LOWER(descricao_item) LIKE '%{filtro}%' ORDER BY descricao_item"
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

    def abrir_arquivo(self):
        if self.bd_open:
            return
        try:
            self.cursor.execute('SELECT descricao_item FROM item ORDER BY descricao_item;')
            itens = self.cursor.fetchall()
            for item in itens:
                valor = item[0]
                self.item_list.addItem(valor)
            self.bd_open = True
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao abrir arquivo', f'Ocorreu um erro ao abrir o arquivo: {str(e)}')

    @pyqtSlot()
    def atualizar_dados_selecionados(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        print("Itens selecionados:", selected_items)
        if len(selected_items) > 30:
            last_item = self.item_list.selectedItems()[-1]
            last_item.setSelected(False)
            QMessageBox.warning(self, 'Atenção', 'Limite de 30 itens selecionados alcançado.')
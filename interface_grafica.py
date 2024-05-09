import time

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
from PyQt5.QtCore import (
    QThread,
    pyqtSignal,
    pyqtSlot,
    QTimer,
)

from database import mysql_connection
from gerador_doc import GeradorDocumentos


class BackgroundWorkThread(QThread):
    update_progress = pyqtSignal(int)  # Sinal para atualizar a barra de progresso
    task_finished = pyqtSignal()  # Sinal para indicar que a tarefa foi concluída
    
    def __init__(self, work_function=None, items=None):
        super().__init__()
        self.work_function = work_function
        self.items = items
        self.tempo = len(self.items) * 60
        self.fifth = self.tempo // 2


    def run(self):
        
        for per in range(self.fifth):
            time.sleep(1)
            self.update_progress.emit(per)
            if per == self.fifth:
                break
        
        self.work_function(self.items)

        for per in range(self.fifth):
            time.sleep(1)
            self.update_progress.emit(per)
            if per == self.fifth:
                break

        self.task_finished.emit()

class InterfaceGrafica(QMainWindow):
    def __init__(self, host, user, passwd, database):
        super().__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()
        self.bd_open = False
        self.setupUI()

    def iniciar_processo(self):
        # Iniciar a thread para rodar em segundo plano
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        if not selected_items:
            QMessageBox.warning(self, "Aviso", "Nenhum item selecionado.")
            return

        # Criar uma nova thread para o trabalho em segundo plano
        self.background_thread = BackgroundWorkThread(work_function=self.gerar_documento_etp, items=selected_items)
        self.background_thread.start()
        
        # Conectar sinais para atualizar a barra de progresso e notificar quando a tarefa for concluída
        self.background_thread.update_progress.connect(self.progress_bar.setValue)

        self.background_thread.task_finished.connect(self.on_task_finished)

        # Iniciar a thread
    
    @pyqtSlot()
    def on_task_finished(self):
        QMessageBox.information(self, "Concluído", "Documento gerado com sucesso!")
        self.progress_bar.setValue(0)
    
    def setupUI(self):
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
        self.mostrar_dados_button.clicked.connect(self.iniciar_processo)

        self.mostrar_dados_button2 = QPushButton("Gerar Termo de Referência - TR", self)
        self.mostrar_dados_button2.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button2.clicked.connect(self.gerar_documentos_tr)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)

        self.reset_timer = QTimer()
        self.reset_timer.setSingleShot(True)
        self.reset_timer.timeout.connect(self.reset_progress_bar)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.item_list)
        layout.addWidget(self.mostrar_dados_button)
        layout.addWidget(self.mostrar_dados_button2)
        layout.addWidget(self.progress_bar)

        central_widget.setLayout(layout)

        self.gerador_documentos = GeradorDocumentos(self.host, self.user, self.passwd, self.database)  # Instanciando GeradorDocumentos
    
    def reset_progress_bar(self):
        self.progress_bar.setValue(0)

    # def iniciar_processo(self):
    #     # Criação da thread para atualizar a barra de progresso
    #     self.progress_thread = BackgroundWorkThread()
    #     self.progress_thread.update_progress.connect(self.progress_bar.setValue)  # Conecta o sinal à barra de progresso
    #     self.progress_thread.start()  # Inicia a thread

    def gerar_documento_etp(self, itens):
        self.gerador_documentos.gerar_documento_etp(itens)
        
    def gerar_documentos_tr(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        self.iniciar_processo()
        if selected_items:
            self.gerador_documentos.gerar_documentos_tr(selected_items)
            self.reset_timer.start(5000)
        else:
            QMessageBox.warning(self, 'Nenhum item selecionado', 'Selecione pelo menos um item antes de gerar os documentos.')
    
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

    def abrir_arquivo(self):
        if not self.bd_open:
            try:
                self.cursor.execute('SELECT descricao_item FROM item order by descricao_item;')
                itens = self.cursor.fetchall()
                for item in itens:
                    valor = item[0]  # Obter o valor da coluna
                    self.item_list.addItem(valor)
                    self.bd_open = True  # Adicionar o valor à lista na interface gráfica
            except Exception as e:
                QMessageBox.warning(self, 'Erro ao abrir arquivo', f'Ocorreu um erro ao abrir o arquivo: {str(e)}')

    @pyqtSlot()
    def atualizar_dados_selecionados(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]
        print("Itens selecionados:", selected_items)
        # self.progress_bar.setValue(len(selected_items))
        if len(selected_items) > 30:
            # Se o limite de 30 itens for ultrapassado, desmarcar o último item selecionado
            last_item = self.item_list.selectedItems()[-1]
            last_item.setSelected(False)
            QMessageBox.warning(self, 'Atenção', 'Limite de 30 itens selecionados alcançado.') 
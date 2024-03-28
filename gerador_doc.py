import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QListWidget
from PyQt5.QtCore import pyqtSlot
import openai
from docx import Document
from datetime import datetime
from pathlib import Path
import os
from interface_login import LoginDialog
from PyQt5.QtWidgets import QProgressBar
from prompts import PromptsInfo



class InterfaceGrafica(QMainWindow):
    def __init__(self, host, user, passwd, database=None):
        super(InterfaceGrafica, self).__init__()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.database = database
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
        self.mostrar_dados_button.clicked.connect(self.mostrar_dados)

        self.mostrar_dados_button2 = QPushButton("Gerar Termo de Referência - TR", self)
        self.mostrar_dados_button2.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button2.clicked.connect(self.mostrar_dados_TR)

        self.mostrar_dados_button3 = QPushButton("Gerar Edital de Licitação", self)
        self.mostrar_dados_button3.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button3.clicked.connect(self.mostrar_dados)

        self.mostrar_dados_button4 = QPushButton("Gerar Contrato", self)
        self.mostrar_dados_button4.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button4.clicked.connect(self.mostrar_dados)
        
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.item_list)
        layout.addWidget(self.mostrar_dados_button)

        central_widget.setLayout(layout)

        layout.addWidget(self.mostrar_dados_button)
        layout.addWidget(self.mostrar_dados_button2)
        layout.addWidget(self.mostrar_dados_button3)
        layout.addWidget(self.mostrar_dados_button4)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("font-size: 12px;")
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(0)

        layout.addWidget(self.progress_bar)

    def abrir_arquivo(self):
        try:
            prompts_info = PromptsInfo(self.host, self.user, self.passwd, self.database)
            prompts_info.cursor.execute('SELECT descricao_item FROM item;')
            itens = prompts_info.cursor.fetchall()
            for item in itens:
                valor = item[0]  # Obter o valor da coluna
                valor_sem_parenteses = valor.strip('()')  # Remover os parênteses
                self.item_list.addItem(valor_sem_parenteses)  # Adicionar o valor à lista na interface gráfica
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao abrir arquivo', f'Ocorreu um erro ao abrir o arquivo: {str(e)}')

    def filtrar_itens(self):
        pass

    @pyqtSlot()
   
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

        try:
            prompts_info = PromptsInfo(self.host, self.user, self.passwd, self.database)
            for item_selecionado in selected_items:
                prompts_info.cursor.execute(f"SELECT * FROM prompt_etp WHERE cod_item = '{item_selecionado}'")
                prompts = prompts_info.cursor.fetchall()
                prompts_list = []
                for prompt in prompts:
                    prompt_dict = {
                        'cod_item': prompt[0],  # Código do item
                        'descricao_item': prompt[1],  # Descrição do item
                        'prompt1': prompt[2],  # Prompt 1
                        'prompt2': prompt[3],  # Prompt 2
                        'prompt3': prompt[4],  # Prompt 3
                        # Adicione mais prompts conforme necessário
                    }
                    prompts_list.append(prompt_dict)
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao recuperar prompts', f'Ocorreu um erro ao recuperar prompts do banco de dados: {str(e)}')



    def mostrar_dados(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]

        if selected_items:
            try:
                prompts_info = PromptsInfo(self.host, self.user, self.passwd, self.database)
                doc = Document()
                doc.add_heading("Documentos Gerados", level=1)  # Adiciona um cabeçalho geral

                for i in range(1, 9):
                    titulo = PromptsInfo.get_titulo_name(i)  # Obtem o título correspondente
                    doc.add_heading(titulo, level=1)  # Adiciona o título

                    for item_selecionado in selected_items:
                        doc.add_heading(f"Item: {item_selecionado}", level=3)  # Adiciona um cabeçalho para cada item
                        prompt_nome = PromptsInfo.get_prompt_name(i)  # Obtem o nome do prompt
                        prompts_info.cursor.execute(f"SELECT {prompt_nome} FROM prompt_etp;")
                        prompt_valor = prompts_info.cursor.fetchone()[0]

                        client = openai.OpenAI(api_key=os.environ.get('KEY'))

                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[{"role": "user", "content": prompt_valor}])
                        resposta = response.choices[0].message.content
                        doc.add_paragraph(resposta)

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                caminho_arquivo = Path.home() / "Desktop" / f"Documentos_Gerados_{timestamp}.docx"

                doc.save(caminho_arquivo)
                QMessageBox.information(self, 'Documentos gerados!', f'Documento salvo com sucesso em: {caminho_arquivo}')
            except Exception as e:
                QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro ao gerar os documentos: {str(e)}')
        else:
            QMessageBox.warning(self, 'Nenhum item selecionado', 'Selecione pelo menos um item antes de gerar os documentos.')


    def mostrar_dados_TR(self):
        pass


def execute():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    login_dialog = LoginDialog()  # Substitua isso pelo seu diálogo de login
    result = login_dialog.exec_()

    if result == QDialog.Accepted:
        username, password = login_dialog.get_username_password()  # Substitua isso pelo método adequado do seu diálogo de login
        authenticated = username == "admin" and password == "admin"

        if authenticated:
            window = InterfaceGrafica('localhost', 'root', 'Erick1@3$5', 'gdl')
            window.setGeometry(100, 100, 800, 400)
            window.show()
            window.button.clicked.disconnect()  # Desconecta qualquer sinal previamente conectado
            window.button.clicked.connect(window.abrir_arquivo)  # Conecta o botão à função abrir_arquivo
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, 'Autenticação falhou.', 'Usuário ou senha inválido.')
    else:
        sys.exit()


if __name__ == "__main__":
    execute()

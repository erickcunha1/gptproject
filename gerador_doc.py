import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QFileDialog, QListWidget
from PyQt5.QtCore import pyqtSlot
import openai
from docx import Document
import pandas as pd
from datetime import datetime
from pathlib import Path
import os
from interface_login import LoginDialog
from PyQt5.QtWidgets import QProgressBar



class InterfaceGrafica(QMainWindow):
    def __init__(self):
        super(InterfaceGrafica, self).__init__()

        self.setWindowTitle("Gerador de Documentos Licitatórios")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Selecione a origem dos dados de referência (PAC):")
        self.label.setStyleSheet("font-size: 14px; font-weight: bold; color: #2C3E50;")

        self.button = QPushButton("Escolher Arquivo", self)
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
        # Lista de dicionários para armazenar os dados extraídos
        self.linhas_dados = []

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setStyleSheet("font-size: 12px;")
        self.progress_bar.setMaximum(30)
        self.progress_bar.setValue(0)

        layout.addWidget(self.progress_bar)

    def abrir_arquivo(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo Excel", "", "Arquivos Excel (*.xlsx)")

        if filepath:
            try:
                df = pd.read_excel(filepath)
                self.df_original = df.copy()
                itens = sorted(df['Descrição do Item'].unique())  # Ordenar os itens em ordem alfabética

                self.output_label.setText(f"Arquivo {filepath} lido com sucesso.")
                self.output_label.setStyleSheet("font-size: 12px; color: #27AE60;")

                self.item_list.clear()
                self.item_list.addItems(itens)

                for _, linha in df.iterrows():
                    dados_linha = {coluna: linha[coluna] for coluna in df.columns}
                    self.linhas_dados.append(dados_linha)

            except Exception as e:
                self.output_label.setText(f"Erro ao ler o arquivo:\n{e}")
                self.output_label.setStyleSheet("font-size: 12px; color: #E74C3C;")

    def filtrar_itens(self):
        if not hasattr(self, 'df_original'):
            QMessageBox.warning(self, 'Atenção', 'Selecione a planilha primeiro.')
            return
        filtro = self.search_entry.text().strip().lower()
        df_filtrado = self.df_original[self.df_original['Descrição do Item'].str.lower().str.contains(filtro)]
        itens_filtrados = df_filtrado['Descrição do Item'].unique()

        itens_selecionados = [item.text() for item in self.item_list.selectedItems()]  # Armazena os itens selecionados

        self.item_list.clear()
        self.item_list.addItems(itens_filtrados)

        # Restaura a seleção dos itens previamente selecionados
        for index in range(self.item_list.count()):
            item = self.item_list.item(index)
            if item.text() in itens_selecionados:
                item.setSelected(True)


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


    def mostrar_dados(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]

        if selected_items:
            doc = Document()
            doc.add_heading("Documentos Gerados", level=1)  # Adiciona um cabeçalho geral

            for i in range(1, 10): 
                titulo = self.get_titulo_name(i)  # Obtem o título correspondente
                doc.add_heading(titulo, level=1)  # Adiciona o título

                for item_selecionado in selected_items:
                    print(f"Dados para '{item_selecionado}':")
                    doc.add_heading(f"Item: {item_selecionado}", level=3)  # Adiciona um cabeçalho para cada item
                    
                    for linha in self.linhas_dados:
                        if linha['Descrição do Item'] == item_selecionado:
                            prompt_nome = f'Prompt{i}-{self.get_prompt_name(i)}'  # Obtem o nome do prompt
                            prompt_valor = linha[prompt_nome]  # Obtem o valor do prompt

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
        else:
            print("Selecione um item antes de mostrar os dados.")

            
    def mostrar_dados_TR(self):
        selected_items = [item.text() for item in self.item_list.selectedItems()]

        if selected_items:
            doc = Document()
            doc.add_heading("ESTUDO TÉCNICO PRELIMINAR - ETP", level=1)

            for i in range(1, 5):
                titulo = self.get_titulo_tr(i)
                doc.add_heading(text=titulo, level=1)

                for item_selecionado in self.linhas_dados:
                    print(f"Dados para '{item_selecionado}':")
            
                    for linha in self.linhas_dados:
                        if linha['Descrição do Item'] == item_selecionado:
                            prompt_nome = f'Prompt{i}-{self.get_prompt_tr(i)}'  # Obtem o nome do prompt
                            prompt_valor = linha[prompt_nome]  # Obtem o valor do prompt

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
        else:
            print("Selecione um item antes de mostrar os dados.")


    def get_prompt_tr(self, number):
        titulo_names = {
            1:'Prompt1-Termo de Referência',
            2:'Prompt2-TR-Fundamentação da Contratação',
            3:'Prompt3-TR- Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto',
            4:'Prompt4-TR- Requisitos da Contratação'
        }
        return titulo_names.get(number, 'Desconhecido')
    
    def get_titulo_tr(self, number):

        titulo_name = { 
            1:"Condições Gerais da Contratação",
            2:"Fundamentação da Contratação",
            3:"Descrição da solução como um todo considerado o ciclo de vida do objeto e especificação do produto",
            4:"Requisitos da Contratação"
        }
        return titulo_name.get(number, 'Desconhecido')
    

    def get_prompt_name(self, prompt_number):
        # Função para obter o nome do prompt com base no número
        prompt_names = {
            1: "objeto",
            2: "Justificativa",
            3: "previsão de contratação",
            4: "requisitos da contratação",
            5: "justificativa-quantitativo",
            6: "estimativa de valor",
            7: "fundamentação legal",
            8: "justificativa-parcelamento",
            9: "posicionamento-conclusivo"
        }
        return prompt_names.get(prompt_number, "Desconhecido")

    def get_titulo_name(self, titulo_number):
        # Função para obter o nome do título com base no número
        titulo_names = {
            1: "Objeto",
            2: "Justificativa da necessidade da contratação, considerado o problema a ser resolvido sob a perspectiva do interesse público",
            3: "Demonstração da previsão da contratação",
            4: "Requisitos para Contratação",
            5: "Estimativas e Justificativas das quantidades para a contratação",
            6: "Estimativa de valor",
            7: "Fundamentação Legal",
            8: "Justificativa do Parcelamento",
            9: "Posicionamento Conclusivo"
        }
        return titulo_names.get(titulo_number, 'Desconhecido')



def execute():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    login_dialog = LoginDialog()
    result = login_dialog.exec_()

    if result == QDialog.Accepted:
        username, password = login_dialog.get_username_password()
        authenticated = username == "admin" and password == "admin"

        if authenticated:
            window = InterfaceGrafica()
            window.setGeometry(100, 100, 800, 400)
            window.show()
            sys.exit(app.exec_())
        else:
            QMessageBox.critical(None, 'Authentication Failed', 'Invalid username or password.')
    else:
        sys.exit()

if __name__ == "__main__":
    execute()
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QLineEdit,
    QComboBox, QVBoxLayout, QWidget, QFileDialog, QMessageBox
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt, pyqtSlot
import pandas as pd
from docx import Document
from pathlib import Path
from datetime import datetime
import openai


class InterfaceGrafica(QMainWindow):
    def __init__(self):
        load_dotenv()
        super(InterfaceGrafica, self).__init__()

        self.setWindowTitle("Gerador de Documentos Jurídicos")

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.label = QLabel("Selecione um arquivo Excel:")
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

        self.item_combobox = QComboBox(self)
        self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)
        self.item_combobox.setStyleSheet("font-size: 12px;")

        self.mostrar_dados_button = QPushButton("Gerar Documento", self)
        self.mostrar_dados_button.setStyleSheet("font-size: 12px; background-color: #E74C3C; color: white;")
        self.mostrar_dados_button.clicked.connect(self.mostrar_dados)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.output_label)
        layout.addWidget(self.search_entry)
        layout.addWidget(self.item_combobox)
        layout.addWidget(self.mostrar_dados_button)

        central_widget.setLayout(layout)

        self.linhas_dados = []
        self.manual_selection = True
        self.db_connection = sqlite3.connect('dados_documentos.db')
        self.create_table()

        # Tentar carregar os dados do último arquivo selecionado
        self.carregar_dados_salvos()

    def create_table(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS documentos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item TEXT,
                prompt1 TEXT,
                prompt2 TEXT,
                prompt3 TEXT,
                prompt4 TEXT,
                prompt5 TEXT,
                prompt6 TEXT,
                prompt7 TEXT,
                timestamp TEXT
            )
        ''')
        self.db_connection.commit()

    def insert_data(self, item, prompts):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO documentos (item, prompt1, prompt2, prompt3, prompt4, prompt5, prompt6, prompt7, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (item, prompts[0], prompts[1], prompts[2], prompts[3], prompts[4], prompts[5], prompts[6], timestamp))
        self.db_connection.commit()

    def carregar_dados_salvos(self):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT DISTINCT item FROM documentos')
        itens = cursor.fetchall()

        if itens:
            self.output_label.setText("Dados carregados do último arquivo.")
            self.output_label.setStyleSheet("font-size: 12px; color: #27AE60;")

            self.item_combobox.currentIndexChanged.disconnect(self.atualizar_dados_selecionados)
            self.item_combobox.clear()
            self.item_combobox.addItems([item[0] for item in itens])
            self.item_combobox.setCurrentIndex(-1)
            self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)

    def abrir_arquivo(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo Excel", "", "Arquivos Excel (*.xlsx)")

        if filepath:
            try:
                df = pd.read_excel(filepath)
                self.df_original = df.copy()

                itens = df['Descrição do Item'].unique()

                self.output_label.setText(f"Arquivo {filepath} lido com sucesso.")
                self.output_label.setStyleSheet("font-size: 12px; color: #27AE60;")

                self.item_combobox.currentIndexChanged.disconnect(self.atualizar_dados_selecionados)
                self.item_combobox.clear()
                self.item_combobox.addItems(itens)
                self.item_combobox.setCurrentIndex(-1)
                self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)

                for _, linha in df.iterrows():
                    dados_linha = {coluna: linha[coluna] for coluna in df.columns}
                    self.linhas_dados.append(dados_linha)

                # Limpar dados antigos e inserir novos dados na base de dados
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM documentos')
                self.db_connection.commit()

                for _, linha in df.iterrows():
                    dados_linha = {coluna: linha[coluna] for coluna in df.columns}
                    self.linhas_dados.append(dados_linha)
                    self.insert_data(dados_linha['Descrição do Item'], [
                        dados_linha['Prompt1-objeto'],
                        dados_linha['Prompt2-Justificativa'],
                        dados_linha['Prompt3-justificativa-quantitativo'],
                        dados_linha['Prompt4-fundamentação legal'],
                        dados_linha['Prompt5-detalhamento técnico'],
                        dados_linha['Prompt6-justificativa-parcelamento'],
                        dados_linha['Prompt7-posicionamento-conclusivo']
                    ])

            except Exception as e:
                self.output_label.setText(f"Erro ao ler o arquivo:\n{e}")
                self.output_label.setStyleSheet("font-size: 12px; color: #E74C3C;")

    def filtrar_itens(self):
        filtro = self.search_entry.text().strip().lower()
        df_filtrado = self.df_original[self.df_original['Descrição do Item'].str.lower().str.contains(filtro)]
        itens_filtrados = df_filtrado['Descrição do Item'].unique()

        self.item_combobox.currentIndexChanged.disconnect(self.atualizar_dados_selecionados)
        self.item_combobox.clear()
        self.item_combobox.addItems(itens_filtrados)
        self.item_combobox.setCurrentIndex(-1)
        self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)

    @pyqtSlot(int)
    def atualizar_dados_selecionados(self, index):
        if self.manual_selection:
            item_selecionado = self.item_combobox.currentText()
            print(f"Atualizar dados para '{item_selecionado}':")

    def mostrar_dados(self):
        self.manual_selection = False

        item_selecionado = self.item_combobox.currentText()

        if item_selecionado:
            print(f"Dados para '{item_selecionado}':")

            for linha in self.linhas_dados:
                if linha['Descrição do Item'] == item_selecionado:
                    lista_dados = [
                        linha['Prompt1-objeto'],
                        linha['Prompt2-Justificativa'],
                        linha['Prompt3-justificativa-quantitativo'],
                        linha['Prompt4-fundamentação legal'],
                        linha['Prompt5-detalhamento técnico'],
                        linha['Prompt6-justificativa-parcelamento'],
                        linha['Prompt7-posicionamento-conclusivo']
                    ]

                    self.insert_data(item_selecionado, lista_dados)

                    tab_order = [
                        "Objeto",
                        "Justificativa",
                        "Justificativa do Quantitativo",
                        "Fundamentação Legal",
                        "Detalhamento Técnico",
                        "Justificativa do Parcelamento",
                        "Posicionamento Conclusivo"
                    ]

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    caminho_arquivo = Path.home() / "Desktop" / f"{item_selecionado}_{timestamp}.docx"

                    doc = Document()
                    client = openai.OpenAI(api_key='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')
                    
                    for i, prompt_valor in enumerate(lista_dados):
                        doc.add_heading(tab_order[i], level=1)

                        response = client.chat.completions.create(
                            model="gpt-3.5-turbo",
                            messages=[
                                {"role": "user", "content": prompt_valor}
                            ]
                        )
                        resposta = response.choices[0].message.content
                        doc.add_paragraph(resposta)

                    doc.save(caminho_arquivo)
                    QMessageBox.information(self, 'Documento gerado!', 'Documento salvo com sucesso!')

        else:
            print("Selecione um item antes de mostrar os dados.")

        self.manual_selection = True

    def closeEvent(self, event):
        self.db_connection.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#ECF0F1"))
    palette.setColor(QPalette.WindowText, Qt.black)
    palette.setColor(QPalette.Button, QColor("#3498DB"))
    palette.setColor(QPalette.ButtonText, Qt.white)
    app.setPalette(palette)

    window = InterfaceGrafica()
    window.setGeometry(100, 100, 800, 400)
    window.show()
    sys.exit(app.exec_())

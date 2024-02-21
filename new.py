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
        super(InterfaceGrafica, self).__init__()

        self.setWindowTitle("Gerador de Documentos Juridicos")

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
        self.search_entry.textChanged.connect(self.filtrar_itens)  # Connect to the textChanged signal

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

        # Lista de dicionários para armazenar os dados extraídos
        self.linhas_dados = []

        # Flag para indicar se a atualização do combo box é devido à seleção manual
        self.manual_selection = True

    def abrir_arquivo(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Selecione um arquivo Excel", "", "Arquivos Excel (*.xlsx)")

        if filepath:
            try:
                df = pd.read_excel(filepath)
                self.df_original = df.copy()

                itens = df['Descrição do Item'].unique()

                self.output_label.setText(f"Arquivo {filepath} lido com sucesso.")
                self.output_label.setStyleSheet("font-size: 12px; color: #27AE60;")

                # Disconnect the signal before clearing and updating the combo box
                self.item_combobox.currentIndexChanged.disconnect(self.atualizar_dados_selecionados)
                self.item_combobox.clear()
                self.item_combobox.addItems(itens)
                self.item_combobox.setCurrentIndex(-1)
                # Reconnect the signal after updating the combo box
                self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)

                for _, linha in df.iterrows():
                    dados_linha = {coluna: linha[coluna] for coluna in df.columns}
                    self.linhas_dados.append(dados_linha)

            except Exception as e:
                self.output_label.setText(f"Erro ao ler o arquivo:\n{e}")
                self.output_label.setStyleSheet("font-size: 12px; color: #E74C3C;")

    def filtrar_itens(self):
        filtro = self.search_entry.text().strip().lower()
        df_filtrado = self.df_original[self.df_original['Descrição do Item'].str.lower().str.contains(filtro)]
        itens_filtrados = df_filtrado['Descrição do Item'].unique()

        # Disconnect the signal before clearing and updating the combo box
        self.item_combobox.currentIndexChanged.disconnect(self.atualizar_dados_selecionados)
        self.item_combobox.clear()
        self.item_combobox.addItems(itens_filtrados)
        self.item_combobox.setCurrentIndex(-1)
        # Reconnect the signal after updating the combo box
        self.item_combobox.currentIndexChanged.connect(self.atualizar_dados_selecionados)

    @pyqtSlot(int)
    def atualizar_dados_selecionados(self, index):
        # Check the flag to determine if the change is due to manual selection
        if self.manual_selection:
            item_selecionado = self.item_combobox.currentText()
            print(f"Atualizar dados para '{item_selecionado}':")
            # Implement any additional logic if needed when combo box selection changes

    def mostrar_dados(self):
        # Set the flag to False to indicate that the change is not due to manual selection
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

        # Set the flag back to True after handling the button click
        self.manual_selection = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Apply Fusion style
    app.setStyle("Fusion")

    # Create a color palette
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor("#ECF0F1"))  # Background color
    palette.setColor(QPalette.WindowText, Qt.black)  # Text color
    palette.setColor(QPalette.Button, QColor("#3498DB"))  # Button color
    palette.setColor(QPalette.ButtonText, Qt.white)  # Button text color
    app.setPalette(palette)

    window = InterfaceGrafica()
    window.setGeometry(100, 100, 800, 400)
    window.show()
    sys.exit(app.exec_())
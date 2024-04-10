from PyQt5.QtWidgets import QMessageBox
import openai
from docx import Document
from datetime import datetime
from pathlib import Path
import os
from prompts import PromptsInfo
from database import mysql_connection
from PyQt5.QtWidgets import QWidget, QMessageBox


class GeradorDocumentos(QWidget):
    def __init__(self, host, user, passwd, database=None):
        super().__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()
        self.client = openai.OpenAI(api_key=os.environ.get('KEY'))

    def gerar_documento_etp(self, selected):
        
        try:
            doc = Document()
            doc.add_heading("Documentos Gerados", level=1)  # Adiciona um cabeçalho geral
            for i in range(1, 9):
                titulo = PromptsInfo.get_titulo_name(i)  # Obtem o título correspondente
                doc.add_heading(titulo.upper(), level=1)  # Adiciona o título

                for item_selecionado in selected:
                    parts = item_selecionado.split("Item:")
                    second_part = parts[0].strip()

                    item = second_part.split()[0]
                    doc.add_heading(f"- {item}", level=3)

                    prompt_nome = PromptsInfo.get_prompt_name(i)  # Obtem o nome do prompt
                    self.cursor.execute(f"SELECT {prompt_nome} FROM prompt_etp;")
                    prompt_valor = self.cursor.fetchone()[0]

                    response = self.client.chat.completions.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt_valor}]
                    )
                    resposta = response.choices[0].message.content
                    doc.add_paragraph(resposta)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = Path.home() / "Desktop" / f"Documentos_Gerados_{timestamp}.docx"

            doc.save(caminho_arquivo)
            QMessageBox.information(self, 'Documentos gerados!', f'Documento salvo com sucesso em: {caminho_arquivo}')
        except Exception as e:
                QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro ao gerar os documentos: {str(e)}')

    def gerar_documento_tr(self):
        pass


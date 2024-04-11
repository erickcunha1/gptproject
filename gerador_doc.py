from PyQt5.QtWidgets import QMessageBox
import openai
from docx import Document
from datetime import datetime
from pathlib import Path
import os
from prompts import PromptsInfo
from database import mysql_connection
from PyQt5.QtWidgets import QWidget

class GeradorDocumentos(QWidget):
    def __init__(self, host, user, passwd, database=None):
        super().__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor()
        self.client = openai.OpenAI(api_key=os.environ.get('KEY'))  # Usar variável de ambiente

    def add_content_to_doc(self, doc, title, content):
        doc.add_heading(title, level=1)
        doc.add_paragraph(content)

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def gerar_documento_etp(self, selected):
        try:
            doc = Document()
            doc.add_heading("Documentos Gerados", level=1)
            for i in range(1, 9):
                titulo = PromptsInfo.get_titulo_name(i)
                for item_selecionado in selected:
                    item = item_selecionado.split("Item:")[0].strip().split()[0]
                    prompt_nome = PromptsInfo.get_prompt_name(i)
                    self.cursor.execute(f"SELECT {prompt_nome} FROM prompt_etp;")
                    prompt_valor = self.cursor.fetchone()[0]

                    resposta = self.generate_response(prompt_valor)
                    self.add_content_to_doc(doc, f"- {titulo.upper()} - {item}", resposta)

            self.save_document(doc)
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')

    def save_document(self, doc):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_arquivo = Path.home() / "Desktop" / f"Documentos_Gerados_{timestamp}.docx"
        doc.save(caminho_arquivo)
        QMessageBox.information(self, 'Documentos gerados!', f'Documento salvo com sucesso em: {caminho_arquivo}')
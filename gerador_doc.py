from datetime import datetime
from pathlib import Path

from PyQt5.QtWidgets import QWidget
from docx import Document
import dotenv
import openai
import os

from prompt import PromptsInfo
from prompt_menager import MenagerPrompt

class GeradorDocumentos(QWidget):
    def __init__(self, host, user, passwd, database=None):
        super().__init__()
        dotenv.load_dotenv()
        KEY = os.getenv('OPENAI_KEY')
        self.client = openai.OpenAI(api_key=KEY)
        self.prompt_manager = MenagerPrompt(host, user, passwd, database)  # Usar variável de ambiente

    def generate_response(self, prompt):
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    
    def save_document(self, doc):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        caminho_arquivo = Path.home() / "Desktop" / f"Documentos_Gerados_{timestamp}.docx"
        doc.save(caminho_arquivo)
        return caminho_arquivo
    
    def gerar_documento_etp(self, selected):
        doc = Document()
        doc.add_heading("Documentos Gerados", level=1)

        for i in range(1, 9):
            titulo = PromptsInfo.get_title_etp(i)
            doc.add_heading(titulo, level=1)
            for item in selected:
                prompt = self.prompt_manager.search_prompt_etp(i, item)
                print(prompt)
                resposta = self.generate_response(prompt)
                doc.add_paragraph(resposta)
                self.prompt_manager.insert_prompt(PromptsInfo.get_column_etp(i), resposta, item)

        self.save_document(doc)
        
    def gerar_documentos_tr(self, selected):
        doc = Document()
        doc.add_heading("TERMO DE REFERÊNCIA - TR", level=1)

        for i in range(1, 11):
            titulo = PromptsInfo.get_titulo_tr(i)
            doc.add_heading(text=titulo, level=1)
            for item in selected:
                prompt_valor = self.search_tr_data(i, item)
                resposta = self.generate_response(prompt_valor)
                doc.add_paragraph(resposta)

        self.save_document(doc)
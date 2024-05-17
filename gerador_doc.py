from PyQt5.QtWidgets import QMessageBox
from docx import Document
from datetime import datetime
from pathlib import Path
from prompts import PromptsInfo
from database import mysql_connection
from PyQt5.QtWidgets import QWidget
import openai
import os

class GeradorDocumentos(QWidget):
    def __init__(self, host, user, passwd, database=None):
        super().__init__()
        self.conexao = mysql_connection(host, user, passwd, database)
        self.cursor = self.conexao.cursor(buffered=True)
        self.client = openai.OpenAI(api_key='')  # Usar variável de ambiente

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


    def get_item_code(self, desc):
        first_query = "SELECT cod_item FROM item WHERE descricao_item = %s"
        self.cursor.execute(first_query, (desc,))
        result = self.cursor.fetchone() 
        return str(result[0])
    

    def search_etp_data(self, i, item):
        prompt_nome = PromptsInfo.get_prompt_name(i)
        cod_item = self.get_item_code(item)
        query = f"SELECT {prompt_nome} FROM prompt_etp WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt_valor = self.cursor.fetchone()[0]
        return prompt_valor
    
    def gerar_documento_etp(self, selected):
        try:
            doc = Document()
            doc.add_heading("Documentos Gerados", level=1)

            for i in range(1, 9):
                titulo = PromptsInfo.get_titulo_name(i)
                doc.add_heading(titulo, level=1)
                for item in selected:
                    prompt_valor = self.search_etp_data(i, item)
                    resposta = self.generate_response(prompt_valor)
                    doc.add_paragraph(resposta)

            doc_gerado = self.save_document(doc)
            os.system(f"start {doc_gerado}")
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')
    
    def search_tr_data(self, i, item):
        prompt_nome = PromptsInfo.get_prompt_tr(i)
        cod_item = self.get_item_code(item)
        query = f"SELECT {prompt_nome} FROM prompt_tr WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt_valor = self.cursor.fetchone()[0]
        return prompt_valor
        
    def gerar_documentos_tr(self, selected):
        try:
            doc = Document()
            doc.add_heading("TERMO DE REFERÊNCIA - TR", level=1)

            for i in range(1, 11):
                titulo = PromptsInfo.get_titulo_tr(i)
                doc.add_heading(text=titulo, level=1)
                for item in selected:
                    prompt_valor = self.search_tr_data(i, item)
                    resposta = self.generate_response(prompt_valor)
                    doc.add_paragraph(resposta)

            doc_gerado = self.save_document(doc)
            # os.system(f"start {doc_gerado}")

        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')
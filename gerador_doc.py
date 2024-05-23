from PyQt5.QtWidgets import QMessageBox
from docx import Document
from datetime import datetime
from pathlib import Path
from prompt import PromptsInfo
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
        return result[0]
    
    def search_prompt_etp(self, i, item):
        column_name = PromptsInfo.get_column_etp(i)
        cod_item = self.get_item_code(item)
        query = f"SELECT {column_name} FROM prompt_etp WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt = self.cursor.fetchone()[0]
        return prompt
    
    def insert_prompt(self, column_name, prompt, item):
        query = "SELECT item.cod_item, prompt_etp.id_prompt, prompt_etp.cod_orgao, prompt_etp.cod_unidade FROM item JOIN prompt_etp ON item.cod_item = prompt_etp.cod_item WHERE item.descricao_item = %s"
        self.cursor.execute(query, (item,))
        record = self.cursor.fetchone()

        if record:
            cod_item = record[0]
            id_prompt = record[1]
            cod_orgao = record[2]
            cod_unidade = record[3]

            # Em seguida, verificamos se já existe um registro na tabela `etp` para o item
            query2 = "SELECT id_prompt FROM etp WHERE cod_item = %s"
            self.cursor.execute(query2, (cod_item,))
            existing_record = self.cursor.fetchone()

            if not existing_record:
                # Se não houver um registro na tabela `etp` para o item, inserimos um novo
                insert_query = "INSERT INTO etp (id_prompt, cod_orgao, cod_unidade, cod_item) VALUES (%s, %s, %s, %s)"
                self.cursor.execute(insert_query, (id_prompt, cod_orgao, cod_unidade, cod_item))
                self.conexao.commit()

            # Em seguida, inserimos o prompt na coluna especificada na tabela `etp`
            update_query = f"UPDATE etp SET {column_name} = %s WHERE cod_item = %s"
            self.cursor.execute(update_query, (prompt, cod_item))
            self.conexao.commit()
        else:
            print("Item não encontrado.")

    
    def gerar_documento_etp(self, selected):
        doc = Document()
        doc.add_heading("Documentos Gerados", level=1)

        for i in range(1, 9):
            titulo = PromptsInfo.get_title_etp(i)
            doc.add_heading(titulo, level=1)
            for item in selected:
                prompt = self.search_prompt_etp(i, item)
                print(prompt)
                resposta = self.generate_response(prompt)
                self.insert_prompt(PromptsInfo.get_column_etp(i), resposta, item)
                doc.add_paragraph(resposta)

        self.save_document(doc)
    
    def search_tr_data(self, i, item):
        column_name = PromptsInfo.get_column_tr(i)
        cod_item = self.get_item_code(item)
        query = f"SELECT {column_name} FROM prompt_tr WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt = self.cursor.fetchone()[0]
        return prompt
        
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
            
            self.save_document(doc)

        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')
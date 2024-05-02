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
        self.client = openai.OpenAI(api_key=)  # Usar variável de ambiente

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
        QMessageBox.information(self, 'Documentos gerados!', f'Documento salvo com sucesso em: {caminho_arquivo}')

    def gerar_documento_etp(self, selected):
        try:
            doc = Document()
            doc.add_heading("Documentos Gerados", level=1)
            for i in range(1, 9):
                titulo = PromptsInfo.get_titulo_name(i)
                doc.add_heading(titulo, level=1)
                for _ in selected:
                    prompt_nome = PromptsInfo.get_prompt_name(i)
                    self.cursor.execute(f"SELECT {prompt_nome} FROM prompt_etp;")
                    prompt_valor = self.cursor.fetchone()[0]
                    resposta = self.generate_response(prompt_valor)
                    doc.add_paragraph(resposta)
            self.save_document(doc)
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')

    def gerar_documentos_tr(self, selected):
        try:
            doc = Document()
            doc.add_heading("TERMO DE REFERÊNCIA - TR", level=1)
            for i in range(1, 11):
                titulo = PromptsInfo.get_titulo_tr(i)
                doc.add_heading(text=titulo, level=1)
                for item_selecionado in selected:
                    query = "SELECT distinct item.cod_item, item.descricao_item, prompt_tr.cod_item, prompt_tr.descricao_objeto_tr, prompt_tr.descricao_fundamentacao_contratacao, prompt_tr.descricao_solucao, prompt_tr.requisitos_contratacao, prompt_tr.modelo_execucao_objeto, prompt_tr.modelo_gestao_contrato, prompt_tr.criterios_medicao_pagamento, prompt_tr.criterios_selecao_fornecedor, prompt_tr.estimativas_valor, prompt_tr.adequacao_orcamentaria FROM item JOIN prompt_tr ON item.cod_item = prompt_tr.cod_item WHERE descricao_item = %s"
                    self.cursor.execute(query, (item_selecionado,))
                    record = self.cursor.fetchone()
                    if record[1] == item_selecionado:
                        resposta = self.generate_response()
                        doc.add_paragraph(resposta)
            self.save_document(doc)
        except Exception as e:
            QMessageBox.warning(self, 'Erro ao gerar documentos', f'Ocorreu um erro: {str(e)}')
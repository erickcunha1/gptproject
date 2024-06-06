from datetime import datetime
from pathlib import Path

from PyQt5.QtWidgets import QWidget
from docx import Document
import dotenv
import openai
import os

from prompt import PromptsInfo
from prompt_menager import MenagerPrompt
from testclass import substituir_descricao_objeto, substituir_criterios_sustentabilidade

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
    
    
    def process_response(self, resposta, desc, column_name_etp):
        if column_name_etp == 'descricao_objeto':
            resposta = substituir_descricao_objeto(resposta).replace('$', ' ' + desc + ' ')
        elif column_name_etp == 'requisitos_contratacao':
            resposta = substituir_criterios_sustentabilidade(resposta).replace('$', ' ' + desc + ' ')
        return resposta

    def gerar_documento_etp(self, selected):
        doc = Document()
        doc.add_heading("ETP", level=1)

        for i in range(1, 9):
            titulo = PromptsInfo.get_title_etp(i)
            doc.add_heading(titulo, level=1)
            for item in selected:
                column_name = PromptsInfo.get_column_etp(i)
                prompt_exists = self.prompt_manager.result_exists(item, column_name, 'etp') # Verifica a existência na tabela ETP
                if prompt_exists:
                    resposta = prompt_exists
                else:
                    prompt = self.prompt_manager.search_prompt_etp(i, item)
                    resposta = self.generate_response(prompt)
                    self.prompt_manager.insert_prompt(PromptsInfo.get_column_etp(i), resposta, item)
                doc.add_paragraph(resposta)
        self.save_document(doc)
        
    def gerar_documentos_tr(self, selected):
        doc = Document()
        doc.add_heading("TERMO DE REFERÊNCIA - TR", level=1)

        desc = None
        for i in range(1, 11):
            titulo = PromptsInfo.get_title_tr(i)
            doc.add_heading(text=titulo, level=1)

            column_name = PromptsInfo.get_column_tr(i)
            column_name_etp = PromptsInfo.get_column_etp(i)

            for item in selected:
                result = None
                if column_name_etp:
                    result = self.prompt_manager.result_exists(item, column_name_etp, 'etp')
                    if column_name_etp == 'descricao_objeto' and result:
                        desc = result[:-1]

                prompt_exists = self.prompt_manager.result_exists(item, column_name, 'termo_referencia')

                if prompt_exists and column_name_etp != 'descricao_justificativa' :
                    resposta = prompt_exists
                else:
                    if column_name_etp == 'descricao_justificativa' and self.prompt_manager.result_exists(item, 'descricao_justificativa', 'etp') == None and self.prompt_manager.result_exists(item, 'descricao_fundamentacao_contratacao', 'termo_referencia') == None:
                        prompt_just = self.prompt_manager.search_prompt_etp(2, item)
                        resposta = self.generate_response(prompt_just)
                        self.prompt_manager.insert_prompt_tr(column_name, resposta, item)
                    else:
                        prompt = self.prompt_manager.search_prompt_tr(i, item)
                        resposta = self.generate_response(prompt)
                        self.prompt_manager.insert_prompt_tr(column_name, resposta, item)

                if result and column_name_etp in ['descricao_objeto', 'requisitos_contratacao']:
                    resposta = self.process_response(resposta, desc, column_name_etp)

                doc.add_paragraph(resposta)
        self.save_document(doc)
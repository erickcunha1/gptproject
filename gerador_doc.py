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
    
    
    # def remover_acentos(self, frase):
    #     nfkd = unicodedata.normalize('NFKD', frase)
    #     # Filtra apenas os caracteres que não são marcas de acentuação
    #     frase_sem_acentos = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    #     return frase_sem_acentos

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
            for item in selected:
                column_name = PromptsInfo.get_column_tr(i)
                column_name_etp = PromptsInfo.get_column_etp(i)

                if column_name_etp is not None:
                    result = self.prompt_manager.result_exists(item, column_name_etp, 'etp')
                    if column_name_etp == 'descricao_objeto':
                        string_tamanho = len(result) - 1
                        desc = result[:string_tamanho]
                    # elif column_name_etp == 'requisitos_contratacao':
                    #     string_tamanho = len(result) - 1
                    #     desc = result[:string_tamanho]

                prompt_exists = self.prompt_manager.result_exists(item, column_name, 'termo_referencia') # Verifica a existência na tabela tr
                if prompt_exists:
                    resposta = prompt_exists
                    if result is not None and column_name_etp == 'descricao_objeto':
                        resposta1 = substituir_descricao_objeto(prompt_exists)
                        resposta = resposta1.replace('$', ' ' + desc + ' ')
                    elif result is not None and column_name_etp == 'requisitos_contratacao':
                        resposta1 = substituir_criterios_sustentabilidade(prompt_exists)
                        print(desc)
                        resposta = resposta1.replace('$', ' ' + desc + ' ')
                else:
                    prompt = self.prompt_manager.search_prompt_tr(i, item) 
                    resposta = self.generate_response(prompt)
                    self.prompt_manager.insert_prompt_tr(PromptsInfo.get_column_tr(i), resposta, item)
                doc.add_paragraph(resposta)
        self.save_document(doc)
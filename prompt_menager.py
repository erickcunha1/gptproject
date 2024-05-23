from database import mysql_connection

class MenagerPrompt:
    def __init__(self, host, user, passwd, database=None) -> None:
        self.connection = mysql_connection(host, user, passwd, database)
        self.cursor = self.connection.cursor(buffered=True)
        
    def prompt_exists(self, item, column_name):
        cod = self.get_code_item(item)
        query = f'SELECT {column_name} FROM etp WHERE cod_item = %s'
        self.cursor.execute(query, (cod,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def insert_promt(self, table, column_name, prompt):
        query = f"INSERT INTO {table} ({column_name}) VALUES (?)"
        self.cursor.execute(query, (prompt,))

    def get_code_item(self, desc_item):
        query = "SELECT distinct item.cod_item, item.descricao_item, prompt_tr.cod_item, prompt_tr.descricao_objeto_tr, prompt_tr.descricao_fundamentacao_contratacao, prompt_tr.descricao_solucao, prompt_tr.requisitos_contratacao, prompt_tr.modelo_execucao_objeto, prompt_tr.modelo_gestao_contrato, prompt_tr.criterios_medicao_pagamento, prompt_tr.criterios_selecao_fornecedor, prompt_tr.estimativas_valor, prompt_tr.adequacao_orcamentaria, prompt_tr.id_prompt_tr, prompt_tr.cod_orgao, prompt_tr.cod_unidade FROM item JOIN prompt_tr ON item.cod_item = prompt_tr.cod_item WHERE descricao_item = %s"
        self.cursor.execute(query, (desc_item,))
        result = self.cursor.fetchone()
        print(result[0], result[13], result[14], result[15])
        return str(result[0])
    
    def search_prompt_etp(self, item, column_name):
        cod_item = self.get_code_item(item)
        query = f"SELECT {column_name} FROM prompt_etp WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt = self.cursor.fetchone()[0]
        return prompt
    
    def search_prompt_tr(self, i, item, column_name):
        cod_item = self.get_code_item(item)
        query = f"SELECT {column_name} FROM prompt_tr WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt_valor = self.cursor.fetchone()[0]
        return prompt_valor

from database import mysql_connection
from prompt import PromptsInfo


class MenagerPrompt:
    def __init__(self, host, user, passwd, database=None) -> None:
        self.connection = mysql_connection(host, user, passwd, database)
        self.cursor = self.connection.cursor(buffered=True)
        # self.prompt_info = PromptsInfo()
        
    def result_exists(self, item, column_name, tabela):
        cod = self.get_code_item(item)
        query = f'SELECT {column_name} FROM {tabela} WHERE cod_item = %s'
        self.cursor.execute(query, (cod,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            return None
        
    def insert_prompt(self, column_name, prompt, item):
        query = """SELECT item.cod_item, prompt_etp.id_prompt, prompt_etp.cod_orgao, prompt_etp.cod_unidade 
        FROM item 
        JOIN prompt_etp ON item.cod_item = prompt_etp.cod_item 
        WHERE item.descricao_item = %s"""

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
                self.connection.commit()

            # Em seguida, inserimos o prompt na coluna especificada na tabela `etp`
            update_query = f"UPDATE etp SET {column_name} = %s WHERE cod_item = %s"
            self.cursor.execute(update_query, (prompt, cod_item))
            self.connection.commit()
        else:
            print("Item não encontrado.")

    def insert_prompt_tr(self, column_name, prompt, item):
        try:
            # Query to find the item details and related prompt_tr information
            query = """
            SELECT item.cod_item, prompt_tr.id_prompt_tr, prompt_tr.cod_orgao, prompt_tr.cod_unidade 
            FROM item 
            JOIN prompt_tr ON item.cod_item = prompt_tr.cod_item 
            WHERE item.descricao_item = %s
            """
            self.cursor.execute(query, (item,))
            record = self.cursor.fetchone()

            if record:
                cod_item = record[0]
                id_prompt = record[1]
                cod_orgao = record[2]
                cod_unidade = record[3]

                # Check if there is already a record in termo_referencia for the item
                query2 = "SELECT id_prompt_tr FROM termo_referencia WHERE cod_item = %s"
                self.cursor.execute(query2, (cod_item,))
                existing_record = self.cursor.fetchone()

                if not existing_record:
                    # Insert a new record in termo_referencia if it doesn't exist
                    insert_query = """
                    INSERT INTO termo_referencia (id_prompt_tr, cod_orgao, cod_unidade, cod_item) 
                    VALUES (%s, %s, %s, %s)
                    """
                    self.cursor.execute(insert_query, (id_prompt, cod_orgao, cod_unidade, cod_item))
                    self.connection.commit()

                # Update the specified column with the prompt in termo_referencia table
                update_query = f"UPDATE termo_referencia SET {column_name} = %s WHERE cod_item = %s"
                self.cursor.execute(update_query, (prompt, cod_item))
                self.connection.commit()
            else:
                print("Item não encontrado.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def get_code_item(self, desc):
        first_query = "SELECT cod_item FROM item WHERE descricao_item = %s"
        self.cursor.execute(first_query, (desc,))
        result = self.cursor.fetchone()
        return result[0]
    
    def search_prompt_etp(self, i, item):
        column_name = PromptsInfo.get_column_etp(i)
        cod_item = self.get_code_item(item)
        query = f"SELECT {column_name} FROM prompt_etp WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt = self.cursor.fetchone()[0]
        return prompt
    
    def search_prompt_tr(self, i, item):
        column_name = PromptsInfo.get_column_tr(i)
        cod_item = self.get_code_item(item)
        query = f"SELECT {column_name} FROM prompt_tr WHERE cod_item = %s;"
        self.cursor.execute(query, (cod_item,))
        prompt_valor = self.cursor.fetchone()[0]
        return prompt_valor

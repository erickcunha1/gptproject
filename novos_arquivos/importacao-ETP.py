
# Substitua pelos seus próprios caminhos e credenciais
#caminho_do_arquivo_excel = "c:\temp\pac-importar.xlsx"

import pandas as pd
from pathlib import Path
import MySQLdb

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "gdl"

# Carrega os dados do Excel em um DataFrame
excel_file = Path.home() / "Desktop" / f"importar-ETP.xlsx"
df = pd.read_excel(excel_file, dtype={'cod_unidade': str})

# Conecta ao banco de dados MySQL
db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE)
cursor = db.cursor()

# Nome da tabela no banco de dados
tabela_mysql = "prompt_etp"

# Itera pelas linhas do DataFrame e insere os dados no banco de dados
for index, row in df.iterrows():
    sql = f"INSERT INTO {tabela_mysql} (id_prompt, id, cod_orgao, cod_unidade, cod_item, descricao_objeto, descricao_justificativa, descricao_previsao_contratacao, requisitos_contratacao, descricao_justificativa_quantidade, prompt_estimativa_valor, prompt_fundamentacao_legal, prompt_justificativa_parcelamento, prompt_posicionamento_conclusivo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(sql)
    values = (row["id_prompt"], row["id"], row["cod_orgao"], row["cod_unidade"], row["cod_item"], row["descricao_objeto"], row["descricao_justificativa"], row["descricao_previsao_contratacao"], row["requisitos_contratacao"], row["descricao_justificativa_quantidade"], row["prompt_estimativa_valor"], row["prompt_fundamentacao_legal"], row["prompt_justificativa_parcelamento"], row["prompt_posicionamento_conclusivo"])
    print(values)
    cursor.execute(sql, values)

# Commit das alterações e fechamento da conexão
db.commit()
db.close()

print("Dados importados com sucesso para o banco de dados MySQL!")

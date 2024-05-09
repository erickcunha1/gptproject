
# Substitua pelos seus próprios caminhos e credenciais
#caminho_do_arquivo_excel = "c:\temp\pac-importar.xlsx"

import pandas as pd
from pathlib import Path
import MySQLdb

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "Erick1@3$55"
DB_DATABASE = "gdl"

# Carrega os dados do Excel em um DataFrame
excel_file = Path.home() / "Desktop" / f"importar TR - novo.xlsx"
df = pd.read_excel(excel_file, dtype={'cod_unidade': str})

# Conecta ao banco de dados MySQL
db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE)
cursor = db.cursor()

# Nome da tabela no banco de dados
tabela_mysql = "prompt_tr"

# Itera pelas linhas do DataFrame e insere os dados no banco de dados
for index, row in df.iterrows():
    
    sql = f"INSERT INTO {tabela_mysql} (id_prompt_tr, id_prompt, id, cod_orgao, cod_unidade, cod_item, descricao_objeto_tr, descricao_fundamentacao_contratacao, descricao_solucao, requisitos_contratacao, modelo_execucao_objeto, modelo_gestao_contrato, criterios_medicao_pagamento, criterios_selecao_fornecedor, estimativas_valor, adequacao_orcamentaria ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #print(sql)
    values = (row["id_prompt_tr"], row["id_prompt"], row["id"], row["cod_orgao"], row["cod_unidade"], row["cod_item"], row["descricao_objeto_tr"], row["descricao_fundamentacao_contratacao"], row["descricao_solucao"], row["requisitos_contratacao"], row["modelo_execucao_objeto"], row["modelo_gestao_contrato"], row["criterios_medicao_pagamento"]+row["Prompt7-TR- continuacao"], row["criterios_selecao_fornecedor"]+row["Prompt8-TR- continuacao"]+row["Prompt8-TR- continuacao 1"], row["estimativas_valor"], row["adequacao_orcamentaria"])
    print(values)
    cursor.execute(sql, values)

# Commit das alterações e fechamento da conexão
db.commit()
db.close()

print("Dados importados com sucesso para o banco de dados MySQL!")
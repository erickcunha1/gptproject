import MySQLdb
import math

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "gdl"

# Conecta ao banco de dados MySQL
db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE)
cursor = db.cursor()
import pandas as pd
from pathlib import Path

# Carrega os dados do Excel
excel_file = Path.home() / "Desktop" / "item-importar2.xlsx"

# Tenta evitar NaN ao ler o arquivo
df = pd.read_excel(excel_file, na_filter=False)

# Substitua valores NaN por uma string vazia ou outro valor padrão
df["cod_item"] = df["cod_item"].fillna("")

# Remova espaços em branco
df["cod_item"] = df["cod_item"].str.strip()

# Nome da tabela no banco de dados
tabela_mysql = "item"

# Itera pelas linhas do DataFrame e insere os dados no banco de dados
for index, row in df.iterrows():
    cod_item = row["cod_item"]
    descricao_item = row["descricao_item"]

    # Verifique se 'cod_item' é vazio ou NaN
    if cod_item == "" or isinstance(cod_item, float) and math.isnan(cod_item):
        print(f"Valor 'cod_item' inválido: {cod_item}, linha {index}, ignorado")
        continue  # Pule esta linha e continue com as demais
    try:
        # Inserção no banco de dados
        sql = f"INSERT INTO {tabela_mysql} (cod_item, descricao_item) VALUES (%s, %s)"
        values = (cod_item, descricao_item)
        cursor.execute(sql, values)
    except:
        continue

# Commit das alterações e fechamento da conexão
db.commit()
db.close()

print("Dados importados com sucesso para o banco de dados MySQL!")

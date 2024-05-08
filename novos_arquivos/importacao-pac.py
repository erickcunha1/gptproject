import pandas as pd
from pathlib import Path
import MySQLdb
from MySQLdb import IntegrityError

# Configurações do banco de dados
DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = ""
DB_DATABASE = "gdl"

# Carrega os dados do Excel em um DataFrame
excel_file = Path.home() / "Desktop" / "pac-importar2.xlsx"
df = pd.read_excel(excel_file, dtype={'cod_unidade': str})

# Conecta ao banco de dados MySQL
db = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD, db=DB_DATABASE)
cursor = db.cursor()

# Nome da tabela no banco de dados
tabela_mysql = "pac"

# Itera pelas linhas do DataFrame e insere os dados no banco de dados
try:
    for index, row in df.iterrows():
        sql = f"INSERT INTO {tabela_mysql} (id, cod_orgao, cod_unidade, cod_item, cod_regiao, cod_tipo_item, cod_unidade_medida, qtd_pac, valor_detalhe, valor_estimado, valor_referencial, valor_ultima_compra, valor_total_planejado, qtd_consumo_anterior, cod_almoxarifado, saldo_estoque ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        values = (row["id"], row["cod_orgao"], row["cod_unidade"], row["cod_item"], row["cod_regiao"], row["cod_tipo_item"], row["cod_unidade_medida"], row["qtd_pac"], row["valor_detalhe"], row["valor_estimado"], row["valor_referencial"], row["valor_ultima_compra"], row["valor_total_planejado"], row["qtd_consumo_anterior"], row["cod_almoxarifado"], row["saldo_estoque"])
        cursor.execute(sql, values)

    db.commit()  # Confirma a transação
    print("Dados importados com sucesso para o banco de dados MySQL!")
except IntegrityError as ie:
    print("Erro de integridade ao inserir dados:", ie)
except Exception as ex:
    print("Erro ao inserir dados:", ex)
finally:
    db.close()  # Fecha a conexão

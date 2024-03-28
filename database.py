from mysql.connector import connect


def mysql_connection(host, user, passwd, database=None):
    connection = connect(
        host = host,
        user = user,
        passwd = passwd,
        database = database
    )
    return connection

conexao = mysql_connection('localhost', 'root', 'Erick1@3$5', database='gdl')

if conexao.is_connected():
    print("Conexão bem-sucedida ao banco de dados MySQL")

    # Execute as operações desejadas aqui, por exemplo:
    cursor = conexao.cursor()

    # Exemplo de consulta
    cursor.execute("SELECT descricao_objeto FROM prompt_etp;")
    resultados = cursor.fetchall()

    # Exemplo de impressão dos resultados
    for linha in resultados:
        print(linha[0])

    # Não se esqueça de fechar a conexão e o cursor quando terminar
    cursor.close()
    conexao.close()
else:
    print("Falha na conexão ao banco de dados MySQL")
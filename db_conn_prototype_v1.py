import psycopg2
import datetime

# Dados para a conexao com o banco de dados
dbname = "postgres"
user = "postgres"
password = "root"
host = "localhost"
port = "5432"

# Cria a conexao com o banco
conn = psycopg2.connect(
    dbname=dbname,
    user=user,
    password=password,
    host=host,
    port=port
)

# Cria o cursor
cursor = conn.cursor()

# Menu de cadastro
print('\t|--------------------|')
print('\t| 1. Novo Cadastro')

# Input de qual opcao o usuario escolhe
opcao = int(input('\t| Opcao: '))

# Verificacao da opcao do usuario
if opcao == 1:
    while True:
        NomeCadastro = input('\t| Nome do cadastro:\n\t| > ')
        NumCadastro = int(input('\t| Numero do cadastro:\n\t| > '))
        NumLote = int(input('\t| Numero do Lote: \n\t| > '))
        NumAves = int(input('\t| Numero de aves no lote: \n\t| > '))
        DataCad = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

        # Desconsiderando a PK da tabela
        cursor.execute(f'INSERT INTO "Cadastros" ("ID_Cadastro", "Nome_Cadastro", "ID_Lote", "Num_Aves", "DT_Cadastro")'
                       f'VALUES (%s, %s, %s, %s, %s)', (NumCadastro, NomeCadastro, NumLote, NumAves, DataCad))

        # todo: Funcao que grava os dados no banco!
        conn.commit()

        # Opcao para adicionar um novo cadastro
        add_cad = input('\t| Novo cadastro? (S/N): ').lower()
        if add_cad != 's':

            # Seleciona todos os cadastros e printa
            cursor.execute('SELECT * FROM "Cadastros"')
            for row in cursor:
                print(row)

            # Fecha a conexao do cursor e do banco
            cursor.close()
            conn.close()
            break

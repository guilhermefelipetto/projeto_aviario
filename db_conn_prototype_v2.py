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
cur = conn.cursor()

# Menu de cadastro
print('\t|--------------------|')
print('\t| 1. Novo Cadastro')

# Input de qual opcao o usuario escolhe
menu_op = int(input('\t| Opcao: '))

# Verificacao da opcao do usuario

if menu_op == 1:
    while True:
        # Retorna a ultima linha da tabela
        cur.execute('SELECT "ID_Cadastro" FROM "Cadastros" ORDER BY "ID_Cadastro" DESC LIMIT 1')

        # Salva o valor do ultimo id da coluna 'ID_Cadastro' na variavel 'ultimo_id'
        ultimo_id = None
        for id_cadastro in cur:
            ultimo_id = id_cadastro[0]

        # Recebe os dados para adicionar no banco de dados
        NomeCadastro = input('\t| Nome do cadastro:\n\t| > ')
        NumLote = int(input('\t| Numero do Lote: \n\t| > '))
        NumAves = int(input('\t| Numero de aves no lote: \n\t| > '))
        DataCad = datetime.datetime.now().strftime('%d/%m/%Y %H:%M')

        # Verifica se existe algum ID
        if ultimo_id is not None:
            NumCadastro = ultimo_id + 1
        else:
            NumCadastro = 1

        cur.execute(f'INSERT INTO "Cadastros" ("ID_Cadastro", "Nome_Cadastro", "ID_Lote", "Num_Aves", "DT_Cadastro")'
                    f'VALUES (%s, %s, %s, %s, %s)', (NumCadastro, NomeCadastro, NumLote, NumAves, DataCad))

        # todo: Funcao para gravar mudancas no banco
        conn.commit()

        # Opcao para adicionar um novo cadastro
        add_cad = input('\t| Novo cadastro? (S/N): ').lower()
        if add_cad != 's':

            cur.execute('SELECT * FROM "Cadastros"')
            for row in cur:
                print(row)

            cur.close()
            conn.close()
            break

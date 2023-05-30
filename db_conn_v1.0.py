import psycopg2
import random

# Variaveis para conexao no banco
dbname = "proj_bpk_1_sem"
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

# Gera o cursor
cur = conn.cursor()


def menu_cadastro():
    """
    Exibe o menu de cadastro para gerar um novo cadastro no db
    :return: 
    """
    print('\t### MENU ###\n\n'
          '\t1. Cadastrar novo ambiente\n'
          '\t2. Cadastrar novo sensor de temperatura\n'
          '\t3. Cadastrar novo sensor de umidade\n'
          '\t4. Cadastrar nova balanca'
          '\t5. Cadastrar nova ave'
          '\t6. Cadastrar tipo alimento\n'
          '\t7. Cadastrar alimento\n')
    op = int(input('\t> '))
    if op == 1:
        print('\n\tCadastrando um novo ambiente.\n')
        nome = input('\tNome do novo ambiente: ')
        registra_ambiente(nome)

    elif op == 2:
        print('\n\tCadastrando um novo sensor de temperatura.\n')
        cur.execute('select * from ambiente')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_ambiente = input(
            '\n\tDigite o ID do ambiente para selecionar em qual ambiente cadastrar o novo sensor de temperatura.'
            '\n\t> '
        )
        nome = input('\n\tNome do novo sensor de temperatura: ')
        registra_sensor_temperatura(id_ambiente, nome)

    elif op == 3:
        print('\n\tCadastrando um novo sensor de umidade.\n')
        cur.execute('select * from ambiente')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_ambiente = input(
            '\n\tDigite o ID do ambiente para selecionar em qual ambiente cadastrar o novo sensor de umidade.'
            '\n\t> '
        )
        nome = input('\n\tNome do novo sensor de temperatura: ')
        registra_sensor_umidade(id_ambiente, nome)

    elif op == 4:
        print('\n\tCadastrando uma nova balanca.\n')
        cur.execute('select * from ambiente')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_ambiente = input(
            '\n\tDigite o ID do ambiente para selecionar em qual ambiente cadastrar a nova balanca.'
            '\n\t> '
        )
        nome = input('\n\tNome da nova balanca: ')
        registra_balanca(id_ambiente, nome)

    elif op == 5:
        print('\n\tCadastrando uma nova ave.\n')
        cur.execute('select * from ambiente')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_ambiente = input(
            '\n\tDigite o ID do ambiente para selecionar em qual ambiente cadastrar a nova ave.'
            '\n\t> '
        )
        nome = input('\n\tNome da nova ave: ')
        rfid = random.choice(range(10000, 99999))
        registra_ave(id_ambiente, rfid, nome)

    elif op == 6:
        print('\n\tCadastrando um novo tipo de alimento.\n')
        nome = input('\n\tNome do novo tipo de alimento: ')
        registra_tipo_alimento(nome)

    elif op == 7:
        print('\n\tCadastrando um novo alimento.\n')
        cur.execute('select * from ambiente')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_ambiente = input(
            '\n\tDigite o ID do ambiente para selecionar em qual ambiente cadastrar o tipo de alimento.'
            '\n\t> '
        )
        cur.execute('select * from tipo_alimento')
        for linha in cur:
            print(f'\t{linha[0], linha[1]}\n')
        id_tipo_alimento = input('\n\tDigite o ID do tipo de alimento para selecionar cadastrar o novo alimento'
                                 'do ambiente\n'
                                 '\n\t> ')
        registra_alimento(id_ambiente, id_tipo_alimento)


def registra_ambiente(nome):
    """
    Registra novo ambiente no db
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into ambiente (nome)"
                f"values ('{nome}')")
    conn.commit()


def registra_sensor_temperatura(id_ambiente, nome):
    """
    Registra novo sensor de temperatura no db
    :param id_ambiente: 
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into sensor_temperatura (id_ambiente, nome)"
                f"values ({id_ambiente}, '{nome}')")
    conn.commit()


def registra_sensor_umidade(id_ambiente, nome):
    """
    Registra novo sensor de umidade no db
    :param id_ambiente: 
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into sensor_umidade (id_ambiente, nome)"
                f"values ({id_ambiente}, '{nome}')")


def registra_balanca(id_ambiente, nome):
    """
    Registra nova balanca no db
    :param id_ambiente: 
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into balanca (id_ambiente, nome)"
                f"values ({id_ambiente}, '{nome}')")


def registra_ave(id_ambiente, rfid, nome):
    """
    Registra nova ave no db
    :param id_ambiente: 
    :param rfid: 
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into balanca (rfid, id_ambiente, nome)"
                f"values ({rfid}, {id_ambiente}, '{nome}')")


def registra_tipo_alimento(nome):
    """
    Registra novo tipo de alimento no db
    :param nome: 
    :return: 
    """
    cur.execute(f"insert into tipo_alimento (nome)"
                f"values ('{nome}')")


def registra_alimento(id_ambiente, id_tipo_alimento):
    """
    Registra novo alimento no db
    :param id_ambiente: 
    :param id_tipo_alimento: 
    :return: 
    """
    cur.execute(f"insert into alimento (id_tipo_alimento, id_ambiente)"
                f"values ({id_tipo_alimento}, {id_ambiente})")


def registra_temperatura(id_ambiente, id_sensor_temperatura, valor):
    """
    Registra novo valor de temperatura no db
    :param id_ambiente: 
    :param id_sensor_temperatura: 
    :param valor: 
    :return: 
    """
    cur.execute(f'insert into temperatura (id_sensor_temperatura, id_ambiente, valor)'
                f'values ({id_sensor_temperatura}, {id_ambiente}, {valor})')


def registra_umidade(id_ambiente, id_sensor_temperatura, valor):
    """
    Registra novo valor de umidade no db
    :param id_ambiente: 
    :param id_sensor_temperatura: 
    :param valor: 
    :return: 
    """
    cur.exe(f'insert into umidade (id_sensor_umidade, id_ambiente, valor)'
            f'values ({id_sensor_temperatura}, {id_ambiente}, {valor})')


def registra_peso(id_ambiente, id_balanca, valor):
    """
    Registra novo valor de peso no db
    :param id_ambiente: 
    :param id_balanca: 
    :param valor: 
    :return: 
    """
    cur.execute(f'insert into peso (id_balanca, id_ambiente, valor)'
                f'values ({id_balanca}, {id_ambiente}, {valor})')


# Em construcao
def ativa_sensores():
    while True:
        return 0


# Chama o menu
menu_cadastro()

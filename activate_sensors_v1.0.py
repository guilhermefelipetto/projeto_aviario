import random
from time import sleep

import psycopg2

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


def retorna_lista_id_ambiente():
    # Ambientes
    cur.execute("select id_ambiente from ambiente")
    lista_id_ambiente = []
    for id_ambiente in cur:
        lista_id_ambiente.append(id_ambiente[0])
    return lista_id_ambiente


def retorna_lista_id_sensor_temperatura():
    # Sensor de temperatura
    cur.execute("select id_sensor_temperatura from sensor_temperatura")
    lista_id_sensor_temperatura = []
    for id_sensor_ambiente in cur:
        lista_id_sensor_temperatura.append(id_sensor_ambiente[0])
    return lista_id_sensor_temperatura


def retorna_lista_id_sensor_umidade():
    # Sensor umidade
    cur.execute("select id_sensor_umidade from sensor_umidade")
    lista_id_sensor_umidade = []
    for id_sensor_umidade in cur:
        lista_id_sensor_umidade.append(id_sensor_umidade[0])
    return lista_id_sensor_umidade


def retorna_lista_id_balanca():
    # Balanca
    cur.execute("select id_balanca from balanca")
    lista_id_balanca = []
    for id_balanca in cur:
        lista_id_balanca.append(id_balanca[0])
    return lista_id_balanca


def activate_sensors():
    while True:
        for id_ambiente in range(len(retorna_lista_id_ambiente())):
            for id_sensor_temperatura in range(len(retorna_lista_id_sensor_temperatura())):
                cur.execute("insert into temperatura (id_ambiente, id_sensor_temperatura, valor) "
                            "values (%s, %s, %s)",
                            (retorna_lista_id_ambiente()[id_ambiente], id_sensor_temperatura + 1,
                             round(random.uniform(10, 31), 1)
                             ))
                conn.commit()
                print("dado de TEMPERATURA inserido no banco com sucesso!")
                print(f"ambiente: {id_ambiente}")
            sleep(2)

            for id_sensor_umidade in range(len(retorna_lista_id_sensor_umidade())):
                cur.execute("insert into umidade (id_ambiente, id_sensor_umidade, valor) "
                            "values (%s, %s, %s)",
                            (retorna_lista_id_ambiente()[id_ambiente], id_sensor_umidade + 1,
                             round(random.uniform(10, 16), 1)
                             ))
                conn.commit()
                print("dado de UMIDADE inserido no banco com sucesso!")
                print(f"ambiente: {id_ambiente}")
            sleep(2)

            for id_balanca in range(len(retorna_lista_id_balanca())):
                cur.execute("insert into peso (id_ambiente, id_balanca, valor) "
                            "values (%s, %s, %s)",
                            (retorna_lista_id_ambiente()[id_ambiente], id_balanca + 1,
                             round(random.uniform(2, 6), 1)
                             ))
                conn.commit()
                print("dado de PESO inserido no banco com sucesso!")
                print(f"ambiente: {id_ambiente}")
            sleep(2)


activate_sensors()

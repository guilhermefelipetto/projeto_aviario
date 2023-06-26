import serial
from time import sleep

import psycopg2

# Variaveis para conexao no banco
dbname = "proj_bpk_1_sem"
user = "postgres"
password = "root"
host = "localhost"
port = "5432"


def conecta_banco():
    # Cria a conexao com o banco
    dbconn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )

    # Gera o cursor
    return dbconn.cursor(), dbconn


try:
    cur, conn = conecta_banco()
    sleep(8)
except psycopg2.OperationalError as err:
    cur = None
    conn = None
    print(f'Verifique a conexao com o banco!\nerr: {str(err)}')

# Conexao com o Arduino
porta = 'COM6'  # Porta serial
baud_rate = 9600  # Velocidade de transmissao

# Inicializa a conexao serial
arduino = serial.Serial(porta, baud_rate, timeout=1)

# Aguarda um tempo para a conexao ser estabelecida
arduino.timeout = 2
arduino.write(b'\r\n')
arduino.readline()


def retorna_lista_id_ambiente():
    # Ambientes
    cur.execute("select id_ambiente from ambiente")
    lista_id_ambiente = [id_amb[0] for id_amb in cur]

    return lista_id_ambiente


def retorna_lista_id_sensor_temperatura():
    # Sensor de temperatura
    cur.execute("select id_sensor_temperatura from sensor_temperatura")
    lista_id_sensor_temperatura = [id_sensor_temperatura[0] for id_sensor_temperatura in cur]

    return lista_id_sensor_temperatura


def retorna_lista_id_sensor_umidade():
    # Sensor umidade
    cur.execute("select id_sensor_umidade from sensor_umidade")
    lista_id_sensor_umidade = [id_sensor_umidade[0] for id_sensor_umidade in cur]

    return lista_id_sensor_umidade


def retorna_lista_id_balanca():
    # Balanca
    cur.execute("select id_balanca from balanca")
    lista_id_balanca = [id_balanca[0] for id_balanca in cur]

    return lista_id_balanca


def retorna_lista_id_sensor_luminosidade():
    # Sensor Luminosidade
    cur.execute("select id_sensor_luminosidade from sensor_luminosidade")
    lista_id_sensor_luminosidade = [id_sensor_luminosidade[0] for id_sensor_luminosidade in cur]

    return lista_id_sensor_luminosidade


# Variaveis sensores
t = None  # Temperature
h = None  # Humidity
lx = None  # Lux
p = None  # Peso


sleep(4)

while True:
    # Solicita uma leitura ao Arduino
    arduino.write(b'READ\r\n')

    # Le a resposta do Arduino
    resposta = arduino.readline().decode('utf-8').rstrip()
    print(resposta.split())

    if resposta.split(' ')[0] == 'Load_cell':
        t = float(resposta.split(" ")[3])
        h = float(resposta.split(" ")[5])
        lx = float(resposta.split(" ")[7])
        p = float(resposta.split(" ")[9])

        for id_ambiente in range(len(retorna_lista_id_ambiente())):
            # t
            for id_sensor_temperatura in range(len(retorna_lista_id_sensor_temperatura())):
                if id_ambiente == 0 and id_sensor_temperatura in [0, 1]:
                    cur.execute("insert into temperatura (id_ambiente, id_sensor_temperatura, valor) "
                                "values (%s, %s, %s)",
                                (retorna_lista_id_ambiente()[id_ambiente], id_sensor_temperatura + 1,
                                 round(t, 1)
                                 ))
                    conn.commit()
                    print(f"dado de TEMPERATURA ({t}) inserido no banco com sucesso!")
                    print(f"ambiente: {id_ambiente}")
                elif id_ambiente == 1 and id_sensor_temperatura in [2, 3]:
                    cur.execute("insert into temperatura (id_ambiente, id_sensor_temperatura, valor) "
                                "values (%s, %s, %s)",
                                (retorna_lista_id_ambiente()[id_ambiente], id_sensor_temperatura + 1,
                                 round(t, 1)
                                 ))
                    conn.commit()
                    print("dado de TEMPERATURA inserido no banco com sucesso!")
                    print(f"ambiente: {id_ambiente}")
                sleep(2)

                # h
                for id_sensor_umidade in range(len(retorna_lista_id_sensor_umidade())):
                    if id_ambiente == 0 and id_sensor_umidade in [0, 1]:
                        cur.execute("insert into umidade (id_ambiente, id_sensor_umidade, valor) "
                                    "values (%s, %s, %s)",
                                    (retorna_lista_id_ambiente()[id_ambiente], id_sensor_umidade + 1,
                                     round(h, 1)
                                     ))
                        conn.commit()
                        print("dado de UMIDADE inserido no banco com sucesso!")
                        print(f"ambiente: {id_ambiente}")

                    elif id_ambiente == 1 and id_sensor_umidade in [2, 3]:
                        cur.execute("insert into umidade (id_ambiente, id_sensor_umidade, valor) "
                                    "values (%s, %s, %s)",
                                    (retorna_lista_id_ambiente()[id_ambiente], id_sensor_umidade + 1,
                                     round(h, 1)
                                     ))
                        conn.commit()
                        print("dado de UMIDADE inserido no banco com sucesso!")
                        print(f"ambiente: {id_ambiente}")
                sleep(2)

                # lx
                for id_sensor_luminosidade in range(len(retorna_lista_id_sensor_luminosidade())):
                    if id_ambiente == 0 and id_sensor_luminosidade in [0, 1]:
                        cur.execute("insert into luminosidade (id_ambiente, id_sensor_luminosidade, valor) "
                                    "values (%s, %s, %s)",
                                    (retorna_lista_id_ambiente()[id_ambiente], id_sensor_luminosidade + 1,
                                     round(lx, 1)
                                     ))
                        conn.commit()
                        print("dado de LUMINOSIDADE inserido no banco com sucesso!")
                        print(f"ambiente: {id_ambiente}")

                    elif id_ambiente == 1 and id_sensor_luminosidade in [2, 3]:
                        cur.execute("insert into luminosidade (id_ambiente, id_sensor_luminosidade, valor) "
                                    "values (%s, %s, %s)",
                                    (retorna_lista_id_ambiente()[id_ambiente], id_sensor_luminosidade + 1,
                                     round(lx, 1)
                                     ))
                        conn.commit()
                        print("dado de LUMINOSIDADE inserido no banco com sucesso!")
                        print(f"ambiente: {id_ambiente}")
                sleep(2)

    if resposta.lower() == 'fim':
        cur.close()
        conn.close()
        break

arduino.close()
cur.close()
conn.close()

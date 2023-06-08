import serial
import time

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

# Conexao com o Arduino
porta = 'COM7'  # Porta serial
baud_rate = 9600  # Velocidade de transmissao

# Inicializa a conexao serial
arduino = serial.Serial(porta, baud_rate, timeout=1)

# Aguarda um tempo para a conexao ser estabelecida
arduino.timeout = 2
arduino.write(b'\r\n')
arduino.readline()

# Variaveis sensores
t = None  # temperature
h = None  # humidity


while True:
    # Solicita uma leitura ao Arduino
    arduino.write(b'READ\r\n')

    time.sleep(2)

    # Le a resposta do Arduino
    resposta = arduino.readline().decode('utf-8').rstrip()

    if resposta.split(' ')[0] == 'Temperature:':
        t = float(resposta.split(" ")[1])
        h = float(resposta.split(" ")[3])

        print(f'T: {t}')
        print(f'H: {h}\n')

    if resposta == 'fim':
        cur.close()
        conn.close()
        break

arduino.close()
cur.close()
conn.close()

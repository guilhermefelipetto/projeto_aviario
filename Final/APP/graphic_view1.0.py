import sys

import psycopg2
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, \
    QListWidgetItem, QListWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

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
except psycopg2.OperationalError as err:
    cur = None
    conn = None
    print(f'Verifique a conexao com o banco!\nerr: {str(err)}')

if cur is None or conn is None:
    # Variaveis globais
    var_win_grafico_temperatura = None
    var_win_grafico_umidade = None
    var_win_grafico_luminosidade = None
    var_win_temperatura = None
    var_win_umidade = None
    var_win_luminosidade = None

# Retorna um lista com todos os ambientes registrados
cur.execute("select * from ambiente")
lista_id_ambiente = [f'{linha[1]}: {linha[0]}' for linha in cur]


def cria_janela():
    app = QApplication(sys.argv)
    main_window = QMainWindow()

    # Label do 'Menu'
    nome_ambiente_label = QLabel("Menu de Graficos", main_window)
    nome_ambiente_label.move(20, 20)
    nome_ambiente_label.setFixedSize(150, 30)

    # Graficos

    # Grafico de temperatura
    button_ambiente = QPushButton("Temperatura", main_window)
    button_ambiente.clicked.connect(win_temperatura)
    button_ambiente.move(20, 60)
    button_ambiente.setFixedSize(300, 30)

    # Grafico de umidade
    button_ambiente = QPushButton("Umidade", main_window)
    button_ambiente.clicked.connect(win_umidade)
    button_ambiente.move(20, 100)
    button_ambiente.setFixedSize(300, 30)

    # Grafico de luminosidade
    button_ambiente = QPushButton("Luminosidade", main_window)
    button_ambiente.clicked.connect(win_luminosidade)
    button_ambiente.move(20, 140)
    button_ambiente.setFixedSize(300, 30)

    # Janela principal
    main_window.setGeometry(100, 100, 700, 500)

    main_window.setWindowTitle("Menu de Graficos")
    main_window.show()

    sys.exit(app.exec_())


def win_temperatura():
    global var_win_temperatura

    if var_win_temperatura is None:
        var_win_temperatura = QMainWindow()
        var_win_temperatura.setWindowTitle("Grafico de Temperatura")
        var_win_temperatura.setGeometry(200, 200, 900, 600)

    button_ambiente = QPushButton("Gerar grafico", var_win_temperatura)
    button_ambiente.clicked.connect(lambda: win_grafico_temperatura(int(id_ambiente_input.text())))
    button_ambiente.move(20, 60)
    button_ambiente.setFixedSize(300, 30)

    # Recebe o id do ambiente
    id_ambiente_label = QLabel("Digite um ID de um ambiente cadastrado:", var_win_temperatura)
    id_ambiente_label.move(20, 20)
    id_ambiente_label.setFixedSize(250, 30)

    id_ambiente_input = QLineEdit(var_win_temperatura)
    id_ambiente_input.move(270, 20)
    id_ambiente_input.setFixedSize(100, 30)

    # Mostra todos os id_ambiente registrados
    list_widget = QListWidget(var_win_temperatura)
    list_widget.move(20, 100)
    list_widget.setFixedSize(300, 150)

    for elem in lista_id_ambiente:
        item = QListWidgetItem(elem)
        list_widget.addItem(item)

    var_win_temperatura.show()


def win_umidade():
    global var_win_umidade

    if var_win_umidade is None:
        var_win_umidade = QMainWindow()
        var_win_umidade.setWindowTitle("Grafico de Umidade")
        var_win_umidade.setGeometry(200, 200, 900, 600)

    button_ambiente = QPushButton("Gerar grafico", var_win_umidade)
    button_ambiente.clicked.connect(lambda: win_grafico_umidade(int(id_ambiente_input.text())))
    button_ambiente.move(20, 60)
    button_ambiente.setFixedSize(300, 30)

    # Recebe o id do ambiente
    id_ambiente_label = QLabel("Digite um ID de um ambiente cadastrado:", var_win_umidade)
    id_ambiente_label.move(20, 20)
    id_ambiente_label.setFixedSize(250, 30)

    id_ambiente_input = QLineEdit(var_win_umidade)
    id_ambiente_input.move(270, 20)
    id_ambiente_input.setFixedSize(100, 30)

    # Mostra todos os id_ambiente registrados
    list_widget = QListWidget(var_win_umidade)
    list_widget.move(20, 100)
    list_widget.setFixedSize(300, 150)

    for elem in lista_id_ambiente:
        item = QListWidgetItem(elem)
        list_widget.addItem(item)

    var_win_umidade.show()


def win_luminosidade():
    global var_win_luminosidade

    if var_win_luminosidade is None:
        var_win_luminosidade = QMainWindow()
        var_win_luminosidade.setWindowTitle("Grafico de Luminosidade")
        var_win_luminosidade.setGeometry(200, 200, 900, 600)

    button_ambiente = QPushButton("Gerar grafico", var_win_luminosidade)
    button_ambiente.clicked.connect(lambda: win_grafico_luminosidade(int(id_ambiente_input.text())))
    button_ambiente.move(20, 60)
    button_ambiente.setFixedSize(300, 30)

    # Recebe o id do ambiente
    id_ambiente_label = QLabel("Digite um ID de um ambiente cadastrado:", var_win_luminosidade)
    id_ambiente_label.move(20, 20)
    id_ambiente_label.setFixedSize(250, 30)

    id_ambiente_input = QLineEdit(var_win_luminosidade)
    id_ambiente_input.move(270, 20)
    id_ambiente_input.setFixedSize(100, 30)

    # Mostra todos os id_ambiente registrados
    list_widget = QListWidget(var_win_luminosidade)
    list_widget.move(20, 100)
    list_widget.setFixedSize(300, 150)

    for elem in lista_id_ambiente:
        item = QListWidgetItem(elem)
        list_widget.addItem(item)

    var_win_luminosidade.show()


def win_grafico_temperatura(id_ambiente):
    global var_win_grafico_temperatura

    if var_win_grafico_temperatura is None:
        var_win_grafico_temperatura = QMainWindow()
        var_win_grafico_temperatura.setWindowTitle("Grafico de Temperatura")
        var_win_grafico_temperatura.setGeometry(200, 200, 900, 600)

    # Crie uma figura do Matplotlib
    fig = plt.figure()

    # Crie um widget do Matplotlib para exibir a figura
    canvas = FigureCanvas(fig)

    # Dados para plotagem
    cur.execute(f"select valor from temperatura where id_ambiente = {id_ambiente}")
    temperaturas = [valor[0] for valor in cur]
    leituras = range(1, len(temperaturas) + 1)

    # Plotagem do gráfico de linha
    ax = fig.add_subplot(111)
    ax.plot(leituras, temperaturas, '-o')
    ax.set_xlabel('Nº Leituras')
    ax.set_ylabel('Temperatura (Cº)')

    # Ajuste dos limites dos eixos x e y
    ax.set_xlim(0, len(temperaturas) + 1)
    ax.set_ylim(min(temperaturas) - 1, max(temperaturas) + 1)

    ax.grid(True)

    # Crie um layout vertical e adicione o widget do Matplotlib a ele
    layout = QVBoxLayout()
    layout.addWidget(canvas)

    # Crie um widget central e defina o layout vertical
    central_widget = QWidget(var_win_grafico_temperatura)
    central_widget.setLayout(layout)
    var_win_grafico_temperatura.setCentralWidget(central_widget)

    var_win_grafico_temperatura.show()


def win_grafico_umidade(id_ambiente):
    global var_win_grafico_umidade

    if var_win_grafico_umidade is None:
        var_win_grafico_umidade = QMainWindow()
        var_win_grafico_umidade.setWindowTitle("Grafico de Umidade")
        var_win_grafico_umidade.setGeometry(200, 200, 900, 600)

    # Crie uma figura do Matplotlib
    fig = plt.figure()

    # Crie um widget do Matplotlib para exibir a figura
    canvas = FigureCanvas(fig)

    # Dados para plotagem
    cur.execute(f"select valor from umidade where id_ambiente = {id_ambiente}")
    umidade = [valor[0] for valor in cur]
    leituras = range(1, len(umidade) + 1)

    # Plotagem do gráfico de linha
    ax = fig.add_subplot(111)
    ax.plot(leituras, umidade, '-o')
    ax.set_xlabel('Nº Leituras')
    ax.set_ylabel('Umidade (%)')

    # Ajuste dos limites dos eixos x e y
    ax.set_xlim(0, len(umidade) + 1)
    ax.set_ylim(min(umidade) - 1, max(umidade) + 1)

    ax.grid(True)

    # Crie um layout vertical e adicione o widget do Matplotlib a ele
    layout = QVBoxLayout()
    layout.addWidget(canvas)

    # Crie um widget central e defina o layout vertical
    central_widget = QWidget(var_win_grafico_umidade)
    central_widget.setLayout(layout)
    var_win_grafico_umidade.setCentralWidget(central_widget)

    var_win_grafico_umidade.show()


def win_grafico_luminosidade(id_ambiente):
    global var_win_grafico_luminosidade

    if var_win_grafico_luminosidade is None:
        var_win_grafico_luminosidade = QMainWindow()
        var_win_grafico_luminosidade.setWindowTitle("Grafico de Luminosidade")
        var_win_grafico_luminosidade.setGeometry(200, 200, 900, 600)

    # Crie uma figura do Matplotlib
    fig = plt.figure()

    # Crie um widget do Matplotlib para exibir a figura
    canvas = FigureCanvas(fig)

    # Dados para plotagem
    cur.execute(f"select valor from luminosidade where id_ambiente = {id_ambiente}")
    umidade = [valor[0] for valor in cur]
    leituras = range(1, len(umidade) + 1)

    # Plotagem do gráfico de linha
    ax = fig.add_subplot(111)
    ax.plot(leituras, umidade, '-o')
    ax.set_xlabel('Nº Leituras')
    ax.set_ylabel('Luminosidade (Lx)')

    # Ajuste dos limites dos eixos x e y
    ax.set_xlim(0, len(umidade) + 1)
    ax.set_ylim(min(umidade) - 1, max(umidade) + 1)

    ax.grid(True)

    # Crie um layout vertical e adicione o widget do Matplotlib a ele
    layout = QVBoxLayout()
    layout.addWidget(canvas)

    # Crie um widget central e defina o layout vertical
    central_widget = QWidget(var_win_grafico_luminosidade)
    central_widget.setLayout(layout)
    var_win_grafico_luminosidade.setCentralWidget(central_widget)

    var_win_grafico_luminosidade.show()


if __name__ == "__main__":
    cria_janela()

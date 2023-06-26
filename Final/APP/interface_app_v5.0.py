import sys

import psycopg2

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel, QListWidget, QListWidgetItem,\
    QVBoxLayout, QHBoxLayout, QWidget

# todo - linguagem QML -> PyQt5

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


def verifica_ambiente_reg():
    verifica_ambiente = None
    # Verifica se ha algum ambiente registrado
    cur.execute("select id_ambiente from ambiente")
    lista_verificadora_id_ambiente = [linha for linha in cur]

    if len(lista_verificadora_id_ambiente) <= 0:
        verifica_ambiente = False
    elif len(lista_verificadora_id_ambiente) >= 1:
        verifica_ambiente = True

    return verifica_ambiente


# Verifica se a conexao foi estabelecida
if cur or conn is None:
    # Variaveis globais
    var_janela_registra_ambiente = None
    var_janela_registra_sensor_temperatura = None
    var_janela_registra_sensor_umidade = None
    var_janela_registra_sensor_luminosidade = None
    var_janela_registra_balanca = None
    var_janela_registra_ave = None
    var_janela_registra_tipo_alimento = None
    var_janela_registra_alimento = None
    var_janela_zero_ambientes = None

    # Retorna um lista com todos os ambientes registrados
    cur.execute("select * from ambiente")
    lista_id_ambiente = [f'{linha[1]}: {linha[0]}' for linha in cur]

    # Retorna uma lista com todos os IDs dos tipos de alimentos registrados
    cur.execute("select * from tipo_alimento")
    lista_id_tipo_alimento = [f'{linha[1]}: {linha[0]}' for linha in cur]

    verifica_ambiente_registrado = verifica_ambiente_reg()

    # Verifica se ha algum tipo de alimento registrado
    cur.execute("select id_tipo_alimento from tipo_alimento")
    lista_verificadora_id_tipo_alimento = [linha for linha in cur]

    if len(lista_verificadora_id_tipo_alimento) <= 0:
        verifica_tipo_alimento_registrado = False
    elif len(lista_verificadora_id_tipo_alimento) >= 1:
        verifica_tipo_alimento_registrado = True


    @pyqtSlot()
    def registra_ambiente(nome):
        """
        Registra novo ambiente no db
        :param nome:
        :return:
        """
        cur.execute(f"insert into ambiente (nome)"
                    f"values ('{nome}')")
        conn.commit()
        global verifica_ambiente_registrado
        verifica_ambiente_registrado = verifica_ambiente_reg()


    @pyqtSlot()
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


    @pyqtSlot()
    def registra_sensor_umidade(id_ambiente, nome):
        """
        Registra novo sensor de umidade no db
        :param id_ambiente:
        :param nome:
        :return:
        """
        cur.execute(f"insert into sensor_umidade (id_ambiente, nome)"
                    f"values ({id_ambiente}, '{nome}')")
        conn.commit()


    @pyqtSlot()
    def registra_sensor_luminosidade(id_ambiente, nome):
        """
        Registra novo sensor de luminosidade no db
        :param id_ambiente:
        :param nome:
        :return:
        """
        cur.execute(f"insert into sensor_luminosidade (id_ambiente, nome)"
                    f"values ({id_ambiente}, '{nome}')")
        conn.commit()


    @pyqtSlot()
    def registra_balanca(id_ambiente, nome):
        """
        Registra nova balanca no db
        :param id_ambiente:
        :param nome:
        :return:
        """
        cur.execute(f"insert into balanca (id_ambiente, nome)"
                    f"values ({id_ambiente}, '{nome}')")
        conn.commit()


    @pyqtSlot()
    def registra_ave(id_ambiente, rfid, nome):
        """
        Registra nova ave no db
        :param id_ambiente:
        :param rfid:
        :param nome:
        :return:
        """
        cur.execute(f"insert into aves (rfid, id_ambiente, nome)"
                    f"values ({rfid}, {id_ambiente}, '{nome}')")
        conn.commit()


    @pyqtSlot()
    def registra_tipo_alimento(nome):
        """
        Registra novo tipo de alimento no db
        :param nome:
        :return:
        """
        cur.execute(f"insert into tipo_alimento (nome)"
                    f"values ('{nome}')")
        conn.commit()


    @pyqtSlot()
    def registra_alimento(id_ambiente, id_tipo_alimento):
        """
        Registra novo alimento no db
        :param id_ambiente:
        :param id_tipo_alimento:
        :return:
        """
        cur.execute(f"insert into alimento (id_tipo_alimento, id_ambiente)"
                    f"values ({id_tipo_alimento}, {id_ambiente})")
        conn.commit()


    def registra_temperatura(id_ambiente, id_sensor_temperatura, valor):
        """
        Registra novo valor de temperatura no db
        :param id_ambiente:
        :param id_sensor_temperatura:
        :param valor:
        :return:
        """
        cur.execute("insert into temperatura (id_sensor_temperatura, id_ambiente, valor)"
                    f"values ({id_sensor_temperatura}, {id_ambiente}, {valor})")
        conn.commit()


    def registra_luminosidade(id_ambiente, id_sensor_luminosidade, valor):
        """
        Registtra novo valor de luminosidade no db
        :param id_ambiente:
        :param id_sensor_luminosidade:
        :param valor:
        :return:
        """
        cur.execute("insert into luminosidade (id_sensor_luminosidade, id_ambiente, valor)"
                    f"values ({id_sensor_luminosidade}, {id_ambiente}, {valor})")
        conn.commit()


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
        conn.commit()


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
        conn.commit()

    # Janela principal
    def cria_janela():
        # Cria a janela
        app = QApplication(sys.argv)
        main_window = QMainWindow()

        # Label do 'Menu'
        nome_ambiente_label = QLabel("Menu de cadastro", main_window)
        nome_ambiente_label.move(20, 20)
        nome_ambiente_label.setFixedSize(150, 30)

        # Define os botoes de registro

        # Registra ambiente
        button_ambiente = QPushButton("Registrar novo ambiente", main_window)
        button_ambiente.clicked.connect(janela_registra_ambiente)
        button_ambiente.move(20, 60)
        button_ambiente.setFixedSize(300, 30)

        # Registra sensor temperatura
        button_sensor_temperatura = QPushButton("Registrar novo sensor de temperatura", main_window)
        button_sensor_temperatura.clicked.connect(janela_registra_sensor_temperatura)
        button_sensor_temperatura.move(20, 100)
        button_sensor_temperatura.setFixedSize(300, 30)

        # Registra sensor umidade
        button_sensor_umidade = QPushButton("Registrar novo sensor de umidade", main_window)
        button_sensor_umidade.clicked.connect(janela_registra_sensor_umidade)
        button_sensor_umidade.move(20, 140)
        button_sensor_umidade.setFixedSize(300, 30)

        # Registrta sensor luminosidade
        button_sensor_luminosidade = QPushButton("Registrar novo sensor de luminosidade", main_window)
        button_sensor_luminosidade.clicked.connect(janela_registra_sensor_luminosidade)
        button_sensor_luminosidade.move(20, 180)
        button_sensor_luminosidade.setFixedSize(300, 30)

        # Registra balanca
        button_balanca = QPushButton("Registrar nova balanca", main_window)
        button_balanca.clicked.connect(janela_registra_balanca)
        button_balanca.move(20, 220)
        button_balanca.setFixedSize(300, 30)

        # Registra ave
        button_ave = QPushButton("Registrar nova ave", main_window)
        button_ave.clicked.connect(janela_registra_ave)
        button_ave.move(20, 260)
        button_ave.setFixedSize(300, 30)

        # Registra tipo alimento
        button_tipo_alimento = QPushButton("Registrar novo tipo de alimento", main_window)
        button_tipo_alimento.clicked.connect(janela_registra_tipo_alimento)
        button_tipo_alimento.move(20, 300)
        button_tipo_alimento.setFixedSize(300, 30)

        # Registra alimento
        button_alimento = QPushButton("Registrar novo alimento", main_window)
        button_alimento.clicked.connect(janela_registra_alimento)
        button_alimento.move(20, 340)
        button_alimento.setFixedSize(300, 30)

        # Define o tamanho da janela
        main_window.setGeometry(100, 100, 700, 525)

        # Define o nome da janela e abre a janela maximizada
        main_window.setWindowTitle("Menu de Cadastro")
        main_window.show()

        sys.exit(app.exec_())


    def janela_registra_ambiente():
        global var_janela_registra_ambiente

        if var_janela_registra_ambiente is None:
            var_janela_registra_ambiente = QMainWindow()
            var_janela_registra_ambiente.setWindowTitle("Registrar Ambiente")
            var_janela_registra_ambiente.setGeometry(200, 200, 500, 300)

            # Registra o ambiente no banco
            button = QPushButton("Registrar novo ambiente", var_janela_registra_ambiente)
            button.clicked.connect(lambda: [registra_ambiente(nome_ambiente_input.text()),
                                            var_janela_registra_ambiente.close()])
            button.move(20, 60)
            button.setFixedSize(200, 30)

            # Recebe o nome do ambiente
            nome_ambiente_label = QLabel("Nome do ambiente:", var_janela_registra_ambiente)
            nome_ambiente_label.move(20, 20)
            nome_ambiente_label.setFixedSize(120, 30)

            nome_ambiente_input = QLineEdit(var_janela_registra_ambiente)
            nome_ambiente_input.move(140, 20)
            nome_ambiente_input.setFixedSize(150, 30)

            var_janela_registra_ambiente.show()


    def janela_registra_sensor_temperatura():
        global var_janela_registra_sensor_temperatura

        # Verifica se ha pelo menos 1 ambiente registrado
        if verifica_ambiente_registrado is False:
            var_janela_registra_sensor_temperatura = True
            if var_janela_registra_sensor_temperatura is True:
                janela_zero_ambientes()

        if var_janela_registra_sensor_temperatura is None:
            var_janela_registra_sensor_temperatura = QMainWindow()
            var_janela_registra_sensor_temperatura.setWindowTitle("Registrar sensor de temperatura")
            var_janela_registra_sensor_temperatura.setGeometry(200, 200, 1200, 800)

            # Registra o sensor de temperatura
            button = QPushButton("Registrar novo sensor de temperatura", var_janela_registra_sensor_temperatura)
            button.clicked.connect(lambda: [registra_sensor_temperatura(int(id_ambiente_input.text()),
                                                                        nome_sensor_temperatura_input.text()),
                                            var_janela_registra_sensor_temperatura.close()])
            button.move(20, 100)
            button.setFixedSize(300, 30)

            # Recebe o nome do sensor de temperatura
            nome_sensor_temperatura_label = QLabel("Nome do sensor de temperatura:",
                                                   var_janela_registra_sensor_temperatura)
            nome_sensor_temperatura_label.move(20, 20)
            nome_sensor_temperatura_label.setFixedSize(200, 30)

            nome_sensor_temperatura_input = QLineEdit(var_janela_registra_sensor_temperatura)
            nome_sensor_temperatura_input.move(220, 20)
            nome_sensor_temperatura_input.setFixedSize(150, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite um ID de um ambiente cadastrado:",
                                       var_janela_registra_sensor_temperatura)
            id_ambiente_label.move(20, 60)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_sensor_temperatura)
            id_ambiente_input.move(270, 60)
            id_ambiente_input.setFixedSize(100, 30)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_sensor_temperatura)
            list_widget.move(20, 150)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            var_janela_registra_sensor_temperatura.show()


    def janela_registra_sensor_umidade():
        global var_janela_registra_sensor_umidade

        # Verifica se ha pelo menos 1 ambiente registrado
        if verifica_ambiente_registrado is False:
            var_janela_registra_sensor_umidade = True
            if var_janela_registra_sensor_umidade is True:
                janela_zero_ambientes()

        if var_janela_registra_sensor_umidade is None:
            var_janela_registra_sensor_umidade = QMainWindow()
            var_janela_registra_sensor_umidade.setWindowTitle("Registrar sensor de temperatura")
            var_janela_registra_sensor_umidade.setGeometry(200, 200, 700, 500)

            # Registra o sensor de umidade
            button = QPushButton("Registrar novo sensor de umidade", var_janela_registra_sensor_umidade)
            button.clicked.connect(lambda: [registra_sensor_umidade(int(id_ambiente_input.text()),
                                                                    nome_sensor_umidade_input.text()),
                                            var_janela_registra_sensor_umidade.close()])
            button.move(20, 100)
            button.setFixedSize(300, 30)

            # Recebe o nome do sensor de umidade
            nome_sensor_umidade_label = QLabel("Nome do sensor de umidade:", var_janela_registra_sensor_umidade)
            nome_sensor_umidade_label.move(20, 20)
            nome_sensor_umidade_label.setFixedSize(200, 30)

            nome_sensor_umidade_input = QLineEdit(var_janela_registra_sensor_umidade)
            nome_sensor_umidade_input.move(200, 20)
            nome_sensor_umidade_input.setFixedSize(170, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite um ID de um ambiente cadastrado:", var_janela_registra_sensor_umidade)
            id_ambiente_label.move(20, 60)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_sensor_umidade)
            id_ambiente_input.move(270, 60)
            id_ambiente_input.setFixedSize(100, 30)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_sensor_umidade)
            list_widget.move(20, 150)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            var_janela_registra_sensor_umidade.show()


    def janela_registra_sensor_luminosidade():
        global var_janela_registra_sensor_luminosidade

        # Verifica se ha pelo menos 1 ambiente registrado
        if verifica_ambiente_registrado is False:
            var_janela_registra_sensor_luminosidade = True
            if var_janela_registra_sensor_luminosidade is True:
                janela_zero_ambientes()

        if var_janela_registra_sensor_luminosidade is None:
            var_janela_registra_sensor_luminosidade = QMainWindow()
            var_janela_registra_sensor_luminosidade.setWindowTitle("Registrar sensor de luminosidade")
            var_janela_registra_sensor_luminosidade.setGeometry(200, 200, 700, 500)

            # Registra sensor de luminosidade
            button = QPushButton("Registrar novo sensor de luminosidade", var_janela_registra_sensor_luminosidade)
            button.clicked.connect(lambda: [registra_sensor_luminosidade(int(id_ambiente_input.text()),
                                                                         nome_sensor_luminosidade_input.text()),
                                            var_janela_registra_sensor_luminosidade.close()])
            button.move(20, 100)
            button.setFixedSize(300, 30)

            # Recebe o nome do sensor de luminosidade
            nome_sensor_luminosidade_label = QLabel("Nome do sensor de luminosidade:",
                                                    var_janela_registra_sensor_luminosidade)
            nome_sensor_luminosidade_label.move(20, 20)
            nome_sensor_luminosidade_label.setFixedSize(250, 30)

            nome_sensor_luminosidade_input = QLineEdit(var_janela_registra_sensor_luminosidade)
            nome_sensor_luminosidade_input.move(220, 20)
            nome_sensor_luminosidade_input.setFixedSize(170, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite o ID de um ambiente cadastrado:",
                                       var_janela_registra_sensor_luminosidade)
            id_ambiente_label.move(20, 60)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_sensor_luminosidade)
            id_ambiente_input.move(250, 60)
            id_ambiente_input.setFixedSize(140, 30)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_sensor_luminosidade)
            list_widget.move(20, 150)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            var_janela_registra_sensor_luminosidade.show()


    def janela_registra_balanca():
        global var_janela_registra_balanca

        # Verifica se ha pelo menos 1 ambiente registrado
        if verifica_ambiente_registrado is False:
            var_janela_registra_balanca = True
            if var_janela_registra_balanca is True:
                janela_zero_ambientes()

        if var_janela_registra_balanca is None:
            var_janela_registra_balanca = QMainWindow()
            var_janela_registra_balanca.setWindowTitle("Registrar nova balanca")
            var_janela_registra_balanca.setGeometry(200, 200, 700, 500)

            # Registra nova balanca
            button = QPushButton("Registrar nova balanca", var_janela_registra_balanca)
            button.clicked.connect(lambda: [registra_balanca(int(id_ambiente_input.text()),
                                                             nome_balanca_input.text()),
                                            var_janela_registra_balanca.close()])
            button.move(20, 100)
            button.setFixedSize(300, 30)

            # Recebe o nome da balanca
            nome_balanca_label = QLabel("Nome da balanca:", var_janela_registra_balanca)
            nome_balanca_label.move(20, 20)
            nome_balanca_label.setFixedSize(200, 30)

            nome_balanca_input = QLineEdit(var_janela_registra_balanca)
            nome_balanca_input.move(140, 20)
            nome_balanca_input.setFixedSize(230, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite um ID de um ambiente registrado:", var_janela_registra_balanca)
            id_ambiente_label.move(20, 60)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_balanca)
            id_ambiente_input.move(270, 60)
            id_ambiente_input.setFixedSize(100, 30)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_balanca)
            list_widget.move(20, 150)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            var_janela_registra_balanca.show()


    def janela_registra_ave():
        global var_janela_registra_ave

        if verifica_ambiente_registrado is False:
            var_janela_registra_ave = True
            if var_janela_registra_ave is True:
                janela_zero_ambientes()

        if var_janela_registra_ave is None:
            var_janela_registra_ave = QMainWindow()
            var_janela_registra_ave.setWindowTitle("Registrar nova ave")
            var_janela_registra_ave.setGeometry(200, 200, 700, 500)

            # Registra nova ave
            button = QPushButton("Registrar nova ave", var_janela_registra_ave)
            button.clicked.connect(lambda: [registra_ave(int(id_ambiente_input.text()), int(rfid_input.text()),
                                                         nome_ave_input.text()),
                                            var_janela_registra_ave.close()])
            button.move(20, 140)
            button.setFixedSize(300, 30)

            # Recebe o nome da ave
            nome_ave_label = QLabel("Nome da ave:", var_janela_registra_ave)
            nome_ave_label.move(20, 20)
            nome_ave_label.setFixedSize(200, 30)

            nome_ave_input = QLineEdit(var_janela_registra_ave)
            nome_ave_input.move(110, 20)
            nome_ave_input.setFixedSize(260, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite um ID de um ambiente registrado:", var_janela_registra_ave)
            id_ambiente_label.move(20, 60)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_ave)
            id_ambiente_input.move(270, 60)
            id_ambiente_input.setFixedSize(100, 30)

            # Recebe o rfid da ave
            rfid_label = QLabel("RFID da ave:", var_janela_registra_ave)
            rfid_label.move(20, 100)
            rfid_label.setFixedSize(100, 30)

            rfid_input = QLineEdit(var_janela_registra_ave)
            rfid_input.move(110, 100)
            rfid_input.setFixedSize(260, 30)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_ave)
            list_widget.move(20, 180)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            var_janela_registra_ave.show()


    def janela_registra_tipo_alimento():
        global var_janela_registra_tipo_alimento

        if var_janela_registra_tipo_alimento is None:
            var_janela_registra_tipo_alimento = QMainWindow()
            var_janela_registra_tipo_alimento.setWindowTitle("Registrar novo tipo de alimento")
            var_janela_registra_tipo_alimento.setGeometry(200, 200, 500, 300)

            # Registra o tipo alimento no banco
            button = QPushButton("Registrar novo tipo de alimento", var_janela_registra_tipo_alimento)
            button.clicked.connect(lambda: [registra_tipo_alimento(nome_tipo_alimento_input.text()),
                                            var_janela_registra_tipo_alimento.close()])
            button.move(20, 60)
            button.setFixedSize(200, 30)

            # Recebe o nome do ambiente
            nome_tipo_alimento_label = QLabel("Nome do tipo de alimento:", var_janela_registra_tipo_alimento)
            nome_tipo_alimento_label.move(20, 20)
            nome_tipo_alimento_label.setFixedSize(150, 30)

            nome_tipo_alimento_input = QLineEdit(var_janela_registra_tipo_alimento)
            nome_tipo_alimento_input.move(180, 20)
            nome_tipo_alimento_input.setFixedSize(170, 30)

            var_janela_registra_tipo_alimento.show()


    def janela_registra_alimento():
        global var_janela_registra_alimento

        if verifica_ambiente_registrado is False or verifica_tipo_alimento_registrado is False:
            var_janela_registra_alimento = True
            if var_janela_registra_alimento is True:
                janela_zero_ambientes()

        if var_janela_registra_alimento is None:
            var_janela_registra_alimento = QMainWindow()
            var_janela_registra_alimento.setWindowTitle("Registrar novo alimento")
            var_janela_registra_alimento.setGeometry(200, 200, 850, 500)

            # Registra o alimento no banco
            button = QPushButton("Registrar novo alimento", var_janela_registra_alimento)
            button.clicked.connect(lambda: [registra_alimento(int(id_ambiente_input.text()),
                                                              int(id_tipo_alimento_input.text())),
                                            var_janela_registra_alimento.close()])
            button.move(20, 100)
            button.setFixedSize(200, 30)

            # Recebe o id do ambiente
            id_ambiente_label = QLabel("Digite um ID de um ambiente registrado:", var_janela_registra_alimento)
            id_ambiente_label.move(20, 20)
            id_ambiente_label.setFixedSize(250, 30)

            id_ambiente_input = QLineEdit(var_janela_registra_alimento)
            id_ambiente_input.move(260, 20)
            id_ambiente_input.setFixedSize(140, 30)

            # Recebe o id do tipo do alimento
            id_tipo_alimento_label = QLabel("Digite um ID de um tipo de alimento registrado:",
                                            var_janela_registra_alimento)
            id_tipo_alimento_label.move(20, 60)
            id_tipo_alimento_label.setFixedSize(280, 30)

            id_tipo_alimento_input = QLineEdit(var_janela_registra_alimento)
            id_tipo_alimento_input.move(300, 60)

            # Mostra todos os id_ambiente registrados
            list_widget = QListWidget(var_janela_registra_alimento)
            list_widget.move(20, 150)
            list_widget.setFixedSize(300, 150)

            for elem in lista_id_ambiente:
                item = QListWidgetItem(elem)
                list_widget.addItem(item)

            # Mostra todos os id_tipo_alimento registrados
            list_widget_alimento = QListWidget(var_janela_registra_alimento)
            list_widget_alimento.move(350, 150)
            list_widget_alimento.setFixedSize(300, 150)

            for elem in lista_id_tipo_alimento:
                item = QListWidgetItem(elem)
                list_widget_alimento.addItem(item)

            var_janela_registra_alimento.show()


    def janela_zero_ambientes():
        global var_janela_zero_ambientes

        if var_janela_zero_ambientes is None:
            var_janela_zero_ambientes = QMainWindow()
            var_janela_zero_ambientes.setWindowTitle("Zero ambientes cadastrados")
            var_janela_zero_ambientes.setGeometry(200, 200, 700, 500)

            # Label
            zero_ambientes = QLabel("Voce precisa cadastrar um ambiente primeiro!\n"
                                    "Cadastre um ambiente e reinicie a aplicacao!", var_janela_zero_ambientes)
            zero_ambientes.move(20, 20)
            zero_ambientes.setFixedSize(400, 70)

            var_janela_zero_ambientes.show()

    cria_janela()

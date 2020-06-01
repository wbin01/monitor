#!/usr/bin/env python3
import time
import os


class Monitor(object):
    """docstring for Monitor"""
    model = None

    def __init__(self,
                 value=5, columns=10,
                 scale_character="|", space_character="⎺",
                 scale_color="green-dark",
                 space_color="blue-dark"):
        # O modelo é uma lista com os valore do último gráfico que foi usado
        # normalmente se inicia com None para que o primeiro modelo seja criado por
        # essa classe. essa função retorna um modelo que pode ser repassado de volta em um loop

        self.value = value
        self.columns = columns
        self.scale_character = scale_character
        self.space_character = space_character
        self.scale_color = scale_color
        self.space_color = space_color

        self.model = self.get_model()
        self.set_model(self.model)

        self.colors = {
            "clean": "\033[0m",

            "red": "\033[0m\033[0;31m",
            "red-bold": "\033[0m\033[1;31m",
            "red-dark": "\033[0m\033[2;31m",
            "red-background": "\033[0m\033[0;31;41m",

            "green": "\033[0m\033[0;32m",
            "green-bold": "\033[0m\033[1;32m",
            "green-dark": "\033[0m\033[2;32m",
            "green-background": "\033[0m\033[0;32;42m",

            "yellow": "\033[0m\033[0;33m",
            "yellow-bold": "\033[0m\033[1;33m",
            "yellow-dark": "\033[0m\033[2;33m",
            "yellow-background": "\033[0m\033[0;33;43m",

            "blue": "\033[0m\033[0;34m",
            "blue-bold": "\033[0m\033[1;34m",
            "blue-dark": "\033[0m\033[2;34m",
            "blue-background": "\033[0m\033[0;34;44m",

            "purple": "\033[0m\033[0;35m",
            "purple-bold": "\033[0m\033[1;35m",
            "purple-dark": "\033[0m\033[2;35m",
            "purple-background": "\033[0m\033[0;35;45m",

            "cyan": "\033[0m\033[0;36m",
            "cyan-bold": "\033[0m\033[1;36m",
            "cyan-dark": "\033[0m\033[2;36m",
            "cyan-background": "\033[0m\033[0;36;46m",

            "white": "\033[0m\033[0;37m",
            "white-bold": "\033[0m\033[1;37m",
            "white-dark": "\033[0m\033[2;37m",
            "white-background": "\033[0m\033[0;37;47m",
        }

    def get_model(self):
        if self.model is None:
            m = list()
            for column in range(self.columns):
                m.append(0)

            self.model = m

        return self.model

    def get_as_list(self, value):

        # Criando uma lista de modelo
        #  * ** ***** ** *
        # [101101111101101] 

        # Lista do tamanho da quantidade de colunas e valores zerados
        if self.model is None:
            self.model = self.get_model()

        # O ultimo item da lista sempre será atualizado.
        self.model.append(value)
        # Devolve tamanho da lista
        del self.model[0]

        # Criar um modelo de string (desenho) com informação do modelo de valores inteiro
        # [0    , 3    , 2    , 5    ]
        # [-----, ***--, **---, *****]
        model_draw = list()
        for m in self.model:
            # quantidade de caracteres vai ser a quantidade do valor
            item = self.scale_character * m

            # Preencher o resto da linha onde é o "vazio", com outro caractere
            fill = ""
            # as colunas são sempre uma escala de 10 %, i.e de 10 em 10
            if m < 10:
                # resto faltante
                rest = 10 - m
                fill = self.space_character * rest

            # Preencher
            item = item + fill

            # Uma linha foi criada
            model_draw.append(item)

        # pegar lista de caracteres e criar uma lista com os valores em
        # que são exibido, na horizontal
        #
        # [0    , 3    , 2    , 5    ]  Modelo de inteiro
        #
        # [-----, ***--, **---, *****]  Modelo de string
        #
        # [---*]                        Modelo para print()
        # [---*]
        # [-*-*]
        # [-***]
        # [-***]
        #  0325

        # Pega o caractere de cima de todos os itens, e cria uma lista
        # depois os próximos caracteres e faz outra lista ...
        model_print = list()
        nc = 9  # de zero a 9 são 10
        for r in range(10):  # Altura da coluna
            character = ""
            for i in model_draw:
                character = character + i[nc]

            model_print.append(character)
            nc -= 1

        return model_print

    def get_as_color_list(self, value):
        as_list = self.get_as_list(value)
        model_print = list()
        for i in as_list:
            model_print.append(i.replace(
                self.scale_character, self.colors[self.scale_color] + self.scale_character + self.colors["clean"]
                ).replace(
                self.space_character, self.colors[self.space_color] + self.space_character + self.colors["clean"]
                )
            )

        return model_print

    def get_as_str(self, value):
        # [---*]
        # [---*]
        # [-*-*]
        # [-***]
        # [-***]
        #  0325
        #
        # "---*
        #  ---*
        #  -*-*
        #  -***
        #  -***"
        #  0325
        as_list = self.get_as_list(value)
        model_str = ""
        for i in as_list:
            model_str = model_str + i + "\n"

        str_print = model_str.rstrip("\n")

        return str_print

    def get_as_color_str(self, value):
        as_str = self.get_as_str(value)
        as_str = as_str.replace(
            self.scale_character, self.colors[self.scale_color] + self.scale_character + self.colors["clean"]
        ).replace(
            self.space_character, self.colors[self.space_color] + self.space_character + self.colors["clean"]
        )

        return as_str

    def set_model(self, new_model):
        self.model = new_model


if __name__ == '__main__':
    import random
    # Valor inicial do monitoramento
    v = 0
    # O modelo inicial do monitoramento (O modelo é uma lista de valores de um gráfico)
    model = None
    # Flag para inverter números aleatórios
    inverse = False

    # Criar 2 monitores
    blue_monitor = Monitor(columns=50, scale_color="blue", space_color="blue-dark")
    blue_model = blue_monitor.get_model()
    blue_monitor.set_model(blue_model)

    red_monitor = Monitor(columns=50, scale_color="red", space_color="red-dark", scale_character="+")
    red_model = red_monitor.get_model()
    red_monitor.set_model(red_model)

    while True:
        # Gerar números aleatórios de 0 a 10
        # Inverte ordem para decrementar ou incrementar
        if inverse:
            v -= random.randrange(0, 2)
        else:
            v += random.randrange(0, 2)

        # Se chegar a 10, inverte ordem para decrementar
        if v >= 10:
            inverse = True
            v = random.randrange(5, 10)  # Não deixa passar de 10

        # Se chegar a 0, inverte ordem para incrementar
        elif v <= 0:
            inverse = False
            v = random.randrange(0, 5)  # Não deixa ser menor que 0

        os.system("clear")

        # Monitor como string. Exibe em um só print
        blue = blue_monitor.get_as_color_str(v)
        blue_model = blue_monitor.get_model()
        print(blue)

        print()

        # Monitor como lista. Exibe em um "for".
        # Bom para colocar informações antes e depois das linhas.
        red = red_monitor.get_as_color_list(v)
        red_model = red_monitor.get_model()

        n = 100
        for p in red:
            num_str = str(n)
            if n < 100:
                num_str = " " + str(n)

            print(num_str + " % |", p)
            n -= 10

        print("        " + "-" * 50)
        print("       0    1    2    3    4    5    6    7    8    9    10")

        time.sleep(0.1)

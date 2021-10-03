#!/usr/bin/env python3


class Monitor(object):
    """Monitor em tempo real. cria um gráfico com um valor"""

    __history = dict()

    def __init__(self,
                 value=5,
                 columns=10,
                 lines=10,
                 primary_character="|",
                 secondary_character="⎺",
                 primary_color="green-dark",
                 secondary_color="blue-dark"):
        """
        Inicia a classe.
        :type value: int
        :type columns: int
        :type lines: int
        :type primary_character: str
        :type secondary_character: str
        :type primary_color: str
        :type secondary_color: str
        """
        self.__value = value
        self.__columns = columns
        self.__lines = lines
        self.__primary_character = primary_character
        self.__secondary_character = secondary_character
        self.__primary_color = primary_color
        self.__secondary_color = secondary_color

        self.__colors = {
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
        
        # Se não houver histórico
        if id(self) not in self.__history:
            self.__history[id(self)] = [0 for i in range(self.__columns)]

    def get_as_list(self, value: int):
        """Retorna uma lista com as linhas que desenham o monitor.

        Cada item é uma string a ser usada em um print dentro de um loop.
        O objetivo deste monitor em lista, é a facilidade de adicionar informações
        antes e depois de cada linha exibida.

        :param value: Inteiro
        """

        # Criando uma lista de modelo
        #  * ** ***** ** *
        # [101101111101101]

        # Cria um modelo com o histórico da lista
        model = self.__history[id(self)]

        # O primeiro e o ultimo item da lista sempre será atualizado.
        model.append(value)
        del model[0]

        # Atualiza histórico na classe, mantendo o valor a cada instancia
        self.__history[id(self)] = model

        # Criar um modelo de string (desenho) com informação do modelo de valores inteiro
        # [0    , 3    , 2    , 5    ]
        # [-----, ***--, **---, *****]
        model_draw = list()
        for m in model:
            # quantidade de caracteres vai ser a quantidade do valor
            item = self.__primary_character * m

            # Preencher o resto da linha onde é o "vazio", com outro caractere
            fill = ""

            # as colunas são sempre uma escala de 10 %, i.e de 10 em 10
            if m < self.__lines:
                # resto faltante
                rest = self.__lines - m
                fill = self.__secondary_character * rest

            # Preencher
            item += fill

            # Uma linha foi criada
            model_draw.append(item)

        # pegar lista de caracteres e criar uma lista com os valores em
        # que são exibido, na horizontal
        #
        # [0    , 3    , 2    , 5    ]  Modelo de inteiro
        #
        # [-----, ***--, **---, *****]  Modelo de string
        #
        # [-      -      -      *    ]  Modelo para print()
        # [-      -      -      *    ]
        # [-      *      -      *    ]
        # [-      *      *      *    ]
        # [-      *      *      *    ]

        # Pega o caractere de cima de todos os itens, e cria uma lista
        # depois os próximos caracteres e faz outra lista ...
        model_print = list()

        # numero de linhas menos 1, pq abaixo a contagem é iniciada do zero e não do um
        nc = self.__lines - 1
        for r in range(self.__lines):  # Altura da coluna
            character = ""
            for i in model_draw:
                character = character + i[nc]

            model_print.append(character)
            nc -= 1

        return model_print

    def get_as_color_list(self, value):
        """Mesmo que "get_as_list()", porém com cores.

        Note que os caracteres de informação de cores não são exibidas no console,
        por isso uma contagem de caracteres em uma string com cores,
        não equivale a quantidade de caracteres exibido no console.

        :param value: Inteiro
        """
        as_list = self.get_as_list(value)
        model_print = list()
        for i in as_list:
            model_print.append(i.replace(
                self.__primary_character,
                self.__colors[self.__primary_color] + self.__primary_character + self.__colors["clean"]
            ).replace(
                self.__secondary_character,
                self.__colors[self.__secondary_color] + self.__secondary_character + self.__colors["clean"])
            )

        return model_print

    def get_as_str(self, value):
        """String do monitor com o valor passado

        Retorna uma string que desenha o monitor com o valor passado.

        :param value: Inteiro
        """
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
        """Mesmo que "get_as_str()", porém com cores.

        Note que os caracteres de informação de cores não são exibidas no console,
        por isso uma contagem de caracteres em uma string com cores,
        não equivale a quantidade de caracteres exibido no console.

        :type value: int
        """
        as_str = self.get_as_str(value)
        as_str = as_str.replace(
            self.__primary_character,
            self.__colors[self.__primary_color] + self.__primary_character + self.__colors["clean"]
        ).replace(
            self.__secondary_character,
            self.__colors[self.__secondary_color] + self.__secondary_character + self.__colors["clean"]
        )

        return as_str

if __name__ == '__main__':
    import time
    import os

    import monitor
    import status
    
    valor_da_bolsa = status.StatusEmulator(min_value=0, max_value=10)
    monitor_da_bolsa = monitor.Monitor(columns=50, lines=10)

    for loop in range(70):
        os.system("clear")
        print(monitor_da_bolsa.get_as_color_str(valor_da_bolsa.get_value()))
        time.sleep(0.1)

    valor_do_bitcoin = status.StatusEmulator(min_value=0, max_value=20)
    monitor_do_bitcoin = monitor.Monitor(columns=50, lines=20, primary_color="red-dark", primary_character="'")

    for loop in range(70):
        os.system("clear")

        vertical_label_num = 100  # Números serão uma etiqueta na vertical antes do monitor
        for line in monitor_do_bitcoin.get_as_color_list(valor_do_bitcoin.get_value()):
            print(("  " + str(vertical_label_num))[-3:] + " % |", line)
            vertical_label_num -= 5

        print("        " + "-" * 50)  # Desenha as etiquetas da horizontal
        print("       0    1    2    3    4    5    6    7    8    9    10")
        time.sleep(0.1)


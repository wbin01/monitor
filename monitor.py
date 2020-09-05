#!/usr/bin/env python3

class Monitor(object):
    """Monitor em tempo real. cria um gráfico com um valor"""

    history = dict()

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
        # O modelo é uma lista com os valore do último gráfico que foi usado
        # normalmente se inicia com None para que o primeiro modelo seja criado por
        # essa classe. essa função retorna um modelo que pode ser repassado de volta em um loop

        self.value = value
        self.columns = columns
        self.lines = lines
        self.primary_character = primary_character
        self.secondary_character = secondary_character
        self.primary_color = primary_color
        self.secondary_color = secondary_color

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
        self._set_history()

    def _get_history(self):
        """
        Retorna uma lista como modelo de histórico para o monitor
        """

        if id(self) not in self.history:
            m = list()
            for column in range(self.columns):
                m.append(0)

            history = m

        else:
            history = self.history[id(self)]

        return history

    def _set_history(self):
        """Atualiza o histórico da instância"""
        self.history[id(self)] = self._get_history()

    def get_as_list(self, value):
        """
        Retorna uma lista com as linhas que desenham o monitor.
        Cada linha é uma string com ae ser usada em um print dentro de um loop.
        O objetivo deste monitor em lista, é a facilidade de adicionar informações
        antes e depois de cada linha exibida.
        :type value: int
        """
        # Criando uma lista de modelo
        #  * ** ***** ** *
        # [101101111101101] 

        # Cria um modelo com o histórico da lista
        model = self.history[id(self)]

        # O ultimo item da lista sempre será atualizado.
        model.append(value)
        # Devolve tamanho da lista
        del model[0]

        self.history[id(self)] = model

        # Criar um modelo de string (desenho) com informação do modelo de valores inteiro
        # [0    , 3    , 2    , 5    ]
        # [-----, ***--, **---, *****]
        model_draw = list()
        for m in model:
            # quantidade de caracteres vai ser a quantidade do valor
            item = self.primary_character * m

            # Preencher o resto da linha onde é o "vazio", com outro caractere
            fill = ""
            # as colunas são sempre uma escala de 10 %, i.e de 10 em 10
            if m < self.lines:
                # resto faltante
                rest = self.lines - m
                fill = self.secondary_character * rest

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
        # [---*]                        Modelo para print()
        # [---*]
        # [-*-*]
        # [-***]
        # [-***]
        #  0325

        # Pega o caractere de cima de todos os itens, e cria uma lista
        # depois os próximos caracteres e faz outra lista ...
        model_print = list()
        nc = self.lines - 1  # numero de linhas menos 1 pq abaixo a contagem é iniciada do zero e não do um
        for r in range(self.lines):  # Altura da coluna
            character = ""
            for i in model_draw:
                character = character + i[nc]

            model_print.append(character)
            nc -= 1

        return model_print

    def get_as_color_list(self, value):
        """
        Mesmo que "get_as_list()", porem com cores.

        Note que os caracteres de informação de cores não são exibidas no console,
        por isso uma contagem de caracteres em uma string com cores,
        não equivale a quantidade de caracteres exibido no console.

        :type value: int
        """
        as_list = self.get_as_list(value)
        model_print = list()
        for i in as_list:
            model_print.append(i.replace(
                self.primary_character, self.colors[self.primary_color] + self.primary_character + self.colors["clean"]
                ).replace(
                self.secondary_character, self.colors[self.secondary_color] + self.secondary_character + self.colors["clean"]
                )
            )

        return model_print

    def get_as_str(self, value):
        """
        Retorna uma string que desenha o monitor com o valor passado.
        :type value: int
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
        """
        Mesmo que "get_as_str()", porem com cores.

        Note que os caracteres de informação de cores não são exibidas no console,
        por isso uma contagem de caracteres em uma string com cores,
        não equivale a quantidade de caracteres exibido no console.

        :type value: int
        """
        as_str = self.get_as_str(value)
        as_str = as_str.replace(
            self.primary_character, self.colors[self.primary_color] + self.primary_character + self.colors["clean"]
        ).replace(
            self.secondary_character, self.colors[self.secondary_color] + self.secondary_character + self.colors["clean"]
        )

        return as_str

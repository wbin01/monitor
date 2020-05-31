#!/usr/bin/env python3
import time
import os

class Monitor(object):
    """docstring for Plot"""
    def __init__(self,
        value, columns=10, model=None,
        scale_character="|", space_character="⎺",
        scale_color="green-dark", space_color="blue-dark",
        color=True
        ):
        # O modelo é uma lista com os valore do ultímo gráfico que foi usado
        # normalmente se inicia com None para que o primeiro modelo seja criado por
        # essa fução. essa função retorna um modelo que pode ser repassado de volta em um loop

        self.value = value
        self.columns = columns
        self.model = model
        self.scale_character = scale_character
        self.space_character = space_character
        self.scale_color = scale_color
        self.space_color = space_color
        self.color = color
        
        self.colors = {
            "clean":            "\033[0m", 

            "red":              "\033[0m\033[0;31m", 
            "red-bold":         "\033[0m\033[1;31m", 
            "red-dark":         "\033[0m\033[2;31m", 
            "red-background":   "\033[0m\033[0;31;41m",

            "green":            "\033[0m\033[0;32m", 
            "green-bold":       "\033[0m\033[1;32m", 
            "green-dark":       "\033[0m\033[2;32m", 
            "green-background": "\033[0m\033[0;32;42m",

            "yellow":           "\033[0m\033[0;33m", 
            "yellow-bold":      "\033[0m\033[1;33m", 
            "yellow-dark":      "\033[0m\033[2;33m", 
            "yellow-background":"\033[0m\033[0;33;43m",  

            "blue":             "\033[0m\033[0;34m", 
            "blue-bold":        "\033[0m\033[1;34m", 
            "blue-dark":        "\033[0m\033[2;34m", 
            "blue-background":  "\033[0m\033[0;34;44m", 

            "purple":           "\033[0m\033[0;35m", 
            "purple-bold":      "\033[0m\033[1;35m", 
            "purple-dark":      "\033[0m\033[2;35m", 
            "purple-background":"\033[0m\033[0;35;45m", 

            "cyan":             "\033[0m\033[0;36m", 
            "cyan-bold":        "\033[0m\033[1;36m", 
            "cyan-dark":        "\033[0m\033[2;36m", 
            "cyan-background":  "\033[0m\033[0;36;46m", 

            "white":            "\033[0m\033[0;37m", 
            "white-bold":       "\033[0m\033[1;37m", 
            "white-dark":       "\033[0m\033[2;37m", 
            "white-background": "\033[0m\033[0;37;47m",  
            }

    def as_list(self):

        # Criando uma lista de modelo
        #  * ** ***** ** *
        # [101101111101101] 

        # Lista do tamanho da quantidade de colunas e valores zerados, 
        if self.model == None:
            self.model = list()
            for column in range(self.columns):
                self.model.append(0)

        # Sempre retira o primeiro item do modelo, para ficar um caractere menor
        # e completa de volta com o valor passado.
        # O ultimo item da lista sempre será atualizado.
        del self.model[0]
        self.model.insert(-1, self.value)

        # Criar um modelo de string (desenho) com informação do modelo de valores inteiro
        # [0    , 3    , 2    , 5    ]
        # [-----, ***--, **---, *****]
        model_draw = list()
        for v in self.model:
            # quantidade de caracteres vai ser a quantidade do valor
            item = self.scale_character * v

            # Preencher o resto da linha onde é o "vazio", com outro caractere
            fill = ""
            # as colunas são sempre uma escala de 10 %, i.e de 10 em 10
            if v < 10:
                # resto faltante
                rest = 10 - v
                fill = self.space_character * rest

            # Preencher
            item = item + fill

            # Uma linha foi criada
            model_draw.append(item)

        # pegar lista de caracteres e criar uma lista com os valores em
        # que são exibido/printados, na horizontal

        # [0    , 3    , 2    , 5    ]  Modelo de inteiro

        # [-----, ***--, **---, *****]  Modelo de string

        # [---*]                        Modelo para print()
        # [---*]
        # [-*-*]
        # [-***]
        # [-***]
        #  0325

        # Pega o caractere de cima de todos os itens, e cria uma lista
        # depois os próximos caracteres e faz outra lista ...
        model_print = list()
        for r in range(10):  # Altura da coluna
            character = ""
            for i in model_draw:
                character = character + i[r]

            model_print.append(character)

        # Fix: Inverter lista
        reverse_model_print = list()
        for i in model_print:
            reverse_model_print.insert(0, i[:-1])

        return [self.model, reverse_model_print]

    def as_list_color(self):
        as_list = self.as_list()[1]

        if self.color:
            model_print = list()
            for i in as_list:
                model_print.append(i.replace(
                    self.scale_character, self.colors[self.scale_color] + self.scale_character + self.colors["clean"]
                    ).replace(
                    self.space_character, self.colors[self.space_color] + self.space_character + self.colors["clean"]
                    )
                )

        return [self.model, model_print]

    def as_str(self):
        as_list = self.as_list()[1]
        # Criar string
        #
        # [---*]      Modelo para print()
        # [---*]
        # [-*-*]
        # [-***]
        # [-***]
        #  0325
        #
        # "---*       str
        #  ---*
        #  -*-*
        #  -***
        #  -***"

        model_str = ""
        for i in as_list:
            model_str = model_str + i + "\n"

        str_print = model_str.rstrip("\n")

        return [self.model, str_print]

    def as_str_color(self):
        as_str = self.as_str()[1]
        if self.color:
            as_str = as_str.replace(
                self.scale_character, self.colors[self.scale_color] + self.scale_character + self.colors["clean"]
                ).replace(
                self.space_character, self.colors[self.space_color] + self.space_character + self.colors["clean"]
                )

        return [self.model, as_str]

    # return [model, reverse_model_print]

if __name__ == '__main__':
    import random

    # Valor inicial do monitoramento
    value = 5
    # O modelo inicial do monitoramento (O modelo é uma lista de valores de um gráfico)
    model = None

    # Flag para inverter numeros aleatórios
    inverse = False
    while True:
        #Gerar numeros aleatórios de 0 a 10

        # Inverte ordem para decrementar ou incrementar
        if inverse:
            value -= random.randrange(0, 2)
        else:
            value += random.randrange(0, 2)

        # Se chegar a 10, inverte oredem para decrementar
        if value >= 10:
            inverse = True
            value = random.randrange(5, 10)  # Não deixa passar de 10

        # Se chegar a 0, inverte oredem para incrementar
        elif value <= 0:
            inverse = False
            value = random.randrange(0, 5)  # Não deixa ser menor que 0

        os.system("clear")

        # Monitor como string. Exibe em um só print
        monitor = Monitor(value=value, columns=50, model=model).as_str_color()
        print(monitor[1])

        print()

        # Monitor como lista. Exibe em um "for".
        # Bom para colocar informações antes e depois das linhas.
        monitor = Monitor(
            value=value, columns=50, model=model, 
            scale_character="+", space_character="-",
            scale_color="red", space_color="yellow-dark"
            ).as_list_color()

        n = 100
        for p in monitor[1]:
            num_str = str(n)
            if n < 100:
                num_str = " " + str(n)

            print(num_str + " % |", p)
            n -= 10

        print("       " + "-" * 50)
        print("       0    1    2    3    4    5    6    7    8    9    10")
        
        model = monitor[0]
        time.sleep(0.1)

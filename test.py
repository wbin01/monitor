import random
import time
import os

import monitor

# Criar 1° monitor
small_monitor = monitor.Monitor(columns=50, lines=10, scale_color="blue", space_color="blue-dark")
small_model = small_monitor.get_model()
small_monitor.set_model(small_model)

# *Nota: Um modelo, é uma lista com as estatísticas anteriores,
# serve pra gerar os números antigos da coluna, como um histórico.

# Criar 2° monitor
big_monitor = monitor.Monitor(
    columns=50, lines=20, scale_color="red", space_color="red-dark", scale_character="+")
big_model = big_monitor.get_model()
big_monitor.set_model(big_model)

# Neste teste, será gerado números aleatórios, decrementando e incrementando
# para emular números de estatísticas, números que ficam alto e depois abaixam de valor

# Valor inicial do monitoramento
v = 0
# Valor máximo do monitoramento. Corresponde ao número de linhas
lines = 20
# Flag para inverter números aleatórios
inverse = False

while True:
    # Decrementa ou incrementa
    if inverse:
        v -= random.randrange(0, 2)
    else:
        v += random.randrange(0, 2)

    # Se valor chegar ao número máximo de linhas, inverte ordem para decrementar
    if v >= lines:
        inverse = True
        v = random.randrange(round(v / 2), lines)  # Não deixa passar do máximo

    # Se chegar a 0, inverte ordem para incrementar
    elif v <= 0:
        inverse = False
        v = random.randrange(0, round(lines / 2))  # Não deixa ser menor que 0

    # Limpar para atualizar a tela do terminal durante o loop
    os.system("clear")

    # Aqui o primeiro monitor é exibido como uma só string.
    # O valor é dividido por 2, pois esse monitor tem metade da altura
    small_monitor_in_blue = small_monitor.get_as_color_str(round(v / 2))
    small_model = small_monitor.get_model()  # Atualiza o modelo do monitor
    print(small_monitor_in_blue)

    print()

    # Aqui o segundo monitor é chamado como uma lista e será exibido em um loop de "for".
    # Em lista serve para colocar informações antes e depois das linhas.
    big_monitor_in_red = big_monitor.get_as_color_list(v)
    big_model = big_monitor.get_model()

    # Números serão uma etiqueta na vertical antes do monitor
    vertical_label_num = 100
    for red_line in big_monitor_in_red:
        vertical_label_str = str(vertical_label_num)

        # Ajustar identamento de números menor que 10 e 100
        if vertical_label_num < 10:
            vertical_label_str = "  " + str(vertical_label_num)
        elif vertical_label_num < 100:
            vertical_label_str = " " + str(vertical_label_num)

        # Exibe etiqueta e a linha do monitor
        print(vertical_label_str + " % |", red_line)
        vertical_label_num -= 5

    # Desenha as etiquetas da horizontal
    print("        " + "-" * 50)
    print("       0    1    2    3    4    5    6    7    8    9    10")

    time.sleep(0.1)

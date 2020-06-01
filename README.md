## monitor

Monitor em tempo real com forma de gráfico.

Wilden Alisson Gomes https://github.com/w-a-gomes

https://github.com/w-a-gomes/monitor

*Screenshot*

![Image](screens/screen.png "screenshot")

Exemplo como na screenshot acima:

```python3
import random
import time
import os

import monitor

# Criar 1° monitor
small_monitor = monitor.Monitor(columns=50, lines=10, scale_color="blue", space_color="blue-dark")

# Criar 2° monitor
big_monitor = monitor.Monitor(
    columns=50, lines=20, scale_color="red", space_color="red-dark", scale_character="+")

# Neste teste, será gerado números aleatórios, decrementando e incrementando
# para emular números de estatísticas, números que ficam com valor alto e depois abaixam

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
    print(small_monitor_in_blue)
    
    print()

    # Aqui o segundo monitor é chamado como uma lista e será exibido em um loop de "for".
    # O monitor em lista serve para colocar informações antes e depois das linhas.
    big_monitor_in_red = big_monitor.get_as_color_list(v)

    # Números serão uma etiqueta na vertical antes do monitor
    vertical_label_num = 100
    for red_line in big_monitor_in_red:
        vertical_label_str = str(vertical_label_num)

        # Ajuste no identamento de números menor que 10 e 100
        if vertical_label_num < 10:
            vertical_label_str = "  " + vertical_label_str
        elif vertical_label_num < 100:
            vertical_label_str = " " + vertical_label_str

        # Exibe etiqueta e a linha do monitor respectivamente
        print(vertical_label_str + " % |", red_line)
        vertical_label_num -= 5

    # Desenha as etiquetas da horizontal
    print("        " + "-" * 50)
    print("       0    1    2    3    4    5    6    7    8    9    10")

    time.sleep(0.1)
```

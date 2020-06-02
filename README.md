## monitor

Monitor em tempo real com forma de gráfico.

Wilden Alisson Gomes https://github.com/w-a-gomes

https://github.com/w-a-gomes/monitor

*Screenshot*

![Image](screens/screen.png "screenshot")

Exemplo, como na screenshot acima:

```python3
import time
import os

import monitor
import status

# Neste teste, será gerado números aleatórios, decrementando e incrementando
# para emular números de estatísticas ou status, números que ficam com valor alto e depois abaixam
status = status.StatusEmulator(min_value=0, max_value=20)

# Criar 1° monitor
small_monitor = monitor.Monitor(columns=50, lines=10)

# Criar 2° monitor
big_monitor = monitor.Monitor(
    columns=50, lines=20, primary_color="red", secondary_color="red-dark", primary_character="+")

# *Lembrete: O valor da quantidade de linha corresponde ao valor máximo do status, então
# um valor real de status deve ser dividido para quantidade de linhas do monitor

while True:
    # Limpar para atualizar a tela do terminal durante o loop
    os.system("clear")

    # Recebe um valor de status em tempo real
    v = status.get_value()

    # Aqui o primeiro monitor é exibido como uma só string.
    # O valor é dividido por 2, pois esse monitor tem metade da altura
    print(small_monitor.get_as_color_str(round(v / 2)))

    print()

    # Aqui o segundo monitor é chamado como uma lista e será exibido em um loop de "for".
    # O monitor em lista serve para colocar informações antes e depois das linhas.
    big_monitor_as_list = big_monitor.get_as_color_list(v)

    # Números serão uma etiqueta na vertical antes do monitor
    vertical_label_num = 100
    for line in big_monitor_as_list:
        vertical_label_str = str(vertical_label_num)

        # Ajuste no identamento de números menor que 10 e 100
        if vertical_label_num < 10:
            vertical_label_str = "  " + vertical_label_str
        elif vertical_label_num < 100:
            vertical_label_str = " " + vertical_label_str

        # Exibe etiqueta e a linha do monitor respectivamente
        print(vertical_label_str + " % |", line)
        vertical_label_num -= 5

    # Desenha as etiquetas da horizontal
    print("        " + "-" * 50)
    print("       0    1    2    3    4    5    6    7    8    9    10")

    time.sleep(0.1)
```

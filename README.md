## monitor

Monitor em tempo real com forma de gráfico.

Wilden Alisson Gomes https://github.com/w-a-gomes

https://github.com/w-a-gomes/monitor

*Screenshot*

![Image](screens/screen.png "screenshot")


Ex:

```python3
import random
import time
import os
# Criar 1° monitor
blue_monitor = Monitor(columns=50, scale_color="blue", space_color="blue-dark")
blue_model = blue_monitor.get_model()
blue_monitor.set_model(blue_model)

# *Nota: Um modelo, é uma lista com as estatísticas anteriores,
# serve pra gerar os números antigos da coluna, como um histórico.

# Criar 2° monitor
red_monitor = Monitor(columns=50, scale_color="red", space_color="red-dark", scale_character="+")
red_model = red_monitor.get_model()
red_monitor.set_model(red_model)

# Neste teste, será gerado números aleatórios de 0 a 10, decrementando e incrementando
# para emular números de estatísticas, números que ficam alto e depois abaixam de valor

# Valor inicial do monitoramento
v = 0
# Flag para inverter números aleatórios
inverse = False
while True:
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

    # Limpar para atualizar a tela do terminal durante o loop
    os.system("clear")

    # Aqui o primeiro monitor é exibido como uma só string.
    blue = blue_monitor.get_as_color_str(v)
    blue_model = blue_monitor.get_model()  # Atualiza o modelo do monitor
    print(blue)

    print()

    # Aqui o segundo monitor é chamado como uma lista e será exibido em um loop de "for".
    # Em lista serve para colocar informações antes e depois das linhas.
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
```

"""
Algoritmo Genético - Minimizar função
Samuel de Souza Lopes
"""

"""
Utilizando uma população de 30 indivíduos
Precisão de 4 casas decimais
Cada indivíduo possui a forma [x:y], 
sendo que x e y possui um sinal (1 bit) uma parte inteira (3 bit) e parte real (24 bits)   
"""

import random
import math
import time


def minimizar(num_it, pc, pm):
    # inicializar P
    P = []
    P = inicializar(P)

    # avaliar P
    f = avaliar(P)
    t = 1

    # g armazena os menores valores de f(x,y) encontrados a cada iteração
    g = [min(f)]

    while t < num_it and criterioparada(g):
        P = selecionar(P, f)
        P = reproduzir(P, pc, pm)
        f = avaliar(P)
        g.append(min(f))

        # print("Aptidão média na iteração {}: {}".format(t, sum(f) / 30))
        # print("Melhor aptidão: {}\n".format(min(f)))

        t += 1

    print(t)
    return min(g)


def inicializar(P):
    for x in range(0, 30):
        linha = []
        for y in range(0, 56):
            linha.append(random.randint(0, 1))
        P.append(linha)

    # caso o individuo possua x >= 5  ou x <= -5, zerar a parte real
    for x in range(0, 30):
        if (P[x][1] == 1 and P[x][2] == 1) or (P[x][1] == 1 and P[x][3] == 1):
            for y in range(4, 28):
                P[x][y] = 0
            P[x][2] = 0
            P[x][3] = 1

    # caso o individuo possua y >= 5 ou y <= -5, zerar a parte real
    for x in range(0, 30):
        if (P[x][29] == 1 and P[x][30] == 1) or (P[x][29] == 1 and P[x][31] == 1):
            for y in range(32, 56):
                P[x][y] = 0
            P[x][30] = 0
            P[x][31] = 1

    return P


# calcula a aptidão dos indivíduos da população
def avaliar(P):
    f = []

    # calcular os valores de f(x, y) para cada indivíduo de P e armazenar em f
    for x in range(0, 30):

        # converter o valor de x do indivíduo para decimal
        xdec = 0
        for y in range(1, 28):
            xdec += (1 / math.pow(2, y - 3)) * P[x][y]
        # se o primeiro bit de x for 0, então inverter sinal de xdec
        if P[x][0] == 0:
            xdec = -xdec

        # converter o valor de y do indivíduo para decimal
        ydec = 0
        for y in range(29, 56):
            ydec += (1 / math.pow(2, y - 31)) * P[x][y]
        # se o primeiro bit de x for 0, então inverter sinal de ydec
        if P[x][28] == 0:
            ydec = -ydec

        # calcular o valor de f(xdec, ydec) e inserir em f[x]
        zdec = math.pow((1 - xdec), 2) + 100 * math.pow((ydec - math.pow(xdec, 2)), 2)

        f.append(zdec)

    return f


# seleciona os indivíduos mais aptos a compor a nova população
def selecionar(P, f):

    # selecionar o indice do individuo com menor valor de z
    menor1 = f[0]
    indmenor1 = 0
    for x in range(0, 30):
        if menor1 > f[x]:
            menor1 = f[x]
            indmenor1 = x

    # selecionar o indice do individuo com segundo menor valor de z
    menor2 = f[0]
    indmenor2 = 0
    for x in range(0, 30):
        if menor2 > f[x] and x != indmenor1:
            menor2 = f[x]
            indmenor2 = x

    # inserir os dois individuos na nova população P_linha
    P_linha = [0] * 30
    P_linha[0] = P[indmenor1]
    P_linha[1] = P[indmenor2]

    # selecionar os outros individuos por torneio
    for x in range(2, 30):
        # sortear dois individuos da população atual
        n = 3
        sorteio = [0]*n
        for y in range(0, n):
            sorteio[y] = random.randint(0, 29)

        # dentre os individuos sorteados, escolher o que possui menor f
        menor = f[sorteio[0]]
        indmenor = sorteio[0]
        for y in range(0, n):
            if menor > f[sorteio[y]]:
                menor = f[sorteio[y]]
                indmenor = sorteio[y]

        # inserir este individuo na nova população
        P_linha[x] = P[indmenor]

    # retorna a nova população
    return P_linha


# aplica mutação e crossover de 1 ponto na população
def reproduzir(P, pc, pm):

    # crossover
    x = 0
    while x < 30:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= pc:
            P = crossover(P, x)

        x += 2

    #mutação
    for x in range(0, 30):
        for y in range(0, 56):
            # gerar número aleatório r no intervalo [0, 1]
            r = random.random()

            # condição para haver mutação
            if r <= pm:
                if P[x][y] == 0:
                    P[x][y] = 1
                else:
                    P[x][y] = 0

    # caso o individuo possua x >= 5  ou x <= -5, zerar a parte real
    for x in range(0, 30):
        if (P[x][1] == 1 and P[x][2] == 1) or (P[x][1] == 1 and P[x][3] == 1):
            for y in range(4, 28):
                P[x][y] = 0
            P[x][2] = 0
            P[x][3] = 1

    # caso o individuo possua y >= 5 ou y <= -5, zerar a parte real
    for x in range(0, 30):
        if (P[x][29] == 1 and P[x][30] == 1) or (P[x][29] == 1 and P[x][31] == 1):
            for y in range(32, 56):
                P[x][y] = 0
            P[x][30] = 0
            P[x][31] = 1

    return P


# executa o crossover de 1 ponto
def crossover(P, x):
    cp = random.randint(1, 55)

    pai1 = P[x]
    pai2 = P[x+1]
    # gerar os novos filhos
    aux = pai1
    pai1 = aux[:cp] + pai2[cp:]
    pai2 = pai2[:cp] + aux[cp:]

    P[x] = pai1
    P[x+1] = pai2

    return P


# calculo de média e desvio padrão dos resultados
def media(valores):
    soma = sum(valores)
    qtd_elementos = len(valores)
    media = soma / float(qtd_elementos)
    return media


def variancia(valores):
    _media = media(valores)
    soma = 0
    _variancia = 0

    for valor in valores:
        soma += math.pow((valor - _media), 2)
    _variancia = soma / float(len(valores))
    return _variancia


def desviopadrao(valores):
    return math.sqrt(variancia(valores))


def criterioparada(g):

    ind = len(g) - 1000

    if ind < 0:
        return 1

    for i in range(ind, len(g)):
        if abs(g[ind] - g[i]) >= 0.00000001:
            return 1

    return 0


pc = 0.6
pm = 0.02

resultados = []
num_it = 300
num_testes = 100
inicio = time.time()
for i in range(0, num_testes):
    resultados.append(minimizar(num_it, pc, pm))
    print("\n---> Execução {} - O valor minímo da função é: {} <---".format(i, resultados[i]))
fim = time.time()

# resultados obtidos
print("\nResultados obtidos em {} execuções, com {} iterações cada: ".format(num_testes, num_it))
print("Média dos valores de min f: {}".format(media(resultados)))
print("Desvio padrão: {}".format(desviopadrao(resultados)))
print("Tempo de execução médio: {}".format((fim - inicio)/num_testes))



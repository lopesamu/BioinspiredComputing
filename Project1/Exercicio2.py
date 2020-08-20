"""
Algoritmo Genético - Maximizar função
Samuel de Souza Lopes
"""

"""
Utilizando uma população de 30 indivíduos
Precisão de 7 casas decimais
Cada indivíduo possui uma parte inteira(1 bit) e parte fracionária (24 bits)   
"""

import random
import math
import time


def maximizar(num_it):

    # inicializar P
    P = []
    P = inicializar(P)

    # avaliar P
    g = []
    f = avaliar(P)

    # g armazena o maior valor de g(x) encontrado em cada iteração
    g.append(max(f))
    t = 1

    while t < num_it and criterioparada(g):
        P = selecionar(P, f)
        P = reproduzir(P, pc, pm)
        f = avaliar(P)
        g.append(max(f))
        #print("Aptidão média na iteração {}: {}".format(t, sum(f) / 30))
        #print("Melhor aptidão: {}".format(max(f)))
        t += 1

    print(t)
    return max(g)


# cria a população inicial
def inicializar(P):

    for x in range(0, 30):
        linha = []
        for y in range(0, 26):
            linha.append(random.randint(0, 1))
        P.append(linha)

    # caso o número de um individuo seja 1, zerar sua parte decimal
    for x in range(0, 30):
        if P[x][0] == 1:
            for y in range(1, 26):
                P[x][y] = 0

    return P


# calcula a aptidão dos indivíduos da população
def avaliar(P):

    f = []

    # calcula os valores de y para cada indivíduo de P e armazena em f
    for x in range(0, 30):

        # converter o individuo P[x] para decimal
        xdec = 0
        for y in range(0, 26):
            xdec += (1/math.pow(2, y))*P[x][y]

        # calcula o valor de f(xdec) e inserir em f[x]
        ydec = 2 ** (-2 * (((xdec - 0.1) / 0.9) ** 2)) * ((math.sin(5 * math.pi * xdec)) ** 6)
        f.append(ydec)

    return f


# se os últimos 1000 valores de g(x) não mudarem, parar a execução do algoritmo
def criterioparada(g):

    ind = len(g) - 1000

    if ind < 0:
        return 1

    for i in range(ind, len(g)):
        if abs(g[ind] - g[i]) >= 0.00000001:
            return 1

    return 0


# os dois individuos com maior valor de y serão selecionados, os outros 28 serão pelo torneio
def selecionar(P, f):

    # ---SELEÇÃO---
    # selecionar o indice do individuo com menor valor de z
    maior1 = f[0]
    indmaior1 = 0
    for x in range(0, 30):
        if maior1 < f[x]:
            maior1 = f[x]
            indmaior1 = x

    # selecionar o indice do individuo com segundo menor valor de z
    maior2 = f[0]
    indmaior2 = 0
    for x in range(0, 30):
        if maior2 < f[x] and x != indmaior1:
            maior2 = f[x]
            indmaior2 = x

    # inserir os dois individuos na nova população P_linha
    P_linha = [0] * 30
    P_linha[0] = P[indmaior1]
    P_linha[1] = P[indmaior2]

    # ---TORNEIO---
    for x in range(2, len(f)):
        # sortear três individuos da população atual
        n = 3
        sorteio = [0]*n
        for y in range(0, n):
            sorteio[y] = random.randint(0, 29)

        # dentre os individuos sorteados, escolher o que possui maior aptidão, ou seja, maior valor de f
        maior = f[sorteio[0]]
        indmaior = sorteio[0]
        for y in range(0, n):
            if maior < f[sorteio[y]]:
                maior = f[sorteio[y]]
                indmaior = sorteio[y]

        # inserir este individuo na nova população
        P_linha[x] = P[indmaior]

    # retorna a nova população
    return P_linha


# executa crossover e mutação na população
def reproduzir(P, pc, pm):
    x = 0
    while x < 30:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= pc:
            P = crossover(P, x)

        x += 2

    for x in range(0, 30):
        for y in range(0, 26):
            # gerar número aleatório r no intervalo [0, 1]
            r = random.random()

            # condição para haver mutação
            if r <= pm:
                if P[x][y] == 0:
                    P[x][y] = 1
                else:
                    P[x][y] = 0

    # caso a mutação ou o crossover gere um número maior que 1, zerar a parte decimal
    for x in range(0, 30):
        if P[x][0] == 1:
            for y in range(1, 25):
                P[x][y] = 0
    return P


# executa crossover de 1 ponto
def crossover(P, x):

    #ponto de crossover
    cp = random.randint(1, 24)

    pai1 = P[x]
    pai2 = P[x+1]
    # gerar os novos filhos
    aux = pai1
    pai1 = aux[:cp] + pai2[cp:]
    pai2 = pai2[:cp] + aux[cp:]

    P[x] = pai1
    P[x+1] = pai2

    return P


# funções para calculo da média e desvio padrão dos resultados
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


pc = 0.6
pm = 0.02

resultados = []
num_it = 5000
num_testes = 20
inicio = time.time()
for i in range(0, num_testes):
    resultados.append(maximizar(num_it))
    print("\n---> Execução {} - O valor máximo da função é: {} <---".format(i, resultados[i]))
fim = time.time()

# resultados obtidos
print("\nResultados obtidos em {} iterações: ".format(num_testes))
print("Média dos valores de max g: {}".format(media(resultados)))
print("Desvio padrão: {}".format(desviopadrao(resultados)))
print("Tempo de execução médio: {}".format((fim - inicio)/num_testes))

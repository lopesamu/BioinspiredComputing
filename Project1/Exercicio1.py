"""
Algoritmo Genético - Reconhecimento de Padrões
Samuel de Souza Lopes
"""

import random
import time
import math


# P é a população de 8 individuos, onde cada indivíduo possui 12 bits e cada linha da matriz representa um indivíduo
def algoritmo_genetico():
    # inicializar P
    P = []
    P = inicializar(P)

    # avaliar P
    f = avaliar(P)

    t = 1

    while criterio_parada(f):
        P = selecionar(P, f)
        P = reproduzir(P, pc)
        f = avaliar(P)
        # mostra a aptidão mínima, média e máxima ao longo das iterações
        print("Aptidão média na iteração {}: {}".format(t, sum(f) / 8))
        print("Aptidão máxima: {}".format(max(f)))
        print("Aptidão mínima: {}\n------".format(min(f)))
        t += 1

    return t


# cria a população inicial
def inicializar(P):
    for i in range(0, 8):
        linha = []
        for j in range(0, 12):
            linha.append(random.randint(0, 1))
        P.append(linha)

    return P


# avalia a população
def avaliar(P):
    # representa o padrão buscado nos indivíduos da população
    bitstring = [1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1]

    # Calcula a distância de Hamming em cada indivíduo da população
    h = []
    for i in range(0, 8):
        h.append(hamming(P[i], bitstring))

    # Calcula a aptidão da população
    f = []
    for i in range(0, 8):
        f.append(12 - h[i])

    return f


# calcula a distancia de Hamming
def hamming(str1, str2):
    diferenca = 0
    for x, y in zip(str1, str2):
        if x != y:
            diferenca += 1
    return diferenca


def criterio_parada(f):
        # caso algum indivíduo da população possua todos os bits iguais ao padrão, finalizar a execução
        if max(f) == 12:
            return 0
        else:
            return 1


# seleciona os indivíduos para compor a nova população por seleção e torneio
def selecionar(P, f):

    # --- SELEÇÃO ---
    # selecionar o indice do individuo com maior aptidão
    maior1 = f[0]
    indmaior1 = 0
    for x in range(0, 8):
        if maior1 < f[x]:
            maior1 = f[x]
            indmaior1 = x

    f[indmaior1] = 0

    # selecionar o indice do individuo com a segunda maior aptidão
    maior2 = f[0]
    indmaior2 = 0
    for x in range(0, 8):
        if maior2 < f[x]:
            maior2 = f[x]
            indmaior2 = x

    f[indmaior1] = maior1

    # inserir os dois individuos selecionados na nova população (P_linha)
    P_linha = [0] * 8
    P_linha[0] = P[indmaior1]
    P_linha[1] = P[indmaior2]

    # --- TORNEIO ---
    for x in range(2, 8):
        # sortear trễs individuos da população atual
        n = 3
        sorteio = [0] * n
        for y in range(0, n):
            sorteio[y] = random.randint(0, 7)

        # dentre os individuos sorteados, escolher o que possui maior aptidão
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


def reproduzir(P, pc):
    i = 0
    while i < 8:
        # gerar número aleatório r no intervalo [0, 1]
        r = random.random()

        # condição para haver crossover
        if r <= pc:
            P = crossover(P, i)

        i += 2

    for i in range(0, 8):
        for j in range(0, 12):
            # gerar número aleatório r no intervalo [0, 1]
            r = random.random()

            # condição para haver mutação
            if r <= pm:
                if P[i][j] == 0:
                    P[i][j] = 1
                else:
                    P[i][j] = 0

    return P


def crossover(P, i):
    cp = random.randint(1, 11)

    pai1 = P[i]
    pai2 = P[i + 1]
    # gerar os novos filhos
    aux = pai1
    pai1 = aux[:cp] + pai2[cp:]
    pai2 = pai2[:cp] + aux[cp:]

    P[i] = pai1
    P[i + 1] = pai2

    return P


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


def desvio_padrao(valores):
    return math.sqrt(variancia(valores))


pc = 1
pm = 0.07

algoritmo_genetico()


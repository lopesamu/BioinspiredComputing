"""
Algoritmo Recozimento Simulado
Samuel de Souza Lopes
"""

import math
import random
import time

def recozimentosimulado(max_it):
    # inicializar T, beta e x
    T = 1
    beta = 0.9
    x = random.random()

    # g armazena os melhores valores x a cada iteração
    g = [avaliar(x)]
    t = 1

    while t < max_it and criterioparada(g):
        x_linha = perturbar(x)
        # caso f(x_linha) seja maior que f(x), atribuir x_linha a x
        if avaliar(x_linha) > avaliar(x):
            x = x_linha
        elif random.random() < (math.exp((avaliar(x_linha) - avaliar(x))/T)):
            x = x_linha
        T *= beta
        g.append(avaliar(x))
        # print("Iteração {} - (x,y) = ({}, {})".format(t, x, avaliar(x)))
        t += 1

    print(t)
    return avaliar(x)


# calcula o valor de y da função
def avaliar(x):
    y = 2 ** (-2 * (((x - 0.1) / 0.9) ** 2)) * ((math.sin(5 * math.pi * x)) ** 6)
    return y


# valores
def perturbar(x):
    # soma o ruido gaussiano a x
    valor = x + random.gauss(0, desvio_padrao)

    # caso valor esteja fora do intervalo [0,1]
    while (valor > 1.0) or (valor < 0.0):
        valor = x + random.gauss(0, desvio_padrao)

    return valor


# caso não haja melhora significativa de x nas últimas 1000 iterações
def criterioparada(g):

    ind = len(g) - 1000

    if ind < 0:
        return 1

    for i in range(ind, len(g)):
        if abs(g[ind] - g[i]) >= 0.00000001:
            return 1

    return 0


# funções para calcular média e desvio padrão dos resultados
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


resultados = []
max_it = 10000000
desvio_padrao = 0.001
num_testes = 20

inicio = time.time()
for i in range(0, num_testes):
    resultados.append(recozimentosimulado(max_it))
    print("\n---> Execução {} - O valor máximo da função é: {} <---".format(i, resultados[i]))
fim = time.time()

# resultados obtidos
print("\nResultados obtidos em {} iterações: ".format(num_testes))
print("Média dos valores de max g: {}".format(media(resultados)))
print("Desvio padrão: {}".format(desviopadrao(resultados)))
print("Tempo de execução médio: {}".format((fim - inicio)/num_testes))
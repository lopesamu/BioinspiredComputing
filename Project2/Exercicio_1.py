from sklearn import datasets
import numpy as np
from pandas_ml import ConfusionMatrix
import math
import random


def perceptron(max_it, alpha, x, d):
    # numero de saidas da rede
    num_saidas = 3

    # numero de atributos de cada entrada
    num_caract = 4

    w = np.zeros((num_saidas, num_caract))
    for i in range(0, num_saidas):
        for j in range(0, num_caract):
            w[i][j] = random.random()

    b = np.ones((num_saidas, 1))
    for i in range(0, num_saidas):
        b[i] = random.random()

    t = 1
    E = 1

    while (t < max_it) and (E > 0.0):
        E = 0
        for i in range(0, len(x)):
            u = np.matmul(w, np.transpose([x[i]])) + b
            y = softmax(u, num_saidas)
            saida_desejada = np.zeros(num_saidas)
            saida_desejada[d[i]] = 1
            e = np.transpose([saida_desejada - y])
            w = w + alpha*e*x[i]
            b = b + alpha*e
            E += soma_erro(e, num_saidas)

        print(t, E)
        t += 1

    return w, b


# calcula o erro quadratico de cada saida da rede
def soma_erro(e, num_saidas):
    soma = 0
    for i in range(0, num_saidas):
        soma += e[i]*e[i]

    return soma


# recebe w, b e uma entrada. A saida eh qual iris a entrada representa
def teste(w, b, entrada, num_saidas):
    u = np.matmul(w, np.transpose([entrada])) + b
    saida = softmax(u, num_saidas)

    # retornar o valor representa a iris
    # 0 - iris setosa
    # 1 - iris versicolor
    # 2 - iris virginica
    for i in range(0, num_saidas):
        if saida[i] == max(saida):
            resultado = i

    return resultado


# funcao para calcular o softmax de uma entrada
def softmax(u, num_saidas):
    soma = 0
    saida = []
    for i in range(0, num_saidas):
        soma += math.exp(u[i])

    for i in range(0, num_saidas):
        saida.append(math.exp(u[i])/soma)

    return saida

# funcoes para calcular media, variancia e desvio padrao
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


# armazena todos os dados do dataset, onde x guarda os atributos e d as saida desejadas
iris = datasets.load_iris()
x = iris.data[:, :4]
d = iris.target

# cria os subconjuntos de treinamento (x1), testes (x2) e validacao (x3)
valores = []
for i in range(0, 50):
    valores.append(i)

populacao = random.sample(valores, 50)

# subconjunto de treinamento x1 - 35 elementos de cada classe
# subconjunto de teste x2 - 8 elementos de cada classe
# subconjunto de validacao x3 - 7 elementos de cada classe
x1 = []
d1 = []
x2 = []
d2 = []
x3 = []
d3 = []

for i in range(0, 35):
    x1.append(x[populacao[i]])
    d1.append(d[populacao[i]])

for i in range(35, 43):
    x2.append(x[populacao[i]])
    d2.append(d[populacao[i]])

for i in range(43, 50):
    x3.append(x[populacao[i]])
    d3.append(d[populacao[i]])

valores = []
for i in range(50, 100):
    valores.append(i)

populacao = random.sample(valores, 50)

for i in range(0, 35):
    x1.append(x[populacao[i]])
    d1.append(d[populacao[i]])

for i in range(35, 43):
    x2.append(x[populacao[i]])
    d2.append(d[populacao[i]])

for i in range(43, 50):
    x3.append(x[populacao[i]])
    d3.append(d[populacao[i]])

valores = []
for i in range(100, 150):
    valores.append(i)

populacao = random.sample(valores, 50)

for i in range(0, 35):
    x1.append(x[populacao[i]])
    d1.append(d[populacao[i]])

for i in range(35, 43):
    x2.append(x[populacao[i]])
    d2.append(d[populacao[i]])

for i in range(43, 50):
    x3.append(x[populacao[i]])
    d3.append(d[populacao[i]])

max_it = 1000
alpha = 0.1

# matriz de confusao
for i in range(0, 10):
    print("Execucao {}".format(i))
    w, b = perceptron(max_it, alpha, x1, d1)

    print("\nSubconjunto de treinamento\n")
    resultado = []
    for j in range(0, len(x1)):
        resultado.append(teste(w, b, x1[j], 3))

    print(ConfusionMatrix(d1, resultado))


    print("\nSubconjunto de teste\n")
    resultado = []
    for j in range(0, len(x2)):
        resultado.append(teste(w, b, x2[j], 3))

    print(ConfusionMatrix(d2, resultado))

    print("\nSubconjunto de validacao\n")
    resultado = []
    for j in range(0, len(x3)):
        resultado.append(teste(w, b, x3[j], 3))

    print(ConfusionMatrix(d3, resultado))



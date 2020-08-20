"""
Samuel de Souza Lopes
Algoritmo ACO para o caixeiro viajante
"""

import random
import math
import matplotlib.pyplot as plt


def aco(cidade, max_it, alfa, beta, ro, n, e, q, feromonio_inicial, b):

    # inicializar a matriz de feromonios
    feromonio = inicializar_feromonio(feromonio_inicial, e)

    # armazena o melhor resultado obtido a cada iteracao
    resultado = []
    resultado_iteracao = []

    t = 1

    while t < max_it:
        # armazena as rotas das formigas
        rota = [0]*n
        l_rota = [0]*n

        # colocar cada formiga 𝑘 em uma cidade selecionada aleatoriamente
        cidade_inicial_formiga = inicializar_formiga(n, e)

        # para cada formiga
        for i in range(0, n):
            # construir a rota da formiga i
            rota[i] = construir_rota(e, cidade_inicial_formiga[i], cidade, feromonio, alfa, beta)
            l_rota[i] = distancia_cidades(cidade, rota[i])

        resultado_iteracao.append(min(l_rota))

        # avalia o tamanho da rota construida por cada formiga
        melhor_rota_iteracao = rota[0]
        l_melhor_rota_iteracao = l_rota[0]

        for i in range(1, n):
            if l_rota[i] < l_melhor_rota_iteracao:
                melhor_rota_iteracao = rota[i]
                l_melhor_rota_iteracao = l_rota[i]

        # caso a melhor rota encontrada na iteracao seja a melhor de todas, armazenar em melhor_rota e l_melhor_rota
        if t == 1:
            melhor_rota = melhor_rota_iteracao
            l_melhor_rota = l_melhor_rota_iteracao
        else:
            if l_melhor_rota_iteracao < l_melhor_rota:
                melhor_rota = melhor_rota_iteracao
                l_melhor_rota = l_melhor_rota_iteracao

        # atualizar as trilhas do feromonio
        feromonio = atualizar_feromonio(feromonio, rota, l_rota, melhor_rota, l_melhor_rota, b, ro, n, e, q)

        # imprimir a melhor rota da iteração t
        print("Iteração {} - Tamanho da melhor rota: {}".format(t, l_melhor_rota))
        resultado.append(l_melhor_rota)

        t += 1

    # gera o gráfico contendo a menor distancia encontrada a cada iteracao
    plt.plot(resultado)
    plt.ylabel('Menor distancia (Lmelhor)')
    plt.xlabel('Iteracao')
    plt.show()

    #gera o gráfico contendo a variação da maior aptidão
    plt.plot(resultado_iteracao)
    plt.ylabel('Menor distância')
    plt.xlabel('Iteracao')
    plt.show()

    return melhor_rota


# cada linha i de cidades contem a coordenada da cidade i+1
def inicializar_cidades():
    cidades = [[565.0, 575.0], [25.0, 185.0], [345.0, 750.0], [945.0, 685.0],
               [845.0, 655.0], [880.0, 660.0], [25.0, 230.0], [525.0, 1000.0],
               [580.0, 1175.0], [650.0, 1130.0], [1605.0, 620.0 ], [1220.0, 580.0],
               [1465.0, 200.0], [1530.0, 5.0], [845.0, 680.0], [725.0, 370.0],
               [145.0, 665.0], [415.0, 635.0], [510.0, 875.0], [560.0, 365.0],
               [300.0, 465.0], [520.0, 585.0], [480.0, 415.0], [835.0, 625.0],
               [975.0, 580.0], [1215.0, 245.0], [1320.0, 315.0], [1250.0, 400.0],
               [660.0, 180.0], [410.0, 250.0], [420.0, 555.0], [575.0, 665.0],
               [1150.0, 1160.0], [700.0, 580.0], [685.0, 595.0], [685.0, 610.0],
               [770.0, 610.0], [795.0, 645.0], [720.0, 635.0], [760.0, 650.0],
               [475.0, 960.0], [95.0, 260.0], [875.0, 920.0], [700.0, 500.0],
               [555.0, 815.0], [830.0, 485.0], [1170.0, 65.0], [830.0, 610.0],
               [605.0, 625.0], [595.0, 360.0], [1340.0, 725.0], [1740.0, 245.0]]

    return cidades


# inicializar os feromonios de cada aresta do grafo
def inicializar_feromonio(feromonio_inicial, e):
    feromonio = [0]*e

    for i in range(0, e):
        linha = []
        for j in range(0, e):
            linha.append(feromonio_inicial)
        feromonio[i] = linha

    return feromonio


# inicializar as formigas em cidades aleatórias
def inicializar_formiga(n, e):
    formiga = [0]*n

    for i in range(0, n):
        formiga[i] = random.randint(0, e - 1)

    return formiga


# calcula a distancia euclidiana entre duas ou mais cidades
def distancia_cidades(cidade, seq_cidades):

    distancia = 0
    for i in range(1, len(seq_cidades)):
        aux = math.pow(cidade[seq_cidades[i]][0] - cidade[seq_cidades[i - 1]][0], 2) + \
              math.pow(cidade[seq_cidades[i]][1] - cidade[seq_cidades[i - 1]][1], 2)
        distancia += math.sqrt(aux)

    # calcular a distância da última cidade visitada com a cidade de origem
    aux = math.pow(cidade[seq_cidades[len(seq_cidades) - 1]][0] - cidade[seq_cidades[0]][0], 2) + \
          math.pow(cidade[seq_cidades[len(seq_cidades) - 1]][1] - cidade[seq_cidades[0]][1], 2)
    distancia += math.sqrt(aux)

    return distancia


# constroi rota para uma formiga
def construir_rota(e, cidade_inicial, cidade, feromonio, alfa, beta):
    rota = []

    # iniciar com a cidade que a formiga esta localizada
    rota.append(cidade_inicial)

    #determinar o conjunto j de cidades ainda não visitadas
    j = [0]*e
    for i in range(0, e):
        if i == cidade_inicial:
            j[i] = -1
        else:
            j[i] = i


    # enquanto o tamanho da rota for diferente do número de cidades
    i = cidade_inicial
    while len(rota) != e:
        # prababilidade da formiga ir da cidade i até a cidade j
        p = [0]*e

        # calcular o divisor de p
        divisor = 0
        for aux in range(0, e):
            if j[aux] != -1:
                visibilidade = 1 / distancia_cidades(cidade, [i, j[aux]])
                divisor = divisor + math.pow(feromonio[i][aux], alfa)*math.pow(visibilidade, beta)

        # calcular a probabilidade para cada cidade j
        for aux in range(0, e):
            if j[aux] == -1:
                p[j[aux]] = 0
            else:
                visibilidade = 1/distancia_cidades(cidade, [i, j[aux]])
                p[j[aux]] = (math.pow(feromonio[i][j[aux]], alfa)*math.pow(visibilidade, beta))/divisor

        # definir a cidade visitada via roleta
        # atualiza o valor de i, ou seja, a cidade inicial da iteracao seguinte
        i = definir_cidade(p, j)

        # atualizar a rota
        rota.append(i)
        # atualizar j
        j[i] = -1

    # retorna a rota calculada
    return rota


# atualizar o feromonio
def atualizar_feromonio(feromonio, rota, l_rota, melhor_rota, l_melhor_rota, b, ro, n, e, q):

    # inicializa a matriz de quantidade de feromonio da iteracao
    delta_feromonio = [0]*e
    for i in range(0, e):
        linha = []
        for j in range(0, e):
            linha.append(0)
        delta_feromonio[i] = linha

    # para cada formiga, atualizar o feromonio de delta_feromonio
    for i in range(0, n):
        for j in range(1, len(rota[i])):
                delta_feromonio[rota[i][j - 1]][rota[i][j]] += q/l_rota[i]
        # para a ultima aresta da rota
        delta_feromonio[rota[i][len(rota) - 1]][rota[i][0]] += q / l_rota[i]

    # no caso de formigas elitistas
    for i in range(1, len(melhor_rota)):
            delta_feromonio[melhor_rota[i - 1]][melhor_rota[i]] += (b*q)/l_melhor_rota
    # para a ultima aresta da melhor rota
    delta_feromonio[melhor_rota[len(melhor_rota) - 1]][melhor_rota[0]] += (b * q) / l_melhor_rota

    # atualizar o feromonio
    for i in range(0, e):
        for j in range(0, e):
            feromonio[i][j] = (1 - ro)*feromonio[i][j] + delta_feromonio[i][j]

    return feromonio


def definir_cidade(p, j):
    roleta = []
    roleta.append(0)
    intervalo = 0
    for i in range(0, len(p)):
        intervalo += round(p[i]*360)
        roleta.append(intervalo)

    roleta[len(roleta) - 1] = 360

    #definir a cidade a ser visitada
    sorteio = random.randint(0, 360)

    sorteado = 0
    for i in range(0, len(j)):
        if j[i] != -1:
            if sorteio > roleta[i]:
                sorteado = i

    return sorteado


# printar a melhor rota obtida
def printar_melhor_rota(cidade, rota):

    eixo_x = []
    eixo_y = []

    for i in range(0, len(rota)):
        eixo_x.append(cidade[rota[i]][0])
        eixo_y.append(cidade[rota[i]][1])

    eixo_x.append(cidade[rota[0]][0])
    eixo_y.append(cidade[rota[0]][1])

    # gera o gráfico da melhor rota
    plt.plot(eixo_x, eixo_y)
    plt.plot(eixo_x, eixo_y, 'o')
    plt.plot(cidade[rota[0]][0], cidade[rota[0]][1], marker='o', color='black')
    plt.show()


def main():
    # inicializar a matriz que contem as coordenadas das cidades
    cidade = inicializar_cidades()
    max_it = 250
    alfa = 1
    beta = 5
    ro = 0.5
    n = 52
    e = 52
    q = 100
    feromonio_inicial = math.pow(10, -6)
    b = 5

    melhor_rota = aco(cidade, max_it, alfa, beta, ro, n, e, q, feromonio_inicial, b)
    printar_melhor_rota(cidade, melhor_rota)
    print("A melhor rota obtida é: ")
    for i in range(0, len(melhor_rota)):
        print("cidade {}".format(melhor_rota[i]))

if __name__ == "__main__":
    main()
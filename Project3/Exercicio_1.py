"""
Samuel de Souza Lopes
Algoritmo PSO para maximização de funções
"""

import random
import matplotlib.pyplot as plt


def pso(max_it, ac1, ac2, vmin, vmax, numero_particulas):

    # melhor resultado obtido a cada iteracao
    melhor_resultado_iteracao = []
    # resultado medio obtido a cada iteracao
    media_resultado_iteracao = []

    # guarda a evolucao do melhor resultado a cada iteracao
    eixoy = []

    # dimensão do domínio da função
    dimensao_dominio = 2

    # inicializar o enxame
    x = inicializar_x(numero_particulas, dimensao_dominio)

    # inicializar a velocidade das particulas
    v = inicializar_v(vmin, vmax, numero_particulas, dimensao_dominio)

    t = 1

    # inicializar a matriz p
    p = inicializar_p(numero_particulas, dimensao_dominio)

    while t < max_it:
        for i in range(0, len(x)):
            if aptidao(x[i]) < aptidao(p[i]):
                p[i] = x[i]
            g = i

            # determinar os vizinhos da particula i
            ind_vizinho_esquerda, ind_vizinho_direita = determinar_vizinho(x, i)
            if aptidao(p[ind_vizinho_esquerda]) < aptidao(p[g]):
                g = ind_vizinho_esquerda
            if aptidao(p[ind_vizinho_direita]) < aptidao(p[g]):
                g = ind_vizinho_direita

            # atualizar velocidade da particula
            v[i] = atualizar_velocidade(v[i], x[i], p[i], p[g], ac1, ac2, vmin, vmax)

            # atualizar posição da particula no espaco de busca
            x[i] = atualizar_posicao(x[i], v[i])

        resultado = []
        for i in range(0, len(x)):
            resultado.append(aptidao(x[i]))

        print("Iteracao {} - {}".format(t, min(resultado)))

        melhor_resultado_iteracao.append(min(resultado))
        media_resultado_iteracao.append(sum(resultado)/len(resultado))

        if t == 1:
            # melhor resultado obtido
            melhor_resultado = min(resultado)
        else:
            if min(resultado) < melhor_resultado:
                melhor_resultado = min(resultado)

        eixoy.append(melhor_resultado)
        t += 1

    #gera o gráfico contendo a menor distancia encontrada a cada iteracao
    #plt.plot(eixoy)
    plt.plot(melhor_resultado_iteracao, label = 'Valor mínimo de f(x,y)')
    plt.plot(media_resultado_iteracao, label = 'Valor médio de f(x,y)')
    plt.ylabel('f(x,y)')
    plt.xlabel('Iteração')
    plt.legend()
    plt.show()

    plt.plot()

    return melhor_resultado


# calcula a aptidao de x
def aptidao(x):
    return (1 - x[0])*(1 - x[0]) + 100*(x[1] - x[0]*x[0])*(x[1] - x[0]*x[0])


# cada linha de x armazena uma coordenada do espaço do domínio da função
def inicializar_x(numero_particulas, dimensao_dominio):

    x = []
    for i in range(0, numero_particulas):
        particula = []
        for j in range(0, dimensao_dominio):
            particula.append(random.uniform(-5, 5))
        x.append(particula)

    return x


def inicializar_v(vmin, vmax, numero_particulas, dimensao_dominio):

    v = []
    for i in range(0, numero_particulas):
        velocidade = []
        for j in range(0, dimensao_dominio):
            velocidade.append(random.uniform(vmin, vmax))
        v.append(velocidade)

    return v


def inicializar_p(numero_particulas, dimensao_dominio):

    aux1 = []
    for i in range(0, numero_particulas):
        aux2 = []
        for j in range(0, dimensao_dominio):
            aux2.append(0)
        aux1.append(aux2)

    return aux1


def determinar_vizinho(x, i):
    if i == 0:
        ind_vizinho_esquerda = len(x) - 1
        ind_vizinho_direita = 1
    elif i == len(x) - 1:
        ind_vizinho_esquerda = len(x) - 2
        ind_vizinho_direita = 0
    else:
        ind_vizinho_esquerda = i + 1
        ind_vizinho_direita = i - 1

    return ind_vizinho_esquerda, ind_vizinho_direita


def atualizar_velocidade(vi, xi, pi, pg, ac1, ac2, vmin, vmax):

    velocidade = [0] * len(xi)

    i = 0
    velocidade[i] = vi[i] + random.uniform(0, ac1) * (pi[i] - xi[i]) + random.uniform(0, ac2) * (pg[i] - xi[i])

    while velocidade[i] < vmin or velocidade[i] > vmax:
        velocidade[i] = vi[i] + random.uniform(0, ac1) * (pi[i] - xi[i]) + random.uniform(0, ac2) * (pg[i] - xi[i])

    i = 1
    velocidade[i] = vi[i] + random.uniform(0, ac1) * (pi[i] - xi[i]) + random.uniform(0, ac2) * (pg[i] - xi[i])

    while velocidade[i] < vmin or velocidade[i] > vmax:
        velocidade[i] = vi[i] + random.uniform(0, ac1) * (pi[i] - xi[i]) + random.uniform(0, ac2) * (pg[i] - xi[i])

    return velocidade

def atualizar_posicao(xi, vi):

    posicao = [0]*len(xi)
    for i in range(0, len(xi)):
        posicao[i] = xi[i] + vi[i]

    return posicao

numero_particulas = 10

print(pso(500, 2.05, 2.05, -2, 2, 10))

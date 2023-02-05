import numpy as np
import random
from chrome_trex import DinoGame

CHANCE_MUT = .20
CHANCE_CO = .25
NUM_INDIVIDUOS = 15
NUM_MELHORES = 3

def poblacion_aleatoria(n):
    population = []
    for i in range(n):
        population.append(np.random.uniform(-10, 10, (3, 10)))
    return population

def valor_de_las_acciones(individuo, estado):
    return individuo @ estado

def mejor_jugada(individuo, estado):
    valores = valor_de_las_acciones(individuo, estado)
    return np.argmax(valores)

def mutacion(individuo):
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_MUT:
                individuo[i][j] *= np.random.uniform(-1.5, 1.5)

def cruzada(individuo1, individuo2):
    hijo = individuo1.copy()
    for i in range(3):
        for j in range(10):
            if np.random.uniform(0, 1) < CHANCE_CO:
                hijo[i][j] = individuo2[i][j]
    return hijo

def calcular_fitness(juego, individuo):
    juego.reset()
    while not juego.game_over:
        estado = juego.get_state()
        accion = mejor_jugada(individuo, estado)
        juego.step(accion)
    return juego.get_score()

def ordenar_lista(lista, ordenada, decreciente=True):
    return [x for _, x in sorted(zip(ordenada, lista), key=lambda p: p[0], reverse=decreciente)]

def proxima_generacion(population, fitness):
    ordenados = ordenar_lista(population, fitness)
    proxima_generacion = ordenados[:NUM_MELHORES]

    while len(proxima_generacion) < NUM_INDIVIDUOS:
        ind1, ind2 = random.choices(population, k=2)
        hijo = cruzada(ind1, ind2)
        mutacion(hijo)
        proxima_generacion.append(hijo)
    return proxima_generacion

num_generaciones = 100
juego = DinoGame(fps=300)

population = poblacion_aleatoria(NUM_INDIVIDUOS)
print('generacion | fitness\n----+-' + '-'*5*NUM_INDIVIDUOS)

for ger in range(num_generaciones):
    # Crie uma lista `fitness` com o fitness de cada indivíduo da população
    # (usando a função calcular_fitness e um `for` loop).
    fitness = []
    for ind in population:
        fitness.append(calcular_fitness(juego, ind))

    # Atualize a população usando a função próxima_geração.
    population = proxima_generacion(population, fitness)

    print('{:3} |'.format(ger),
          ' '.join('{:4d}'.format(s) for s in sorted(fitness, reverse=True)))

fitness = []
for ind in population:
    fitness.append(calcular_fitness(juego, ind))

juego.fps = 40
ordenados = ordenar_lista(population, fitness)
mejor = ordenados[0]
print('Mejor jugador/induviduo', mejor)
fit = calcular_fitness(juego, mejor)
print('Fitness: {:4.1f}'.format(juego.get_score()))
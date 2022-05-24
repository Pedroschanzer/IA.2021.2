import random
import copy
from matplotlib import pyplot as plt


def evaluate(individual):
    ataques = 0
    for _cont, _rainha in enumerate(individual):
        for casa in range(_cont + 1, 8):
            if _rainha == individual[casa]:
                ataques += 1
            elif abs(individual[casa] - _rainha) == abs(casa - _cont):
                ataques += 1
    return ataques


def tournament(participants):
    ganhador = None
    stats_ganhador = float('inf')
    for _jogador in participants:
        stats_jogador = evaluate(_jogador)
        if (stats_jogador < stats_ganhador):
            ganhador = _jogador
            stats_ganhador = stats_jogador
    return ganhador


def crossover(parent1, parent2, index):
    aux = copy.deepcopy(parent1[index:])
    pai_2 = copy.deepcopy(parent2)
    pai_1 = copy.deepcopy(parent1)
    pai_1[index:] = copy.deepcopy(pai_2[index:])
    pai_2[index:] = copy.deepcopy(aux)
    return pai_1, pai_2


def mutate(individual, m):
    rand = random.randint(0, 100) / 100
    if rand < m:
        _index = random.randint(0, len(individual) - 1)
        individual[_index] = random.randint(1, 8)
    return individual


MAX_L = []
MIN_L = []
AVERAGE_L = []

def run_ga(g, n, k, m, e):
    population = []
    #GENERATE POPULATION--------------------------------
    for _ in range(n):
        ind_l = []
        for _ in range(8):
            ind_l.append(random.randint(1, 8))
        population.append(ind_l)
    #Fetch Fitness -------------------------------------
    MAX_L.append(evaluate(tournament(population)))
    #Fetch Min -----------------------------------------
    least_fit = population[0]
    min_value = evaluate(population[0])
    for _ind in population:
        candidate = evaluate(_ind)
        if candidate > min_value:
            least_fit = _ind
            min_value = candidate
    MIN_L.append(evaluate(least_fit))
    #GET AVERAGE ---------------------------------------
    average=0
    for _ind in population:
        average = average + evaluate(_ind)
    average = average / len(population)
    AVERAGE_L.append(average)
    #---------------------------------------------------
    for _ in range(g):
        if e:
            nova_populacao = [tournament(population)]
        else:
            nova_populacao = []
        while len(nova_populacao) < n:
            player1, player2 = tournament(random.sample(population, k)), tournament(random.sample(population, k))
            out1, out2 = crossover(player1, player2, random.randint(0, 7))
            out1 = mutate(out1, m)
            out2 = mutate(out2, m)
            nova_populacao = copy.deepcopy(nova_populacao + [out1] + [out2])
        population = nova_populacao
        MAX_L.append(evaluate(tournament(population)))
        #Fetch Min -----------------------------------------
        least_fit = population[0]
        min_value = evaluate(population[0])
        for _ind in population:
            candidate = evaluate(_ind)
            if candidate > min_value:
                least_fit = _ind
                min_value = candidate
        MIN_L.append(evaluate(least_fit))
        #GET AVERAGE ---------------------------------------
        for _ind in population:
            average = average + evaluate(_ind)
        average = average / len(population)
        AVERAGE_L.append(average)
        #---------------------------------------------------
    return tournament(population)


if __name__ == '__main__':
    g = 125
    n = 50
    k = 10
    m = 0.45
    e = True
    result = run_ga(g, n, k, m, e)
    print(result)
    print(evaluate(result))
    plt.plot([i for i in range(g+1)], MAX_L, label='Max Fitness', color='green')
    plt.plot([i for i in range(g+1)], AVERAGE_L, label='Average Fitness', color='blue')
    plt.plot([i for i in range(g+1)], MIN_L, label='Min Fitness', color='red')
    plt.xlabel("Generations")
    plt.ylabel("Ataques")
    plt.title('Reolvendo 8 Queens Puzzle com Algorítmos Genéticos')
    plt.legend()
    plt.show()

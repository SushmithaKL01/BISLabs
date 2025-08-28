import random
CHROM_LENGTH = 5
POP_SIZE = 4
CROSS_RATE = 0.8
MUT_RATE = 0.1

def fitness(x):
    return x**2

def encode(x):
    return format(x, f'0{CHROM_LENGTH}b')

def decode(b):
    return int(b, 2)

def roulette_selection(pop, fitnesses):
    total_fit = sum(fitnesses)
    pick = random.uniform(0, total_fit)
    current = 0
    for i, f in enumerate(fitnesses):
        current += f
        if current > pick:
            return pop[i]
    return pop[-1]

def crossover(p1, p2):
    if random.random() < CROSS_RATE:
        point = random.randint(1, CHROM_LENGTH - 1)
        c1 = p1[:point] + p2[point:]
        c2 = p2[:point] + p1[point:]
        return c1, c2
    return p1, p2

def mutate(chrom):
    chrom_list = list(chrom)
    for i in range(CHROM_LENGTH):
        if random.random() < MUT_RATE:
            chrom_list[i] = '1' if chrom_list[i] == '0' else '0'
    return ''.join(chrom_list)

def genetic_algorithm():
    population = [encode(x) for x in [12, 23, 5, 19]]
    print("Initial Population:", population, [decode(c) for c in population])

    for gen in range(1, 6):
        decoded = [decode(c) for c in population]
        fitnesses = [fitness(x) for x in decoded]
        total_fit = sum(fitnesses)
        probs = [f / total_fit for f in fitnesses]
        expected = [p * POP_SIZE for p in probs]

        print(f"\nGeneration {gen}")
        for i in range(POP_SIZE):
            print(f"x={decoded[i]}, bin={population[i]}, fit={fitnesses[i]}, prob={probs[i]:.3f}, exp_count={expected[i]:.2f}")

        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = roulette_selection(population, fitnesses)
            p2 = roulette_selection(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            c1, c2 = mutate(c1), mutate(c2)
            new_pop.extend([c1, c2])

        population = new_pop[:POP_SIZE]

    decoded = [decode(c) for c in population]
    fitnesses = [fitness(x) for x in decoded]
    best_idx = fitnesses.index(max(fitnesses))
    print("\nFinal Best Solution:", decoded[best_idx], population[best_idx], "fitness=", fitnesses[best_idx])

genetic_algorithm()
genetic_algorithm()
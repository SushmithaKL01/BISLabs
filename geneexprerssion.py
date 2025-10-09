import random

CHROM_LENGTH = 15  # 5 codons * 3 bits
CODON_LENGTH = 3
POP_SIZE = 4
CROSS_RATE = 0.8
MUT_RATE = 0.1
GENS = 5

def fitness(phenotype):
    return sum(x**2 for x in phenotype)

def encode(codons):
    return ''.join(format(c, f'0{CODON_LENGTH}b') for c in codons)

def decode(chrom):
    return [int(chrom[i:i+CODON_LENGTH], 2) for i in range(0, CHROM_LENGTH, CODON_LENGTH)]

def roulette_selection(pop, fits):
    pick = random.uniform(0, sum(fits))
    current = 0
    for c, f in zip(pop, fits):
        current += f
        if current > pick:
            return c
    return pop[-1]

def crossover(p1, p2):
    if random.random() < CROSS_RATE:
        point = random.randint(1, CHROM_LENGTH - 1)
        return p1[:point]+p2[point:], p2[:point]+p1[point:]
    return p1, p2

def mutate(chrom):
    return ''.join('1' if (bit == '0' and random.random() < MUT_RATE) else
                   '0' if (bit == '1' and random.random() < MUT_RATE) else bit
                   for bit in chrom)

def GEA():
    population = [encode([random.randint(0, 7) for _ in range(CHROM_LENGTH // CODON_LENGTH)]) for _ in range(POP_SIZE)]

    for _ in range(GENS):
        phenotypes = [decode(c) for c in population]
        fitnesses = [fitness(p) for p in phenotypes]

        new_pop = []
        while len(new_pop) < POP_SIZE:
            p1 = roulette_selection(population, fitnesses)
            p2 = roulette_selection(population, fitnesses)
            c1, c2 = crossover(p1, p2)
            new_pop += [mutate(c1), mutate(c2)]
        population = new_pop[:POP_SIZE]

    phenotypes = [decode(c) for c in population]
    fitnesses = [fitness(p) for p in phenotypes]
    best = fitnesses.index(max(fitnesses))
    print("Best phenotype:", phenotypes[best], "Fitness:", fitnesses[best])

GEA()

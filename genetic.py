import random

def genetic_algorithm(population,fitness,mutate,mutation_rate=0.01):
    while True:
        weights = [fitness(ind) for ind in population]
        new_population = []
        for i in range(len(population)):
            parent1 , parent2 = random.choices(population, weights=weights, k=2) # weghted random choice
            child = crossover(parent1,parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population

def crossover(parent1,parent2):
    c = random.randint(0,len(parent1))
    return parent1[:c] + parent2[c:] 


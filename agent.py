import board as B 
import piece as P
import genetic as G 
import evaluation as E
from copy import deepcopy
import random as r

class Agent():
    def __init__(self, board_format : B.Board,
                population_size=100,
                mutation_rate=0.01,
                answer_format =[]):
        self.board = board_format
        self.answer_format = answer_format
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self._generate_population()
        self.best = None
        # # self.fitness = E.Fitness(self.board)
        # self.mutate = G.Mutate(self.board)
        # self.genetic = G.Genetic(self.population, self.fitness, self.mutate, self.mutation_rate)

    def _generate_population(self):
        return  [[self.board.random_placement(i.rotate(r.randint(0,3))) for i in self.answer_format] for _ in range(self.population_size)]

    def fitness(self,individual):
        c = 0 
        board = deepcopy(self.board)
        for piece in individual:
            if not board.put_piece(piece):
                break
            c+=1
        return E.Evaluation.evaluate(board) * c


    def mutate(self,individual):
        p = r.randint(0,len(individual))
        self.board.random_placement(individual[p].rotate(r.randint(0,3)))
        return individual
    

    def genetic_algorithm(self,count):
        best_fitness = float('-inf')
        while count:
            weights = [self.fitness(ind) for ind in self.population]
            new_population = []
            for i in range(self.population_size):
                parent1 , parent2 = r.choices(self.population, weights=weights, k=2) # weghted random choice
                child = self.crossover(parent1,parent2)
                if r.random() < self.mutation_rate:
                    child = self.mutate(child)
                new_population.append(child)
                # Check if this child is the best we've seen so far
                child_fitness = self.fitness(child)
                if child_fitness > best_fitness:
                    best_fitness = child_fitness
                    self.best = child
            self.population = new_population
            count -=1
    
    def crossover(self,parent1,parent2):
        c = r.randint(0,self.population_size)
        return parent1[:c] + parent2[c:] 
    
    def run(self,count):
        self.genetic_algorithm(count)
        return self.best
    
    
    def simulated_annealing(self, initial_individual, initial_temperature, cooling_rate, max_iterations):
        current_individual = initial_individual
        current_fitness = self.fitness(current_individual)
        best_individual = current_individual
        best_fitness = current_fitness
        temperature = initial_temperature

        for _ in range(max_iterations):
            
            neighbor = self.mutate(deepcopy(current_individual))
            neighbor_fitness = self.fitness(neighbor)

            if neighbor_fitness > current_fitness or r.random() < self.acceptance_probability(current_fitness, neighbor_fitness, temperature):
                current_individual = neighbor
                current_fitness = neighbor_fitness
                
                if current_fitness > best_fitness:
                    best_individual = current_individual
                    best_fitness = current_fitness

            temperature *= cooling_rate

        return best_individual

    def acceptance_probability(self, current_fitness, neighbor_fitness, temperature):
        if neighbor_fitness > current_fitness:
            return 1.0
        return r.exp((neighbor_fitness - current_fitness) / temperature)
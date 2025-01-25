import board as B 
import evaluation as E
from copy import deepcopy, copy
import random as r
import math

class SA_AGENT():
    def __init__(self, board_format: B.Board,
                 population_size=100,
                 mutation_rate=0.01,
                 answer_format=[],
                 optimize=False):
        self.board = deepcopy(board_format)
        self.board_format = deepcopy(board_format)
        self.answer_format = answer_format
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self._generate_population()
        self.optimize = optimize
        self.best = None
        self.ev = E.Evaluation()

    def _generate_population(self):
        return [[copy(self.board.random_placement(i.rotate(r.randint(0, 3)))) for i in self.answer_format] for _ in range(self.population_size)]

    def fitness(self, individual):
        c = 0
        for p in individual:
            piece = copy(p)
            path, cl = self.board.put_piece(piece, self.optimize)
            if not path:
                break
            if cl:
                self.board.clear_rows()
            c += 1
        if c == 0:
            c = 0.001
        v = self.ev.evaluate(self.board)
        self.revert_the_board(self.board.height - v)  # Revert board changes
        if v == 0:
            v = 0.001
        return v * c

    def revert_the_board(self, lines_changed):
        for i in range(lines_changed):
            self.board.board[i] = [copy(_) for _ in self.board_format.board[i]]

    def mutate(self, individual):
        p = r.randint(0, len(individual) - 1)
        self.board.random_placement(individual[p].rotate(r.randint(0, 3)))
        return individual

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
        return math.exp((neighbor_fitness - current_fitness) / temperature)

    def run(self, count):
        initial_individual = r.choice(self.population)  
        best_solution = self.simulated_annealing(
            initial_individual=initial_individual,
            initial_temperature=100.0,
            cooling_rate=0.95,          
            max_iterations=count
        )
        self.best = best_solution
        return self.best

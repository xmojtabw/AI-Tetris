import board as B 
import piece as P
import genetic as G 
import evaluation as E
from copy import deepcopy, copy
import random as r

class Agent():
    def __init__(self, board_format : B.Board,
                population_size=100,
                mutation_rate=0.01,
                answer_format =[],
                optimize = False ):
        self.board = deepcopy(board_format)
        self.board_format = deepcopy(board_format)
        self.answer_format = answer_format
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.population = self._generate_population()
        self.optimize = optimize
        self.best = None
        self.ev = E.Evaluation()
        # # self.fitness = E.Fitness(self.board)
        # self.mutate = G.Mutate(self.board)
        # self.genetic = G.Genetic(self.population, self.fitness, self.mutate, self.mutation_rate)

    def _generate_population(self):
        return  [[copy(self.board.random_placement(i.rotate(r.randint(0,3)))) for i in self.answer_format] for _ in range(self.population_size)]

    def fitness(self,individual):
        
            
        c = 0 
        for p in individual:
            piece = copy(p)
            path , cl = self.board.put_piece(piece,self.optimize)
            if not path:
                break
            if cl:
                self.board.clear_rows()
            c+=1
        if c==0:
            c=0.001
        #return  c
        v = self.ev.evaluate(self.board)
        self.revert_the_board(self.board.height - v) # notice !! this works by the value of v which is the maximum height of the pieces
        if v==0:
            v=0.001
        return v  * c
    
    def revert_the_board(self,lines_changed):
        for i in range(lines_changed):
            self.board.board[i] = [copy(_) for _ in self.board_format.board[i]]
        # for i in self.board.board:
        #     if any(cell["fill"] for cell in i):
        #         print("look here didn't revert!")





    def mutate(self,individual):
        p = r.randint(0,len(individual)-1)
        self.board.random_placement(individual[p].rotate(r.randint(0,3)))
        return individual
    

    def genetic_algorithm(self,count):
        best_fitness = float('-inf')
        while count:
            weights = [self.fitness(ind) for ind in self.population]
            # print(f"{count}: weights:", sum(weights)/self.population_size)
            # print(f"{count}: max:", max(weights))
            new_population = []
            for _ in range(self.population_size):
                parent1 , parent2 = r.choices(self.population, weights=weights, k=2) # weghted random choice
                child = [copy(_) for _ in self.crossover(parent1,parent2)]
                if r.random() < self.mutation_rate:
                    self.mutate(child)
                new_population.append(child)
                # Check if this child is the best we've seen so far
                child_fitness = self.fitness(child)
                if child_fitness > best_fitness:
                    best_fitness = child_fitness
                    self.best = [copy(i) for i in child]
                    print(f"{_}: best changed to {best_fitness}")
                    # b = deepcopy(self.board)
                    # for p in self.best:
                    #     b.put_piece(p)
                    #     b.clear_rows()
                    # b.print_board()
            self.population = new_population
            count -=1
    
    def crossover(self,parent1,parent2):
        c = r.randint(0,self.population_size)
        return parent1[:c] + parent2[c:] 
    
    def run(self,count):
        self.genetic_algorithm(count)
        return self.best
import random
import numpy as np

# One Max Problem : 10개의 변수(0 또는 1의 값을 가짐)들의 합을 최대화
class Problem:
    def __init__(self):
        self.n = 10         # 10개의 변수 존재

    def GetInitialPopulation(self, pop_size):
        population = []
        for i in range(pop_size):
            # n개의 무작위 0 또는 0의 값을 갖는 리스트 생성
            chromosome = [random.randint(0, 1) for i in range(self.n)]
            population.append(chromosome)
        return population

    def EvaluatePopulation(self, population):
        fitnesses = []
        for chromosome in population:
            fitness = self.FitnessFunction(chromosome)
            fitnesses.append(fitness)
        return fitnesses

    def FitnessFunction(self, chromosome):
        return sum(chromosome)

    def GetBestChromosome(self, population, fitnesses, best, best_fitness):
        for i in range(len(fitnesses)):
            if fitnesses[i] > best_fitness:
                best = population[i]
                best_fitness = fitnesses[i]
        return best, best_fitness

problem = Problem()

def Select2Chromosomes(population, fitnesses):
    index = [i for i in range(len(population))]
    sum_fitness = sum(fitnesses)
    probability = [fitness / sum_fitness for fitness in fitnesses]
    i, j = np.random.choice(index, 2, p=probability, replace=False)

    return population[i], population[j]

def OnePointCrossover(parent1, parent2, crossover_rate):
    n = len(parent1)
    child1, child2 = parent1, parent2

    if random.random() < crossover_rate:
        pos = random.randint(1, n - 1)
        child1 = parent1[0:pos] + parent2[pos:n]
        child2 = parent2[0:pos] + parent1[pos:n]

    return child1, child2

def FlipMutation(child1, child2, mutation_rate):
    n = len(child1)
    c1, c2 = child1, child2

    for i in range(n):
        if random.random() < mutation_rate:
            c1[i] = 0 if c1[i] == 1 else 1
        if random.random() < mutation_rate:
            c2[i] = 0 if c2[i] == 1 else 1

    return c1, c2

# Genetic Algorithm
def GeneticAlgorithm():
    pop_size = 8
    crossover_rate = 1.0
    mutation_rate = 0.01

    population = problem.GetInitialPopulation(pop_size)
    best, best_fitness = [], -1
    generation = 0

    while True:
        fitnesses = problem.EvaluatePopulation(population)
        best, best_fitness = problem.GetBestChromosome(population, fitnesses, best, best_fitness)
        print(best, best_fitness)

        if generation == 10:
            break

        child_count = 0
        new_population = []

        while True:
            parent1, parent2 = Select2Chromosomes(population, fitnesses)
            child1, child2 = OnePointCrossover(parent1, parent2, crossover_rate)
            child1, child2 = FlipMutation(child1, child2, mutation_rate)
            new_population.append(child1)
            new_population.append(child2)

            child_count += 2
            if child_count == pop_size:
                break

        population = new_population
        generation = generation + 1

    return best, best_fitness

best_solution, best_obj_value = GeneticAlgorithm()
print(">>> Best 목적 함수값 :", best_obj_value)
print(">>> Best 해 :", best_solution)

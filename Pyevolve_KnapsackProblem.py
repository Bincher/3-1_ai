from pyevolve import *

class Problem:
    def __init__(self):
        infile = open("knapsack_data.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.item_count = data[0]
        data.pop(0)
        self.max_weight = data[0]
        data.pop(0)
        self.item_data = []
        for i in range(0, len(data), 2):
            temp = [data[i], data[i + 1]]
            self.item_data.append(temp)
        infile.close()

    def FitnessFunction(self, chromosome):
        global best_value, best_weight

        value = 0.0
        weight = 0.0

        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                value += self.item_data[i][0]
                weight += self.item_data[i][1]

        if weight > self.max_weight:
            value -= (weight - self.max_weight) * 10
            if value < 0:
                value = 0

        if value > best_value:
            best_value = value
            best_weight = weight

        return value

knapsack = Problem()
best_value = 0.0
best_weight = 0.0

def main():
    genome = G1DBinaryString.G1DBinaryString(knapsack.item_count)
    genome.evaluator.set(knapsack.FitnessFunction)
    genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)
    genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMinimax(Consts.minimaxType["maximize"])
    ga.setGenerations(200)
    ga.setPopulationSize(100)
    ga.selector.set(Selectors.GTournamentSelector)

    pop = ga.getPopulation()
    pop.scaleMethod.set(Scaling.SigmaTruncScaling)

    ga.evolve(freq_stats = 10)
    print(ga.bestIndividual())
    print("최대값 :", best_value)
    print("무게합 :", best_weight)

main()

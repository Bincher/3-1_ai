from pyevolve import *
import math

def main():
    genome = G1DList.G1DList(tsp.city_count - 1)
    genome.evaluator.set(tsp.FitnessFunction)
    genome.setParams(rangemin=1, rangemax=tsp.city_count - 1)
    genome.initializator.set(Initializators.G1DListInitializatorOrder)
    genome.crossover.set(Crossovers.G1DListCrossoverPMX)
    genome.mutator.set(Mutators.G1DListMutatorSwap)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setMinimax(Consts.minimaxType["minimize"])
    ga.setGenerations(1000)
    ga.setPopulationSize(100)
    ga.selector.set(Selectors.GTournamentSelector)
    ga.setCrossoverRate(0.9)
    ga.setMutationRate(0.001)
    #ga.setMaxTime(300)       # 수행 시간 제한

    pop = ga.getPopulation()
    pop.scaleMethod.set(Scaling.SigmaTruncScaling)

    ga.evolve(freq_stats = 10)
    print(ga.bestIndividual())
    print("최단 거리 :", best_value)

class Problem:
    def __init__(self):
        infile = open("tsp299.txt", "r")
        data = infile.read().split()
        data = [eval(x) for x in data]
        self.city_count = data[0]  # 도시가 5개라면 도시 번호는 [0, 1, 2, 3, 4]
        data.pop(0)
        pos_x = []
        pos_y = []
        for i in range(0, self.city_count * 3, 3):
            pos_x.append(data[i + 1])
            pos_y.append(data[i + 2])

        self.distance = []
        for i in range(self.city_count):
            self.distance.append([])
            for j in range(self.city_count):
                self.distance[i].append(0)

        for i in range(self.city_count - 1):
            for j in range(i + 1, self.city_count):
                self.distance[i][j] = int(math.sqrt((pos_x[i] - pos_x[j]) ** 2 + (pos_y[i] - pos_y[j]) ** 2))
                self.distance[j][i] = self.distance[i][j]

    def FitnessFunction(self, chromosome):
        global best_value

        tour = chromosome.getInternalList()

        sum_distance = self.distance[0][tour[0]]
        for i in range(len(tour) - 1):
            sum_distance += self.distance[tour[i]][tour[i + 1]]
        sum_distance += self.distance[tour[len(tour) - 1]][0]

        if best_value == None or sum_distance < best_value:
            best_value = sum_distance

        return sum_distance

tsp = Problem()
best_value = None
main()

from pyevolve import *
import random

def EvalFunc(chromosome):
    return sum(chromosome)

def OneMaxInitializer(genome, **args):
    lst = [random.choice((0, 1)) for i in range(genome.getListSize())]
    genome.setInternalList(lst)

def OneMaxCrossover(genome, **args):
    g_mom = args["mom"]
    g_dad = args["dad"]

    cut = random.randint(1, len(g_mom) - 1)

    sister = g_mom.clone()
    sister[cut:] = g_dad[cut:]
    brother = g_dad.clone()
    brother[cut:] = g_mom[cut:]

    return (sister, brother)

def OneMaxMutator(genome, **args):
    m_count = 0                     # 실제 돌연변이 개수
    p_mutation = args["pmut"]       # 돌연변이 확률

    for i in range(len(genome)):
        if random.random() < p_mutation:
            m_count += 1
            genome[i] = (genome[i] + 1) % 2

    return m_count

def main():
    genome = G1DBinaryString.G1DBinaryString(20)
    genome.evaluator.set(EvalFunc)
    genome.initializator.set(OneMaxInitializer)
    genome.crossover.set(OneMaxCrossover)
    genome.mutator.set(OneMaxMutator)

    ga = GSimpleGA.GSimpleGA(genome)
    ga.setGenerations(30)
    ga.setPopulationSize(50)
    ga.setCrossoverRate(1.0)
    ga.setMutationRate(0.02)

    ga.evolve(freq_stats = 5)
    print(ga.bestIndividual())

main()
from pyevolve import *

def EvalFunc(chromosome):
    return sum(chromosome)

def main():
    genome = G1DBinaryString.G1DBinaryString(20)
    genome.evaluator.set(EvalFunc)
    #genome.initializator.set(Initializators.G1DBinaryStringInitializator)   # default : =
    #genome.crossover.set(Crossovers.G1DBinaryStringXSinglePoint)    # default : =
    #genome.mutator.set(Mutators.G1DBinaryStringMutatorFlip)         # defulat : =

    ga = GSimpleGA.GSimpleGA(genome)
    #ga.setMinimax(Consts.minimaxType["maximize"])   # defulat : maximize
    ga.setGenerations(30)       # default : 100
    ga.setPopulationSize(50)    # default : 80
    #ga.setCrossoverRate(1.0)    # default : 0.9
    #ga.setMutationRate(0.01)    # default : 0.02
    #ga.selector.set(Selectors.GRouletteWheel)  # default : Rank Selection
    #ga.setElitism(True)        # default : True
    #ga.setElitismReplacement(1)    # default : 1

    #pop = ga.getPopulation()
    #pop.scaleMethod.set(Scaling.NoScaling)  # defulat : Linear Scaling

    ga.evolve(freq_stats = 5)
    print(ga.bestIndividual())

main()

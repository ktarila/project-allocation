"""Main entry point for creating timetable"""

from os.path import abspath, join, isfile

import random
import pickle
import numpy

from deap import base
from deap import algorithms
from deap import creator
from deap import tools

from ga import genetic_operators
from project_allocation import readinput, solution
from project_allocation import config as cfg


NGEN = 500
# NGEN = 1
MU = 400
LAMBDA = 150
CXPB = 0.7
MUTPB = 0.2
RANDSEED = 64
FREQ = 50  # save checkpoint ever 50 generations
MAXGENNOINPROVE = 50
POP_SIZE = 100


def initindividual(icls, content):
    """Initialize an individual"""
    return icls(content)


def initpopulation(pcls, ind_init, ind_list):
    """Initilize a population from list"""
    return pcls(ind_init(c) for c in ind_list)


def evolution(checkpoint=None):
    """Evolve population with soft constraint operators"""
    # for ind in pop:
    #     print(ind, "\n", genetic_operators.hevaluation(ind))
    pop = initialize_pop()

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()

    toolbox.register("individual", initindividual, creator.Individual)
    toolbox.register("population", initpopulation, list,
                     toolbox.individual, pop)

    toolbox.register("evaluate", genetic_operators.evaluate)

    toolbox.register("mutate", genetic_operators.mutate)
    toolbox.register("mate", genetic_operators.crossover)
    # toolbox.register("mate", tools.cxTwoPoint)
    # toolbox.register("mate", genetic_operators.huniformcrossover)
    # toolbox.register("select", tools.selNSGA2)
    toolbox.register("select", tools.selTournament, tournsize=3)
    return evolve(toolbox, checkpoint)


def evolve(toolbox, checkpoint):
    """Evolve a population and return final population
    eaMuPlusLambda implementation with saving checkpoints
    stop criteria at minimum or consecutive non improve

    If evolve type is True then hardconstraint evolve
    else soft constraint evolve"""
    # pop = toolbox.population(n=MU)

    stats = tools.Statistics(lambda ind: ind.fitness.values)
    stats.register("avg", numpy.mean)
    stats.register("std", numpy.std)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)

    if isfile(checkpoint):
        # A filename that has been given exists,then load data from the file
        with open(checkpoint, "rb") as cp_file:
            cpoint = pickle.load(cp_file)
        pop = cpoint["population"]
        gen = cpoint["generation"]
        halloffame = cpoint["halloffame"]
        consecutive = cpoint["consecutive"]
        logbook = cpoint["logbook"]
        random.setstate(cpoint["rndstate"])
        # print(cpoint["consecutive"], cpoint["generation"])
    else:
        # Start a new evolution
        pop = toolbox.population()
        gen = 0
        consecutive = 0
        halloffame = tools.HallOfFame(maxsize=1)
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + stats.fields

    # Evaluate the individuals with an invalid fitness
    invalid_ind = [ind for ind in pop if not ind.fitness.valid]
    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
    for ind, fit in zip(invalid_ind, fitnesses):
        ind.fitness.values = fit

    # log generation 0
    halloffame.update(pop)
    record = stats.compile(pop)
    logbook.record(gen=gen, nevals=len(invalid_ind), **record)
    print(logbook.stream)

    fits = [ind.fitness.values[0] for ind in pop]
    currentmin = min(fits)
    if gen == 0:
        gen += 1

    print(type(pop))

    # Begin the generational process
    # for gen in range(1, NGEN + 1)
    while gen < NGEN and currentmin > 0 and consecutive < MAXGENNOINPROVE:
        # Vary the population
        cfg.CURRENTGEN = gen
        offspring = algorithms.varOr(pop, toolbox, LAMBDA, CXPB, MUTPB)

        # Evaluate the individuals with an invalid fitness - No fit val
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Select the next generation population
        pop[:] = toolbox.select(pop + offspring, MU)

        # Update records and log book
        halloffame.update(pop)
        record = stats.compile(pop)
        logbook.record(gen=gen, nevals=len(invalid_ind), **record)

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        # check for no improvement
        if currentmin <= min(fits):
            consecutive += 1
        else:
            consecutive = 0


        currentmin = min(fits)
        # save checkpoint
        if gen % FREQ == 0:
            # Fill the dictionary using the dict(key=value[, ...]) constructor
            cpoint = dict(population=pop, generation=gen,
                          halloffame=halloffame,
                          logbook=logbook,
                          rndstate=random.getstate(),
                          consecutive=consecutive)

            with open(checkpoint, "wb") as cp_file:
                pickle.dump(cpoint, cp_file)

        print(logbook.stream)  # print records for generation
        # print(currentmin, consecutive)
        gen += 1

    print("-- End of (successful) evolution --")

    # Fill the dictionary using the dict(key=value[, ...]) constructor
    # save last state before exit
    cpoint = dict(population=pop, generation=gen,
                  halloffame=halloffame,
                  logbook=logbook, rndstate=random.getstate(),
                  consecutive=consecutive)

    with open(checkpoint, "wb") as cp_file:
        pickle.dump(cpoint, cp_file)

    # return halloffame and final population
    return halloffame, pop


def initialize_pop():
    """Get first generation of population"""
    pop = []
    for _ in range(POP_SIZE):
        rand_sol = solution.create_random_solution()
        pop.append(rand_sol)
    return pop


def main():
    """Module's main entry point (zopectl.command)."""

    # Reading student input file - and save in global variable
    readinput.read_student()
    readinput.read_subject_areas()

    checkpointname = 'checkpoint.cph'  # file to store GA checkpoints
    cp_fullpath = join(abspath('./Checkpoints'), checkpointname)

    # evolution
    hof, pop = evolution(cp_fullpath)

    final_solution = hof[0]
    final_val = solution.get_solution_quality(final_solution, True)
    print(final_val)
    print(hof[0])


if __name__ == '__main__':
    main()

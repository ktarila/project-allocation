"""Genetic Operators, Mutation and Cross over for SPA Problem"""
import random
import copy
from project_allocation import solution
from project_allocation import config as cfg


def evaluate(individual):
    """get the quality of an individual
    in population"""

    return solution.get_solution_quality(individual),


def mutate(individual):
    """Mutation move a random allocation to a new allocation"""
    num_students = len(cfg.STUDENTS)
    rand_student = random.randint(0, num_students - 1)

    indi = copy.copy(individual)
    indi[rand_student] = random.choice(cfg.STUDENTS[rand_student]['proj_pref'])

    # print(individual, "old Individual")
    # print(indi, "new Individual")

    return indi,


def crossover(ind1, ind2):
    """Two point crossover"""

    c_slice = len(ind1) // 2  # get cross over point

    first_half = list(range(0, c_slice))
    second_half = list(range(c_slice, len(ind1)))

    new_i1 = copy.copy(ind1)
    new_i2 = copy.copy(ind2)

    new_ind1 = [ind1[index] for index in first_half] + [ind2[index]
                                                        for index in second_half]
    new_ind2 = [ind2[index] for index in first_half] + [ind1[index]
                                                        for index in second_half]
    for idx in range(0, len(ind1)):
        new_i1[idx] = new_ind1[idx]
        new_i2[idx] = new_ind2[idx]

    return new_i1, new_i2

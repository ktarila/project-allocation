"""Utility methods used in the gravitational search algorithm"""
import numpy as np
from project_allocation import solution


def distance_vectors(sol_first, sol_second):
    """Get distance R between two solution lists"""
    dist = 0
    if len(sol_first) != len(sol_second):
        return 0
    for idx, val in enumerate(sol_first):
        if val != sol_second[idx]:
            dist += 1
    return dist


def get_masses(population):
    """Get masses of agents in a population"""
    pop_fitness = []
    masses = []
    for agent in population:
        pop_fitness.append(solution.get_solution_quality(agent))
    max_fitness = max(pop_fitness)
    min_fitness = min(pop_fitness)
    if max_fitness == min_fitness:
        return np.ones(len(population))
    else:
        diff = max_fitness - min_fitness
        sum_fitness = sum(pop_fitness)
        for fitness in pop_fitness:
            small_em = (fitness - min_fitness) / diff
            mass = small_em / sum_fitness
            masses.append(mass)
    return masses


def gravitation_constant(iteration, max_iterations):
    """Get gravitation constant"""
    alpha = 20
    g_initial = 100
    g_current = np.exp(-alpha * float(iteration) / max_iterations)
    grav_const = g_initial * g_current
    return grav_const

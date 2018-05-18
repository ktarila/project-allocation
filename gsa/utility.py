"""Utility methods used in the gravitational search algorithm"""
import numpy as np
from project_allocation import solution
from project_allocation import config as cfg


def initialize_gsa(num_iterations, num_agents, dimension):
    """Initialize variables for GSA"""
    cfg.NUM_AGENTS = num_agents
    cfg.MAX_ITERATIONS = num_iterations
    cfg.VELOCITY = np.zeros((num_agents, dimension))


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


def gravitation_constant(iteration):
    """Get gravitation constant"""
    alpha = 20
    g_initial = 100
    g_current = np.exp(-alpha * float(iteration) / cfg.MAX_ITERATIONS)
    grav_const = g_initial * g_current
    return grav_const


def dimension_grav_field(population, index, masses, iteration):
    """Get the gravitation field of a variable : single allele in an individual"""
    total_force = 0
    g_constant = gravitation_constant(iteration)
    for idx, val in enumerate(population[index]):
        mass_i = masses[index]
        for jdx, value in enumerate(population):
            if jdx != index:
                distance_r = distance_vectors(population[index], value)
                dim_diff = 0
                if value[idx] != val:
                    dim_diff = 1
                # compute force
                force_d = g_constant * dim_diff * (
                    (mass_i * masses[jdx]) / (distance_r + cfg.EPSILON))
            total_force += force_d
    return total_force


def agent_grav_field(agent, population, masses, iteration):
    """Compute the grav field of an agent in a population"""
    grav_field = []
    for idx, _ in enumerate(agent):
        dim_grav_field = dimension_grav_field(
            population, idx, masses, iteration)
        grav_field.append(dim_grav_field)
    return grav_field


def pop_grav_field(population, iteration):
    """Compute the gravitation field of population"""
    masses = get_masses(population)
    pop_gf = []
    for agent in population:
        agent_gf = agent_grav_field(agent, population, masses, iteration)
        pop_gf.append(agent_gf)
    return pop_gf

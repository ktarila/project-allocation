"""Utility methods used in the gravitational search algorithm"""
import random
import numpy as np
from project_allocation import solution
from project_allocation import config as cfg


def initialize_gsa(num_iterations, num_agents):
    """Initialize variables for GSA"""
    dimension = len(cfg.STUDENTS)
    cfg.NUM_AGENTS = num_agents
    cfg.MAX_ITERATIONS = num_iterations
    cfg.VELOCITY = np.zeros((num_agents, dimension))
    initial_pop = []
    for _ in range(num_agents):
        initial_pop.append(solution.create_random_solution())
    return initial_pop


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
    # print(pop_fitness)
    max_fitness = max(pop_fitness)
    min_fitness = min(pop_fitness)
    # print(max_fitness, min_fitness)
    if max_fitness == min_fitness:
        return list(np.ones(len(population)))
    else:
        diff = min_fitness - max_fitness
        sum_fitness = sum(pop_fitness)
        for fitness in pop_fitness:
            small_em = (fitness - max_fitness) / diff
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
    # print(index, g_constant)
    # # print(population)
    # for item in population:
    #     print(item)
    mass_i = masses[index]
    # print(mass_i)
    for idx, val in enumerate(population[index]):
        for jdx, value in enumerate(population):
            force_d = 0
            # print(jdx, index)
            if jdx != index:
                # print("here")
                distance_r = distance_vectors(population[index], value)
                dim_diff = 0
                if value[idx] != val:
                    dim_diff = 1
                # compute force
                force_d = g_constant * dim_diff * (
                    (mass_i * masses[jdx]) / (distance_r + cfg.EPSILON))
                # print("g_const:", g_constant)
                # print(mass_i, masses[jdx])
                # print(distance_r, cfg.EPSILON)
                # print(dim_diff, "dim diff", force_d, "force_d")
            total_force += (random.random() * force_d)
            # print(total_force)
    return total_force


def agent_grav_field(agent, population, masses, iteration, agent_index):
    """Compute the grav field of an agent in a population"""
    grav_field = []
    for _ in agent:
        dim_grav_field = dimension_grav_field(
            population, agent_index, masses, iteration)
        grav_field.append(dim_grav_field)
    return grav_field


def pop_acceleration(population, iteration):
    """Compute the gravitation field of population"""
    masses = get_masses(population)
    # print(masses)
    pop_gf = []
    for idx, agent in enumerate(population):
        agent_gf = agent_grav_field(agent, population, masses, iteration, idx)
        pop_gf.append(agent_gf)
    np_array = np.array(pop_gf, dtype='f')
    masses_array = np.array(masses, dtype='f')

    # get acceleration
    acceleration = np_array / masses_array[:, None]
    # print(np_array.shape)
    # print(masses_array.shape)
    # print(masses_array)
    # mass can be zero so change divide by zero(nan) to number
    return np.nan_to_num(acceleration)

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
    """Get masses of agents in a population
       worst solution has a mass of zero"""
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


def update_velocity(acceleration):
    """Update velocity of agents"""
    random_vector = np.random.rand(len(acceleration))
    updated_velocity = cfg.VELOCITY * random_vector[:, None]
    cfg.VELOCITY = acceleration + updated_velocity
    return cfg.VELOCITY


def get_normalized_velocity(acceleration):
    """Get normalized velocity in range 0 to 1
       probability of updating higher for high values"""
    vel = update_velocity(acceleration)
    # print(vel)
    return (vel - np.min(vel)) / np.ptp(vel)


def find_interval(val, partition):
    """ find_interval -> i
        partition is a sequence of numerical values
        x is a numerical value
        The return value "i" will be the index for which applies
        partition[i] < x < partition[i+1], if such an index exists.
        -1 otherwise
    """

    for i, value in enumerate(partition):
        if val < value:
            return i - 1
    return -1


def weighted_choice(sequence, weights, secure=True):
    """ weighted_choice selects a random element of the sequence according to the list of weights"""

    if secure:
        crypto = random.SystemRandom()
        rand_x = crypto.random()
    else:
        rand_x = random.random()
    cum_weights = [0] + list(np.cumsum(weights))
    # convert to range 0 and 1 because random func is in range 0 to 1
    cum_weights = np.array(cum_weights)
    cum_weights = (cum_weights - np.min(cum_weights)) / np.ptp(cum_weights)
    index = find_interval(rand_x, cum_weights)
    print(rand_x, "rand_value")
    # print(cum_weights)
    return sequence[index]


def dimension_new_position(population, index, masses, norm_vel):
    """Get the updated value of a variable : single allele in an individual"""
    column_vel = norm_vel[:, index]
    kbest = 2  # best 10 values
    masses = np.array(masses, dtype='f')
    # print(type(masses), masses)
    # print(column_vel, "col_velocity")
    ind = list(np.argpartition(masses, -kbest)[-kbest:])
    # print(type(ind), ind)

    # filter masses and velocity to contain only top indices
    # filtered_masses = np.array(masses)[ind]
    # print(filtered_masses, "filtered_masses")
    filtered_vector = np.array(column_vel)[ind]
    # print(filtered_vector, "col_vector")

    # get weighted position index
    w_ind = weighted_choice(ind, filtered_vector, False)
    print(w_ind)
    new_position = population[w_ind][index]
    print(new_position)  # accept new pos based on mutation prob
    if random.random() <= 0.1:
        print("To reject new position. Select random new val from possible")

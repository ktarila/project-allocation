"""Operators to create the ant colony optimization algorithm"""

from random import shuffle, random
import copy
import math
import sys
import numpy as np
from project_allocation import config as cfg
from project_allocation import solution, readinput


def initialize_matrix():
    """Initialize the matrix for ants"""

    cfg.ADJ_MATRIX = np.full(
        (len(cfg.PROJECT_AREAS), len(cfg.STUDENTS)), cfg.T_MAX, dtype='f')
    # print(cfg.ADJ_MATRIX.shape)
    cfg.ANT_GLOBAL = solution.create_random_solution()


def evapourate():
    """Reduce pheromone in adjacent matrix"""
    coef = 1 - cfg.RHO
    cfg.ADJ_MATRIX = cfg.ADJ_MATRIX * coef


def update_trail(allocation):
    """Update ant trail based on quality of solution"""
    current_quality = solution.get_solution_quality(allocation)
    best_quality = solution.get_solution_quality(cfg.ANT_GLOBAL)

    if best_quality > current_quality:
        reward = 1
    else:
        reward = 1 / (1 + current_quality - best_quality)

    # print(reward)

    # evapourate pheromones
    evapourate()

    # print(allocation)

    # update rewards for allocation
    for idx, val in enumerate(allocation):
        # print(val, idx)
        cfg.ADJ_MATRIX[int(val) - 1][int(idx)] += reward

    # set min max if greater or less
    cfg.ADJ_MATRIX[cfg.ADJ_MATRIX > cfg.T_MAX] = cfg.T_MAX
    cfg.ADJ_MATRIX[cfg.ADJ_MATRIX < cfg.T_MIN] = cfg.T_MIN


def assign_project(stud_index, ant_sol, use_heuristic):
    """Assign a project to student"""

    # deep copy so modification wont change original
    # Compute heuristic factor here
    temp_sol = copy.deepcopy(ant_sol)
    # print(temp_sol)

    # get only allowed allocations for student
    stud_prefs = cfg.STUDENTS[stud_index]['proj_pref']
    if use_heuristic:
        heu = []
        for val in stud_prefs:
            temp_sol[stud_index] = val
            temp_quality = solution.get_solution_quality(temp_sol)
            heu.append(math.ceil(temp_quality))
        # print(heu)
        max_heu = max(heu) + 1
        heuristic = [max_heu - val for val in heu]
        # print(heuristic)
        # print("\n")

    probability = list(np.zeros(len(stud_prefs), dtype='f'))

    # compute probabilities
    for idx, val in enumerate(stud_prefs):
        # print(val, stud_index)
       # trail is val - 1 coz projects start from 1
        trail = cfg.ADJ_MATRIX[val - 1][stud_index]
        trail_factor = math.pow(trail, cfg.BETA)

        # heuristic_factor = math.pow(heuristic, cfg.ALPHA);
        if use_heuristic:
            heuristic_factor = math.pow(heuristic[idx], cfg.ALPHA)
        else:
            heuristic_factor = 0
        probability[idx] = trail_factor + heuristic_factor
        # print(trail_factor, heuristic_factor)
    return select_project(probability, stud_prefs)


def select_project(probability, stud_prefs):
    """Select a project based on probabilities"""
    norm_prob = [val / sum(probability) for val in probability]

    cumulative_prob = 0
    rand_val = random()
    for idx, val in enumerate(norm_prob):
        cumulative_prob += val
        if rand_val <= cumulative_prob:
            return stud_prefs[idx]
    # should not get here
    print("Error in cumulative probability")
    return stud_prefs[0]


def ant_graph_walk(use_heuristic):
    """An ant walk that results in a generated project allocation"""

    num_stud = len(cfg.STUDENTS)
    # initial solution is array of zeros
    ant_sol = np.zeros(num_stud)

    indices = [val for val in range(num_stud)]
    # shuffle indices so projects are assigned randomly
    # print(indices)
    shuffle(indices)
    # print(indices)
    for stud in indices:
        # assign a project
        proj = assign_project(stud, ant_sol, use_heuristic)
        ant_sol[stud] = proj
    return ant_sol


def ant_colony(num_ants, num_cycles, use_heu=False):
    """Run the ants colony optimizaation algorithm"""
    u_heu = use_heu
    for idx in range(num_cycles):
        # if (idx % 70) == 0:
        #     u_heu = not u_heu
        #     cfg.ADJ_MATRIX = np.full(
        #         (len(cfg.PROJECT_AREAS), len(cfg.STUDENTS)), cfg.T_MAX, dtype='f')

        cyclebest = []
        cycle_best_quality = sys.maxsize
        cycle_scores = []
        print("Iteration: ", idx)
        for jdx in range(num_ants):
            ant_walk = ant_graph_walk(u_heu)
            walk_quality = solution.get_solution_quality(ant_walk)
            cycle_scores.append(walk_quality)
            if cycle_best_quality > walk_quality:
                cycle_best_quality = walk_quality
                cyclebest = ant_walk
            print("\tCycle", idx, "Ant", jdx, "Quality: ", walk_quality)
            if cycle_best_quality == 0:
                cfg.ANT_GLOBAL = cyclebest
                readinput.write_to_file(cycle_scores, idx + 1, "/aco_log.csv", cyclebest)
                return cyclebest
        update_trail(cyclebest)
        if cycle_best_quality < solution.get_solution_quality(cfg.ANT_GLOBAL):
            cfg.ANT_GLOBAL = cyclebest
        print("\t\tGlobal best: ", solution.get_solution_quality(cfg.ANT_GLOBAL))
        readinput.write_to_file(cycle_scores, idx + 1, "/aco_log.csv", cfg.ANT_GLOBAL)
    return cfg.ANT_GLOBAL

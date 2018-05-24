"""Entry point of programme"""
import math
from os.path import abspath, join, isfile
import pickle
from project_allocation import readinput
from project_allocation import solution
from project_allocation import config as cfg
from gsa import utility
# from project_allocation.config import STUDENTS, PROJECT_AREAS, SUPERVISORS


def main():
    """Module's main entry point (zopectl.command)."""
    # Reading student input file - and save in global variable
    readinput.read_student()
    readinput.read_subject_areas()

    checkpointname = 'checkpointgsa.cph'  # file to store GA checkpoints
    checkpoint = join(abspath('./Checkpoints'), checkpointname)

    # Gravitational search algorithm


    population = utility.initialize_gsa(cfg.NUM_ITERATIONS, cfg.NUM_AGENTS)

    # load checkpoint or initialize
    if isfile(checkpoint):
        # A filename that has been given exists,then load data from the file
        with open(checkpoint, "rb") as cp_file:
            cpoint = pickle.load(cp_file)
        population = cpoint["population"]
        cfg.VELOCITY = cpoint["velocity"]
        cfg.CURRENT_ITERATION = cpoint["iteration"]
        global_best = cpoint["global_best"]
        gb_quality = cpoint["gb_quality"]
        # print(cpoint["consecutive"], cpoint["generation"])
    else:
        # Start a new evolution
        global_best = population[0]
        gb_quality = solution.get_solution_quality(global_best)

    for idx in range(cfg.CURRENT_ITERATION, cfg.NUM_ITERATIONS + 1):
        print(idx, "************************************")
        # print(population)
        sol_q = []
        for agent in population:
            quality = solution.get_solution_quality(agent)
            sol_q.append(quality)
        print("Average agent in iteration ", idx,
              " is ", sum(sol_q) / len(sol_q))
        print("Best agent in iteration ", idx, " is ", min(sol_q))

        if min(sol_q) < gb_quality:
            gb_quality = min(sol_q)
            global_best = population[sol_q.index(gb_quality)]

        acceleration = utility.pop_acceleration(population, idx)
        updated_velocity = utility.update_velocity(acceleration)
        norm_velocity = utility.get_normalized_velocity(updated_velocity)
        # print("Updated norm velocity")
        # print(updated_velocity)

        # Get evolved population
        k_best = int(math.log(cfg.NUM_ITERATIONS - idx + 1) * 10 + 5)
        population = utility.update_population(
            population, norm_velocity, k_best)

        # Fill the dictionary using the dict(key=value[, ...]) constructor
        cpoint = dict(population=population, iteration=idx,
                      global_best=global_best,
                      gb_quality=gb_quality,
                      velocity=updated_velocity)

        with open(checkpoint, "wb") as cp_file:
            pickle.dump(cpoint, cp_file)
    solution.get_solution_quality(global_best, True)


if __name__ == '__main__':
    main()

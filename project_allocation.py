"""Entry point of programme"""
import math
from project_allocation import readinput
from project_allocation import solution
from gsa import utility
# from project_allocation.config import STUDENTS, PROJECT_AREAS, SUPERVISORS


def main():
    """Module's main entry point (zopectl.command)."""
    # Reading student input file - and save in global variable
    readinput.read_student()
    readinput.read_subject_areas()
    # print(STUDENTS)
    # print(PROJECT_AREAS)
    # print(SUPERVISORS)
    # rand_solution = solution.create_random_solution()
    # quality = solution.get_solution_quality(rand_solution)
    # print("Quality of ", rand_solution, "is: ", quality)

    # Gravitational search algorithm
    num_iterations = 90
    num_agents = 50
    population = utility.initialize_gsa(num_iterations, num_agents)
    for idx in range(1, num_iterations + 1):
        print(idx, "************************************")
        # print(population)
        sol_q = []
        for agent in population:
            quality = solution.get_solution_quality(agent)
            sol_q.append(quality)
        print("Average agent in iteration ", idx,
              " is ", sum(sol_q) / len(sol_q))
        print("Best agent in iteration ", idx, " is ", min(sol_q))

        acceleration = utility.pop_acceleration(population, idx)
        updated_velocity = utility.get_normalized_velocity(acceleration)
        # print("Updated norm velocity")
        # print(updated_velocity)

        # Get evolved population
        k_best = int(math.log(num_iterations - idx + 1) * 10 + 5)
        population = utility.update_population(
            population, updated_velocity, k_best)


if __name__ == '__main__':
    main()

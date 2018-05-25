"""Entry point of programme"""
from project_allocation import readinput
from project_allocation import solution
from aco import ant_operators
# from project_allocation.config import STUDENTS, PROJECT_AREAS, SUPERVISORS


def main():
    """Module's main entry point (zopectl.command)."""
    # Reading student input file - and save in global variable
    readinput.read_student()
    readinput.read_subject_areas()

    ant_operators.initialize_matrix()
    ant_solution = ant_operators.ant_colony(8, 1000)

    final_sol = solution.get_solution_quality(ant_solution, True)
    print("Final best solution is: ", final_sol)


if __name__ == '__main__':
    main()

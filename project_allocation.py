"""Entry point of programme"""
from project_allocation import readinput, solution
# from project_allocation.config import STUDENTS, PROJECT_AREAS, SUPERVISORS


def main():
    """Module's main entry point (zopectl.command)."""
    # Reading student input file - and save in global variable
    readinput.read_student()
    readinput.read_subject_areas()
    # print(STUDENTS)
    # print(PROJECT_AREAS)
    # print(SUPERVISORS)
    rand_solution = solution.create_random_solution()
    quality = solution.get_solution_quality(rand_solution)
    print("Quality of ", rand_solution, "is: ", quality)


if __name__ == '__main__':
    main()

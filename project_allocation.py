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
    # print(rand_solution)
    # allocation = solution.solution_to_allocation(rand_solution)
    # print(allocation)
    # supervisors = solution.get_supervisor_students(allocation)
    # for item in supervisors:
    #     print(item, len(supervisors[item]))
    lect_num_penalty = solution.get_extra_student_penalty(rand_solution)
    stud_pref_penalty = solution.get_student_pref_penalty(rand_solution)
    print(lect_num_penalty, stud_pref_penalty, (
        lect_num_penalty + stud_pref_penalty))


if __name__ == '__main__':
    main()

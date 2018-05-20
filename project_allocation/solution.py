"""Module that creates and evaluates a project allocation solution"""

import itertools
from operator import itemgetter
from statistics import mean
from random import choice
# import numpy as np
from project_allocation import config as cfg


def create_random_solution():
    """Create a random solution to the project allocation problem"""
    # max_projects = len(cfg.PROJECT_AREAS)
    # max_students = len(cfg.STUDENTS)
    rand_sol = []
    for value in cfg.STUDENTS:
        # print(value)
        rand_sol.append(choice(value['proj_pref']))
    # print(len(rand_sol))
    return rand_sol
    # return list(np.random.randint(1, max_projects, max_students))


def solution_to_allocation(solution):
    """Convert a solution to project allocation"""
    allocation_list = []
    for idx, val in enumerate(solution):
        val_idx = val - 1  # convert index to 0 to n -1
        allocation_list.append(
            {'student': cfg.STUDENTS[idx]['name'], 'supervisor': cfg.PROJECT_AREAS[
                val_idx]['supervisor'], 'area': cfg.PROJECT_AREAS[val_idx]['area']})
    return allocation_list


def get_supervisor_students(allocation_list):
    """group students by supervisors"""
    supervisor_students = {}

    # Important to sort data by `supervisor` key first.
    allocation_list = sorted(allocation_list, key=itemgetter('supervisor'))

    # Display data grouped by `class`
    for key, value in itertools.groupby(allocation_list, key=itemgetter('supervisor')):
        temp = []
        # print(key, value)
        for data in value:
            temp.append(data)
        supervisor_students[key] = temp
    return supervisor_students


def get_extra_student_penalty(solution):
    """get the number of students allocated to lecturer above the max"""
    penalty = 0
    allocation_list = solution_to_allocation(solution)
    supervisor_students = get_supervisor_students(allocation_list)
    for item in supervisor_students:
        if len(supervisor_students[item]) > cfg.SUPERVISORS[item]:
            extra = len(supervisor_students[item]) - cfg.SUPERVISORS[item]
            penalty += extra
    return penalty


def get_student_pref_penalty(solution):
    """get penalty for student not allocated perference"""
    penalty = 0
    for idx, value in enumerate(solution):
        stud_prefs = cfg.STUDENTS[idx]['proj_pref']
        pref_penalty = 0
        try:
            pref_penalty = stud_prefs.index(value)
        except ValueError:
            # penalty of 50 if assigned to non desired project
            pref_penalty = 50
        # print(pref_penalty, value, stud_prefs)
        penalty += pref_penalty
    return penalty


def get_cgpa_equal_penalty(solution):
    """Get sum of difference between Lecturers average cgpa"""
    penalty = 0
    allocation_list = solution_to_allocation(solution)
    supervisor_students = get_supervisor_students(allocation_list)
    mean_cgpa_per_supervisor = {}
    for key, value in supervisor_students.items():
        stud_details = []
        for student in value:
            stud = [float(item['cgpa'])
                    for item in cfg.STUDENTS if item['name'] == student['student']]
            stud_details = stud_details + stud
        mean_cgpa_per_supervisor[key] = mean(stud_details)
    # get unique supervisor combination pairs
    supervisor_combinations = list(itertools.combinations(cfg.SUPERVISORS, 2))
    # difference in each pair
    for item in supervisor_combinations:
        val = list(item)
        # set average to 0 if supervisor not allocated any student
        if val[0] not in mean_cgpa_per_supervisor:
            mean_cgpa_per_supervisor[val[0]] = 0
        if val[1] not in mean_cgpa_per_supervisor:
            mean_cgpa_per_supervisor[val[1]] = 0
        difference = abs(mean_cgpa_per_supervisor[
            val[0]] - mean_cgpa_per_supervisor[val[1]])
        penalty += difference
    return penalty


def get_solution_quality(solution):
    """Get the quality of a timetable solution"""
    gesp = get_extra_student_penalty(solution)
    gspp = get_student_pref_penalty(solution)
    gcep = get_cgpa_equal_penalty(solution)
    # print('GESP - Above average num students', gesp)
    # print('gcep - CGPA equal average', gcep)
    # print('gspp - Student Pref', gspp)
    return gesp * 5 + 10 * gcep + gspp

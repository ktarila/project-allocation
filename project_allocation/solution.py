"""Module that creates and evaluates a project allocation solution"""

import itertools
from operator import itemgetter
import numpy as np
from project_allocation import config as cfg


def create_random_solution():
    """Create a random solution to the project allocation problem"""
    max_projects = len(cfg.PROJECT_AREAS)
    max_students = len(cfg.STUDENTS)
    return list(np.random.randint(1, max_projects, max_students))


def solution_to_allocation(solution):
    """Convert a solution to project allocation"""
    allocation_list = []
    for idx, val in enumerate(solution):
        allocation_list.append(
            {'student': cfg.STUDENTS[idx]['name'], 'supervisor': cfg.PROJECT_AREAS[
                val]['supervisor'], 'area': cfg.PROJECT_AREAS[val]['area']})
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

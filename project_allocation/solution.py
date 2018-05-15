"""Module that creates and evaluates a project allocation solution"""

import numpy as np
import itertools
from operator import itemgetter
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
            {'student': cfg.STUDENTS[idx].name, 'supervisor': cfg.PROJECT_AREAS[
                val].supervisor, 'area': cfg.PROJECT_AREAS[val].area})
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

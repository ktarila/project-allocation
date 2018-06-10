"""Read the input file to create allocation"""
from math import ceil
from pathlib import Path
import os.path
import numpy as np
from project_allocation import student
from project_allocation import project
from project_allocation import solution as sol
from project_allocation import config as cfg


def read_student():
    """Read the input files"""
    with open("data/student_bk.csv") as file:
        for line in file:
            data = line.strip('\n').split("\t")
            stud = student.Student(data[0], list(map(int, data[1:6])), data[6])
            cfg.STUDENTS.append(stud.to_dict())


def read_subject_areas():
    """Read the input files"""
    with open("data/subjectareas.csv") as file:
        for line in file:
            data = line.strip('\n').split("\t")
            proj_areas = project.Project(data[0], data[1])
            cfg.PROJECT_AREAS.append(proj_areas.to_dict())
            # default max allocation per lecturer is 13
            cfg.SUPERVISORS[data[1]] = 13
    # update supevisor max to equal students per lecturers
    total = ceil(len(cfg.STUDENTS) / len(cfg.SUPERVISORS))
    for item in cfg.SUPERVISORS:
        cfg.SUPERVISORS[item] = total


def write_to_file(solution, iteration, name="/gsa_log.csv", current_best=[]):
    """Write solution log to a file"""
    filename = "Log/gsa_log.csv"
    direct = os.path.abspath(os.path.join(filename, os.pardir))
    filename = direct + name
    # print(filename)
    my_file = Path(filename)
    # print(my_file)
    if not my_file.is_file():
        new_file = open(filename, "w")
        new_file.write("Iteration\tMin\tMax\tAvg\tStd\tcurrent_best\n")
        new_file.close()

    file_log = open(filename, "a+")

    n_array = np.array(solution)
    avg = np.mean(n_array)
    maximum = np.max(n_array)
    minimum = np.min(n_array)
    s_dev = np.std(n_array)
    c_best = ','.join(str(int(val)) for val in current_best)

    format_list = [iteration, minimum, maximum, avg, s_dev, c_best]

    string = "{}\t{}\t{}\t{}\t{}\t{}\n".format(*format_list)
    file_log.write(string)
    file_log.close()


def write_best_file(solution, name="/gsa_log_best.csv"):
    """Write best solution log to a file"""
    filename = "Log/gsa_log_best.csv"
    direct = os.path.abspath(os.path.join(filename, os.pardir))
    filename = direct + name
    # print(filename)
    my_file = Path(filename)
    # print(my_file)
    if not my_file.is_file():
        new_file = open(filename, "w")
        new_file.write("fitness\tsolution\n")
        new_file.close()

    file_log = open(filename, "a+")
    solution_str = ','.join(str(int(val)) for val in solution)
    fitness = sol.get_solution_quality(solution)

    format_list = [fitness, solution_str]

    string = "{}\t{}\n".format(*format_list)
    file_log.write(string)
    file_log.close()


def input_stats():
    """Compute input statistics"""

    supervisors = list((cfg.SUPERVISORS.keys()))
    num_sup = len(supervisors)

    pref_1 = [0] * num_sup
    pref_2 = [0] * num_sup
    pref_3 = [0] * num_sup
    pref_4 = [0] * num_sup
    pref_5 = [0] * num_sup

    for stud in cfg.STUDENTS:
        for idx, pref in enumerate(stud['proj_pref']):
            val = pref - 1
            # print(cfg.PROJECT_AREAS[val])
            index = supervisors.index(cfg.PROJECT_AREAS[val]['supervisor'])
            # print(idx, val, pref, stud['proj_pref'])
            if idx == 0:
                pref_1[index] += 1
            if idx == 1:
                pref_2[index] += 1
            if idx == 2:
                pref_3[index] += 1
            if idx == 3:
                pref_4[index] += 1
            if idx == 4:
                pref_5[index] += 1
    return [pref_1, pref_2, pref_3, pref_4, pref_5]

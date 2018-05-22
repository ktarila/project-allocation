"""Read the input file to create allocation"""
from math import ceil
from project_allocation import student
from project_allocation import project
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

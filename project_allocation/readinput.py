"""Read the input file to create allocation"""
from project_allocation import student
from project_allocation import project
from project_allocation import config as cfg


def read_student():
    """Read the input files"""
    with open("data/student.csv") as file:
        for line in file:
            data = line.strip('\n').split("\t")
            stud = student.Student(data[0], data[1:5], data[6])
            cfg.STUDENTS.append(stud)


def read_subject_areas():
    """Read the input files"""
    with open("data/subjectareas.csv") as file:
        for line in file:
            data = line.strip('\n').split("\t")
            proj_areas = project.Project(data[0], data[1])
            cfg.PROJECT_AREAS.append(proj_areas)
            # default max allocation per lecturer is 13
            cfg.SUPERVISORS[data[1]] = 13

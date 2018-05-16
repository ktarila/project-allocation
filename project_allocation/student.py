"""This module describes the student object"""

class Student(object):
    """A Student:

    Attributes:
        name: Unique name/id.
        projects: A list of prefered projects.
        cgpa: student average
    """

    def __init__(self, name, proj_pref, cgpa):
        """Return a student object with *name* and  prefered
        project topics is *proj_pref* and student cgpa."""
        self.name = name
        self.proj_pref = proj_pref
        self.cgpa = cgpa

    def get_name(self):
        """Return the name of student"""
        return self.name

    def get_projects(self):
        """Return the list of prefered projects"""
        return self.proj_pref

    def get_cgpa(self):
        """Return the name of student"""
        return self.cgpa

    def to_dict(self):
        """Dictionary of student object"""
        return self.__dict__

    def __str__(self):
        " Returns a dictionary of object"
        return str(self.__dict__)

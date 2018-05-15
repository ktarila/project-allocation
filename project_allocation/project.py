"""This module describes the project object"""


class Project(object):
    """A Student:

    Attributes:
        name: Unique name/id.
        projects: A list of prefered projects.
    """

    def __init__(self, area, supervisor):
        """Return a student object with *name* and  prefered
        project topics is *proj_pref* and student cgpa."""
        self.area = area
        self.supervisor = supervisor

    def get_area(self):
        """Return the name of student"""
        return self.area

    def __str__(self):
        " Returns a dictionary of object"
        return str(self.__dict__)

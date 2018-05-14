"""This module describes the project object"""

class Project(object):
    """A Student:

    Attributes:
        name: Unique name/id.
        projects: A list of prefered projects.
    """

    def __init__(self, name, title):
        """Return a student object with *name* and  prefered
        project topics is *proj_pref* and student cgpa."""
        self.name = name
        self.title = title

    def get_name(self):
        """Return the name of student"""
        return self.name

    def get_title(self):
        """Return the list of prefered projects"""
        return self.title


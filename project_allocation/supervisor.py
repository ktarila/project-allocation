"""This module describes the student object"""

class Supervisor(object):
    """A Student:

    Attributes:
        name: Unique name/id.
        projects: A list of supervisor projects.
        workload: Max students
    """

    def __init__(self, name, projects, workload):
        """Return a student object with *name* and  prefered
        project topics is *proj_pref* and student cgpa."""
        self.name = name
        self.projects = projects
        self.workload = workload

    def get_name(self):
        """Return the name of student"""
        return self.name

    def get_projects(self):
        """Return the list of prefered projects"""
        return self.projects

    def get_workload(self):
        """Return the name of student"""
        return self.workload

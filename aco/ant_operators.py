"""Operators to create the ant colony optimization algorithm"""

import numpy as np
from project_allocation import config as cfg


def initialize_matrix():
    """Initialize the matrix for ants"""

    return np.full((len(cfg.PROJECT_AREAS), len(cfg.STUDENTS)), cfg.T_MIN, dtype='f')

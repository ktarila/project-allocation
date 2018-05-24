""" Python configuration files
It holds global variables"""

STUDENTS = []
PROJECT_AREAS = []
SUPERVISORS = {}
MAX_ITERATIONS = None
VELOCITY = None
EPSILON = 0.1
MUTATION_PROB = 0.1
CURRENT_ITERATION = 1
NUM_ITERATIONS = 100
NUM_AGENTS = 55

# ant colony constants

# minumum pheromone value
T_MIN = 0.01
# maximum pheromone value
T_MAX = 10
# heuristic weight -- high Ants less sensitive to pheromone trail more
# sensitive to heuristics
ALPHA = 8
# trail weight -- high means ants are less sensitive to heuristic more
# senstive to pheromone trail
BETA = 2
# rate of evapouration -- high means fast evapouration rate (range between 0 and 1);
# 0 and 1);
RHO = 0.05

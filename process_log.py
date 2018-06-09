"""Process log file to create graphs for output"""
import copy
from matplotlib import pyplot as plt
from project_allocation import solution
from project_allocation import readinput


def read_logfile(filename="aco_log.csv"):
    """Read a log file and save in a list"""
    full_path = "Log/" + filename
    results = []
    with open(full_path) as infile:
        next(infile)
        run_result = []
        first_run = None
        for line_number, line in enumerate(infile):
            print("Processing", line_number, "for ", filename)
            line_dict = {}
            data = line.strip().split("\t")
            # print(data)
            if first_run == int(data[0]):
                # reset list
                results.append(copy.deepcopy(run_result))
                run_result = []
            if first_run is None:
                first_run = int(data[0])
            # print(first_run)
            line_dict['min'] = float(data[1])
            line_dict['max'] = float(data[2])
            line_dict['avg'] = float(data[3])
            line_dict['std'] = float(data[4])
            line_dict['best'] = list(map(int, data[5].split(",")))
            run_result.append(line_dict)
            # break
    best_run = get_best_run(results)
    # print(len(results))
    # print(best_run)
    return results[best_run['index']]


def get_best_run(results):
    """Get the best run in result"""
    best = []
    for idx, result in enumerate(results):
        seq = [x['min'] for x in result]
        min_seq = min(seq)
        dict_min = {}
        dict_min['index'] = idx
        dict_min['value'] = min_seq
        best.append(dict_min)
    # print(best)

    # get best of best
    best_run = min(best, key=lambda best: best['value'])
    return best_run


def get_convergence_list(result):
    """Get the list of solution fitness"""
    print("....Generating Convergence list")
    convergence_list = []
    for item in result:
        fitness = solution.get_solution_quality(item['best'], False)
        convergence_list.append(fitness)
    return convergence_list


def main():
    """Main entry point of python script"""
    readinput.read_student()
    readinput.read_subject_areas()

    # get log file for ant run
    ant_best_run = read_logfile("aco_log.csv")
    ant_convergence = get_convergence_list(ant_best_run)

    # get log file for ga run
    ga_best_run = read_logfile("ga_log.csv")
    ga_convergence = get_convergence_list(ga_best_run)

    # get log file for gsa run
    gsa_best_run = read_logfile("gsa_log.csv")
    gsa_convergence = get_convergence_list(gsa_best_run)

    list_len = [len(ant_convergence), len(ga_convergence), len(gsa_convergence)]

    # extend ga convergence list
    if len(ga_convergence) < max(list_len):
        num_req = max(list_len) - len(ga_convergence)
        temp_list = [ga_convergence[-1]] * num_req
        ga_convergence = ga_convergence + temp_list

    # extend gsa convergence list
    if len(gsa_convergence) < max(list_len):
        num_req = max(list_len) - len(gsa_convergence)
        temp_list = [gsa_convergence[-1]] * num_req
        gsa_convergence = gsa_convergence + temp_list

    plt.plot(ant_convergence, color='black', linestyle='--',
             label='Ant Colony Optimisation')
    plt.plot(ga_convergence, color='black',
             linestyle=':', label='Genetic Algorithm')
    plt.plot(gsa_convergence, color='black',
             label='Gravitational Search Algorithm')
    plt.legend()
    plt.xlabel('Number of iterations')
    plt.ylabel('Quality of solution (minimisation)')
    plt.show()

if __name__ == '__main__':
    main()

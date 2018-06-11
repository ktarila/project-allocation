"""Process log file to create graphs for output"""
import copy
from matplotlib import pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap
from project_allocation import solution
from project_allocation import readinput


def read_log_best(filename="aco_log_best.csv"):
    """Process best file"""
    print(filename)
    full_path = "Log/" + filename
    results = []
    with open(full_path) as infile:
        next(infile)
        for line in infile:
            line_dict = {}
            data = line.strip().split("\t")
            line_dict['min'] = float(data[0])
            line_dict['best'] = list(map(int, data[1].split(",")))
            results.append(line_dict)
    # best = min(results, key=lambda results: results['min'])
    # print(best)
    return results


def compute_performance_metric(filename="aco_log_best.csv"):
    """Get min max average"""
    results = read_log_best(filename)
    best = min(results, key=lambda results: results['min'])
    pref_metric = solution.group_student_pref_penalty(best['best'])
    print(solution.get_solution_quality(best['best'], verbose=True))
    print(pref_metric)


def compute_min_max_avg(filename="aco_log_best.csv"):
    """Get min max average"""
    aco_results = read_log_best(filename)
    aco_fitness = [d['min'] for d in aco_results if 'min' in d]
    min_max_avg = {}
    min_max_avg['min'] = min(aco_fitness)
    min_max_avg['max'] = max(aco_fitness)
    min_max_avg['avg'] = sum(aco_fitness) / len(aco_fitness)
    print(min_max_avg)


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

    readinput.input_props()

    pref_lists = readinput.input_stats()
    data = np.array(pref_lists)
    print(data)

    # matplotlib.style.use('ggplot')

    # patterns = [ "/" , "\\" , "|" , "-" , "+" , "x", "o", "O", ".", "*" ]
    patterns = ["", "o", "*", "/", "", "o", "+", "*", ""]
    x = np.arange(data.shape[1])
    colors = sns.color_palette("Greys_r", n_colors=data.shape[1])

    # fig, ax=plt.subplots()
    print(x)
    print(data[0, :])
    # plt.subplot(2, 3, 1)
    # plt.bar(x, data[0,:], edgecolor='black', width=1, label="label {}".format(0))
    fig = plt.figure()
    ax1 = fig.add_subplot(2, 3, 1)
    for i in range(len(x)):
        ax1.bar(i, data[0][i], color=colors[i], edgecolor='black',
                hatch=patterns[i], label="Supervisor {}".format(i + 1))
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    ax2 = fig.add_subplot(2, 3, 2)
    for i in range(len(x)):
        ax2.bar(i, data[1][i], color=colors[i], edgecolor='black',
                hatch=patterns[i])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    ax3 = fig.add_subplot(2, 3, 3)
    for i in range(len(x)):
        ax3.bar(i, data[2][i], color=colors[i], edgecolor='black',
                hatch=patterns[i])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    ax4 = fig.add_subplot(2, 3, 4)
    for i in range(len(x)):
        ax4.bar(i, data[3][i], color=colors[i], edgecolor='black',
                hatch=patterns[i])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    ax5 = fig.add_subplot(2, 3, 5)
    for i in range(len(x)):
        ax5.bar(i, data[4][i], color=colors[i], edgecolor='black',
                hatch=patterns[i])
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=False)  # labels along the bottom edge are off

    ax1.legend(framealpha=1, ncol=1).draggable()
    ax1.set_title("1st preference", fontsize=8)
    ax2.set_title("2nd preference", fontsize=8)
    ax3.set_title("3rd preference", fontsize=8)
    ax4.set_title("4th preference", fontsize=8)
    ax5.set_title("5th preference", fontsize=8)
    plt.subplots_adjust(top=0.92, bottom=0.08, left=0.10, right=0.95, hspace=0.25,
                        wspace=0.35)
    plt.show()

    # fig, ax=plt.subplots()
    # for i in range(data.shape[1]):
    #     bottom=np.sum(data[:,0:i], axis=1)
    #     # ax.bar(x,data[:,i], bottom=bottom, color=colors[i], label="label {}".format(i))
    #     ax.bar(x,data[:,i], bottom=bottom, color=colors[i], edgecolor='black', hatch=patterns[i], label="label {}".format(i))

    # plt.legend(framealpha=1, ncol=4).draggable()
    # plt.yticks(np.arange(0, 100, 6))
    # plt.gray()
    # plt.show()
    # for item in pref_lists:
    #     print(item)

    # number = len(pref_lists[0])

    # ind = np.arange(number)    # the x locations for the groups
    # width = 0.35       # the width of the bars: can also be len(x) sequence

    # p1 = plt.bar(ind, pref_lists[0], width)
    # p2 = plt.bar(ind, pref_lists[1], width,
    #              bottom=pref_lists[0])
    # p3 = plt.bar(ind, pref_lists[2], width,
    #              bottom=pref_lists[1])
    # p4 = plt.bar(ind, pref_lists[3], width,
    #              bottom=pref_lists[2])
    # p5 = plt.bar(ind, pref_lists[4], width,
    #              bottom=pref_lists[3])

    # plt.ylabel('Scores')
    # plt.title('Scores by group and gender')
    # plt.xticks(ind, ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9'))
    # # plt.yticks(np.arange(0, 81, 10))
    # plt.legend((p1[0], p2[0], p3[0], p4[0], p5[0]),
    #            ('Men', 'Women', 'P3', 'P4', 'P5'))

    # plt.show()

    # sol = solution.create_stud_solution()
    # fitness = solution.get_solution_quality(sol, True)
    # print(fitness)

    # compute_performance_metric("aco_log_best.csv")
    # print("\n\n")
    # compute_performance_metric("ga_log_best.csv")
    # print("\n\n")
    # compute_performance_metric("gsa_log_best.csv")
    # print("\n\n")

    # compute_min_max_avg("aco_log_best.csv")
    # compute_min_max_avg("gsa_log_best.csv")
    # compute_min_max_avg("ga_log_best.csv")

    # get log file for ant run
    # ant_best_run = read_logfile("aco_log.csv")
    # ant_convergence = get_convergence_list(ant_best_run)

    # # get log file for ga run
    # ga_best_run = read_logfile("ga_log.csv")
    # ga_convergence = get_convergence_list(ga_best_run)

    # # get log file for gsa run
    # gsa_best_run = read_logfile("gsa_log.csv")
    # gsa_convergence = get_convergence_list(gsa_best_run)

    # list_len = [len(ant_convergence), len(ga_convergence), len(gsa_convergence)]

    # # extend ga convergence list
    # if len(ga_convergence) < max(list_len):
    #     num_req = max(list_len) - len(ga_convergence)
    #     temp_list = [ga_convergence[-1]] * num_req
    #     ga_convergence = ga_convergence + temp_list

    # # extend gsa convergence list
    # if len(gsa_convergence) < max(list_len):
    #     num_req = max(list_len) - len(gsa_convergence)
    #     temp_list = [gsa_convergence[-1]] * num_req
    #     gsa_convergence = gsa_convergence + temp_list

    # plt.plot(ant_convergence, color='black', linestyle='--',
    #          label='Ant Colony Optimisation')
    # plt.plot(ga_convergence, color='black',
    #          linestyle=':', label='Genetic Algorithm')
    # plt.plot(gsa_convergence, color='black',
    #          label='Gravitational Search Algorithm')
    # plt.legend()
    # plt.xlabel('Number of iterations')
    # plt.ylabel('Quality of solution (minimisation)')
    # plt.show()

if __name__ == '__main__':
    main()

import sys
import os
import configparser
import time


root_path = os.path.abspath('..')
if root_path not in sys.path:
    sys.path.append(root_path)


def run(solve, year, day, verbose=False):
    from common.aoc_input import aoc_input
    start_time = time.time()
    input_string = aoc_input(year, day)
    p1, p2 = solve(input_string, verbose)
    if isinstance(p1, str) and '\n' in p1:
        p1 = '\n' + p1
    if isinstance(p2, str) and '\n' in p2:
        p2 = '\n' + p2
    elapsed_time = time.time() - start_time
    print_dict = {'year': year, 'day': day, 'p1': p1, 'p2': p2, 'time': elapsed_time}
    config = configparser.ConfigParser()
    config.read('../common/config.ini')

    printformat = config['dayprint']['format'].replace('\\n','\n')
    printvars = config['dayprint']['variables']
    printvars = [print_dict[var] for var in printvars.split(',')]
    print(printformat.format(*printvars))

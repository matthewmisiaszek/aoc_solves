import sys
import os
import configparser
import argparse
import time


root_path = os.path.abspath('..')
if root_path not in sys.path:
    sys.path.append(root_path)


if __name__=='__main__':
    module_path = ''
else:
    module_path = os.path.dirname(__file__)+'/'
cfg = 'config.ini'
config = configparser.ConfigParser()
config.read(module_path+cfg)


def run(solve, year, day, verbose=False, strip=True):
    start_time = time.time()
    parser = argparse.ArgumentParser(description='AoC Solver Argument Parser')
    parser.add_argument('path', nargs='?', default=aoc_input_path(year, day))
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()
    # input_string = aoc_input(year, day, strip)
    # print(args.path)
    # print(args.v)
    input_string = open(args.path).read()
    if strip:
        input_string = input_string.rstrip()
    p1, p2 = solve(input_string=input_string, verbose=args.v or verbose)
    if isinstance(p1, str) and '\n' in p1:
        p1 = '\n' + p1
    if isinstance(p2, str) and '\n' in p2:
        p2 = '\n' + p2
    elapsed_time = time.time() - start_time
    print_dict = {'year': year, 'day': day, 'p1': p1, 'p2': p2, 'time': elapsed_time}
    # config = configparser.ConfigParser()
    config.read('../common/config.ini')
    printformat = config['dayprint']['format'].replace('\\n','\n')
    printvars = config['dayprint']['variables']
    printvars = [print_dict[var] for var in printvars.split(',')]
    print(printformat.format(*printvars))


def aoc_input_path(year, day):
    input_path = config['files']['input_directory']
    file_format = config['files']['input_format']
    file_variables = config['files']['input_variables']
    year_day = {'year': year, 'day': day}
    pvars = [year_day[var] for var in file_variables.split(',')]
    input_path = os.path.expandvars(input_path)
    input_path = os.path.expanduser(input_path)
    full_path = input_path + file_format.format(*pvars)
    return full_path


def aoc_input(year, day, strip=True):
    full_path = aoc_input_path(year, day)
    input_string = open(full_path).read()
    if strip is True:
        input_string = input_string.rstrip()
    return input_string

holiday_greeting = config['customization']['holiday_greeting']
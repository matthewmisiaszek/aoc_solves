"""Boilerplate Library for Inputs, Timing, and Zealous Execution Normalization (BLITZEN)"""

import sys
import os
import configparser
import argparse
import time
import shutil
import re


# add root of this repository to system path so that modules may be imported
root_path = os.path.dirname(os.path.dirname(__file__))
if root_path not in sys.path:
    sys.path.append(root_path)


# find appropriate configuration directory
# if no custom config exists, copy default
module_path = os.path.dirname(__file__)
defaultconfig = os.path.join(module_path, 'config.ini')
if 'APPDATA' in os.environ:
    confighome = os.environ['APPDATA']
elif 'XDG_CONFIG_HOME' in os.environ:
    confighome = os.environ['XDG_CONFIG_HOME']
else:
    confighome = os.path.join(os.environ['HOME'], '.config')
configpath = os.path.join(confighome, 'aoc_blitzen')
if not os.path.exists(configpath):
    os.makedirs(configpath)
customconfig = os.path.join(configpath, 'config.ini')
if not os.path.exists(customconfig):
    shutil.copy(defaultconfig, customconfig)
    
config = configparser.ConfigParser()
config.read(customconfig)


def extract(pattern, string):
    # take a pattern (formatting string) and a string created from that pattern as input
    # and output the parameters that were formatted using the pattern
    fvals = {}
    pattern = re.sub(r':[.\w]+}', '}', pattern)  # remove formatting instructions
    pattern_l = r'((?:^|[^{]){)'  # match and capture a { preceded by not {
    pattern_r = r'(}(?:$|[^{]))'  # match and capture a } succeeded by not }
    ppat = re.compile(pattern_l + r'(?P<name>\w+)' + pattern_r)  # match and capture parameter names
    i = 0
    while True:
        match = ppat.search(pattern, pos=i)
        if not match:
            break
        i = match.end() - 1
        n = match.group('name')
        # find other paramters with same name and append _ to the name
        pattern = pattern[:i] + re.sub(pattern_l + n + pattern_r, r'\1' + n + r'_\2', pattern[i:])
        fvals[n] = r'(?P<{n}>[\s\S]*)'.format(n=n)
    pattern = re.sub(r'([.^$*+\-?()\[\]\\|:])', r'\\\1', pattern)  # add escapes
    pattern = re.sub(r'\\\\|/', r'[\\\\/]', pattern) # support for \ and / in file system

    rp = pattern.format(**fvals)  # replace parameter names with named groups
    match = re.search(rp, string)
    if not match:
        print(string)
        return {key: 'ERR' for key in fvals}
    else:
        return {key: val.strip('\n') for key, val in match.groupdict().items()}


def run(*args, year=None, day=None, verbose=False, strip=True):
    start_time = time.time()
    parser = argparse.ArgumentParser(description='AoC Solver Argument Parser')
    parser.add_argument('path', nargs='?', default='')
    parser.add_argument('-v', action='store_true')  # force verbose
    parser.add_argument('-q', action='store_true')  # force quiet
    sysargs = parser.parse_args()
    if year is None or day is None:  # if year and day not specified in function call, extract from filepath
        filepath = str(sys.modules['__main__'].__file__)
        vals = extract(config['files']['solution_format'], filepath)
        if year is None:
            year = vals['year']
        if day is None:
            day = vals['day']
    if sysargs.path:  # path to input file has been provided
        input_path = sysargs.path
    else:
        input_path = aoc_input_path(year, day)
    input_string = open(input_path).read()
    if strip:
        input_string = input_string.rstrip()

    def wrap(solve):
        if solve.__module__ == '__main__':
            p1, p2 = solve(input_string=input_string, verbose=(sysargs.v or verbose) and (not sysargs.q))
            if isinstance(p1, str) and '\n' in p1:
                p1 = '\n' + p1
            if isinstance(p2, str) and '\n' in p2:
                p2 = '\n' + p2
            elapsed_time = time.time() - start_time
            print_dict = {'year': int(year), 'day': int(day), 'p1': p1, 'p2': p2, 'time': float(elapsed_time)}
            printformat = config['dayprint']['format']
            print(printformat.format(**print_dict))
        return solve

    if args:  # decorator invoked with no arguments
        return wrap(*args)
    else:  # decorator invoked with arguments, return decorator
        return wrap


def aoc_input_path(year, day):
    input_path = config['files']['input_directory']
    file_format = config['files']['input_format']
    year_day = {'year': int(year), 'day': int(day)}
    input_path = os.path.expandvars(input_path)
    input_path = os.path.expanduser(input_path)
    full_path = input_path + file_format.format(**year_day)
    return full_path


def aoc_input(year, day, strip=True):
    full_path = aoc_input_path(year, day)
    input_string = open(full_path).read()
    if strip is True:
        input_string = input_string.rstrip()
    return input_string


holiday_greeting = config['customization']['holiday_greeting']
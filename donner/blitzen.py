"""Boilerplate Library for Inputs, Timing, and Zealous Execution Normalization (BLITZEN)"""

import argparse
import configparser
import datetime
import os
import re
import shutil
import sys
import time
import requests
import json


def append_root():
    # add root of this repository to system path so that modules may be imported
    root_path = os.path.dirname(os.path.dirname(__file__))
    if root_path not in sys.path:
        sys.path.append(root_path)
    return root_path


root_path = append_root()


class Config(configparser.ConfigParser):
    def __init__(self):
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
        configdir = os.path.join(confighome, 'aoc_blitzen')
        if not os.path.exists(configdir):
            os.makedirs(configdir)
        customconfig = os.path.join(configdir, 'config.ini')
        self.path = customconfig
        self.dir = configdir
        if not os.path.exists(customconfig):
            shutil.copy(defaultconfig, customconfig)

        super().__init__()
        self.read(customconfig)
        config_defaults = configparser.ConfigParser()
        config_defaults.read(defaultconfig)
        changes = False
        for section in config_defaults.sections():
            if section not in self:
                self.add_section(section)
                changes = True
            for item in config_defaults[section]:
                if item not in self[section]:
                    self[section][item] = config_defaults[section][item]
                    changes = True
        if changes:
            self.save()

    def save(self):
        with open(self.path, 'w') as f:
            self.write(f)


config = Config()
holiday_greeting = config['customization']['holiday_greeting']


def aocstr(a):
    if isinstance(a, (list, tuple)):
        return ','.join((str(i) for i in a))
    else:
        return str(a)


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


def fetch(year, day):
    """Attempt to fetch user input and outputs for year, day"""
    if config['user']['token'] == 'N':
        return
    input_path, output_path = aoc_input_path(year, day)
    if os.path.exists(input_path) and os.path.exists(output_path):
        return
    if not os.path.exists(input_path):
        print(f'Input file not found at {input_path}.')
    if not os.path.exists(output_path):
        print(f'Output file not found at {output_path}.')
    print('Fetching...')
    # test token
    cookies = {'session': config['user']['token']}
    url = 'https://adventofcode.com/2024/leaderboard/self'
    while requests.get(url, cookies=cookies).url != url and cookies['session'] != 'N':
        print('Session cookie is missing or incorrect.  Please enter your AoC session cookie.  \nEnter "N" if you do not want to automatically download data.')
        cookies['session'] = input('session:')
    # save token if applicable
    if cookies['session'] != config['user']['token']:
        config['user']['token'] = cookies['session']
        config.save()
    if config['user']['token'] == 'N':
        return
    # check if / when this input will be available.  wait if it'll be less than 10 minutes.
    drop = datetime.datetime(year, 12, day) - datetime.timedelta(seconds=time.timezone - 18000)
    if drop - datetime.datetime.now() > datetime.timedelta(minutes=10):
        raise Exception("This input won't be available for a while.  Please try again within 10 minutes of midnight.")
    while (remaining := drop - datetime.datetime.now()) > datetime.timedelta():
        print(f'\rPuzzle releases in: {remaining.seconds//60:02}:{remaining.seconds%60:02}.{remaining.microseconds//10000:02} ...', end='')
        time.sleep(.3)  # .3 looked good on my machine...
    print('\r', end='')
    # create the appropriate directories if needed
    for f in (input_path, output_path):
        f_dir = os.sep.join(f.split(os.sep)[:-1])
        if not os.path.isdir(f_dir):
            os.makedirs(f_dir)
    if not os.path.exists(input_path):
        url = f'https://adventofcode.com/{year}/day/{day}/input'
        resp = requests.get(url, cookies=cookies)
        with open(input_path, 'w') as input_file:
            input_file.write(resp.text.strip('\n'))
        print('Input file downloaded!')
    if not os.path.exists(output_path):
        url = f'https://adventofcode.com/{year}/day/{day}'
        resp = requests.get(url, cookies=cookies)
        answers = re.findall(r'Your puzzle answer was <code>([\S]+)</code>\.', resp.text)
        if day == 25:
            answers.append(config['customization']['holiday_greeting'])
        if len(answers) == 2:
            with open(output_path, 'w') as output_file:
                output_file.write('\n'.join(answers))
            print('Output file downloaded!')



def run(*args, year=None, day=None, verbose=False, json_output=False):
    parser = argparse.ArgumentParser(description='AoC Solver Argument Parser')
    parser.add_argument('path', nargs='?', default='')
    parser.add_argument('-v', action='store_true')  # force verbose
    parser.add_argument('-q', action='store_true')  # force quiet
    parser.add_argument('-json', action='store_true')  # print json formatted output
    sysargs = parser.parse_args()
    verbose = (sysargs.v or verbose) and (not sysargs.q)
    json_output = json_output or sysargs.json
    if year is None or day is None:  # if year and day not specified in function call, extract from filepath
        filepath = str(sys.modules['__main__'].__file__)
        vals = extract(config['files']['solution_format'], filepath)
        if year is None:
            year = int(vals['year'])
        if day is None:
            day = int(vals['day'])
    if sysargs.path:  # path to input file has been provided
        input_path = sysargs.path
        output_path = None
    else:
        input_path, output_path = aoc_input_path(year, day)
        if (not os.path.exists(input_path)) or (not os.path.exists(output_path)):
            fetch(year, day)
    start_time = time.time()
    input_string = open(input_path).read()
    p1ans = p2ans = 'Unknown'
    if output_path is not None and os.path.exists(output_path):
        p1ans, p2ans = open(output_path).read().split('\n')
    input_string = input_string.rstrip()

    def wrap(solve):
        if solve.__module__ == '__main__':
            p1, p2 = solve(input_string=input_string, verbose=verbose)
            p1, p2 = aocstr(p1), aocstr(p2)
            if '\n' in p1:
                p1 = '\n' + p1
            if '\n' in p2:
                p2 = '\n' + p2
            elapsed_time = time.time() - start_time
            p1chk = 'True' if p1 == p1ans else 'False'
            p2chk = 'True' if p2 == p2ans else 'False'
            print_dict = {
                'year': int(year), 'day': int(day),
                'p1': p1, 'p1ans': p1ans, 'p1chk': p1chk,
                'p2': p2, 'p2ans': p2ans, 'p2chk': p2chk,
                'time': float(elapsed_time)
            }
            if json_output:
                print(json.dumps(print_dict))
            else:
                printformat = config['dayprint']['format']
                print(printformat.format(**print_dict))
        return solve

    if args:  # decorator invoked with no arguments
        return wrap(*args)
    else:  # decorator invoked with arguments, return decorator
        return wrap


def aoc_input_path(year, day):
    """return the fully qualified path to the input and output files for year, day"""
    year_day = {'year': year, 'day': day, 'config': config.dir}
    for f in ('input_format', 'output_format'):
        file_format = config['files'][f]
        file_path = os.path.normpath(os.path.expandvars(os.path.expanduser(file_format.format(**year_day))))
        yield file_path

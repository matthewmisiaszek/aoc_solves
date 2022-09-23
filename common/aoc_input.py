import os
from configparser import ConfigParser


def aoc_input(year, day):
    if __name__=='__main__':
        module_path = ''
    else:
        module_path = os.path.dirname(__file__)+'/'
    cfg = 'config.ini'
    config = ConfigParser()
    config.read(module_path+cfg)
    input_path = config['files']['input_directory']
    file_format = config['files']['input_format']
    file_variables = config['files']['input_variables']
    year_day = {'year':year,'day':day}
    vars = [year_day[var] for var in file_variables.split(',')]
    input_path = os.path.expandvars(input_path)
    input_path = os.path.expanduser(input_path)
    full_path = input_path + file_format.format(*vars)
    return open(full_path).read().strip()

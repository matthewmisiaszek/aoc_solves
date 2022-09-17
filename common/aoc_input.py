import os
def aoc_input(year, day):
    if __name__=='__main__':
        module_path = ''
    else:
        module_path = os.path.dirname(__file__)+'/'
    cfg = 'paths.cfg'
    paths = [path.split(': ') for path in open(module_path + cfg).read().strip().split('\n')]
    paths = {name:path for name, path in paths}
    input_path = paths['input']
    input_path = os.path.expandvars(input_path)
    input_path = os.path.expanduser(input_path)
    full_path = input_path + '/{:04d}/{:02d}_in'.format(year, day)
    return open(full_path).read().strip()

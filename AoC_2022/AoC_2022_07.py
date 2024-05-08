import blitzen
import re

ROOT = '/'
FS_SIZE = 70000000
NEED_SIZE = 30000000
P1SIZE = 100000
PARENT = '..'
CDPAT = r'\$ cd (.*)'
FPAT = r'(\d+).*'


@blitzen.run
def main(input_string, verbose=False):
    root_path = (ROOT,)
    path = root_path
    directories = {path: 0}
    for line in input_string.split('\n'):
        d = re.search(CDPAT, line)
        if d:
            d = d.group(1)
            if d == PARENT:
                path = path[:-1]
            elif d == ROOT:
                path = root_path
            else:
                path += (d,)
                if path not in directories:
                    directories[path] = 0
        else:
            f = re.search(FPAT, line)
            if f:
                directories[path] += int(f.group(1))

    for directory in sorted(directories.keys(), key=len, reverse=True):
        if len(directory) > 1:
            directories[directory[:-1]] += directories[directory]

    p1 = sum(directory for directory in directories.values() if directory <= P1SIZE)

    need = NEED_SIZE - FS_SIZE + directories[root_path]
    for p2 in sorted(directories.values()):
        if p2 >= need:
            break
    return p1, p2


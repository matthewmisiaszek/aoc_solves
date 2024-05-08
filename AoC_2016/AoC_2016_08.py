import blitzen
import re


@blitzen.run
def main(input_string, verbose=False):
    on, off = '#', ' '
    screen_width, screen_height = 50, 6
    input_string = re.sub('x=|y=|by', '', input_string)
    screen = [[off] * screen_width] * screen_height
    for line in input_string.split('\n'):
        line = line.split()
        cmd = line.pop(0)
        if cmd == 'rect':
            x, y = (int(i) for i in line.pop(0).split('x'))
            for yi in range(y):
                screen[yi] = [on] * x + screen[yi][x:]
        elif cmd == 'rotate':
            axis = line.pop(0)
            if axis == 'column':
                screen = list(zip(*screen))
            a = int(line.pop(0))
            b = int(line.pop(0))
            screen[a] = screen[a][-b:] + screen[a][:-b]
            if axis == 'column':
                screen = list(map(list, zip(*screen)))
        if verbose:
            code = '\n'.join([''.join(row) for row in screen])
            print(code)
    code = '\n'.join([''.join(row) for row in screen])
    p1 = code.count(on)
    p2 = code
    return p1, p2


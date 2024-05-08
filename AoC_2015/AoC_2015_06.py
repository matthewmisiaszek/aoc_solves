import blitzen
import re
import numpy as np


def main(input_string, verbose=False):
    size = 1000
    pattern = r'(.*) (\d*),(\d*) through (\d*),(\d*)'
    zero = np.zeros((size, size))
    one = np.full(zero.shape, 1)
    p1 = zero.copy()
    p2 = p1.copy()
    for line in input_string.split('\n'):
        command, x1, y1, x2, y2 = re.match(pattern, line).groups()
        x1, y1, x2, y2 = (int(i) for i in (x1, y1, x2, y2))
        affected = (slice(x1, x2 + 1), slice(y1, y2 + 1))
        if command == 'turn on':
            p1[affected] = 1
            p2[affected] += 1
        elif command == 'turn off':
            p1[affected] = 0
            p2[affected] -= 1
            p2 = np.maximum(p2, zero)
        elif command == 'toggle':
            p1[affected] = one[affected] - p1[affected]
            p2[affected] += 2
    p1 = int(p1.sum())
    p2 = int(p2.sum())
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2015, day=6, verbose=True)

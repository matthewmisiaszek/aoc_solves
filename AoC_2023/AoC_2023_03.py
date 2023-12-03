import dancer
import re
from collections import defaultdict


EXCLUDE = '.\n'
DIGIT = '1234567890'
GEAR = '*'


def main(input_string, verbose=False):
    p1 = 0
    width = input_string.find('\n') + 1
    input_string += '.' * width
    gears = defaultdict(list)
    for number in re.finditer(r'\d+', input_string):
        val = int(number.group(0))
        adj = False
        neighbors = []
        for i in range(number.start()-1, number.end()+1):
            for a in (-1, 1):
                neighbors.append(i + a * width)
        neighbors.append(number.start() - 1)
        neighbors.append(number.end())
        for n in neighbors:
            c = input_string[n]
            if c in EXCLUDE:
                continue
            adj = True
            if c is GEAR:
                gears[n].append(val)
        if adj:
            p1 += val

    p2 = 0
    for gear in gears.values():
        if len(gear) == 2:
            p2 += gear[0] * gear[1]
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=3, verbose=True)

import dancer
from common.misc import CRT
import re


def main(input_string, verbose=False):
    pattern = 'Disc #(\d*) has (\d*) positions; at time=0, it is at position (\d*).'
    n, b = zip(*[(int(n), -1 * (int(p) + int(s)))
                 for p, n, s in re.findall(pattern, input_string)])
    p1 = CRT(n, b)
    n += (11,)
    b += (-1 - len(b),)
    p2 = CRT(n, b)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=15, verbose=True)

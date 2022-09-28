import DANCER
import numpy as np
from common import misc


class PowerGrid:
    def __init__(self, gridsn, size=300):
        self.cellpower = np.array(
            [[misc.digits(((x + 10) * y + gridsn) * (x + 10))[-3] - 5 for x in range(1, size + 1)] for y in
             range(1, size + 1)])
        self.sumtable = np.array([[self.cellpower[:y + 1, :x + 1].sum() for x in range(size)] for y in range(size)])
        self.size = size

    def squarepower(self, x, y, size):
        shape = self.sumtable.shape
        ret = 0
        if x + size <= shape[1] and y + size <= shape[0]:
            ret += self.sumtable[y + size - 1, x + size - 1]
        if x > 0:
            ret -= self.sumtable[y + size - 1, x - 1]
        if y > 0:
            ret -= self.sumtable[y - 1, x + size - 1]
        if x > 0 and y > 0:
            ret += self.sumtable[y - 1, x - 1]
        return ret


def maxofsize(powergrid, size):
    maxpower = 0
    maxloc = (0, 0)
    for x in range(0, powergrid.size - size):
        for y in range(0, powergrid.size - size):
            power = powergrid.squarepower(x, y, size)
            if power > maxpower:
                maxpower = power
                maxloc = (x + 1, y + 1)
    return maxpower, maxloc


def main(input_string, verbose=False):
    input_int = int(input_string)
    powergrid = PowerGrid(input_int)
    p1 = maxofsize(powergrid, 3)[1]
    maxpower = 0
    for size in range(3, powergrid.size - 1):
        newpower = maxofsize(powergrid, size)
        if newpower[0] > maxpower:
            maxpower = newpower[0]
            maxloc = newpower[1]
            maxsize = size
    p2 = (*maxloc, maxsize)
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2018, day=11, verbose=True)

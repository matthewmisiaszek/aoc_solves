from common2021 import aoc_input
import time
from collections import defaultdict


def intersect(a, b):
    ret = []
    for ax, bx in zip(a, b):
        minx = max(min(ax), min(bx))
        maxx = min(max(ax), max(bx))
        if minx <= maxx:
            ret.append((minx, maxx))
        else:
            return False
    return tuple(ret)


def volume(region):
    ret = 1
    for n, x in region:
        ret *= x - n + 1
    return ret


def parse(init_proc):
    for d in 'x=.yz,':
        init_proc = init_proc.replace(d, ' ')
    ret = []
    for step in init_proc.split('\n'):
        step = step.split()
        state, dims = step[0], step[1:]
        xn, xx, yn, yx, zn, zx = [int(i) for i in dims]
        region = ((xn, xx), (yn, yx), (zn, zx))
        ret.append((region, state == 'on'))
    return ret


def startup(init_proc):
    reactor, power, power_states = defaultdict(int), 0, []
    for region, state in init_proc:
        for region2, value2 in tuple(reactor.items()):
            intersection = intersect(region, region2)
            if intersection:
                reactor[intersection] -= value2
                power -= value2 * volume(intersection)
                if reactor[intersection] == 0:
                    reactor.pop(intersection)
        if state:
            reactor[region] += 1
            power += volume(region)
        power_states.append(power)
    return power_states


def main(input_string, verbose=False):
    init_proc = parse(input_string)
    init_proc += [(((-50, 50), (-50, 50), (-50, 50)), False)]  # turn off init_proc area and measure difference
    power_states = startup(init_proc)
    p1 = power_states[-2] - power_states[-1]
    p2 = power_states[-2]
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2021, 22), verbose=True)

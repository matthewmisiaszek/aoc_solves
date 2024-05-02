import blitzen
from donner import spatial, printer
import re


def parse(input_string):
    dirt = set()
    for axis, a, bn, bx in re.findall(r'(.)=(\d*), (?:.)=(\d*)..(\d*)', input_string):
        a, bn, bx = (int(i) for i in (a, bn, bx))
        if axis == 'x':
            dirt.update({spatial.Point(a, b) for b in range(bn, bx + 1)})
        else:
            dirt.update({spatial.Point(b, a) for b in range(bn, bx + 1)})
    bn, bx = spatial.bounds(dirt)
    return dirt, bn.x, bx.x, bn.y, bx.y


def print_fun(dirt, wet, settled):
    pdict = {}
    pdict.update({point: '~' for point in settled})
    pdict.update({point:'#' for point in dirt})
    pdict.update({point: '|' for point in wet})

    printer.printdict(pdict, default='.')


def main(input_string, verbose=False):
    dirt, xn, xx, yn, yx = parse(input_string)
    wet = {spatial.Point(500, yn)}
    settled = dirt.copy()
    # print_fun(dirt, wet, settled)
    changes = -1
    while changes != 0:
        lwet = len(wet)
        lset = len(settled)
        tocheck = wet.copy()
        for w in tuple(wet):
            if w in wet and w.y<=yx:
                loc = w + spatial.SOUTH
                if loc in wet:
                    continue
                if loc not in settled:
                    while loc not in settled and loc.y<=yx:
                        wet.add(loc)
                        loc += spatial.SOUTH
                    continue
                loc += spatial.NORTH
                # print_fun(dirt, wet, settled)
                if loc not in tocheck:
                    continue
                lwall = rwall = False
                while loc not in settled and loc+spatial.SOUTHWEST in settled:
                    loc += spatial.WEST
                lbound = loc.x
                if loc in settled:
                    lwall = True
                    loc += spatial.EAST
                while loc not in settled and loc+spatial.SOUTHEAST in settled:
                    loc += spatial.EAST
                if loc in settled:
                    rwall = True
                rbound = loc.x
                y = loc.y
                lbound += 1 if lwall else -1
                rbound += -1 if rwall else 1
                layer = {spatial.Point(x, y) for x in range(lbound, rbound + 1)}
                if lwall and rwall:
                    wet.difference_update(layer)
                    tocheck.difference_update(layer)
                    settled.update(layer)
                else:
                    wet.update(layer)
                    tocheck.difference_update(layer)
                # print_fun(dirt, wet, settled)
        changes = abs(len(wet)-lwet) + abs(len(settled)-lset)
    wet = wet - settled
    settled = settled - dirt

    if verbose:
        print_fun(dirt, wet, settled)
    p1 = len(wet)+len(settled)
    p2 = len(settled)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=17, verbose=True)
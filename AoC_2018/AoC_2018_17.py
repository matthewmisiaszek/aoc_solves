import dancer
from common import spatial, printer
import re


def parse(input_string):
    dirt = set()
    for axis, a, bn, bx in re.findall('(.)=(\d*), (?:.)=(\d*)..(\d*)', input_string):
        a, bn, bx = (int(i) for i in (a, bn, bx))
        if axis == 'x':
            dirt.update({planar.Point(a, b) for b in range(bn, bx + 1)})
        else:
            dirt.update({planar.Point(b, a) for b in range(bn, bx + 1)})
    xn, yn, xx, yx = planar.bounds(dirt)
    # f = input_string.split('\n')
    # dirt = set()
    # for line in f:
    #     a,b = line.split(',')
    #     a1, a2 = a.split('=')
    #     b1, b2 = b.split('=')
    #     c = a1 =='x'
    #     d = int(a2)
    #     bn, bx = b2.split('..')
    #     bn = int(bn)
    #     bx = int(bx)
    #     for b in range(bn, bx+1):
    #         if c:
    #             dirt.add((d, b))
    #         else:
    #             dirt.add((b, d))
    # yn = min(dirt, key=lambda x: x[1])[1]
    # yx = max(dirt, key=lambda x: x[1])[1]
    # xn = min(dirt)[0]-1
    # xx = max(dirt)[0]+1
    return dirt, xn, xx, yn, yx

def getleft(point):
    return (point[0]-1, point[1])
def getright(point):
    return (point[0]+1, point[1])
def getfloor(point):
    return (point[0], point[1]+1)


def print_fun(dirt, wet, settled):
    pdict = {}
    pdict.update({point: '~' for point in settled})
    pdict.update({point:'#' for point in dirt})
    pdict.update({point: '|' for point in wet})

    printer.printdict(pdict, default='.')
    # s=''
    # for y in range(yn, yx+1):
    #     for x in range(xn,xx+1):
    #         point = (x,y)
    #         if point in dirt:
    #             s+='#'
    #         elif point in wet:
    #             s+='|'
    #         elif point in settled:
    #             s+='~'
    #         else:
    #             s+='.'
    #     s+='\n'
    # print(s)

def main(input_string, verbose=False):
    dirt, xn, xx, yn, yx = parse(input_string)

    turtle = planar.Turtle()
    wet = {planar.Point(500, yn)}
    settled = dirt.copy()
    # print_fun(dirt, wet, settled)
    changes = -1
    while changes != 0:
        lwet = len(wet)
        lset = len(settled)
        for w in tuple(wet):
            if w in wet and w.y<=yx:
                turtle.goto(position=w)
                while turtle.position not in settled and turtle.position.y<=yx:
                    wet.add(turtle.position)
                    turtle.move(planar.SOUTH)
                turtle.move(planar.NORTH)
                while turtle.position not in settled and turtle.position+turtle.dict[planar.SOUTHWEST] in settled:
                    turtle.move(planar.WEST)
                lwall = turtle.position in settled
                lbound = turtle.position.x
                turtle.move(planar.EAST)
                while turtle.position not in settled and turtle.position+turtle.dict[planar.SOUTHEAST] in settled:
                    turtle.move(planar.EAST)
                rwall = turtle.position in settled
                rbound = turtle.position.x
                y = turtle.position.y
                lbound += 1 if lwall else -1
                rbound += -1 if rwall else 1
                layer = {planar.Point(x, y) for x in range(lbound, rbound+1)}
                if lwall and rwall:
                    wet.difference_update(layer)
                    settled.update(layer)
                else:
                    wet.update(layer)
        changes = abs(len(wet)-lwet) + abs(len(settled)-lset)
        print(changes)
        # print('\n\n\n\n')
        # print_fun(dirt, wet, settled)
    # old_wet = set()
    # old_settled = set()
    # while wet!=old_wet or settled!=old_settled:
    #     old_wet = wet.copy()
    #     old_settled = settled.copy()
    #     for wi in tuple(wet):
    #         if wi in wet:
    #             floor = getfloor(wi)
    #             if floor in dirt or floor in settled:
    #                 left = getleft(wi)
    #                 while left not in settled and getfloor(left) in settled:
    #                     left = getleft(left)
    #                 lbound = left[0]
    #                 lwall = left in settled
    #                 right = getright(wi)
    #                 while right not in settled and getfloor(right) in settled:
    #                     right = getright(right)
    #                 rbound = right[0]
    #                 rwall = right in settled
    #                 if lwall and rwall:
    #                     for x in range(lbound+lwall, rbound-rwall+1):
    #                         wet.discard((x, wi[1]))
    #                         settled.add((x, wi[1]))
    #                 else:
    #                     for x in range(lbound+lwall, rbound-rwall+1):
    #                         wet.add((x, wi[1]))
    #             else:
    #                 while floor[1]<=yx and floor not in settled and floor not in wet:
    #                     wet.add(floor)
    #                     floor = getfloor(floor)

    settled = settled - dirt
    if verbose:
        print_fun(dirt, wet, settled)
    p1 = len(wet)+len(settled)
    p2 = len(settled)
    return p1, p2

if __name__ == "__main__":
    dancer.run(main, year=2018, day=17, verbose=True)
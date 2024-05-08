import blitzen
from AoC_2019.intcode import Intcode
from donner import graph, spatial

COMMANDS = {(0, 1): 1, (0, -1): 2, (-1, 0): 3, (1, 0): 4}
COMMANDS = {spatial.NAMES_2D[direction]: i + 1 for i, direction in enumerate('UDLR')}


@blitzen.run
def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    droid = Intcode(program)
    loc, heading = spatial.Point(), 0
    ship_set = set()
    start = loc

    while True:
        # ship is a network of width-1 hallways with no loops
        # search path is "keep your right hand on the wall until you get back to start"
        # if you bump into a wall, turn left.  If you don't, turn right.  If you reach start, break.
        code = COMMANDS[spatial.ENWS[heading]]
        status = droid.run(code)
        if status == 0:
            heading += 1
        else:
            heading -= 1
            loc = loc + spatial.ENWS[heading]
            ship_set.add(loc)
            if status == 2:
                o2sys = loc
            if loc == start:
                break
        heading %= 4

    # if verbose is True:
    #     pdict = {key: '+' for key in ship_set}
    #     pdict[start] = 'D'
    #     pdict[o2sys] = 'O'
    #     printer.printdict(pdict)

    # length of shortest path to every point in ship relative to o2sys
    ship_graph = graph.set_to_graph(ship_set)
    dijkstra = ship_graph.dijkstra(o2sys, ship_set, all_paths=True)

    p1 = dijkstra[start]
    p2 = max(dijkstra.values())
    return p1, p2


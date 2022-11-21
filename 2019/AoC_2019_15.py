import dancer
from AoC_2019.intcode import Intcode
from common import elementwise as ew, printer, graph, constants as con

COMMANDS = {(0, 1): 1, (0, -1): 2, (-1, 0): 3, (1, 0): 4}


def main(input_string, verbose=False):
    program = [int(i) for i in input_string.split(',')]
    droid = Intcode(program)
    loc, heading = con.origin2, 0
    ship = graph.Graph()
    start = loc

    while True:
        # ship is a network of width-1 hallways with no loops
        # search path is "keep your right hand on the wall until you get back to start"
        # if you bump into a wall, turn left.  If you don't, turn right.  If you reach start, break.
        code = COMMANDS[con.D2D4[heading]]
        status = droid.run(code)
        if status == 0:
            heading += 1
        else:
            heading -= 1
            nloc = ew.sum2d(loc, con.D2D4[heading])
            ship.add_edge_eq(loc, nloc)
            loc = nloc
            if status == 2:
                o2sys = loc
            if loc == start:
                break
        heading %= 4

    if verbose is True:
        pdict = {key: '+' for key in ship.graph.keys()}
        pdict[start] = 'D'
        pdict[o2sys] = 'O'
        printer.printdict(pdict)

    # length of shortest path to every point in ship relative to o2sys
    dijkstra = ship.dijkstra(o2sys, ship.graph.keys(), all_paths=True)

    p1 = dijkstra[start]
    p2 = max(dijkstra.values())
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=15, verbose=True)

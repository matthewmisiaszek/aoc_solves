import dancer
from common import constants as con, elementwise as ew


def main(input_string, verbose=False):
    wires = []
    for wire_path in input_string.split('\n'):
        loc = con.origin2
        wire = {}
        steps = 0
        for move in wire_path.split(','):
            direction = move[0]
            distance = int(move[1:])
            for _ in range(distance):
                steps += 1
                loc = ew.sum2d(loc, con.UDLR[direction])
                if loc not in wire:
                    wire[loc] = steps
        wires.append(wire)
    wire0, wire1 = wires
    intersections = wire0.keys() & wire1.keys()
    p1 = min(ew.manhattan(a) for a in intersections)
    p2 = min(wire0[a] + wire1[a] for a in intersections)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=3, verbose=True)

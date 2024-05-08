import blitzen
from donner import spatial as sp


@blitzen.run
def main(input_string, verbose=False):
    wires = []
    for wire_path in input_string.split('\n'):
        loc = sp.Point()
        wire = {}
        steps = 0
        for move in wire_path.split(','):
            direction = move[0]
            distance = int(move[1:])
            for _ in range(distance):
                steps += 1
                loc += sp.NAMES_2D[direction]
                if loc not in wire:
                    wire[loc] = steps
        wires.append(wire)
    wire0, wire1 = wires
    intersections = wire0.keys() & wire1.keys()
    p1 = min(a.manhattan() for a in intersections)
    p2 = min(wire0[a] + wire1[a] for a in intersections)
    return p1, p2


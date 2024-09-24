import blitzen
from donner import graph, spatial, printer


NEIGHBORS = {
    'S': set(spatial.ENWS),
    'F': {spatial.EAST, spatial.SOUTH},
    '7': {spatial.WEST, spatial.SOUTH},
    'L': {spatial.NORTH, spatial.EAST},
    'J': {spatial.NORTH, spatial.WEST},
    '|': {spatial.SOUTH, spatial.NORTH},
    '-': {spatial.WEST, spatial.EAST},
}
HAS_NORTH = {key for key, val in NEIGHBORS.items() if spatial.NORTH in val}
START = 'S'


@blitzen.run
def main(input_string, verbose=False):
    sketch = graph.text_to_dict(input_string)
    for start, char in sketch.items():
        if char == START:
            break
    pipe = set()
    position = start
    while True:
        pipe.add(position)
        for heading in NEIGHBORS[sketch[position]]:
            ph = position + heading
            if ph not in pipe and (
                    position != start or
                    (ph in sketch and sketch[ph] in NEIGHBORS and heading * -1 in NEIGHBORS[sketch[ph]])
            ):
                position = ph
                break
        else:
            break
    p1 = len(pipe) // 2
    nb, xb = spatial.bounds(sketch)
    within = set()
    for y in range(nb.y, xb.y+1):
        inside = False
        for x in range(nb.x, xb.x+1):
            point = spatial.Point(x, y)
            if point in pipe:
                if sketch[point] in HAS_NORTH:
                    inside = not inside
            else:
                if inside:
                    within.add(point)
    p2 = len(within)
    if verbose:
        charmap = {a: b for a, b in zip('-|F7LJS', '═║╔╗╚╝╬')}
        toprint = {p: 'O' for p in sketch.keys()}
        toprint.update({p: charmap[sketch[p]] for p in pipe})
        toprint.update({p: 'I' for p in within})
        printer.printdict(toprint)
    return p1, p2


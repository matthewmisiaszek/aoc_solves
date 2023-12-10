import dancer
from common import graph, spatial, printer

NEIGHBORS = {
    'S': set(spatial.ENWS),
    'F': {spatial.EAST, spatial.SOUTH},
    '7': {spatial.WEST, spatial.SOUTH},
    'L': {spatial.NORTH, spatial.EAST},
    'J': {spatial.NORTH, spatial.WEST},
    '|': {spatial.SOUTH, spatial.NORTH},
    '-': {spatial.WEST, spatial.EAST},
}
START = 'S'


def region_size(region, tiles, bounds):
    region &= tiles
    queue = region.copy()
    while queue:
        current = queue.pop()
        for n in spatial.ENWS:
            neighbor = current + n
            if neighbor in region:
                continue
            if neighbor in tiles:
                queue.add(neighbor)
                region.add(neighbor)
            if not spatial.inbounds(neighbor, bounds):
                region.clear()
                return 0
    return len(region)


def main(input_string, verbose=False):
    sketch = graph.text_to_dict(input_string)
    for start, char in sketch.items():
        if char == START:
            break
    animal = spatial.Turtle(position=start)
    rset, lset, new = set(), set(), True
    while new:
        for new_heading in NEIGHBORS[sketch[animal.position]]:
            if animal.position != start and new_heading == animal.heading * -1:
                continue
            ahead = animal.position + new_heading
            if ahead not in sketch:
                continue
            ahead_type = sketch[ahead]
            if ahead_type not in NEIGHBORS:
                continue
            if new_heading * -1 not in NEIGHBORS[ahead_type]:
                continue
            break
        animal.goto(heading=new_heading)
        lset.add(animal.position + animal.heading.left())
        rset.add(animal.position + animal.heading.right())
        _, _, new = animal.drive()
        lset.add(animal.position + animal.heading.left())
        rset.add(animal.position + animal.heading.right())
    tiles = set(sketch.keys()) - animal.visited
    bounds = spatial.bounds(sketch.keys())
    p2 = sum(region_size(region, tiles, bounds) for region in (lset, rset))
    p1 = len(animal.visited) // 2
    if verbose:
        toprint = {p: 'O' for p in sketch.keys()}
        toprint.update({p: sketch[p] for p in animal.visited})
        toprint.update({p: 'I' for p in lset | rset})
        printer.printdict(toprint)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=10, verbose=True)

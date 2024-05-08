import blitzen
from donner import spatial as sp


@blitzen.run
def main(input_string, verbose=False):
    directions = [(line[0], int(line[1:])) for line in input_string.split(', ')]
    heading = sp.NORTH
    position = sp.Point()
    p2 = None
    history = {position}
    for turn, distance in directions:
        if turn == 'R':
            heading = heading.right()
        elif turn == 'L':
            heading = heading.left()
        for _ in range(distance):
            position += heading
            if p2 is None and position in history:
                p2 = position.manhattan()
            history.add(position)
    p1 = position.manhattan()
    return p1, p2


import dancer
from common import cart2d
from common import elementwise as ew


def main(input_string, verbose=False):
    directions = [(line[0], int(line[1:])) for line in input_string.split(', ')]
    heading = cart2d.Cart().north
    position = (0, 0)
    p2 = None
    history = {position}
    for turn, distance in directions:
        if turn == 'R':
            heading = heading.right
        elif turn == 'L':
            heading = heading.left
        for _ in range(distance):
            position = heading.move(position)
            if p2 is None and position in history:
                p2 = sum(ew.eabs(position))
            history.add(position)
    p1 = sum(ew.eabs(position))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=1, verbose=True)

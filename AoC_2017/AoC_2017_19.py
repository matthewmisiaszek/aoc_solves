import blitzen
from donner import printer
from donner import graph
from donner import spatial as sp


def main(input_string, verbose=False):
    path = graph.text_to_dict(input_string, exclude=' ')
    letters = {loc for loc, c in path.items() if c not in '+|-'}
    seen_letters = ''
    steps = 1
    direction = sp.SOUTH
    loc = sp.Point(input_string.split('\n')[0].find('|'), 0)
    while True:
        steps += 1
        loc += direction
        if loc in letters:
            seen_letters += path[loc]
        elif loc not in path:
            steps -= 1
            loc -= direction
            if loc + direction.left() in path:
                direction = direction.left()
            elif loc + direction.right() in path:
                direction = direction.right()
            else:
                break
    if verbose:
        printer.printdict(path)
    p1 = seen_letters
    p2 = steps
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=19, verbose=True)

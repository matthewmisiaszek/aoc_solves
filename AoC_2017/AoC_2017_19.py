import dancer
from common.cart2d import Cart
from common import printer


def main(input_string, verbose=False):
    path = {(x, y): c for y, line in enumerate(input_string.split('\n')) for x, c in enumerate(line) if c != ' '}
    letters = {loc for loc, c in path.items() if c not in '+|-'}
    seen_letters = ''
    steps = 1
    direction = Cart().south
    loc = (input_string.split('\n')[1].find('|'), 1)
    while True:
        steps += 1
        loc = direction.move(loc)
        if loc in letters:
            seen_letters += path[loc]
        elif loc not in path:
            steps -= 1
            loc = direction.back.move(loc)
            if direction.left.move(loc) in path:
                direction = direction.left
            elif direction.right.move(loc) in path:
                direction = direction.right
            else:
                break
    if verbose:
        printer.printdict(path)
    p1 = seen_letters
    p2 = steps
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=19, verbose=True)

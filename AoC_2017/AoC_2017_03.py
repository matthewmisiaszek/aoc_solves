import dancer
from common import cart2d
from common import constants as con
from common import elementwise as ew


def part1(square):
    a = (square ** .5) // 1  # size of largest complete square of data
    b = square - a ** 2  # remainder
    c = b % (a + 1)  # position along side
    d = (a - 1) // 2  # half length of side
    return int(d + abs(d - c))


def part2(target):
    cart = cart2d.Cart()
    memory = {(0, 0): 1}
    square = (0, 0)
    heading = cart.east
    value = 1
    while value < target:
        if heading.left.move(square) not in memory:
            heading = heading.left
        square = heading.move(square)
        neighbors = tuple(ew.sum2d(square, d) for d in con.D2D8)
        value = sum((memory[neighbor] for neighbor in neighbors if neighbor in memory))
        memory[square] = value
    return value


def main(input_string, verbose=False):
    input_int = int(input_string)
    p1 = part1(input_int)
    p2 = part2(input_int)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=3, verbose=True)

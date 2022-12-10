import dancer
from common import constants as con, elementwise as ew


def simulate_rope(moves, length):
    rope = [con.origin2] * length
    tails = [{con.origin2} for _ in range(length)]
    for direction, distance in moves:
        rope[0] = ew.sum2d(rope[0], con.UDLR[direction], distance)
        for i in range(length - 1):
            diff = ew.ediff(rope[i], rope[i + 1])
            while max(ew.eabs(diff)) > 1:
                rope[i + 1] = ew.sum2d(rope[i + 1], ew.esign(diff))
                tails[i + 1].add(rope[i + 1])
                diff = ew.ediff(rope[i], rope[i + 1])
    return tails


def parse(input_string):
    moves = []
    for line in input_string.split('\n'):
        direction, distance = line.split()
        moves.append((direction, int(distance)))
    return moves


def main(input_string, verbose=False):
    moves = parse(input_string)
    tails = simulate_rope(moves, 10)
    p1 = len(tails[1])
    p2 = len(tails[-1])
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=9, verbose=True)

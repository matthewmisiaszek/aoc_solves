import dancer
from common import constants as con, elementwise as ew


def simulate_rope(moves, length):
    rope = [con.origin2] * length
    tails = {con.origin2}
    for direction, distance in moves:
        for _ in range(distance):
            rope[0] = ew.sum2d(rope[0], con.UDLR[direction])
            for i in range(length - 1):
                (ax, ay), (bx, by) = rope[i], rope[i + 1]
                dx, dy = ax - bx, ay - by
                if abs(dx) > 1 or abs(dy) > 1:
                    if abs(dx) > 1:
                        dx //= abs(dx)
                    if abs(dy) > 1:
                        dy //= abs(dy)
                    rope[i + 1] = (bx + dx, by + dy)
            tails.add(rope[-1])
    return len(tails)


def parse(input_string):
    moves = []
    for line in input_string.split('\n'):
        direction, distance = line.split()
        moves.append((direction, int(distance)))
    return moves


def main(input_string, verbose=False):
    moves = parse(input_string)
    p1 = simulate_rope(moves, 2)
    p2 = simulate_rope(moves, 10)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=9, verbose=True)

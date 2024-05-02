import blitzen
from donner import spatial


def simulate_rope(moves, length):
    rope = [spatial.Point()] * length
    tails = [{spatial.Point()} for _ in range(length)]
    for direction, distance in moves:
        for _ in range(distance):
            rope[0] += spatial.NAMES_2D[direction]
            for i in range(1, length):
                diff = rope[i - 1] - rope[i]
                if abs(diff.x) > 1 or abs(diff.y) > 1:
                    rope[i] += diff.sign()
                    tails[i].add(rope[i])
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
    blitzen.run(main, year=2022, day=9, verbose=True)

import blitzen


def part1(n_elves):
    elves = tuple(range(1, n_elves + 1))
    while len(elves) > 1:
        elves = elves[::2][len(elves) % 2 == 1:]
    return elves[0]


def part2(n_elves):
    elves = list(range(1, n_elves + 1))
    while len(elves) > 1:
        split = len(elves) // 2 - 1 + 2 * (len(elves) % 2)
        elves = elves[split:] + elves[:split]
        elves = elves[::3]
        elves.sort()
    return elves[0]


def main(input_string, verbose=False):
    n_elves = int(input_string)
    p1 = part1(n_elves)
    p2 = part2(n_elves)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2016, day=19, verbose=True)

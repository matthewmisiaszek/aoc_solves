import dancer

ABC = 'ABC'
XYZ = 'XYZ'


def part1(opp, you):
    out = (you - opp + 1) % 3
    return you + 1 + out * 3


def part2(opp, out):
    you = (opp + out - 1) % 3
    return out * 3 + you + 1


def parse(input_string):
    split_string = [line.split() for line in input_string.split('\n')]
    guide = [(ABC.find(a), XYZ.find(b)) for a, b in split_string]
    return guide


def main(input_string, verbose=False):
    guide = parse(input_string)
    p1 = sum(part1(opp, you) for opp, you in guide)
    p2 = sum(part2(opp, out) for opp, out in guide)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=2, verbose=True)

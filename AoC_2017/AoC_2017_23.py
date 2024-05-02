import blitzen
import AoC_2017.AoC_2017_18 as tablet


def isprime(n):
    for i in range(2, int(n ** .5) + 1):
        if n % i == 0:
            return False
    return True


def part2(instructions):
    h = 0
    b0 = int(instructions[0][2]) * int(instructions[4][2]) - int(instructions[5][2])
    c0 = b0 - int(instructions[7][2])
    inc = -int(instructions[30][2])
    for b in range(b0, c0 + 1, inc):
        if not isprime(b):
            h += 1
    return h


def main(input_string, verbose=False):
    instructions = tuple(line.split() for line in input_string.split('\n'))
    p1 = next(tablet.program(instructions))
    p2 = part2(instructions)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=23, verbose=True)

import blitzen
import re


def part1(example_list):
    return sum(a <= password.count(c) <= b
               for a, b, c, password in example_list)


def part2(example_list):
    return sum((a <= len(password) and password[a - 1] == c) ^
               (b <= len(password) and password[b - 1] == c)
               for a, b, c, password in example_list)


@blitzen.run
def main(input_string, verbose=False):
    pattern = '(.*)-(.*) (.): (.*)'
    example_list = tuple((int(a), int(b), c, d) for a, b, c, d in re.findall(pattern, input_string))
    p1 = part1(example_list)
    p2 = part2(example_list)
    return p1, p2


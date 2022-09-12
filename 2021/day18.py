from common2021 import aoc_input


def explode(number):
    for i, (depth, value) in enumerate(number):
        if depth >= 4:
            if i >= 1:
                number[i - 1][1] += number[i][1]
            if i + 2 < len(number):
                number[i + 2][1] += number[i + 1][1]
            number[i] = [depth - 1, 0]
            number.pop(i + 1)
            return True
    return False


def split(number):
    for i, (depth, value) in enumerate(number):
        if value >= 10:
            number[i] = [depth + 1, value // 2]
            number.insert(i + 1, [depth + 1, value - value // 2])
            return True
    return False


def magnitude(number):
    while len(number) > 1:
        maxdepth = max(number)[0]
        for i, (depth, value) in enumerate(number):
            if depth == maxdepth:
                number[i] = [depth - 1, value * 3 + number[i + 1][1] * 2]
                number.pop(i + 1)
                break
    return number[0][1]


def parse(input_file):
    f = input_file.split('\n')
    depths = [[line[:i].count('[') - line[:i].count(']') - 1
               for i in range(len(line))]
              for line in f]
    numbers = tuple(tuple((d, int(c))
                          for d, c in zip(depth, line)
                          if c in '0123456789')
                    for depth, line in zip(depths, f))
    return numbers


def part1(numbers):
    result = numbers[0]
    numbers = [[[n[0] + 1, n[1]] for n in number]
               for number in numbers[1:]]
    for number in numbers:
        result = [[n[0] + 1, n[1]] for n in result] + number
        while explode(result) or split(result):
            pass
    return magnitude(result)


def part2(numbers):
    return max([part1([numbers[a], numbers[b]])
                for a in range(len(numbers))
                for b in range(len(numbers))
                if a != b])


def main(input_string, verbose=False):
    numbers = parse(input_string)
    p1 = part1(numbers)
    p2 = part2(numbers)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2021, 18), verbose=True)

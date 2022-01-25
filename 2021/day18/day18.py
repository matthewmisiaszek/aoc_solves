def addto(x, n, i):
    if isinstance(x[1 - i], int):
        x[1 - i] += n
    else:
        recadd(x[1 - i], n, i)


def recadd(x, n, i):
    if isinstance(x[i], list):
        recadd(x[i], n, i)
    else:
        x[i] += n


def explode(x, depth):
    for i in range(2):
        if isinstance(x[i], list):
            if depth >= 3 and isinstance(x[i][0], int) and isinstance(x[i][1], int):
                addto(x, x[i][1 - i], i)
                exp = [0, 0]
                exp[i] = x[i][i]
                x[i] = 0
                return True, exp
            else:
                explosion, exp = explode(x[i], depth + 1)
                if explosion is True:
                    addto(x, exp[1 - i], i)
                    exp[1 - i] = 0
                    return True, exp
    return False, [0, 0]


def split(x):
    for i in range(2):
        if isinstance(x[i], int):
            if x[i] > 9:
                x[i] = [x[i] // 2, x[i] - x[i] // 2]
                return True
        elif isinstance(x[i], list):
            if split(x[i]):
                return True
    return False


def sums(x):
    if isinstance(x[0], list):
        x[0] = sums(x[0])
    if isinstance(x[1], list):
        x[1] = sums(x[1])
    return x[0] * 3 + x[1] * 2


def reduce(x):
    go = True
    while go is True:
        go = False
        explosion, exp = explode(x, 0)
        go = go or explosion
        if go is False:
            dosplit = split(x)
            go = go or dosplit


def part1(input_file):
    f = open(input_file).read().split('\n')
    x = eval(f.pop(0))
    for line in f:
        line = eval(line)
        x = [x, line]
        reduce(x)
    return sums(x)


def part2(input_file):
    f = open(input_file).read().split('\n')
    maxfish = 0
    for line1 in f:
        for line2 in f:
            if line1 != line2:
                x = [eval(line1), eval(line2)]
                reduce(x)
                maxfish = max(maxfish, sums(x))
    return maxfish


def main(input_file='input.txt', verbose=False):
    p1 = part1(input_file)
    p2 = part2(input_file)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)

import blitzen


def extrapolate(x):
    while any(x[-1]):
        x.append([b-a for a, b in zip(x[-1], x[-1][1:])])
    for i in range(1, len(x)):
        x[-i - 1].insert(0, x[-i - 1][0] - x[-i][0])
        x[-i - 1].append(x[-i - 1][-1] + x[-i][-1])
    return x[0][-1], x[0][0]


@blitzen.run
def main(input_string, verbose=False):
    history = [[int(i) for i in line.split()] for line in input_string.split('\n')]
    p1, p2 = (sum(i) for i in zip(*(extrapolate([line]) for line in history)))
    return p1, p2


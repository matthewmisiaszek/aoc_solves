import blitzen


def checksafe(levels):
    sign = None
    for a, b in zip(levels, levels[1:]):
        if 1 <= abs(b - a) <= 3 and (sign is None or (b > a) == sign):
            sign = b > a
        else:
            return False
    return True


@blitzen.run
def main(input_string, verbose=False):
    p1 = p2 = 0
    for line in input_string.split('\n'):
        levels = [int(i) for i in line.split()]
        if checksafe(levels):
            p1 += 1
            p2 += 1
        else:
            for i in range(len(levels)):
                if checksafe(levels[:i] + levels[i+1:]):
                    p2 += 1
                    break
    return p1, p2

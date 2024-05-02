import blitzen
from math import ceil


def main(input_string, verbose=False):
    f = input_string
    for d in ['target area: x=', ',', 'y=']:
        f = f.replace(d, '')
    target = [[int(b) for b in a.split('..')] for a in f.split()]
    for targeti in target:
        targeti.sort()

    xmin = int((-1 + (1 + 8 * target[0][0]) ** .5) // 2)
    goodc = 0
    ymax = target[1][0] * (target[1][0] + 1) // 2

    for y in range(target[1][0] - 1, -target[1][0] + 1):
        y2, airtime = -y, 0
        if y > 0:
            y2, airtime = y + 1, 2 * y + 1
        t0 = int(((1 - 2 * y2) + ((2 * y2 - 1) ** 2 - 8 * target[1][0]) ** .5) // 2) + airtime
        t1 = ceil(((1 - 2 * y2) + ((2 * y2 - 1) ** 2 - 8 * target[1][1]) ** .5) / 2) + airtime
        if t1 <= t0:
            for x in range(xmin, target[0][1] + 1):
                for t in range(t1, t0 + 1):
                    if (t >= x and target[0][0] <= x * (x + 1) // 2 <= target[0][1]) or \
                            (t < x and target[0][0] <= x * (x + 1) // 2 - (x - t) * ((x - t) + 1) // 2 <= target[0][1]):
                        goodc += 1
                        break
    p1, p2 = ymax, goodc

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2021, day=17, verbose=True)

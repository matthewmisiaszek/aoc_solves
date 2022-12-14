import dancer

ENTRANCE = 500 + 0j
FALL_PRIORITY = (0 + 1j, -1 + 1j, 1 + 1j)


def parse(input_string):
    rocks = set()
    for line in input_string.split('\n'):
        points = line.split(' -> ')
        for a, b in zip(points, points[1:]):
            ax, ay = (int(i) for i in a.split(','))
            bx, by = (int(i) for i in b.split(','))
            for x in range(min(bx, ax), max(ax, bx) + 1):
                for y in range(min(by, ay), max(ay, by) + 1):
                    rocks.add(x+y*1j)
    return rocks


def main(input_string, verbose=False):
    rocks = parse(input_string)
    lrocks = len(rocks)
    floor = max(rock.imag for rock in rocks) + 2
    p1 = None
    while ENTRANCE not in rocks:
        grain = ENTRANCE
        while True:
            for d in FALL_PRIORITY:
                ngrain = grain + d
                if ngrain not in rocks and ngrain.imag < floor:
                    grain = ngrain
                    break
            else:
                if p1 is None and grain.imag == floor - 1:
                    p1 = len(rocks) - lrocks
                rocks.add(grain)
                break
    p2 = len(rocks) - lrocks
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=14, verbose=True)

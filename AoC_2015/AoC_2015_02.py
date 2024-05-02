import blitzen


def main(input_string, verbose=False):
    paper = 0
    ribbon = 0
    for line in input_string.split('\n'):
        l, w, h = (int(i) for i in line.split('x'))
        sides = (l * w, w * h, h * l)
        paper += 2 * sum(sides) + min(sides)
        ribbon += 2 * (l + w + h - max(l, w, h)) + l * w * h

    p1 = paper
    p2 = ribbon
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2015, day=2, verbose=True)

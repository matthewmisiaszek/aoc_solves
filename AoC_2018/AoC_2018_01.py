import blitzen


def main(input_string, verbose=False):
    f = tuple(int(i) for i in input_string.split("\n"))
    s = 0
    cache = set()
    cache.add(s)
    p1 = None
    while True:
        for l in f:
            s += l
            if s in cache:
                p2 = s
                return p1, p2
            else:
                cache.add(s)
        if p1 is None:
            p1 = s


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=1, verbose=True)

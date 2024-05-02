import blitzen


def main(input_string, verbose=False):
    f = input_string.split('\n')
    p1, p2 = (sum([int(f[i]) < int(f[i + s]) for i in range(len(f) - s)]) for s in [1, 3])
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2021, day=1, verbose=True)

import dancer


def main(input_string, verbose=False):
    input_string = input_string.replace(',', ' ').replace('-', ' ')
    p1, p2 = 0, 0
    for line in input_string.split('\n'):
        a, b, c, d = (int(i) for i in line.split())
        p1 += (c - a) * (d - b) <= 0
        p2 += max(a, c) <= min(b, d)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=4, verbose=True)

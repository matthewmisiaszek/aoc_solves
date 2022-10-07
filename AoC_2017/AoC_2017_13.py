import dancer


def caught(scanner_depth, scanner_range, start):
    return (start + scanner_depth) % (scanner_range * 2 - 2) == 0


def main(input_string, verbose=False):
    firewall = tuple(tuple(int(i) for i in line.split(': '))
                     for line in input_string.split('\n'))
    p1 = sum((d * r
              for d, r in firewall
              if caught(d, r, 0)))
    p2 = 0
    while any((caught(d, r, p2)
               for d, r in firewall)):
        p2 += 1
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=13, verbose=True)

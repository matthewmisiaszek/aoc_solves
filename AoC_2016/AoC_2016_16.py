import blitzen


def generate(data, size):
    while len(data) < size:
        a = data
        b = tuple(not i for i in reversed(a))
        data = a + (False,) + b
    return data[:size]


def checksum(data):
    csum = data
    while len(csum) % 2 == 0:
        csum = tuple(a == b for a, b in zip(csum[::2], csum[1::2]))
    return csum


def csum_to_str(csum):
    io = ('0', '1')
    return ''.join(io[i] for i in csum)


def main(input_string, verbose=False):
    data = tuple(c == '1' for c in input_string)
    p1 = csum_to_str(checksum(generate(data, size=272)))
    p2 = csum_to_str(checksum(generate(data, size=35651584)))
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2016, day=16, verbose=True)

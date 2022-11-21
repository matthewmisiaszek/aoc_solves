import dancer


def makedigit(signal, pmasks, nmasks):
    ret = sum(sum(signal[a:b]) for a, b in pmasks)
    ret -= sum(sum(signal[a:b]) for a, b in nmasks)
    return abs(ret) % 10


def part1(signal):
    pmasks = tuple(tuple((j, j + i) for j in range(i - 1, len(signal), i * 4)) for i in range(1, len(signal) + 1))
    nmasks = tuple(tuple((j, j + i) for j in range(3*i-1, len(signal), i*4)) for i in range(1, len(signal)+1))
    for phase in range(100):
        signal = tuple(makedigit(signal, pmasks[i-1], nmasks[i-1]) for i in range(1, len(signal)+1))
    return ''.join(str(i) for i in signal[:8])


def fft(signal):
    a = sum(signal)
    for i in signal:
        yield a % 10
        a -= i


def part2(signal):
    offset = int(''.join(str(i) for i in signal[:7]))
    signal *= 10000
    signal = signal[offset:]
    for phase in range(100):
        signal = tuple(fft(signal))
    return ''.join(str(i) for i in signal[:8])


def main(input_string, verbose=False):
    signal = tuple(int(i) for i in input_string)
    p1 = part1(signal)
    p2 = part2(signal)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=16, verbose=True)

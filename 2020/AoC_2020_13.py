import DANCER
from common.misc import CRT


def main(input_string, verbose=False):
    earliest, ids = input_string.split('\n')
    ids = [(int(bus), -i) for i, bus in enumerate(ids.split(',')) if bus.isdigit()]
    earliest = int(earliest)
    wait, best_bus = min([(bus - earliest % bus, bus) for bus, _ in ids])
    p1 = wait * best_bus
    p2 = CRT(*zip(*ids))
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=13, verbose=True)

import blitzen
from donner.misc import CRT


@blitzen.run
def main(input_string, verbose=False):
    earliest, ids = input_string.split('\n')
    ids = [(int(bus), -i) for i, bus in enumerate(ids.split(',')) if bus.isdigit()]
    earliest = int(earliest)
    wait, best_bus = min([(bus - earliest % bus, bus) for bus, _ in ids])
    p1 = wait * best_bus
    p2 = CRT(*zip(*ids))
    return p1, p2


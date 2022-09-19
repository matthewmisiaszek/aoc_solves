from common2020 import aoc_input
from common.timer import timer


def part1(adapters, outlet, device):
    joltages = [outlet] + adapters + [device]
    jolt_differences = [a-b for a,b in zip(joltages[1:], joltages)]
    one_jolt = jolt_differences.count(1)
    three_jolt = jolt_differences.count(3)
    return one_jolt * three_jolt


def part2(adapters, outlet, device):
    adapter_set = set(adapters)
    closed = {device: 1}
    queue = [outlet]
    while queue:
        current = queue.pop()
        not_closed = []
        possibilities = 0
        for next_adapter in range(current + 1, current + 4):
            if next_adapter in closed:
                possibilities += closed[next_adapter]
            elif next_adapter in adapter_set:
                not_closed.append(next_adapter)
        if not_closed:
            queue.append(current)
            queue += not_closed
        else:
            closed[current] = possibilities
    return closed[0]


def main(input_string, verbose=False):
    adapters = sorted(int(i) for i in input_string.split('\n'))
    outlet = 0
    device = max(adapters) + 3
    p1 = part1(adapters, outlet, device)
    p2 = part2(adapters, outlet, device)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 10), verbose=True)
    print('Time:  ', timer())

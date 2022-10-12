import dancer
import re
from itertools import permutations
from common import constants as con, elementwise as ew


def manh(a, b):
    return abs(a[0] - b[0]) + abs(a[1] + b[1])


def parse(input_string):
    pattern = '/dev/grid/node-x(\d*)-y(\d*) *(\d*)T *(\d*)T *(\d*)T *(\d*)%'
    size = {}
    used = {}
    for x, y, size_i, used_i, _, _ in [[int(i) for i in line] for line in re.findall(pattern, input_string)]:
        node = (x, y)
        size[node] = size_i
        used[node] = used_i
    return size, used


def part1(size, used):
    viable_pairs = 0
    for a, b in permutations(size.keys(), 2):
        if used[a] != 0 and a != b and used[a] <= size[b] - used[b]:
            viable_pairs += 1
    return viable_pairs


def merge(used, old_hist, new_hist, empty_node, target):
    i = 0
    for i in range(min(len(old_hist), len(new_hist))):
        if old_hist[i] != new_hist[i]:
            break
    for b, a, d in reversed(old_hist[i:]):
        used[b] -= d
        used[a] += d
        empty_node = b
        if target == b:
            target = a
    for a, b, d in new_hist[i:]:
        used[b] -= d
        used[a] += d
        empty_node = b
        if target == b:
            target = a
    return new_hist, empty_node, target


def branch(size, used, empty_node, target, access, history, queue, closed):
    for direction in con.D2D4:
        new_empty_node = ew.sum2d(empty_node, direction)
        if new_empty_node in size:
            data_size = used[new_empty_node]
            if data_size <= size[empty_node] - used[empty_node]:
                if new_empty_node == target:
                    new_target = empty_node
                else:
                    new_target = target
                new_history = history + ((empty_node, new_empty_node, data_size),)
                if (new_empty_node, new_target) not in closed:
                    score = manh(new_target, access) + manh(new_empty_node, new_target)
                    queue.add((score, new_history))
                    closed.add((new_empty_node, new_target))


def part2(size, used):
    empty_node = min(used.keys(), key=lambda node: used[node])
    nodes_with_y_0 = {(x, y) for x, y in size.keys() if y == 0}
    target = max(nodes_with_y_0)
    access = (0, 0)
    queue = {(0, tuple())}
    history = tuple()
    closed = set()
    while queue:
        current = min(queue)
        queue.discard(current)
        cscore, chist = current
        history, empty_node, target = merge(used, history, chist, empty_node, target)
        if target == access:
            break
        else:
            branch(size, used, empty_node, target, access, history, queue, closed)
    return len(history)


def main(input_string, verbose=False):
    size, used, = parse(input_string)
    p1 = part1(size, used)
    p2 = part2(size, used)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=22, verbose=True)

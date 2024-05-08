import blitzen
import re
import string


def parse(input_string):
    pattern = 'Step (.) must be finished before step (.) can begin.'
    pairs = re.findall(pattern, input_string)
    prereqs = {}
    for a, b in pairs:
        if b not in prereqs:
            prereqs[b] = set()
        prereqs[b].add(a)
        if a not in prereqs:
            prereqs[a] = set()
    return prereqs


def part1(prereqs):
    todo = list(string.ascii_uppercase)
    order = []
    complete = set()
    while todo:
        for step in todo:
            if not prereqs[step] - complete:
                order.append(step)
                complete.add(step)
                break
        todo.remove(step)
    return ''.join(order)


def part2(prereqs, workers, verbose=False):
    todo = list(string.ascii_uppercase)
    # queue item: time, task,
    queue = {(0, '')}
    workers = 4
    complete = set()
    while queue:
        t, task = min(queue)
        queue.discard((t, task))
        workers += 1
        complete.add(task)
        added = []
        for step in todo:
            if workers and not prereqs[step] - complete:
                queue.add((t + 61 + string.ascii_uppercase.index(step), step))
                workers -= 1
                added.append(step)
        for step in added:
            todo.remove(step)
        if verbose:
            in_progress = tuple(x for _, x in queue)# + ('_',) * workers
            print('{:04d}'.format(t),complete, in_progress, todo)
    return t

@blitzen.run
def main(input_string, verbose=False):
    prereqs = parse(input_string)
    p1 = part1(prereqs)
    p2 = part2(prereqs, 5, verbose)
    return p1, p2


import DANCER
from collections import defaultdict, deque


def main(input_string, verbose=False):
    # map of all nodes that can be reached from a given node
    nodes = defaultdict(list)
    for line in input_string.split('\n'):
        a, b = line.split('-')
        nodes[a].append(b)
        nodes[b].append(a)
    start, end = 'start', 'end'  # convenience
    # queue, each item is list, starting with Bool: small cave visited twice then all visited caves
    q = deque([[False, start]])
    p1, p2 = 0, 0  # number of paths for p1 and p2
    while q:
        curr = q.pop()
        if curr[-1] == end:  # if the last visited cave is end, you're done
            p2 += 1  # increment scores
            p1 += not curr[0]  # if small cave twice, don't count
        else:
            for node in nodes[curr[-1]]:  # for each node accessible from the most recent node
                if node != start and (node.isupper() or not curr[0] or node not in curr):  # check that it's valid
                    if not curr[0] and not node.isupper() and node in curr:
                        # if this is the second time we've visited a small cave, set flag to True
                        q.appendleft([True] + curr[1:] + [node])  # append new item to queue
                    else:
                        q.appendleft(curr + [node])  # append new item to queue

    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2021, day=12, verbose=True)

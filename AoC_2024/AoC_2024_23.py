import blitzen
from donner import graph
from itertools import combinations


def check_group(group, network):
    group = set(group)
    for node in group:
        if (set(network[node]) | {node}) & group != group:
            return False
    return True


def find_groups_size(network, n):
    groups = set()
    for node in network:
        members = sorted(list(network[node]) + [node])
        for group in combinations(members, n):
            if check_group(group, network):
                groups.add(group)
    return groups


@blitzen.run
def main(input_string, verbose=False):
    p1 = 0
    network = graph.Graph()
    for line in input_string.split('\n'):
        a, b = line.split('-')
        network.add_edge_eq(a, b)
    for group in find_groups_size(network, 3):
        for node in group:
            if node[0] == 't':
                p1 += 1
                break
    maxgroupsize = max([len(neighbors) + 1 for neighbors in network.values()])
    for n in range(maxgroupsize, -1, -1):
        groups = find_groups_size(network, n)
        if groups:
            break
    group = groups.pop()
    p2 = ','.join(sorted(group))
    return p1, p2

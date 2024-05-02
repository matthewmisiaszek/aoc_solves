import blitzen
from donner import graph


def unique_paths(start, target, wm):
    wmc = wm.copy()
    for paths in range(5):
        for used in wmc.dijkstra(start, {target}, full_paths=True):
            for a, b in zip(used, used[1:]):
                wmc[a].pop(b)
                wmc[b].pop(a)
            break
        else:
            break
    return paths


def main(input_string, verbose=False):
    wm = graph.Graph()
    for line in input_string.split('\n'):
        node, neighbors = line.split(': ')
        for neighbor in neighbors.split(' '):
            wm.add_edge_eq(node, neighbor)
    p1 = sum(unique_paths(node, target, wm) == 3 for target in wm)
    p1 = p1 * (len(wm) - p1)
    p2 = blitzen.holiday_greeting
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2023, day=25, verbose=True)

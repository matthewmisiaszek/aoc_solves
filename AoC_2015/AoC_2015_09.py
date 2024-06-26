import blitzen
from itertools import permutations


@blitzen.run
def main(input_string, verbose=False):
    graph = {}
    for line in input_string.split('\n'):
        points, distance = line.split(' = ')
        a, b = points.split(' to ')
        distance = int(distance)
        for i, j in ((a, b), (b, a)):
            if i not in graph:
                graph[i] = {}
            graph[i][j] = distance
    paths = permutations(graph.keys())
    distances = [sum([graph[a][b]
                      for a, b in zip(path, path[1:])])
                 for path in paths]
    p1 = min(distances)
    p2 = max(distances)
    return p1, p2


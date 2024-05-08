import blitzen
from donner import graph
from string import ascii_lowercase

START_KEY = 'S'
END_KEY = 'E'
START_H = 'a'
END_H = 'z'


@blitzen.run
def main(input_string, verbose=False):
    amap = graph.text_to_dict(input_string)  # map of (x,y):c
    poi = {val: key for key, val in amap.items()}  # map of c:(x,y) to find S, E
    amap.update({poi[START_KEY]: START_H, poi[END_KEY]: END_H})  # replace S, E with their heights
    nmap = {key: ascii_lowercase.find(val) for key, val in amap.items()}  # substitute letters for int
    heighmap = graph.set_to_graph(nmap.keys())  # graph ignoring elevation
    for point, neighbors in heighmap.graph.items():  # delete neighbors that require climbing gear
        for neighbor in tuple(neighbors.keys()):
            if nmap[neighbor] - nmap[point] > 1:
                neighbors.pop(neighbor)
    p1 = heighmap.simple_dijkstra(poi[START_KEY], poi[END_KEY])
    low_points = {key for key, val in amap.items() if val == START_H}  # set of points at start height
    p2 = heighmap.dijkstra(low_points, {poi[END_KEY]})[poi[END_KEY]]
    return p1, p2


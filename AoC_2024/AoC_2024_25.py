import blitzen
from donner import graph
from itertools import combinations


@blitzen.run
def main(input_string, verbose=False):
    p1 = 0
    things = [set(graph.text_to_dict(thing, include='#')) for thing in input_string.split('\n\n')]
    for a, b in combinations(things, 2):
        if not (a & b):
            p1 += 1
    p2 = blitzen.holiday_greeting
    return p1, p2


import blitzen
import math


INSTRUCTIONS = 'LR'
A, Z = 'A', 'Z'
AAA, ZZZ = 'AAA', 'ZZZ'


def parse(input_string):
    instructions, network_list = input_string.split('\n\n')
    instructions = tuple(INSTRUCTIONS.index(i) for i in instructions)
    network = {}
    for line in network_list.split('\n'):
        node, children = line.split(' = ')
        l, r = children[1:-1].split(', ')
        network[node] = (l, r)
    return instructions, network


def navigate(instructions, network, start, finish):
    node = start
    i = 0
    while node not in finish:
        inst = instructions[i%len(instructions)]
        node = network[node][inst]
        i += 1
    return i


@blitzen.run
def main(input_string, verbose=False):
    instructions, network = parse(input_string)
    p1 = navigate(instructions, network, AAA, {ZZZ})
    anodes = {node for node in network if node[-1] == A}
    znodes = {node for node in network if node[-1] == Z}
    frequencies = [navigate(instructions, network, node, znodes) for node in anodes]
    p2 = math.lcm(*frequencies)
    return p1, p2


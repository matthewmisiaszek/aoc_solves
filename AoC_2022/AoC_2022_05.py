import dancer
from itertools import zip_longest

SPACE = ' '
GCC_MODELS = {9000: -1, 9001: 1}


def parse(input_string):
    stacks_str, moves_str = input_string.split('\n\n')
    stacks_transform = [''.join(stack).rstrip()
                        for stack in zip_longest(*reversed(stacks_str.split('\n')), fillvalue=SPACE)]
    stacks = {stack[0]: stack[1:] for stack in stacks_transform if stack}
    stacks.pop(SPACE)
    moves = []
    for line in moves_str.split('\n'):
        _, n, _, f, _, t = line.split()
        moves.append((int(n), f, t))
    return stacks, moves


def gcc(stacks, moves, model):
    step = GCC_MODELS[model]
    for n, f, t in moves:
        stacks[t] += stacks[f][-n:][::step]
        stacks[f] = stacks[f][:-n]
    return ''.join(stacks[key][-1] for key in sorted(stacks.keys()))


def main(input_string, verbose=False):
    stacks, moves = parse(input_string)
    p1 = gcc(stacks.copy(), moves, 9000)
    p2 = gcc(stacks, moves, 9001)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=5, verbose=True)

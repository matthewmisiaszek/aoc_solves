import dancer

STRIP = False
SPACE = ' '


def parse(input_string):
    stacks_str, moves_str = input_string.split('\n\n')
    stacks = []
    for stack in stacks_str.split('\n')[-1][1::4]:
        stacks.append([])
    for line in reversed(stacks_str.split('\n')[:-1]):
        for i, val in enumerate(line[1::4]):
            if val != SPACE:
                stacks[i].append(val)
    moves = []
    for line in moves_str.strip().split('\n'):
        _, n, _, f, _, t = line.split()
        n = int(n)
        f = int(f) - 1
        t = int(t) - 1
        moves.append((n, f, t))
    return stacks, moves


def gcc(stacks, moves, model):
    for n, f, t in moves:
        crates = stacks[f][-n:]
        stacks[f] = stacks[f][:-n]
        if model != 9001:
            crates.reverse()
        stacks[t].extend(crates)
    return ''.join(stack[-1] for stack in stacks if stack)


def main(input_string, verbose=False):
    stacks, moves = parse(input_string)
    p2stacks = [stack.copy() for stack in stacks]
    p1 = gcc(stacks, moves, 9000)
    p2 = gcc(p2stacks, moves, 9001)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2022, day=5, verbose=True, strip=False)

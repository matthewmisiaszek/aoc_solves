import DANCER
from collections import defaultdict


def validate(modelno, f):
    vars = defaultdict(int)
    for i in range(-100, 100):
        vars[str(i)] = i

    for line in f:
        line = line.split()
        op = line[0]
        if op == 'inp':
            vars[line[1]] = modelno.pop(0)
        elif op == 'add':
            vars[line[1]] += vars[line[2]]
        elif op == 'mul':
            vars[line[1]] *= vars[line[2]]
        elif op == 'div':
            if vars[line[2]] == 0:
                return False
            vars[line[1]] //= vars[line[2]]
        elif op == 'mod':
            if vars[line[2]] <= 0:
                return False
            if vars[line[1]] < 0:
                return False
            vars[line[1]] %= vars[line[2]]
        elif op == 'eql':
            if vars[line[1]] == vars[line[2]]:
                vars[line[1]] = 1
            else:
                vars[line[1]] = 0
    if vars['z'] == 0:
        return True
    else:
        return False


def main(input_string, verbose=False):
    f = input_string.split('\n')
    section_length = 18
    vals = [[line.split() for line in f[section_length * i:section_length * (i + 1)]] for i in
            range(len(f) // section_length)]
    a, b, c = [[int(section[n][2]) for section in vals] for n in (5, 15, 4)]  # add x a, add y b, div z c
    stack = []
    rels = {}
    for i, (a, b, c) in enumerate(zip(a, b, c)):
        if c == 1:
            stack.append((i, b))
        else:
            i0, b0 = stack.pop(-1)
            diff = a + b0
            if diff > 0:
                rels[i] = (i0, diff)
            else:
                rels[i0] = (i, -diff)
    maxmno = [0] * len(vals)
    minmno = [0] * len(vals)
    for i0, (i1, diff) in rels.items():
        maxmno[i0] = 9
        maxmno[i1] = 9 - diff
        minmno[i1] = 1
        minmno[i0] = 1 + diff
    p1 = ''.join([str(i) for i in maxmno])
    p2 = ''.join([str(i) for i in minmno])
    if verbose:
        print('Part 1: Max Model Number: ', p1, ' Check Valid: ', validate(maxmno, f))
        print('Part 2: Min Model Number: ', p2, ' Check Valid: ', validate(minmno, f))
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2021, day=24, verbose=True)

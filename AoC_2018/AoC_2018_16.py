import blitzen


def addr(regs, a, b, c):
    regs[c] = regs[a] + regs[b]


def addi(regs, a, b, c):
    regs[c] = regs[a] + b


def mulr(regs, a, b, c):
    regs[c] = regs[a] * regs[b]


def muli(regs, a, b, c):
    regs[c] = regs[a] * b


def banr(regs, a, b, c):
    regs[c] = regs[a] & regs[b]


def bani(regs, a, b, c):
    regs[c] = regs[a] & b


def borr(regs, a, b, c):
    regs[c] = regs[a] | regs[b]


def bori(regs, a, b, c):
    regs[c] = regs[a] | b


def setr(regs, a, b, c):
    regs[c] = regs[a]


def seti(regs, a, b, c):
    regs[c] = a


def gtir(regs, a, b, c):
    regs[c] = int(a > regs[b])


def gtri(regs, a, b, c):
    regs[c] = int(regs[a] > b)


def gtrr(regs, a, b, c):
    regs[c] = int(regs[a] > regs[b])


def eqir(regs, a, b, c):
    regs[c] = int(a == regs[b])


def eqri(regs, a, b, c):
    regs[c] = int(regs[a] == b)


def eqrr(regs, a, b, c):
    regs[c] = int(regs[a] == regs[b])


def parse_example(example):
    example = example.translate({ord(c): None for c in 'Before:Aft,[]'})
    return [[int(i) for i in line.strip().split()] for line in example.split('\n')]


def main(input_string, verbose=False):
    input_file = input_string.split('\n\n\n\n')
    examples = input_file.pop(0).split('\n\n')
    p1 = 0
    potentials = {}
    flist = [addr, addi, mulr, muli, banr, bani, borr, bori, setr, seti, gtir, gtri, gtrr, eqir, eqri, eqrr]
    for example in examples:
        cf = 0
        before, (o, a, b, c), after = parse_example(example)
        for i, fun in enumerate(flist):
            working = before.copy()
            fun(working, a, b, c)
            if working == after:
                cf += 1
                if o not in potentials:
                    potentials[o] = set()
                potentials[o].add(i)
        if cf >= 3:
            p1 += 1
    # print(p1)
    mapping = {}
    while len(mapping) < len(flist):
        for k in tuple(potentials.keys()):
            potentials[k] = potentials[k].difference(mapping.values())
            if len(potentials[k]) == 1:
                mapping[k] = list(potentials[k])[0]
                potentials.pop(k)
    if input_file:
        code = input_file.pop()
        regs = [0] * 4
        for op in code.split('\n'):
            o, a, b, c = [int(i) for i in op.split()]
            flist[mapping[o]](regs, a, b, c)
        p2 = regs[0]
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2018, day=16, verbose=True)

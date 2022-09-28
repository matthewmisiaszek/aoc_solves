import core


def main(input_string, verbose=False):
    program = [line.split() for line in input_string.split('\n')]

    # who knows if all this is the same for everyone's code but whatever
    a = int(program[7][2])
    b = int(program[8][1])
    c = int(program[9][2]) + 1
    d = int(program[11][2]) + 1
    e = int(program[12][2])
    f = int(program[13][2]) + 1
    g = int(program[14][1])
    h = int(program[18][1])
    i = int(program[20][2])

    hist_set = set()
    hist_list = []

    regs = [0, 0, 0, 0, 0, 0]
    regs[5] = a | regs[4]
    regs[4] = b
    while True:
        regs[2] = regs[5] % c
        regs[4] += regs[2]
        regs[4] %= d
        regs[4] *= e
        regs[4] %= f
        if regs[5] < g:
            if regs[4] in hist_set:
                break
            hist_set.add(regs[4])
            hist_list.append(regs[4])
            regs[2] = h
            regs[5] = a | regs[4]
            regs[4] = b
        else:
            regs[2] = regs[5] // i
            regs[5] = regs[2]

    p1 = hist_list[0]
    p2 = hist_list[-1]
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2018, day=21, verbose=True)

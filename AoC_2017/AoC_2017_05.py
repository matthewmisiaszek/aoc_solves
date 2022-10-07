import dancer


def steps(jumps, change):
    i = 0
    len_jumps = len(jumps)
    step_count = 0
    while 0 <= i < len_jumps:
        jump = jumps[i]
        jumps[i] += change if jump >= 3 else 1
        i += jump
        step_count += 1
    return step_count


def main(input_string, verbose=False):
    jumps = [int(i) for i in input_string.split('\n')]
    p1 = steps(jumps.copy(), 1)
    p2 = steps(jumps.copy(), -1)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2017, day=5, verbose=True)

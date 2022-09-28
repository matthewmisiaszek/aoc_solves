import DANCER


def main(input_string, verbose=False):
    f = input_string.split('\n')

    depth1, depth2, travel = 0, 0, 0
    for l in f:
        dir, val = l.split()
        val = int(val)
        if dir == 'forward':
            travel += val
            depth2 += depth1 * val
        elif dir == 'up':
            depth1 -= val
        else:  # down
            depth1 += val
    p1, p2 = depth1 * travel, depth2 * travel
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2021, day=2, verbose=True)

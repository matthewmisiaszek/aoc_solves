def main(input_file='input.txt', verbose=False):
    f = open(input_file).read().split('\n')

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
    p1,p2=depth1*travel,depth2*travel
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1,p2]))
    return p1,p2

if __name__ == "__main__":
   main(verbose=True)
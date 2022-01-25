def main(input_file='input.txt', verbose=False):
    f=open(input_file).read().split('\n')
    p1,p2=(sum([int(f[i])<int(f[i+s]) for i in range(len(f)-s)]) for s in [1,3])
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1,p2]))
    return p1,p2

if __name__ == "__main__":
   main(verbose=True)
import statistics


def main(input_file='input.txt', verbose=False):
    crabs = [int(i) for i in open(input_file).read().split(',')]
    crabs.sort()
    median, average = int(statistics.median(crabs)), int(statistics.mean(crabs))
    p1 = sum([abs(crab - median) for crab in crabs])
    p2 = min([sum([sum(range(abs(crab - average) + 1)) for crab in crabs]) for average in [average, average + 1]])
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(verbose=True)

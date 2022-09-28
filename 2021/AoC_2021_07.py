import DANCER
import statistics


def main(input_string, verbose=False):
    crabs = [int(i) for i in input_string.split(',')]
    crabs.sort()
    median, average = int(statistics.median(crabs)), int(statistics.mean(crabs))
    p1 = sum([abs(crab - median) for crab in crabs])
    p2 = min([sum([sum(range(abs(crab - average) + 1)) for crab in crabs]) for average in [average, average + 1]])
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2021, day=7, verbose=True)

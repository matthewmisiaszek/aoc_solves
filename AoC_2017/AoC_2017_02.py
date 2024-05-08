import blitzen
import itertools


@blitzen.run
def main(input_string, verbose=False):
    spreadsheet = [[int(i) for i in line.split()] for line in input_string.split('\n')]
    p1 = sum([max(row) - min(row) for row in spreadsheet])
    p2 = sum([sum([a // b for a, b in itertools.permutations(row, 2) if a % b == 0]) for row in spreadsheet])
    return p1, p2


import blitzen
from collections import Counter


@blitzen.run
def main(input_string, verbose=False):
    messages = [[c for c in line] for line in input_string.split('\n')]
    transposed = tuple(zip(*messages))
    charcount = [Counter(column) for column in transposed]
    p1 = ''.join(max(col, key=lambda x: col[x]) for col in charcount)
    p2 = ''.join(min(col, key=lambda x: col[x]) for col in charcount)
    return p1, p2


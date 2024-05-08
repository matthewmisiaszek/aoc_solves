import blitzen
from string import ascii_lowercase


@blitzen.run
def main(input_string, verbose=False):
    p1, p2 = 0, 0
    for group in input_string.split('\n\n'):
        members = group.count('\n') + 1
        for c in ascii_lowercase:
            count = group.count(c)
            p1 += count > 0
            p2 += count == members
    return p1, p2


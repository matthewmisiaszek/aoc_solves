import blitzen
from donner.misc import md5hash


def mine(seed, zeroes):
    i = 0
    z = '0' * zeroes
    while True:
        if md5hash(seed + str(i))[:zeroes] == z:
            return i
        i += 1


@blitzen.run
def main(input_string, verbose=False):
    p1 = mine(input_string, 5)
    p2 = mine(input_string, 6)
    return p1, p2


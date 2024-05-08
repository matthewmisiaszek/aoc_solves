import blitzen
from collections import Counter


@blitzen.run
def main(input_string, verbose=False):
    passphrase_list = [passphrase.split() for passphrase in input_string.split('\n')]
    p1 = sum([max(Counter(passphrase).values()) == 1 for passphrase in passphrase_list])
    passphrase_list = [[''.join(sorted(word)) for word in passphrase] for passphrase in passphrase_list]
    p2 = sum([max(Counter(passphrase).values()) == 1 for passphrase in passphrase_list])
    return p1, p2


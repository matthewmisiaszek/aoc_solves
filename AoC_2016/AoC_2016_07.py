import blitzen
import re
from string import ascii_lowercase as alph
from itertools import permutations


def tls_check(sequences):
    for a, b in permutations(alph, 2):
        abba = a + b + b + a
        if abba in sequences:
            return True
    return False


def ssl_check(supernet, hypernet):
    for a, b in permutations(alph, 2):
        aba = a + b + a
        bab = b + a + b
        if aba in supernet and bab in hypernet:
            return True
    return False


def main(input_string, verbose=False):
    tls_count = 0
    ssl_count = 0
    for ip in input_string.split('\n'):
        ip_split = re.split(r'\[|\]', ip)
        supernet = ','.join(ip_split[::2])
        hypernet = ','.join(ip_split[1::2])
        if tls_check(supernet) and not tls_check(hypernet):
            tls_count += 1
        if ssl_check(supernet, hypernet):
            ssl_count += 1
    p1 = tls_count
    p2 = ssl_count
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2016, day=7, verbose=True)

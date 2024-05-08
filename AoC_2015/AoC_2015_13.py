import blitzen
import re
from itertools import permutations


def check_happy(arrangement, happiness):
    ret = 0
    for a, b in zip(arrangement, arrangement[1:] + arrangement[0:1]):
        if a in happiness and b in happiness[a]:
            ret += happiness[a][b]
        if b in happiness and a in happiness[b]:
            ret += happiness[b][a]
    return ret


@blitzen.run
def main(input_string, verbose=False):
    happiness = {}
    pattern = r'(\S*) would (\S*) (\d*) happiness units by sitting next to (\S*).'
    for a, gl, val, b in re.findall(pattern, input_string):
        if a not in happiness:
            happiness[a] = {}
        val = int(val)
        if gl == 'lose':
            val = - val
        happiness[a][b] = val
    p1 = max(check_happy(perm, happiness) for perm in permutations(happiness.keys()))
    happiness['you'] = {}
    p2 = max(check_happy(perm, happiness) for perm in permutations(happiness.keys()))
    return p1, p2


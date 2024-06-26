import blitzen
from collections import defaultdict
from string import ascii_uppercase


def emptylist():
    return [0 for _ in range(26)]


def iteratecache(cache, ruledict):
    abc = ascii_uppercase
    newcache = defaultdict(emptylist)
    for key in ruledict.keys():
        a, c = key
        b = ruledict[key]

        newcache[key] = [a + b for a, b in zip(cache[(a, b)], cache[(b, c)])]
        newcache[key][abc.find(b)] += 1
    return newcache


def calculate(cache, template):
    abc = ascii_uppercase
    lfreq = emptylist()
    for i in range(len(template) - 1):
        a = template[i]
        c = template[i + 1]
        lfreq = [a + b for a, b in zip(cache[a, c], lfreq)]
    for c in template:
        lfreq[abc.find(c)] += 1

    lfreq = [(a, b) for a, b in zip(abc, lfreq)]
    lfreq.sort(key=lambda x: x[1])
    while lfreq[0][1] == 0:
        lfreq.pop(0)

    return lfreq[-1][1] - lfreq[0][1]


def _all(n, template, ruledict):
    cache = defaultdict(emptylist)
    for i in range(n):
        cache = iteratecache(cache, ruledict)
    return calculate(cache, template)


@blitzen.run
def main(input_string, verbose=False):
    template, rules = input_string.split('\n\n')
    ruledict = {}
    for rule in rules.split('\n'):
        rule = rule.replace(' -> ', '')
        ruledict[(rule[0], rule[1])] = rule[2]

    p1 = _all(10, template, ruledict)
    p2 = _all(40, template, ruledict)

    return p1, p2


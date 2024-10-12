import blitzen
from math import prod


def parse(input_string):
    wtext, ptext = input_string.split('\n\n')
    wdict = {}
    for workflow in wtext.split('\n'):
        name, rules = workflow[:-1].split('{')
        rules = rules.split(',')
        wdict[name] = rules
    plist = []
    for part in ptext.split('\n'):
        pdict = {}
        for category in part[1:-1].split(','):
            name, val = category.split('=')
            val = int(val)
            pdict[name] = (val, val)
        plist.append(pdict)
    return wdict, plist


def combinations(part, wdict, workflow, index):
    for n, x in part.values():
        if n > x:
            return 0
    if workflow == 'A':
        return prod((b-a+1 if b >= a else 0 for a, b in part.values()))
    elif workflow == 'R':
        return 0
    rule = wdict[workflow][index]
    if ':' in rule:
        test, dest = rule.split(':')
        cat = test[0]
        comp = test[1]
        val = int(test[2:])
        pn, px = part[cat]
        passing = part.copy()
        failing = part.copy()
        if comp == '>':
            passing[cat] = (max(pn, val+1), px)
            failing[cat] = (pn, min(px, val))
        else:
            passing[cat] = (pn, min(px, val-1))
            failing[cat] = (max(pn, val), px)
        return combinations(passing, wdict, dest, 0) + combinations(failing, wdict, workflow, index+1)
    else:
        return combinations(part, wdict, rule, 0)


def part1(wdict, plist):
    return sum(combinations(part, wdict, 'in', 0)*sum(p[1] for p in part.values()) for part in plist)


def part2(wdict):
    return combinations({i:(1,4000) for i in 'xmas'}, wdict, 'in', 0)


@blitzen.run
def main(input_string, verbose=False):
    wdict, plist = parse(input_string)
    p1 = part1(wdict, plist)
    p2 = part2(wdict)
    return p1, p2


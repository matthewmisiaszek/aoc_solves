from common2020 import aoc_input
from common.timer import timer
import re


def byr(field):
    return len(field) == 4 and 1920 <= int(field) <= 2002


def iyr(field):
    return len(field) == 4 and 2010 <= int(field) <= 2020


def eyr(field):
    return len(field) == 4 and 2020 <= int(field) <= 2030


def hgt(field):
    val, unit = field[:-2], field[-2:]
    if unit == 'cm':
        return 150 <= int(val) <= 193
    elif unit == 'in':
        return 59 <= int(val) <= 76
    else:
        return False


def hcl(field):
    return bool(re.match('^#[\da-f]{6}$', field))


def ecl(field):
    return field in {'amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'}


def pid(field):
    return bool(re.match('^\d{9}$', field))


def parse(input_string):
    passports_raw = tuple(tuple(item.split(':')
                                for item in passport.split())
                          for passport in input_string.split('\n\n'))
    passports = tuple({key: value
                       for key, value in passport}
                      for passport in passports_raw)
    return passports


def check_passport1(passport, rules):
    return passport.keys() & rules.keys() == rules.keys()


def check_passport2(passport, rules):
    if check_passport1(passport, rules):
        for key, fun in rules.items():
            if fun(passport[key]):
                pass
            else:
                return False
        return True
    else:
        return False


def part1(passports, rules):
    return sum(tuple(check_passport1(passport, rules) for passport in passports))


def part2(passports, rules):
    return sum(tuple(check_passport2(passport, rules) for passport in passports))


def main(input_string, verbose=False):
    rules = {'byr': byr,
             'iyr': iyr,
             'eyr': eyr,
             'hgt': hgt,
             'hcl': hcl,
             'ecl': ecl,
             'pid': pid}
    passports = parse(input_string)
    p1 = part1(passports, rules)
    p2 = part2(passports, rules)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 4), verbose=True)
    print('Time:  ', timer())

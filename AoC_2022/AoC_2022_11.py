import blitzen
from math import prod
import re


class Monkey:
    def __init__(self, worrydiv, idx, items, test, true, false, op):
        self.id = int(idx)
        self.items = [int(i) for i in items.split(',')]  # starting items
        self.test = int(test)  # divisible by...
        self.true = int(true)  # if true throw to monkey _
        self.false = int(false)  # if false throw to monkey _
        op, oth = op.split()  # ASSUME operation takes form new = old (+|*) (\d*|old)
        self.power = 1
        self.inc = 0
        self.fact = 1
        if op == '*':
            if oth == 'old':
                self.power = 2
            else:
                self.fact = int(oth)
        elif op == '+':
            if oth == 'old':
                self.fact = 2
            else:
                self.inc = int(oth)
        self.counter = 0  # how many items this monkey has inspected
        self.worrydiv = worrydiv  # how much worry is divided after inspection
        self.worrymod = 1  # modulus worry by this value after inspection

    def turn(self, monkeys):
        while self.items:
            self.counter += 1
            item = self.items.pop(0)
            item = (item ** self.power * self.fact + self.inc) // self.worrydiv % self.worrymod
            if item % self.test == 0:
                monkeys[self.true].items.append(item)
            else:
                monkeys[self.false].items.append(item)


def part(input_string, worrydiv, rounds):
    pattern = open(blitzen.root_path + '/AoC_2022/monkey_pattern').read()
    monkeys = [Monkey(worrydiv, **match.groupdict())
               for match in re.finditer(pattern, input_string)]  # monkeys in order listed
    monkey_dict = {monkey.id: monkey for monkey in monkeys}  # monkeys indexed by ID (probably the same order)
    worrymod = prod(monkey.test for monkey in monkeys)  # product of every monkey's test
    for monkey in monkeys:  # set worry mod
        monkey.worrymod = worrymod
    for _ in range(rounds):  # do rounds
        for monkey in monkeys:
            monkey.turn(monkey_dict)
    activity = sorted(monkey.counter for monkey in monkeys)
    return activity[-2] * activity[-1]


def main(input_string, verbose=False):
    p1 = part(input_string, worrydiv=3, rounds=20)
    p2 = part(input_string, worrydiv=1, rounds=10000)

    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=11, verbose=True)

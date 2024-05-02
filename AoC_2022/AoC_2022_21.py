import blitzen
import re
from collections import defaultdict
from sympy import symbols, solve


ROOT = 'root'
HUMN = 'humn'


def parse(input_string):
    math_monkeys = {}
    waiting = defaultdict(set)
    for name, a, op, b in re.findall(r'(\S+): (\S+) (\+|-|\*|/) (\S+)', input_string):
        math_monkeys[name] = (a, op, b)
        waiting[a].add(name)
        waiting[b].add(name)
    val_monkeys = {}
    monkey_queue = set()
    for name, val in re.findall(r'(\S+): (\d+)', input_string):
        val_monkeys[name] = val
        monkey_queue.update(waiting[name])
    return math_monkeys, val_monkeys, monkey_queue, waiting


def solve_monkeys(math_monkeys, val_monkeys, monkey_queue, waiting):
    while monkey_queue:
        curr = monkey_queue.pop()
        a, op, b = math_monkeys[curr]
        if a in val_monkeys and b in val_monkeys:
            a = val_monkeys[a]
            b = val_monkeys[b]
            val_monkeys[curr] = '(' + a + op + b + ')'
            if curr in waiting:
                monkey_queue.update(waiting[curr])
    return val_monkeys[ROOT]


def main(input_string, verbose=False):
    math_monkeys, val_monkeys, monkey_queue, waiting = parse(input_string)
    p1 = int(eval(solve_monkeys(math_monkeys, val_monkeys.copy(), monkey_queue.copy(), waiting)))
    val_monkeys[HUMN]=HUMN
    a, op, b = math_monkeys[ROOT]
    math_monkeys[ROOT] = (a, '-', b)
    humn = symbols(HUMN)
    p2 = int(solve(eval(solve_monkeys(math_monkeys, val_monkeys, monkey_queue, waiting)))[0])
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=21, verbose=True)

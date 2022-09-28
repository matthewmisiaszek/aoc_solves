import DANCER
import re


def parse(input_string):
    outside_in = {} # what bags are in each bag and how many?
    inside_out = {} # what bags may this bag be found in?
    for bag in input_string.split('\n'):
        parent, children = bag.split(' bags contain ')
        children = re.findall('(\d{1,}) ([a-z ]*) bag', children)
        outside_in[parent] = {}
        for qty, child in children:
            outside_in[parent][child] = int(qty)
            if child not in inside_out:
                inside_out[child] = set()
            inside_out[child].add(parent)
    return inside_out, outside_in


def part1(inside_out, start):
    queue = {start}
    closed = set()
    while queue:
        bag = queue.pop()
        if bag not in closed:
            closed.add(bag)
            if bag in inside_out:
                queue.update(inside_out[bag])
    return len(closed) - 1


def part2(outside_in, start):
    queue = [(start, 1)]
    bagcount = - 1
    while queue:
        bag, qty = queue.pop()
        bagcount += qty
        if bag in outside_in:
            for child, cqty in outside_in[bag].items():
                queue.append((child, cqty * qty))
    return bagcount


def main(input_string, verbose=False):
    inside_out, outside_in = parse(input_string)
    p1 = part1(inside_out, 'shiny gold')
    p2 = part2(outside_in, 'shiny gold')
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=7, verbose=True)

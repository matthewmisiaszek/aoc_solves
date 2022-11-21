import dancer
from collections import defaultdict


ONE_TRILLION_UNITS = 1000000000000
ORE = 'ORE'
FUEL = 'FUEL'


def ceil(val):
    cval = int(val // 1)
    if val % 1 > 0:
        cval += 1
    return cval


def ore_needed(reactions, parents, pt2=False):
    need = {FUEL: 1}
    ore = 0
    while need:
        need_parents = set().union(*[parents[itm] for itm in need.keys()])
        new_need = defaultdict(int)
        for chem, qty_needed in need.items():
            if chem in need_parents:
                new_need[chem] += qty_needed
            else:
                yield_qty, inputs = reactions[chem]
                needed_reactions = (qty_needed / yield_qty)
                if pt2 is False:
                    needed_reactions = ceil(needed_reactions)
                for input_chem, input_qty in inputs.items():
                    if input_chem == ORE:
                        ore += input_qty * needed_reactions
                    else:
                        new_need[input_chem] += input_qty * needed_reactions
        need = new_need
    return ore


def get_parents(chem, reactions):
    parents = set()
    if chem in reactions:
        _, inputs = reactions[chem]
        for parent in inputs.keys():
            parents.add(parent)
            parents.update(get_parents(parent, reactions))
    return parents


def parse(input_string):
    reactions = {}
    for line in input_string.split('\n'):
        inputs, outputs = line.split(' => ')
        output_qty, output_chem = outputs.split()
        inputs = inputs.split(', ')
        ilist = {input_chem: int(input_qty) for input_qty, input_chem in (i.split() for i in inputs)}
        reactions[output_chem] = (int(output_qty), ilist)
    parents = {chem: get_parents(chem, reactions) for chem in reactions.keys()}
    return reactions, parents


def main(input_string, verbose=False):
    reactions, parents = parse(input_string)
    p1 = ore_needed(reactions, parents)
    p2 = int(ONE_TRILLION_UNITS / ore_needed(reactions, parents, True))
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2019, day=14, verbose=True)

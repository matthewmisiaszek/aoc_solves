import blitzen
from donner import graph, spatial as sp
from collections import defaultdict

ROUNDS = 10


def main(input_string, verbose=False):
    elves = set(graph.text_to_dict(input_string, '.').keys())
    consider = [(sp.NORTH, (sp.NORTHWEST, sp.NORTH, sp.NORTHEAST)),
                (sp.SOUTH, (sp.SOUTHWEST, sp.SOUTH, sp.SOUTHEAST)),
                (sp.WEST, (sp.NORTHWEST, sp.WEST, sp.SOUTHWEST)),
                (sp.EAST, (sp.NORTHEAST, sp.EAST, sp.SOUTHEAST))]
    moves = -1
    history = []
    while moves != 0:
        proposals = defaultdict(list)
        for elf in elves:
            for direction in sp.ENWS8:
                if elf + direction in elves:
                    break
            else:
                continue
            for direction, check in consider:
                for d2 in check:
                    if elf + d2 in elves:
                        break
                else:
                    proposals[elf + direction].append(elf)
                    break
        moves = 0
        for proposal, proposers in proposals.items():
            if len(proposers) == 1:
                elves.add(proposal)
                for elf in proposers:
                    elves.discard(elf)
                moves += 1
        consider = consider[1:] + consider[:1]
        bn, bx = sp.bounds(elves)
        history.append((bx.x - bn.x + 1) * (bx.y - bn.y + 1) - len(elves))

    p1 = history[ROUNDS - 1]
    p2 = len(history)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2022, day=23, verbose=True)

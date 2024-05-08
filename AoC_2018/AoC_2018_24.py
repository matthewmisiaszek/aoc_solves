import blitzen
import re
from collections import defaultdict


class Group:
    def __init__(self, group, army_name):
        units, hit_points, strengths, attack_damage, attack_type, initiative = group
        self.units = int(units)
        self.hp = int(hit_points)
        self.ap = int(attack_damage)
        self.type = attack_type
        self.initiative = int(initiative)
        self.strengths = defaultdict(lambda: 1)
        strengths = strengths.replace('(', '').replace(')', '').strip()
        strengthsdict = {'weak': 2, 'immune': 0}
        if strengths:
            for a in strengths.split('; '):
                b, c = a.split(' to ')
                c = c.split(', ')
                for ci in c:
                    self.strengths[ci] = strengthsdict[b]
        self.army = army_name

    def ep(self):
        return self.units * self.ap

    def damage(self, oth):
        return self.ep() * oth.strengths[self.type]

    def targetsort(self, oth):
        return self.damage(oth), oth.ep(), oth.initiative

    def canattack(self, oth):
        return self.units > 0 and \
               oth.units > 0 and \
               self.army != oth.army and \
               self.damage(oth) > 0

    def attack(self, oth):
        damage = self.damage(oth)
        units_lost = min(damage // oth.hp, oth.units)
        oth.units -= units_lost
        return units_lost


def combat(input_file, boost):
    pattern = '(.*) units each with (.*)hit points(.*)with an attack that does (.*) (.*) damage at initiative (.*)'
    groups = [Group(group, army.split('\n')[0])
              for army in input_file.split('\n\n')
              for group in re.findall(pattern, army)]
    for group in groups:
        if group.army == 'Immune System:':
            group.ap += boost
    casualties = 1
    while casualties:
        # target selection
        groups.sort(key=lambda g: (g.ep(), g.initiative), reverse=True)
        attacks = []
        defenders = groups.copy()
        for attacker in groups:
            potential_defenders = [defender for defender in defenders if attacker.canattack(defender)]
            if potential_defenders:
                maxdefender = max(potential_defenders, key=lambda defender: attacker.targetsort(defender))
                defenders.remove(maxdefender)
                attacks.append((attacker.initiative, attacker, maxdefender))
        # attack phase
        attacks.sort(reverse=True)
        casualties = sum([attacker.attack(defender) for _, attacker, defender in attacks])
    remaining_units = sum([group.units for group in groups])
    remaining_armies = list({group.army for group in groups if group.units > 0})
    if len(remaining_armies) > 1:
        return 'Draw!', remaining_units
    else:
        return remaining_armies[0], remaining_units


def part1(input_file):
    return combat(input_file, 0)[1]


def part2(input_file):
    winner = 0
    boost = -1
    # history=[]
    while winner != 'Immune System:':
        boost += 1
        winner, remaining = combat(input_file, boost)
        # history.append((winner, remaining))
        # print(boost, winner, remaining)
    return remaining


@blitzen.run
def main(input_string, verbose=False):
    p1 = part1(input_string)
    p2 = part2(input_string)
    return p1, p2


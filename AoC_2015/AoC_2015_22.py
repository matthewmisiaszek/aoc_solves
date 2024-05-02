import blitzen
import re


def re_default(line, pattern, default=0):
    ref = re.findall(pattern, line)
    if ref:
        return int(ref[0])
    else:
        return default


class Spell:
    def __init__(self, line):
        ((self.name, cost),) = re.findall(r'(.*) costs (\d*) mana.', line)
        self.cost = int(cost)
        self.duration = re_default(line, r'lasts for (\d*) turns.', 1)
        self.damage = re_default(line, r'(\d*) damage')
        self.hp = re_default(line, r'(\d*) hit points')
        self.mana = re_default(line, r'(\d*) new mana')
        self.armor = re_default(line, r'armor is increased by (\d*)')

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class Fighter:
    def __init__(self, hp, damage, mana):
        self.hp = hp
        self.damage = damage
        self.mana = mana

    def copy(self):
        return Fighter(self.hp, self.damage, self.mana)

    def __hash__(self):
        return hash((self.hp, self.damage, self.mana))

    def __lt__(self, other):
        return self.hp < other.hp

    def __str__(self):
        return 'hp: ' + str(self.hp) + ' mana: ' + str(self.mana) + ' damage: ' + str(self.damage)

    def __repr__(self):
        return self.__str__()


def apply_effects(you, boss, spell_status, spells):
    armor = 0
    for status, spell in zip(spell_status, spells):
        if status > 0:
            boss.hp -= spell.damage
            you.hp += spell.hp
            you.mana += spell.mana
            armor += spell.armor
    spell_status = tuple(max(s - 1, 0) for s in spell_status)
    return armor, spell_status


def fight(spells, you, boss, attrition=0):
    spell_sum = sum(spell.cost for spell in spells)  # cost to cast all spells
    # you strikes first but I've coded it so boss strikes first because it's easier
    # so you gets extra hp to offset that effect.
    you.hp += boss.damage
    spell_status = (0,) * len(spells)  # how many seconds remaining for each spell
    queue = {(0, you, boss, spell_status)}  # spend, you, boss, spell_status
    minwin = None
    while queue:
        curr = max(queue)  # DFS - way more low spend games than high spend games
        queue.discard(curr)
        spend, you, boss, spell_status = curr
        if minwin is not None and minwin - spend > spell_sum:
            # if we are a full spell_sum less than the lowest cost win...
            # then we're definitely below the minimum threshold to win
            # this isn't a matter of doing the spells in a different order
            return minwin
        if minwin is None or spend < minwin:
            # Don't bother with games where we've spent more than the current minimum.  We don't care.
            # start boss's turn
            armor, spell_status = apply_effects(you, boss, spell_status, spells)
            if boss.hp <= 0:
                minwin = spend  # ded.
            you.hp -= max(boss.damage - armor, 1)
            # start your turn
            you.hp -= attrition
            if you.hp > 0:
                armor, spell_status = apply_effects(you, boss, spell_status, spells)
                if boss.hp <= 0:
                    minwin = spend  # ded.
                for i, (status, spell) in enumerate(zip(spell_status, spells)):
                    if status == 0 and spell.cost <= you.mana:  # cast every spell you can as a new queue item
                        new_you = you.copy()
                        new_you.mana -= spell.cost
                        new_boss = boss.copy()
                        new_status = list(spell_status)
                        new_status[i] = spell.duration
                        new_status = tuple(new_status)
                        new_spend = spend + spell.cost
                        new_itm = (new_spend, new_you, new_boss, new_status)
                        queue.add(new_itm)


def parse(input_string):
    spell_file = open(blitzen.root_path + '/AoC_2015/spells.txt').read()
    spells = tuple(Spell(line) for line in spell_file.split('\n'))
    bhp, bd = (int(line[-1]) for line in [line.split() for line in input_string.split('\n')])
    boss = Fighter(bhp, bd, 0)
    you = Fighter(50, 0, 500)
    return you, boss, spells


def main(input_string, verbose=False):
    you, boss, spells = parse(input_string)
    p1 = fight(spells, you.copy(), boss.copy())
    p2 = fight(spells, you, boss, 1)
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2015, day=22, verbose=True)

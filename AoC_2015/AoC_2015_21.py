import dancer
from itertools import product


class Fighter:
    def __init__(self, stats):
        self.damage = stats['Damage']
        self.armor = stats['Armor']
        self.hp = stats['Hit Points']


def item_shop():
    file = open(dancer.root_path + '/AoC_2015/item_shop.txt').read()
    items = {}
    for section in file.split('\n\n'):
        section = section.split('\n')
        title, header = section[0].split(':')
        properties = header.split()
        items[title] = {}
        for line in section[1:]:
            line = line.split()
            vals = line[-len(properties):]
            name = ''.join(line[:-len(properties)])
            items[title][name] = {prop: val for prop, val in zip(properties, vals)}
    items['Armor']['None'] = {}
    items['Rings']['None'] = {}
    items['Rings2'] = items['Rings'].copy()
    return items


def fight(boss_stats, loadout_stats):
    boss = Fighter(boss_stats)
    you = Fighter(loadout_stats)
    while True:
        boss.hp -= max(1, you.damage - boss.armor)
        if boss.hp <= 0:
            return True
        you.hp -= max(1, boss.damage - you.armor)
        if you.hp <= 0:
            return False


def main(input_string, verbose=False):
    boss_stats = {a: int(b) for a, b in [line.split(': ') for line in input_string.split('\n')]}
    items = item_shop()
    item_types = list(items.keys())
    wins, losses = set(), set()
    for loadout in product(*[items[item_type].keys() for item_type in item_types]):
        loadout_stats = {'Hit Points': 100}
        for item, item_type in zip(loadout, item_types):
            for prop, val in items[item_type][item].items():
                if prop not in loadout_stats:
                    loadout_stats[prop] = 0
                loadout_stats[prop] += int(val)
        if fight(boss_stats, loadout_stats):
            wins.add(loadout_stats['Cost'])
        else:
            losses.add(loadout_stats['Cost'])
    p1 = min(wins)
    p2 = max(losses)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2015, day=21, verbose=True)

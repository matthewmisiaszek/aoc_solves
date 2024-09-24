import blitzen
import re


class Record:
    cache = {}

    def __init__(self, condition: str, groups: tuple, fold=1):
        self.condition = '?'.join((condition,) * fold)
        self.groups = groups * fold
        self.combos = self.check()

    def check(self):
        if self in Record.cache:
            return Record.cache[self]
        if self.groups:
            combos = self.check_group()
        elif '#' in self.condition:
            combos = 0
        else:
            combos = 1
        Record.cache[self] = combos
        return combos

    def check_group(self):
        combos = 0
        pattern = r'(?:^|[\?\.])([\?#]{' + self.groups[0] + r'})(?:[\?\.]|$)'
        limit = self.condition.find('#') if '#' in self.condition else len(self.condition)
        i = 0
        while True:
            match = re.search(pattern, self.condition[i:])
            if match and i + match.start(1) <= limit:
                combos += Record(self.condition[i + match.end():], self.groups[1:]).combos
                i = i + match.start(1) + 1
            else:
                break
        return combos

    def __hash__(self):
        return hash((self.condition, self.groups))

    def __eq__(self, other):
        return self.condition == other.condition and self.groups == other.groups


@blitzen.run
def main(input_string, verbose=False):
    records = tuple(line.split() for line in input_string.split('\n'))
    p1 = sum(Record(condition, tuple(groups.split(','))).combos for condition, groups in records)
    p2 = sum(Record(condition, tuple(groups.split(',')), fold=5).combos for condition, groups in records)
    return p1, p2

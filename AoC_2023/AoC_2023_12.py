import dancer
import re


class Record:
    def __init__(self, condition, groups):
        self.condition = condition
        self.groups = groups

    def __hash__(self):
        return hash((self.condition, self.groups))

    def __eq__(self, other):
        return self.condition == other.condition and self.groups == other.groups

    def __str__(self):
        return str(self.condition) + '|' + str(self.groups)

    def __repr__(self):
        return self.__str__()

    def impossible(self):
        return '#' in self.condition and not self.groups

    def complete(self):
        return '#' not in self.condition and not self.groups

    def limit(self):
        return self.condition.find('#') if '#' in self.condition else len(self.condition)

    def pattern(self):
        return r'[\?\.]([\?#]{' + self.groups[0] + r'})[\?\.]'


def parse_line(line):
    condition, groups = line.split()
    groups = tuple(groups.split(','))
    return Record(condition, groups)


def combos(record, fold=1, cache={}):
    record = Record('.' + '?'.join((record.condition,) * fold) + '.', record.groups * fold)
    queue = [record]
    while queue:
        current = queue.pop()
        if current in cache:
            continue
        if current.impossible():
            cache[current] = 0
            continue
        if current.complete():
            cache[current] = 1
            continue
        i = 0
        pattern = current.pattern()
        limit = current.limit()
        to_check = []
        while True:
            match = re.search(pattern, current.condition[i:])
            if match and i + match.start(1) <= limit:
                new_record = Record(current.condition[i + match.end(1):], current.groups[1:])
                to_check.append(new_record)
                i = i + match.start(1)
            else:
                break
        if all(check_record in cache for check_record in to_check):
            cache[current] = sum(cache[check_record] for check_record in to_check)
        else:
            queue.append(current)
            queue += to_check
    return cache[record]


def main(input_string, verbose=False):
    records = tuple(parse_line(line) for line in input_string.split('\n'))
    p1 = sum(combos(record) for record in records)
    p2 = sum(combos(record, fold=5) for record in records)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2023, day=12, verbose=True)

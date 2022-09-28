import DANCER
import re


def parse(input_string, start):
    raw_rules, messages = [i.split('\n') for i in input_string.split('\n\n')]
    raw_rules = {a: b.strip() for a, b in [line.split(':') for line in raw_rules]}
    parsed_rules = {'"a"': 'a', '"b"': 'b', '|': '|'}
    to_parse = [start]
    while to_parse:
        rule = to_parse.pop()
        elements = raw_rules[rule].strip().split()
        new_to_parse = set(elements) - parsed_rules.keys()
        if new_to_parse:
            to_parse.append(rule)
            to_parse += list(new_to_parse)
        else:
            parsed_rules[rule] = '(' + ''.join((parsed_rules[element] for element in elements)) + ')'
    return messages, parsed_rules


def main(input_string, verbose=False):
    messages, rules = parse(input_string, '0')
    pattern = re.compile('^' + rules['0'] + '$')
    p1 = sum([bool(pattern.match(message)) for message in messages])
    pattern424231 = '^' + rules['42'] + '{2,}' + rules['31'] + '+' + '$'
    pattern42star = '^' + rules['42'] + '*'
    p2 = sum([bool(re.match(pattern424231, message))  # if there's at least 2 42s followed by at least one 31 and...
              and re.match(pattern42star, message).end() * 2 > len(message)  # more than half the message matches 42
              for message in messages])
    return p1, p2


if __name__ == "__main__":
    DANCER.run(main, year=2020, day=19, verbose=True)

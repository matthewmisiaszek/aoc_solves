import core


def parse_ticket(ticket):
    return tuple(int(i) for i in ticket.split(','))


def parse(input_string):
    rules_str, your_ticket_str, nearby_tickets_str = input_string.split('\n\n')
    rules = {}
    for rule in rules_str.split('\n'):
        key, ranges = rule.split(': ')
        value = set()
        for range_i in ranges.split(' or '):
            n, x = (int(i) for i in range_i.split('-'))
            value.update(set(range(n, x + 1)))
        rules[key] = value
    your_ticket = parse_ticket(your_ticket_str.split('\n')[1])
    nearby_tickets = {parse_ticket(ticket) for ticket in nearby_tickets_str.split('\n')[1:]}
    return rules, your_ticket, nearby_tickets


def part1(nearby_tickets, rules):
    any_rule = set().union(*rules.values())
    error_rate = 0
    for ticket in tuple(nearby_tickets):
        bad_fields = tuple(field for field in ticket if field not in any_rule)
        if bad_fields:
            nearby_tickets.discard(ticket)
            error_rate += sum(bad_fields)
    return error_rate


def part2(your_ticket, nearby_tickets, rules, key_filter):
    nearby_fields = tuple(set(i) for i in zip(*nearby_tickets))
    possible_fields = [set(key for key, value in rules.items()
                           if field & value == field)
                       for field in nearby_fields]
    final_fields = [''] * len(possible_fields)
    change = True
    while change is True:
        change = False
        for i, field in enumerate(possible_fields):
            if len(field) == 1:
                field = field.pop()
                for other_field in possible_fields:
                    other_field.discard(field)
                final_fields[i] = field
                change = True
    ret = 1
    for field, value in zip(final_fields, your_ticket):
        if key_filter in field:
            ret *= value
    return ret


def main(input_string, verbose=False):
    rules, your_ticket, nearby_tickets = parse(input_string)
    p1 = part1(nearby_tickets, rules)
    p2 = part2(your_ticket, nearby_tickets, rules, 'departure')
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2020, day=16, verbose=True)

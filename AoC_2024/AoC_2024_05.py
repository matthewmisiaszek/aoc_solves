import blitzen


@blitzen.run
def main(input_string, verbose=False):

    rules, orders = input_string.split('\n\n')

    rulesforward, rulesreverse = {}, {}
    for rule in rules.split('\n'):
        a, b = rule.split('|')
        if a not in rulesforward:
            rulesforward[a] = set()
        rulesforward[a].add(b)
        if b not in rulesreverse:
            rulesreverse[b] = set()
        rulesreverse[b].add(b)

    orders = [order.split(',') for order in orders.split('\n')]

    p1 = p2 = 0
    for order in orders:
        num_before = [len(set(order) & rulesreverse[a]) if a in rulesreverse else 0 for a in order]
        num_after = [-len(set(order) & rulesforward[a]) if a in rulesforward else 0 for a in order]
        if num_before == sorted(num_before) and num_after == sorted(num_after):
            p1 += int(order[len(order)//2])
        else:
            order = sorted(zip(num_before, num_after, order))
            order = [i for _, _, i in order]
            p2 += int(order[len(order)//2])
    return p1, p2


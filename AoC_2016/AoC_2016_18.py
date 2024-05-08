import blitzen


@blitzen.run
def main(input_string, verbose=False):
    trap = '^'
    row = tuple(tile == trap for tile in input_string)
    safe_count = [len(row) - sum(row)]
    for _ in range(400000 - 1):
        row = tuple(a ^ b for a, b in zip((False,) + row, row[1:] + (False,)))
        safe_count.append(safe_count[-1] + len(row) - sum(row))
    p1 = safe_count[40 - 1]
    p2 = safe_count[400000 - 1]
    return p1, p2


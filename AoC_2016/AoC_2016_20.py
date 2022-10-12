import dancer


def union(a, b):
    an, ax = a
    bn, bx = b
    if max(an, bn) <= min(ax, bx) + 1:
        return min(an, bn), max(ax, bx)
    else:
        return False


def main(input_string, verbose=False):
    blocks = set(tuple(int(i) for i in line.split('-')) for line in input_string.split('\n'))
    consolidated_blocks = set()
    while blocks:
        consolidated_block = blocks.pop()
        while True:
            for block in blocks:
                new_consolidated_block = union(block, consolidated_block)
                if new_consolidated_block:
                    consolidated_block = new_consolidated_block
                    break
            else:
                break
            blocks.discard(block)
        consolidated_blocks.add(consolidated_block)
    consolidated_blocks = tuple(sorted(consolidated_blocks))
    p1 = consolidated_blocks[0][1] + 1
    p2 = 2 ** 32 - sum(b - a + 1 for a, b in consolidated_blocks)
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=20, verbose=True)

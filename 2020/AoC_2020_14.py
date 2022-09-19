from common2020 import aoc_input
from common.timer import timer
from common.common import digits


def apply_mask1(dec_val, mask):
    bin_val = digits(dec_val, 2, 36)
    mask_bin_val = tuple(mask[i] if i in mask else c for i, c in enumerate(bin_val))
    mask_dec_val = digits(mask_bin_val, 2)
    return mask_dec_val


def part1(input_string):
    input_string = input_string.replace('mem[', '').replace(']', '')
    mask = {}
    mem = {}
    for line in input_string.split('\n'):
        l, r = line.split(' = ')
        if l == 'mask':
            mask = {i: c == '1' for i, c in enumerate(r) if c != 'X'}
        else:
            reg = int(l)
            val = apply_mask1(int(r), mask)
            mem[reg] = val
    return sum(mem.values())


def apply_mask2(dec_val, maskx, mask1):
    bin_val = digits(dec_val, 2, 36)
    bin_val_1 = tuple(mask1[i] if i in mask1 else a for i, a in enumerate(bin_val))
    mask_base = digits(bin_val_1, 2)
    masked = set()
    for n in range(2 ** (len(maskx))):
        combo = digits(n, 2, len(maskx))
        masked.add(mask_base + sum((a * 2 ** (35 - b) for a, b in zip(combo, maskx))))
    return masked


def part2(input_string):
    input_string = input_string.replace('mem[', '').replace(']', '')
    mem = {}
    maskx = set()
    mask1 = set()
    for line in input_string.split('\n'):
        l, r = line.split(' = ')
        if l == 'mask':
            maskx = tuple(i for i, c in enumerate(r) if c == 'X')
            mask1 = {i: c == '1' for i, c in enumerate(r) if c != '0'}
        else:
            regs = apply_mask2(int(l), maskx, mask1)
            val = int(r)
            for regs2 in mem.values():
                regs2.difference_update(regs)
            if val not in mem:
                mem[val] = set()
            mem[val].update(regs)
    return sum(key * len(val) for key, val in mem.items())


def main(input_string, verbose=False):
    p1 = part1(input_string)
    p2 = part2(input_string)
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 14), verbose=True)
    print('Time:  ', timer())

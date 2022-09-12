from common2021 import aoc_input


def main(input_string, verbose=False):
    rpt = [[int(c) for c in line] for line in input_string.split('\n')]
    bits, rptlen = len(rpt[0]), len(rpt)
    bitrange, rptrange, range2 = range(bits), range(rptlen), range(2)

    # Part 1:
    epsilon = sum(round((sum([line[bit] for line in rpt]) + .5) / rptlen) * (2 ** (bits - bit - 1)) for bit in bitrange)
    gamma = 2 ** bits - epsilon - 1
    p1 = epsilon * gamma
    if verbose:
        print('Power Consumption: ', p1)

    # Part 2:
    masks = [[True for i in rptrange] for mask in range2]
    for bit in range(bits):
        common = [round((sum([rpt[n][bit] * mask[n] for n in rptrange]) + .5) / sum(mask)) for mask in masks]
        common[1] = 1 - common[1]
        for i in range2:  # i is which life support system
            for n in rptrange:
                if sum(masks[i]) > 1 and rpt[n][bit] != common[i] and masks[i][n] == True:
                    masks[i][n] = False
    masks = [mask.index(True) for mask in masks]
    ratings = [sum([rpt[mask][bit] * (2 ** (bits - bit - 1)) for bit in bitrange]) for mask in masks]
    p2 = ratings[0] * ratings[1]
    if verbose:
        print('Life Support Rating: ', p2)

    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2021, 3), verbose=True)

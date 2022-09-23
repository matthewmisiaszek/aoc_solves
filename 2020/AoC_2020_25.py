import sys
sys.path.append('..')
from common.aoc_input import aoc_input
from common.timer import timer
from common.holiday_greeting import holiday_greeting


def main(input_string, verbose=False):
    card_pkey, door_pkey = [int(i) for i in input_string.split('\n')]
    subject_number = 7
    modfact = 20201227
    pkey = 1
    card_loops = 0
    while pkey != card_pkey:
        pkey *= subject_number
        pkey %= modfact
        card_loops += 1
    ekey = 1
    subject_number = door_pkey
    for loop in range(card_loops):
        ekey *= subject_number
        ekey %= modfact
    p1 = ekey
    p2 = holiday_greeting
    if verbose:
        print('Part 1: {0[0]}\nPart 2: {0[1]}'.format([p1, p2]))
    return p1, p2


if __name__ == "__main__":
    main(aoc_input(2020, 25), verbose=True)
    print('Time:  ', timer())

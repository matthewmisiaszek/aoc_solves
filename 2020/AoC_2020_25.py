import core


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
    p2 = core.holiday_greeting
    return p1, p2


if __name__ == "__main__":
    core.run(main, year=2020, day=25, verbose=True)

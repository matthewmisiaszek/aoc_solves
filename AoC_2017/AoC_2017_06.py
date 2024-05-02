import blitzen


def main(input_string, verbose=False):
    banks = tuple(int(i) for i in input_string.split())
    nbanks = len(banks)
    history = {}
    red_count = 0
    while banks not in history:
        history[banks] = red_count
        blocks = max(banks)
        big_bank = banks.index(blocks)
        even = blocks // nbanks
        odd = blocks % nbanks
        banks = tuple(bank * (1 - int(idx == big_bank))
                      + even
                      + int(0 < (idx - big_bank) % nbanks <= odd)
                      for idx, bank in enumerate(banks))
        red_count += 1

    p1 = red_count
    p2 = red_count - history[banks]
    return p1, p2


if __name__ == "__main__":
    blitzen.run(main, year=2017, day=6, verbose=True)

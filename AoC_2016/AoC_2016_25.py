import dancer
from AoC_2016.assembunny import AsmBny


def main(input_string, verbose=False):
    assembunny = AsmBny(input_string, initial={'out': ''}, return_reg='out')
    i = 0
    while assembunny.run() != '01010101':
        assembunny.reset()
        i += 1
        assembunny.regs['a'] = i
    p1 = i
    p2 = dancer.holiday_greeting
    return p1, p2


if __name__ == "__main__":
    dancer.run(main, year=2016, day=25, verbose=True)
